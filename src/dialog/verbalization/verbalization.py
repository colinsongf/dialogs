#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi                                                       
 08/07/2010                                                                       
 The package contains functions to perform test                                   
 It is more used for the subject                                                  
 Functions:                                                                       
    unit_tests : to perform unit tests                                            
"""


import logging
import unittest

from sentence import *

import utterance_rebuilding

class Verbalizer:
    """Implements the verbalization module: Verbalizer.verbalize() takes as
    input a Sentence object and build from it a sentence in natural language.
    """
    def verbalize(self, sentence):
        logging.debug("Verbalizing now...")
        nl_sentence = utterance_rebuilding.verbalising(sentence)
        logging.debug("Rebuild sentence to: \"" + nl_sentence + "\"")
        return nl_sentence



class TestVerbalization(unittest.TestCase):
    """
    Function to compare 2 nominal groups                                            
    """
    
    
    def test_01(self):
        print ''
        print '######################## test 1.1 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="The bottle is on the table. The bottle is blue. The bottle is Blue."
        
        sentences=[Sentence('statement', '',
            [Nominal_Group(['the'],['bottle'],[],[],[])],
            [Verbal_Group(['be'], [],'present simple',
                [],
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '',
            [Nominal_Group(['the'],['bottle'],[],[],[])],
            [Verbal_Group(['be'], [],'present simple',
                [Nominal_Group([],[],['blue'],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '',
            [Nominal_Group(['the'],['bottle'],[],[],[])],
            [Verbal_Group(['be'], [],'present simple',
                [Nominal_Group([],['Blue'],[],[],[])],
                [],
                [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_02(self):
        
        print ''
        print '######################## test 1.2 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon."
     
        sentences=[Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],['blue'],[Nominal_Group([],['Jido'],[],[],[])],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['play'], [],'future simple', 
                [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
        
    def test_03(self):
        
        print ''
        print '######################## test 1.3 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="It's on the table. I give it to you. Give me the bottle. I don't give the bottle to you."
        
        sentences=[Sentence('statement', '', 
            [Nominal_Group([],['it'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Indirect_Complement(['to'],[Nominal_Group([],['you'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('imperative', '', 
            [], 
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])],
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Indirect_Complement(['to'],[Nominal_Group([],['you'],[],[],[])])],
                [], [] ,'negative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_04(self):
        
        print ''
        print '######################## test 1.4 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="You aren't preparing the car and my father's moto at the same time. Is my brother's bottle in your right?"
        
        sentences=[Sentence('statement', '', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['prepare'], [],'present progressive', 
                [Nominal_Group(['the'],['car'],[],[],[]),Nominal_Group(['the'],['moto'],[],[Nominal_Group(['my'],['father'],[],[],[])],[])], 
                [Indirect_Complement(['at'],[Nominal_Group(['the'],['time'],['same'],[],[])])],
                [], [] ,'negative',[])]),
        Sentence('yes_no_question', '', 
            [Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['in'],[Nominal_Group(['your'],['right'],[],[],[])])],
                [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_05(self):
    
        print ''
        print '######################## test 1.5 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? Shall I go?"
        
        sentences=[Sentence('statement', '', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['should+drive'], [],'present conditional', 
                [Nominal_Group(['the'],['car'],['big', 'new'],[Nominal_Group(['the'],['wife'],[],[Nominal_Group(['his'],['uncle'],['poorest'],[], [])],[])],[])], 
                [],
                [], [] ,'negative',[])]),
        Sentence('yes_no_question', '', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['should+give'], [],'present conditional', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Indirect_Complement([],[Nominal_Group([],['you'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('yes_no_question', '', 
            [Nominal_Group([],['I'],[],[],[])],  
            [Verbal_Group(['shall+go'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    
    
    def test_06(self):
    
        print ''
        print '######################## test 1.6 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Isn't he doing his homework and his game now? Can't he take this bottle? Hello."
        
        sentences=[Sentence('yes_no_question', '', 
            [Nominal_Group([],['he'],[],[],[])], 
            [Verbal_Group(['do'], [],'present progressive', 
                [Nominal_Group(['his'],['homework'],[],[],[]), Nominal_Group(['his'],['game'],[],[],[])], 
                [],
                [], ['now'] ,'negative',[])]),
        Sentence('yes_no_question', '', 
            [Nominal_Group([],['he'],[],[],[])],  
            [Verbal_Group(['can+take'], [],'present simple', 
                [Nominal_Group(['this'],['bottle'],[],[],[])], 
                [],
                [], [] ,'negative',[])]),
        Sentence('start', '', [], [])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_07(self):
        
        print ''
        print '######################## test 1.7 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Don't quickly give me the blue bottle. I want to play with my guitar. I'd like to go to the cinema."
        
        sentences=[Sentence('imperative', '', 
            [], 
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['the'],['bottle'],['blue'],[],[])], 
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                ['quickly'], [] ,'negative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['want'], [Verbal_Group(['play'], 
                    [],'', 
                    [], 
                    [Indirect_Complement(['with'],[Nominal_Group(['my'],['guitar'],[],[],[])])],
                    [], [] ,'affirmative',[])], 
                'present simple',
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])],  
            [Verbal_Group(['like'], [Verbal_Group(['go'], 
                    [],'', 
                    [], 
                    [Indirect_Complement(['to'],[Nominal_Group(['the'],['cinema'],[],[],[])])],
                    [], [] ,'affirmative',[])], 
                'present conditional',
                [], 
                [],
                [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_08(self):
        
        print ''
        print '######################## test 1.8 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="The man who talks, has a new car. I play the guitar that I bought yesterday."
        
        sentences=[Sentence('statement', '', 
            [Nominal_Group(['the'],['man'],[],[],[Sentence('relative', 'who', 
                [],  
                [Verbal_Group(['talk'],[],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])])],  
            [Verbal_Group(['have'], [],'present simple', 
                [Nominal_Group(['a'],['car'],['new'],[],[])],
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])],  
            [Verbal_Group(['play'], [],'present simple', 
                [Nominal_Group(['the'],['guitar'],[],[],[Sentence('relative', 'that', 
                    [Nominal_Group([],['I'],[],[],[])],  
                    [Verbal_Group(['buy'],[],'past simple', 
                        [], 
                        [],
                        [], ['yesterday'] ,'affirmative',[])])])],
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_09(self):
        
        print ''
        print '######################## test 1.9 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Don't quickly give me the bottle which is on the table, and the glass which I cleaned yesterday, at my left."
        
        sentences=[Sentence('imperative', '', 
            [],  
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                    [],  
                    [Verbal_Group(['be'], [],'present simple', 
                        [],
                        [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                        [], [] ,'affirmative',[])])]),
                Nominal_Group(['the'],['glass'],[],[],[Sentence('relative', 'which', 
                    [Nominal_Group([],['I'],[],[],[])],  
                    [Verbal_Group(['clean'], [],'past simple', 
                        [],
                        [],
                        [], ['yesterday'] ,'affirmative',[])])])],
            [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]), Indirect_Complement(['at'],[Nominal_Group(['my'],['left'],[],[],[])])],
            ['quickly'], [] ,'negative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_10(self):
        
        print ''
        print '######################## test 1.10 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="The bottle that I bought from the store which is in the shopping center, is yours."
        
        sentences=[Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'that', 
                [Nominal_Group([],['I'],[],[],[])],  
                [Verbal_Group(['buy'], [],'past simple', 
                    [], 
                    [Indirect_Complement(['from'],[Nominal_Group(['the'],['store'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'], [],'present simple', 
                            [], 
                            [Indirect_Complement(['in'],[Nominal_Group(['the'],['center'],['shopping'],[],[])])],
                            [], [] ,'affirmative',[])])])])],
                    [], [] ,'affirmative',[])])])],  
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],['yours'],[],[],[])],
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_11(self):
        
        print ''
        print '######################## test 1.11 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="When won't the planning session take place? When must you take the bus?"
        
        sentences=[Sentence('w_question', 'date', 
            [Nominal_Group(['the'],['session'],['planning'],[],[])], 
            [Verbal_Group(['take+place'], [],'future simple', 
                [], 
                [],
                [], [] ,'negative',[])]),
        Sentence('w_question', 'date', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['must+take'], [],'present simple', 
                [Nominal_Group(['the'],['bus'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_12(self):
        
        print ''
        print '######################## test 1.12 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Where is Broyen? Where are you going? Where must Jido and you be from?"
        
        sentences=[Sentence('w_question', 'place', 
            [Nominal_Group([],['Broyen'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'place', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['go'], [],'present progressive', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'origin', 
            [Nominal_Group([],['Jido'],[],[],[]),Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['must+be'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_13(self):
        
        print ''
        print '######################## test 1.13 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What time is the news on TV? What size do you wear? The code is written by me. Is Mahdi going to the Laas?"
        
        sentences=[Sentence('w_question', 'time', 
            [Nominal_Group(['the'],['news'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group([],['TV'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'size', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['wear'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group(['the'],['code'],[],[],[])], 
            [Verbal_Group(['write'], [],'present passive', 
                [], 
                [Indirect_Complement(['by'],[Nominal_Group([],['me'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('yes_no_question', '', 
            [Nominal_Group([],['Mahdi'],[],[],[])], 
            [Verbal_Group(['go'], [],'present progressive', 
                [], 
                [Indirect_Complement(['to'],[Nominal_Group(['the'],['Laas'],[],[],[])])],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_14(self):
        
        print ''
        print '######################## test 1.14 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What's the weather like in the winter here? What were you doing? What isn't Jido going to do tomorrow?"
        
        sentences=[Sentence('w_question', 'description', 
            [Nominal_Group(['the'],['weather'],[],[],[])], 
            [Verbal_Group(['like'], [],'present simple', 
                [], 
                [Indirect_Complement(['in'],[Nominal_Group(['the'],['winter'],[],[],[])])],
                [], ['here'] ,'affirmative',[])]),
        Sentence('w_question', 'thing', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['do'], [],'past progressive', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'thing', 
            [Nominal_Group([],['Jido'],[],[],[])], 
            [Verbal_Group(['go'], [Verbal_Group(['do'], 
                    [],'', 
                    [], 
                    [],
                    [], ['tomorrow'] ,'affirmative',[])],
                'present progressive', 
                [], 
                [],
                [], [] ,'negative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_15(self):
        
        print ''
        print '######################## test 1.15 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What's happening? What must happen in the company today? What didn't happen here? No, sorry."
        
        sentences=[Sentence('w_question', 'situation', 
            [], 
            [Verbal_Group(['happen'], [],'present progressive', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'situation', 
            [],  
            [Verbal_Group(['must+happen'], [],'present simple', 
                [], 
                [Indirect_Complement(['in'],[Nominal_Group(['the'],['company'],[],[],[])])],
                [], ['today'] ,'affirmative',[])]),
        Sentence('w_question', 'situation', 
            [],  
            [Verbal_Group(['happen'], [],'past simple', 
                [], 
                [],
                [], ['here'] ,'negative',[])]),
        Sentence('disagree', '', [], [])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_16(self):
        
        print ''
        print '######################## test 1.16 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What's the biggest bottle's color on your left? What does your brother do for a living?"
        
        sentences=[Sentence('w_question', 'thing', 
            [Nominal_Group(['the'],['color'],[],[Nominal_Group(['the'],['bottle'],['biggest'],[],[])],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'explication', 
            [Nominal_Group(['your'],['brother'],[],[],[])], 
            [Verbal_Group(['do'], [],'present simple', 
                [], 
                [Indirect_Complement(['for'],[Nominal_Group(['a'],[],['living'],[],[])])],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_17(self):
        
        print ''
        print '######################## test 1.17 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What kind of people don't read this magazine? What kind of music must he listen to everyday?"
        
        sentences=[Sentence('w_question', 'classification+people', 
            [], 
            [Verbal_Group(['read'], [],'present simple', 
                [Nominal_Group(['this'],['magazine'],[],[],[])], 
                [],
                [], [] ,'negative',[])]),
        Sentence('w_question', 'classification+music', 
            [Nominal_Group([],['he'],[],[],[])], 
            [Verbal_Group(['must+listen+to'], [],'present simple', 
                [], 
                [],
                [], ['everyday'] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_18(self):
        
        print ''
        print '######################## test 1.18 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What kind of sport is your favorite? What's the problem with him? What's the matter with this person?"
        
        sentences=[Sentence('w_question', 'classification+sport', 
            [Nominal_Group(['your'],[],['favorite'],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'thing', 
            [Nominal_Group(['the'],['problem'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['with'],[Nominal_Group([],['him'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'thing', 
            [Nominal_Group(['the'],['matter'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['with'],[Nominal_Group(['this'],['person'],[],[],[])])],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_19(self):
        
        print ''
        print '######################## test 1.19 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="How old are you? How long is your uncle's store opened tonight? How long is your uncle's store open tonight?"
        
        sentences=[Sentence('w_question', 'old', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'long', 
            [Nominal_Group(['the'],['store'],[],[Nominal_Group(['your'],['uncle'],[],[],[])],[])], 
            [Verbal_Group(['open'], [],'present passive', 
                [], 
                [],
                [], ['tonight'] ,'affirmative',[])]),
        Sentence('w_question', 'long', 
            [Nominal_Group(['the'],['store'],[],[Nominal_Group(['your'],['uncle'],[],[],[])],[])],  
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],[],['open'],[],[])], 
                [],
                [], ['tonight'] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_20(self):
        
        print ''
        print '######################## test 1.20 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="How far is it from the hotel to the restaurant? How soon can you be here? How often does Jido go skiing?"
        
        sentences=[Sentence('w_question', 'far', 
            [Nominal_Group([],['it'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['from'],[Nominal_Group(['the'],['hotel'],[],[],[])]),Indirect_Complement(['to'],[Nominal_Group(['the'],['restaurant'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'soon', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['can+be'], [],'present simple', 
                [], 
                [],
                [], ['here'] ,'affirmative',[])]),
        Sentence('w_question', 'often', 
            [Nominal_Group([],['Jido'],[],[],[])],  
            [Verbal_Group(['go+skiing'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_21(self):
        
        print ''
        print '######################## test 1.21 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="How much water should they transport? How much guests weren't at the party? How much does the motocycle cost?"
        
        sentences=[Sentence('w_question', 'quantity', 
            [Nominal_Group([],['they'],[],[],[])], 
            [Verbal_Group(['should+transport'], [],'present conditional', 
                [Nominal_Group(['a'],['water'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'quantity', 
            [Nominal_Group(['a'],['guests'],[],[],[])], 
            [Verbal_Group(['be'], [],'past simple', 
                [], 
                [Indirect_Complement(['at'],[Nominal_Group(['the'],['party'],[],[],[])])],
                [], [] ,'negative',[])]),
        Sentence('w_question', 'quantity', 
            [Nominal_Group(['the'],['motocycle'],[],[],[])],  
            [Verbal_Group(['cost'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_22(self):
        
        print ''
        print '######################## test 1.22 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="How about going to the cinema? How haven't they gotten a loan for their business? OK."
        
        sentences=[Sentence('w_question', 'invitation', 
            [], 
            [Verbal_Group(['go'], [],'present progressive', 
                [], 
                [Indirect_Complement(['to'],[Nominal_Group(['the'],['cinema'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'manner', 
            [Nominal_Group([],['they'],[],[],[])], 
            [Verbal_Group(['get'], [],'present perfect', 
                [Nominal_Group(['a'],['loan'],[],[],[])], 
                [Indirect_Complement(['for'],[Nominal_Group(['their'],['business'],[],[],[])])],
                [], [] ,'negative',[])]),
        Sentence('agree', '',[],[])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_23(self):
        
        print ''
        print '######################## test 1.23 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What did you think of Steven Spilburg's new movie? How could I get to the restaurant from here?"
        
        sentences=[Sentence('w_question', 'opinion', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['like'], [],'past simple', 
                [Nominal_Group(['the'],['movie'],['new'],[Nominal_Group([],['Steven', 'Spilburg'],[],[],[])],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'manner', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['could+get+to'], [],'present conditional', 
                [Nominal_Group(['the'],['restaurant'],[],[],[])], 
                [Indirect_Complement(['from'],[Nominal_Group([],['here'],[],[],[])])],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_24(self):
        
        print ''
        print '######################## test 1.24 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Why should she go to Toulouse? Who could you talk to on the phone? Whose blue bottle and red glass are these?"
        
        sentences=[Sentence('w_question', 'reason', 
            [Nominal_Group([],['she'],[],[],[])], 
            [Verbal_Group(['should+go'], [],'present conditional', 
                [], 
                [Indirect_Complement(['to'],[Nominal_Group([],['Toulouse'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'people', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['could+talk+to'], [],'present conditional', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['phone'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'owner', 
            [Nominal_Group([],['bottle'],['blue'],[],[]), Nominal_Group([],['glass'],['red'],[],[])], 
            [Verbal_Group(['be'], [],'', 
                [], 
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
       
    def test_25(self):
       
        print ''
        print '######################## test 1.25 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What are you thinking about the idea that I present you? What color is the bottle which you bought?"
        
        sentences=[Sentence('w_question', 'opinion', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['think+about'], [],'present progressive', 
                [Nominal_Group(['the'],['idea'],[],[],[Sentence('relative', 'that', 
                    [Nominal_Group([],['I'],[],[],[])], 
                    [Verbal_Group(['present'], [],'present simple', 
                        [], 
                        [Indirect_Complement([],[Nominal_Group([],['you'],[],[],[])])],
                        [], [] ,'affirmative',[])])])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'color', 
            [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['buy'], [],'past simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_26(self):
        
        print ''
        print '######################## test 1.26 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Which salesperson's competition won the award which we won in the last years?"
        
        sentences=[Sentence('w_question', 'choice', 
            [Nominal_Group(['the'],['competition'],[],[Nominal_Group(['the'],['salesperson'],[],[],[])],[])], 
            [Verbal_Group(['win'], [],'past simple', 
                [Nominal_Group(['the'],['award'],[],[],[Sentence('relative', 'which', 
                    [Nominal_Group([],['we'],[],[],[])], 
                    [Verbal_Group(['win'], [],'past simple', 
                        [], 
                        [Indirect_Complement(['in'],[Nominal_Group(['the'],['year'],['last'],[],[])])],
                        [], [] ,'affirmative',[])])])], 
                [],
                [], [] ,'affirmative',[])])]
        
        sentences[0].sv[0].d_obj[0].relative[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_27(self):
        
        print ''
        print '######################## test 1.27 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What will your house look like? What do you think of the latest novel which Jido wrote?"
        
        sentences=[Sentence('w_question', 'description', 
            [Nominal_Group(['your'],['house'],[],[],[])], 
            [Verbal_Group(['look+like'], [],'future simple', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'opinion', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['think+of'], [],'present simple', 
                [Nominal_Group(['the'],['novel'],['latest'],[],[Sentence('relative', 'which', 
                    [Nominal_Group([],['Jido'],[],[],[])], 
                    [Verbal_Group(['write'], [],'past simple', 
                        [], 
                        [],
                        [], [] ,'affirmative',[])])])], 
            [],
            [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_28(self):
        
        print ''
        print '######################## test 1.28 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Learn that I want you to give me the blue bottle. You'll be happy, if you do your job."
        
        sentences=[Sentence('imperative', '', 
            [], 
            [Verbal_Group(['learn'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[Sentence('subsentence', 'that', 
                    [Nominal_Group([],['I'],[],[],[])], 
                    [Verbal_Group(['want'], [Verbal_Group(['give'], [],'', 
                            [Nominal_Group(['the'],['bottle'],['blue'],[],[])], 
                            [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                            [], [] ,'affirmative',[])],'present simple', 
                        [], 
                        [Indirect_Complement([],[Nominal_Group([],['you'],[],[],[])])],
                        [], [] ,'affirmative',[])])])]),
        Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['be'], [],'future simple', 
                    [Nominal_Group([],[],['happy'],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'if', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['do'], [],'present simple', 
                            [Nominal_Group(['your'],['job'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
       
   
    def test_29(self):
        print ''
        print '######################## test 1.29 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="You'll be happy, if you do your job. Do you want the blue or green bottle?"
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['be'], [],'future simple', 
                    [Nominal_Group([],[],['happy'],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'if', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['do'], [],'present simple', 
                            [Nominal_Group(['your'],['job'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['want'], [], 
                    'present simple',
                    [Nominal_Group(['the'],[],['blue'],[],[]),Nominal_Group([],['bottle'],['green'],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]

        sentences[1].sv[0].d_obj[1]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_30(self):
        print ''
        print '######################## test 1.30 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What's wrong with him? I'll play a guitar or a piano and a violon. I played a guitar a year ago."
        
        sentences=[Sentence('w_question', 'thing', 
            [Nominal_Group([],[],['wrong'],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['with'],[Nominal_Group([],['him'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['play'], [],'future simple', 
                [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['play'], [],'past simple', 
                [Nominal_Group(['a'],['guitar'],[],[],[])], 
                [Indirect_Complement(['ago'],[Nominal_Group(['a'],['year'],[],[],[])])],
                [], [] ,'affirmative',[])])]
        
        sentences[1].sv[0].d_obj[1]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
         
    def test_31(self):
        print ''
        print '######################## test 1.31 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Who are you talking to? You should have the bottle. Would you've played a guitar? You'd have played a guitar."
        
        sentences=[Sentence('w_question', 'people', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['talk+to'], [],'present progressive', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['should+have'], [],'present conditional', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('yes_no_question', '', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['play'], [],'past conditional', 
                [Nominal_Group(['a'],['guitar'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['play'], [],'past conditional', 
                [Nominal_Group(['a'],['guitar'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_32(self):
        print ''
        print '######################## test 1.32 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What do you do for a living in this building? What does your brother do for a living here?"
        
        sentences=[Sentence('w_question', 'explication', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['do'], [],'present simple', 
                [], 
                [Indirect_Complement(['for'],[Nominal_Group(['a'],[],['living'],[],[])]),
                 Indirect_Complement(['in'],[Nominal_Group(['this'],['building'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'explication', 
            [Nominal_Group(['your'],['brother'],[],[],[])], 
            [Verbal_Group(['do'], [],'present simple', 
                [], 
                [Indirect_Complement(['for'],[Nominal_Group(['a'],[],['living'],[],[])])],
                [], ['here'] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_33(self):
        print ''
        print '######################## test 1.33 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="This is a bottle. There is a bottle on the table."
        
        sentences=[Sentence('statement', '',
            [Nominal_Group(['this'],[],[],[],[])],
            [Verbal_Group(['be'], [],'present simple',
                [Nominal_Group(['a'],['bottle'],[],[],[])],
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '',
            [Nominal_Group(['there'],[],[],[],[])],
            [Verbal_Group(['be'], [],'present simple',
                [Nominal_Group(['a'],['bottle'],[],[],[])], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_34(self):
        print ''
        print '######################## test 1.34 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Is it on the table or the shelf?"
        
        sentences=[Sentence('yes_no_question', '',
                [Nominal_Group([],['it'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])]),
                     Indirect_Complement([],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[0].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
        
    def test_35(self):
        
        print ''
        print '######################## test 1.35 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Where is it? On the table or on the shelf?"
     
        sentences=[Sentence('w_question', 'place',
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '', 
                [], 
                [Verbal_Group([], [],'', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])]),
                     Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[1].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_36(self):
        
        print ''
        print '######################## test 1.36 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Is it on your left or in front of you?"
        
        sentences=[Sentence('yes_no_question', '',
                [Nominal_Group([],['it'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])]),
                     Indirect_Complement(['in+front+of'],[Nominal_Group([],['you'],[],[], [])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[0].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_37(self):
        
        print ''
        print '######################## test 1.37 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Where is it? On your left or in front of you?"
        
        sentences=[Sentence('w_question', 'place',
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '',
                [Nominal_Group([],[],[],[],[])],
                [Verbal_Group([], [],'',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])]),
                     Indirect_Complement(['in+front+of'],[Nominal_Group([],['you'],[],[], [])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[1].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    
    def test_38(self):
        
        print ''
        print '######################## test 1.38 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="The blue bottle? What do you mean?"
        
        sentences=[Sentence('yes_no_question', '', 
                        [Nominal_Group(['the'],['bottle'],['blue'],[],[])], 
                        []),
                    Sentence('w_question', 'thing', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['mean'], [],'present simple', [], [], [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)    
    
    
        
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format="%(message)s")
       
    # executing verbalization tests
    suiteVerbalization = unittest.TestLoader().loadTestsFromTestCase(TestVerbalization)

    
    unittest.TextTestRunner(verbosity=2).run(suiteVerbalization)
    
