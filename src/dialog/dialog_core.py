#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging

from threading import Thread
from Queue import Queue, Empty
from collections import deque


from helpers import colored_print

from dialog_exceptions import UnsufficientInputError, UnidentifiedAnaphoraError

from dialog.sentence import *

from speaker_identification import SpeakerIdentifier
from parsing.parser import Parser

from interpretation.resolution import Resolver
from interpretation.content_analysis import ContentAnalyser
from interpretation.anaphora_matching import replacement
from verbalization.verbalization import Verbalizer

DIALOG_VERSION = "0.2"

class Dialog(Thread):
    """The main Dialog class.
    
    The speaker ID can be specified at initializtion by passing it to the 
    constructor.
    """
    #This holds the history of conversation of all the instances of Dialog.
    dialog_history = []
    
    def __init__(self, speaker = None):
        Thread.__init__(self)
        
        self.go_on = True
        self._logger = logging.getLogger('dialog')
        
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
        # Sentence object and the verbalized version. For testing purposes.
        self.last_sentence = (None, None)
    
    def run(self):
        while self.go_on:
                  
            try:               
                input = self._nl_input_queue.get(block = False).strip()
                self._logger.info(colored_print("\n-------[       NL INPUT      ]-------\n", 'green'))
                self._logger.info(colored_print("- " + input + "\n", 'blue'))
                self.in_interaction = True
                self.waiting_for_more_info = False
                
                try:
                    self._process(input)
                except UnsufficientInputError as uie:
                    self._logger.info(colored_print("Not enough informations! Going back to human:", 'magenta'))
                    self._last_output = uie.value
                    
                    #Waiting for more info to solve content
                    self.waiting_for_more_info = True
                    
                    #Output towards human
                    sys.stdout.write(self._verbalizer.verbalize(uie.value['question']) + "\n")
                    self._logger.info(colored_print("- " +  \
                            self._verbalizer.verbalize(uie.value['question']), \
                            'blue') + "\n")
                
                except UnidentifiedAnaphoraError as uae:
                    self._logger.info(colored_print("Not sure of the interpretation...  Asking for confirmation to human:", 'magenta'))
                    self._anaphora_input = uae.value
                    
                    #waiting for more info to solve anaphora
                    self.waiting_for_more_info = True
                    
                    #Output towards human
                    sys.stdout.write(self._verbalizer.verbalize(uae.value['question']) + "\n")
                    self._logger.info("- " + colored_print( \
                            self._verbalizer.verbalize(uae.value['question']), \
                            'blue') + "\n")
                            
                            
            except Empty:
                pass
            
            try:
                output = self._sentence_output_queue.get(block = False)
                self._logger.info(colored_print("> Returning output: ", 'bold'))
                
                nl_output = self._verbalizer.verbalize(output)
                sys.stdout.write(colored_print( \
                            nl_output , \
                            'red') + "\n")
                            
                # Store output 
                Dialog.dialog_history.extend(output)
                
                
            except Empty:
                pass
            
            
    def stop(self):
        while(not self._nl_input_queue.empty()):
            pass
        self.go_on = False

    def input(self, input, speaker = None):
        if speaker:
            self.current_speaker = speaker
        else:
            self.current_speaker = self._speaker
        
        #Input for Unsifficient input  Error 
        if self.waiting_for_more_info and self._last_output:
            self._logger.info(colored_print("New content provided by human! merging it with the previous sentence.", 'magenta'))
            
            self._last_output['object_with_more_info'] = nom_gr_remerge(self._parser.parse(input, None),
                                                                self._last_output['status'],
                                                                self._last_output['object'])
            #No more info needed
            self.waiting_for_more_info = False
        
        #Input for Unidentified Anaphora Error
        if self.waiting_for_more_info and self._anaphora_input:
            self._logger.info(colored_print("Ok. Got a confirmation. Processing it.", 'magenta'))
            
            self._anaphora_input['object_with_more_info'] = replacement(self._parser.parse(input, None),
                                                                                   self._anaphora_input['object'] , 
                                                                                   self._anaphora_input['objects_list'][1:],
                                                                                   self._anaphora_input['object_to_confirm'])
            #No more info needed
            self.waiting_for_more_info = False
        
        
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
        self.in_interaction = True
        self.input(input, speaker)
        while(self.in_interaction):
            if answer and self.waiting_for_more_info:
                self._logger.debug(colored_print("> Automatically answering: ", 'bold'))
                self._logger.info(colored_print(answer, 'red'))
                self.input(answer, speaker)
                
                answer = None
            #elif self.waiting_for_more_info:
            #    return None
            #pass
        
        return (self.last_stmts_set, self.last_sentence)

    def _process(self, nl_input):
        #Parsing
        self._logger.info(colored_print("\n-------[       PARSING       ]-------\n", 'green'))
            
        # Current sentence possibly created from a occured exception
        if self._last_output:
            current_sentence = self._last_output['sentence']
        elif self._anaphora_input:
            current_sentence = self._anaphora_input['sentence']
        else:
            current_sentence = None
               
        self.sentences.appendleft(self._parser.parse(nl_input, current_sentence)[0])
        
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
            
            #Content analysis
            self._logger.info(colored_print("\n-------[   CONTENT ANALYSIS   ]-------\n", 'green'))
            
            self.last_stmts_set = self._content_analyser.analyse(self.active_sentence, 
                                                                    self.current_speaker)
            
            #Verbalization
            if self._content_analyser.analyse_output():
                
                self._logger.info(colored_print("\n-------[  VERBALIZATION   ]-------\n", 'green'))
                self.last_sentence = (self._content_analyser.analyse_output(), 
                                        self._verbalizer.verbalize(self._content_analyser.analyse_output()))
                                        
                self._sentence_output_queue.put(self.last_sentence[0])
            else:
                self._logger.info(colored_print("\nNothing to verbalize!", 'magenta'))
                self.last_sentence = (None, "")
            
            #Dialog History
            self._logger.debug(colored_print("Sentence saved in history.", 'magenta'))
            Dialog.dialog_history.append(self.active_sentence)
            
        #Finalizing the processing
        self.active_sentence = None
        self._logger.info(colored_print("\n[ NL sentence \"" + nl_input + "\" processed! ]", 'green'))
        self.in_interaction = False
        


def unit_tests():
    print("Please run the 'dialog_test' Python script.")
    print
    print("> ./dialog_test")

if __name__ == '__main__':
    print("Please run the 'dialog' Python script.")
    print
    print("> dialog")
