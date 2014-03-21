#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import sys
from Queue import Queue, Empty
from collections import deque
from threading import Thread

from dialog_exceptions import *
from kb import KbError
from dialogs.sentence import *
from helpers.helpers import colored_print, wait_for_keypress
from helpers import emotions
from interpretation.anaphora_matching import replacement
from interpretation.content_analysis import ContentAnalyser
from interpretation.resolution import Resolver
from parsing.parser import Parser
from speaker_identification import SpeakerIdentifier
from verbalization.verbalization import Verbalizer


class Dialog(Thread):
    """The main Dialog class.
    
    The speaker ID can be specified at initializtion by passing it to the 
    constructor.
    """
    #This holds the history of conversation of all the instances of Dialog.
    dialog_history = []
    
    def __init__(self, speaker = None, demo = False):
        Thread.__init__(self)
        
        self.go_on = True
        self._logger = logging.getLogger('dialogs')
        
        self._demo_mode = demo
        
        if speaker:
            self._speaker = speaker
        else:
            self._speaker = SpeakerIdentifier().get_current_speaker_id()
            
        self._parser = Parser()
        self._resolver = Resolver()
        self._content_analyser = ContentAnalyser()
        self._verbalizer = Verbalizer()
        
        self._nl_input_queue = Queue()
        self._sentence_output_queue = Queue()
        
        #true when the Dialog module is within an interaction with a speaker
        self.in_interaction = False
        
        #the current set of sentences that dialog is dealing with
        self.sentences = deque()
        
        #the current sentence being worked on. Specifically, if active_sentence
        #is set, the parser will _complete_ this sentence instead of creating a
        #new one.
        self.active_sentence = None
        
        #true when, during an interaction, more infos is needed.
        self.waiting_for_more_info = False
        
        #contains the last result of a failed resolution (including the object 
        #that could not be resolved. Cf doc of UnsufficientInputError for details.
        self._last_output = None
        
        #contains the last result of a failed resolution of an anaphoric words (it, one) (including the object 
        #that could not be resolved. Cf doc of UnidentifiedAnaphoraError for details.
        self._anaphora_input = None
        
        #the ID of the speaker we are talking with. used to resolve references
        #like 'me', 'you', etc.
        self.current_speaker = None
        
        #the set of the statements generated by the analysis of the last sentence.
        # For testing purposes.
        self.last_stmts_set = []
        
        #last utterance outputed to user. This is a tuple containing both the
        # Sentence object and the verbalized version.
        self.last_sentence = (None, None)

    def run(self):
        while self.go_on:

            try:
                # block with a (short) timeout to prevent maxing the CPU
                input = self._nl_input_queue.get(True, 0.1).strip()
                ResourcePool().mark_active(self._speaker)
                self._logger.info(colored_print("\n-------[       NL INPUT      ]-------\n", 'green'))
                self._logger.info(colored_print("- " + input + "\n", 'blue'))
                self.in_interaction = True
                
                try:
                    self._process(input)
                except UnsufficientInputError as uie:
                    self._logger.info(colored_print("Not enough informations! Going back to human:", 'magenta'))
                    self._last_output = uie.value

                    #Output towards human
                    sys.stdout.write(self._verbalizer.verbalize(uie.value['question']) + "\n")
                    sys.stdout.flush()
                    self._logger.info(colored_print("- " +
                                                    self._verbalizer.verbalize(uie.value['question']),
                                                    'blue') + "\n")

                    #Waiting for more info to solve content
                    self.waiting_for_more_info = True
                
                except InterruptedInteractionError as iie:
                    self._logger.info(colored_print("I can not continue. I interrupt the interaction.", 'magenta'))

                    #Output towards human
                    sys.stdout.write(self._verbalizer.verbalize(iie.value) + "\n")
                    sys.stdout.flush()
                    self._logger.info(colored_print("- " +
                                                    self._verbalizer.verbalize(iie.value),
                                                    'blue') + "\n")

                except UnidentifiedAnaphoraError as uae:
                    self._logger.info(colored_print("Not sure of the interpretation...  Asking for confirmation to human:", 'magenta'))
                    self._anaphora_input = uae.value
                    
                    #waiting for more info to solve anaphora
                    self.waiting_for_more_info = True
                    
                    #Output towards human
                    sys.stdout.write(self._verbalizer.verbalize(uae.value['question']) + "\n")
                    sys.stdout.flush()
                    self._logger.info("- " + colored_print(
                        self._verbalizer.verbalize(uae.value['question']),
                        'blue') + "\n")
                except GrammaticalError as ge:
                    self._logger.info(colored_print("Grammatical error! " + \
                        "I can not correctly parse the sentence. Asking " + \
                        "the speaker to reformulate", 'magenta'))
                    #waiting for more info to solve anaphora
                    self.waiting_for_more_info = True
                    #Output towards human
                    sys.stdout.write("I didn't really understand your last sentence. Could you reformulate?\n")
                    sys.stdout.flush()

                except DialogError as de:
                    self._logger.info(colored_print("Error! " + de.value, 'magenta'))
                    #Output towards human
                    emotions.confused()
                    sys.stdout.write("Sorry, I'm confused... Could you repeat in a different way?\n")
                    sys.stdout.flush()

                except KbError as ke:
                    self._logger.info(colored_print("Error! " + ke.value, 'magenta'))
                    #Output towards human
                    emotions.confused()
                    sys.stdout.write("Sorry, I'm confused... My knowledge looks somehow broken...\n")
                    sys.stdout.flush()

                    # interrupt the interaction
                    self.in_interaction = False

            except Empty:
                pass
            
            try:
                output = self._sentence_output_queue.get(block = False)
                self._logger.info(colored_print("> Returning output: ", 'bold'))
                
                nl_output = self._verbalizer.verbalize(output)
                sys.stdout.write(nl_output + "\n")
                sys.stdout.flush()
                self._logger.info("- " + colored_print(
                    nl_output,
                    'blue') + "\n")
                            
               
                
            except Empty:
                pass
            
    def stop(self):
        while not self._nl_input_queue.empty():
            pass
        self.go_on = False

    def input(self, input, speaker = None):

        input = input.decode('utf-8').encode('ascii')

        if speaker:
            self.current_speaker = speaker
        else:
            self.current_speaker = self._speaker
        
        self._nl_input_queue.put(input)
        
        
    def test(self, speaker, input, answer = None):
        """This method eases the testing of dialog by returning only when a 
        sentence is completely processed.
        The optional 'answer' argument is used to answer a request for more 
        details from the resolution code.
        
        The method returns a tuple containing the last produced statements (if 
        relevant) and the last sentence produced (as a tuple of (Sentence, 
        verbalized sentence), is relevant).
        """
        import time
        self.in_interaction = True
        self.input(input, speaker)
        while self.in_interaction:
            if self.waiting_for_more_info:
                if answer:
                    self._logger.debug(colored_print("> Automatically answering: ", 'bold'))
                    self._logger.info(colored_print(answer, 'red'))
                    self.input(answer, speaker)
                    answer = None
                else:
                    return [], self.last_sentence
            time.sleep(0.1)

        return self.last_stmts_set, self.last_sentence

    def _process(self, nl_input):
        #Parsing
        self._logger.info(colored_print("\n-------[       PREPROCESSING       ]-------\n", 'green'))
        preprocessed_sentences = self._parser.preprocess(nl_input, None)

        for s in preprocessed_sentences:
            self._logger.debug(s)

        self._logger.info(colored_print("\n-------[       PARSING       ]-------\n", 'green'))

        parsed_sentences = self._parser.parse(preprocessed_sentences, None)

        for s in parsed_sentences:
            self._logger.debug(str(s))

        if self._demo_mode:
            wait_for_keypress()

        #Unsufficient input or unidentified anaphora Error processing
        for s in parsed_sentences:

            #Check the sentence is grammatically valid, else go back to the human
            if not s.isvalid():
                raise GrammaticalError(s)
 
            if s.isaborting():
                parsed_sentences.remove(s)
                self._last_output = self._anaphora_input = None
                self.waiting_for_more_info = False
                sys.stdout.write("Alright. Forgotten!\n")
                sys.stdout.flush()
                self._logger.info("- " + colored_print(
                    "Alright. Forgotten!",
                    'blue') + "\n")
                
                break
            
            if s.islearning() and self._last_output:
                s.append_sub_sentence(self._last_output['sentence'])
                self._last_output = None
                self.waiting_for_more_info = False
                break
                    
        if self.waiting_for_more_info:
            self._logger.info(colored_print("Waiting for more information activated\n", 'magenta'))
            #Processing Unsifficient input  Error with sentences remerge
            if self._last_output:
                self._logger.info(colored_print("New content provided by human! merging it with the previous sentence.", 'magenta'))
                
                self._last_output['object_with_more_info'] = nominal_group_remerge(parsed_sentences,
                                                                    self._last_output['status'],
                                                                    self._last_output['object'])
                #current_sentence that is to replace if it is to answer unsificient input
                parsed_sentences = [self._last_output['sentence']]
            
            #Processing Unidentified Anaphora Error with sentences replacement
            if self._anaphora_input:
                self._logger.info(colored_print("Ok. Got a confirmation. Processing it.", 'magenta'))
                
                self._anaphora_input['object_with_more_info'] = replacement(parsed_sentences,
                                                                       self._anaphora_input['object'] , 
                                                                       self._anaphora_input['objects_list'][1:],
                                                                       self._anaphora_input['object_to_confirm'])
                #current_sentence that is to replace if it is to answer unidentified anaphora
                parsed_sentences = [self._anaphora_input['sentence']]
                
            #No more info needed
            self.waiting_for_more_info = False
            
        #end of Unsufficient input or unidentified anaphora Error processing
        
        
        #Sentences Queue()
        [self.sentences.append(stnts) for stnts in parsed_sentences]
        
        for s in range(len(self.sentences)): #sentences is a deque. Cannot do a simple [:] to iterate over a copy
            self.active_sentence = self.sentences.popleft()
            
            #Resolution
            self._resolver.sentences_store = Dialog.dialog_history
            uie_object = self._last_output['object'] if self._last_output else None
            uie_object_with_more_info = self._last_output['object_with_more_info'] if uie_object else None
            self._last_output = None
            
            uae_object = self._anaphora_input['object'] if self._anaphora_input else None
            uae_object_with_more_info = self._anaphora_input['object_with_more_info'] if uae_object else None
            uae_object_list = self._anaphora_input['objects_list'] if uae_object else None
            self._anaphora_input = None
            
            
            self._logger.info(colored_print("\n-------[ RESOLVING SENTENCE  ]-------\n", 'green'))
            
            self.active_sentence = self._resolver.references_resolution(self.active_sentence,
                                                                        self.current_speaker,
                                                                        uae_object,
                                                                        uae_object_with_more_info,
                                                                        uae_object_list)
            
            self.active_sentence = self._resolver.noun_phrases_resolution(self.active_sentence,
                                                                          self.current_speaker,
                                                                          uie_object,
                                                                          uie_object_with_more_info)
            
            self.active_sentence = self._resolver.verbal_phrases_resolution(self.active_sentence)
            
            self._logger.info(colored_print("\n[ Sentence after resolution ]", 'green'))
            self._logger.info(str(self.active_sentence))
            
            if self._demo_mode:
                wait_for_keypress()
            
            #Content analysis
            self._logger.info(colored_print("\n-------[   CONTENT ANALYSIS   ]-------\n", 'green'))
            
            self.last_stmts_set, self.current_situation_id = self._content_analyser.analyse(self.active_sentence, 
                                                                    self.current_speaker)
            
            if self._demo_mode:
                wait_for_keypress()
            
            #Verbalization
            if self._content_analyser.analyse_output():
            
                self._logger.info(colored_print("\n-------[  VERBALIZATION   ]-------\n", 'green'))
                self.last_sentence = (self._content_analyser.analyse_output(), 
                                        self._verbalizer.verbalize(self._content_analyser.analyse_output()))
                
                if self.current_situation_id:
                    self._logger.debug(colored_print("Answer: <%s>: Sent to knowledge base." % self.last_sentence[1], 'magenta'))
                    self._logger.debug("Up to the robot controller now!")
                    try:
                        ResourcePool().ontology_server.revise(['%s verbalisesTo "%s"' % (self.current_situation_id,
                                                                                     self.last_sentence[1])],
                                                              {"method":"add", "models":[ResourcePool.default_model]})
                    except AttributeError:
                        #No knowledge base
                        pass
                else:
                    self._sentence_output_queue.put(self.last_sentence[0])
                
                if self._demo_mode:
                    wait_for_keypress()
                
            else:
                self._logger.info(colored_print("\nNothing to verbalize!", 'magenta'))
                self.last_sentence = (None, "")
            
            #Dialog History
            self._logger.debug(colored_print("Sentence and answer saved in history.", 'magenta'))
            Dialog.dialog_history.append(self.active_sentence)
            if self.last_sentence[0]:
                Dialog.dialog_history.extend(self.last_sentence[0])
            
        #Finalizing the processing
        self.active_sentence = None
        self._logger.info(colored_print("\n[ NL sentence \"" + nl_input + "\" processed! ]", 'green'))

        if self.last_sentence[0] and self.last_sentence[0][0].data_type == END:
            # Exit!
            self.stop()

        self.in_interaction = False
        


def unit_tests():
    print("Please run the 'dialog_test' Python script.")
    print
    print("> ./dialog_test")

if __name__ == '__main__':
    print("Please run the 'dialogs' Python script.")
    print
    print("> dialogs")
