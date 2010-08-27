#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger("dialog")

import unittest

from dialog.resources_manager import ResourcePool
from dialog.dialog_core import Dialog
from dialog.interpretation.questions_handler import QuestionHandler
from dialog.sentence import SentenceFactory, Sentence
from dialog.interpretation.statements_builder import *
from dialog.interpretation.statements_builder_test import dump_resolved

class TestQuestionHandler(unittest.TestCase):
    def setUp(self):
    
        try:
            ResourcePool().ontology_server.add(['SPEAKER rdf:type Human', 'SPEAKER rdfs:label "Patrick"',
                     'blue_cube rdf:type Cube',
                     'blue_cube hasColor blue',
                     'blue_cube isOn table1',
                     
                     'another_cube rdf:type Cube',
                     'another_cube isAt shelf1',
                     'another_cube belongsTo SPEAKER',
                     'another_cube hasSize small',
                     
                     'shelf1 rdf:type Shelf',
                     'table1 rdf:type Table',
                     
                     'see_shelf rdf:type See',
                     'see_shelf performedBy myself',
                     'see_shelf actsOnObject shelf1',
                     
                     'take_blue_cube performedBy myself',
                     'take_blue_cube rdf:type Get',
                     'take_blue_cube actsOnObject blue_cube',
                     
                     'take_my_cube canBePerformedBy SPEAKER',
                     'take_my_cube involves another_cube',
                     'take_my_cube rdf:type Take',
                     
                     'SPEAKER focusesOn another_cube',
                     
                     'id_danny rdfs:label "Danny"',
                     
                     'give_another_cube rdf:type Give',
                     'give_another_cube performedBy id_danny',
                     'give_another_cube receivedBy SPEAKER',
                     'give_another_cube actsOnObject another_cube',
                     
                     'see_some_one rdf:type See',
                     'see_some_one performedBy id_danny',
                     'see_some_one actsOnObject SPEAKER',
                     ])
        except AttributeError: #the ontology server is not started or doesn't know the method
            pass
        
        try:
            ResourcePool().ontology_server.addForAgent('SPEAKER',
                    [
                     'SPEAKER rdfs:label "Patrick"',
                     'blue_cube rdf:type Cube',
                     'blue_cube hasColor blue',
                     'blue_cube isOn table1',
                     
                     'another_cube rdf:type Cube',
                     'another_cube isAt shelf1',
                     'another_cube belongsTo SPEAKER',
                     'another_cube hasSize small',
                     
                     'shelf1 rdf:type Shelf',
                     'table1 rdf:type Table',
                     
                     'see_shelf rdf:type See',
                     'see_shelf performedBy myself',
                     'see_shelf actsOnObject shelf1',
                     
                     'take_blue_cube performedBy myself',
                     'take_blue_cube rdf:type Get',
                     'take_blue_cube actsOnObject blue_cube',
                     
                     'take_my_cube canBePerformedBy SPEAKER',
                     'take_my_cube involves another_cube',
                     'take_my_cube rdf:type Take',
                     
                     'SPEAKER focusesOn another_cube',
                     
                     'id_danny rdfs:label "Danny"',
                     
                     'give_another_cube rdf:type Give',
                     'give_another_cube performedBy id_danny',
                     'give_another_cube receivedBy SPEAKER',
                     'give_another_cube actsOnObject another_cube',
                     
                     'see_some_one rdf:type See',
                     'see_some_one performedBy id_danny',
                     'see_some_one actsOnObject SPEAKER',
                     ])
        except AttributeError: #the ontology server is not started or doesn't know the method
            pass
        
        self.qhandler = QuestionHandler("SPEAKER")
        self.sfactory = SentenceFactory()
    
    def test_1_where_question(self):
        print "\n*************  test_1_where_question ******************"
        print "Where is the blue cube?"
        sentence = Sentence("w_question", "place", 
                             [Nominal_Group(['the'],
                                            ['cube'],
                                            [['blue',[]]],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present_simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])]) 
        statement_query = ['blue_cube isOn ?concept']
        expected_result = ['table1']
        self.process(sentence , statement_query, expected_result)

    def test_2_where_question(self):
        print "\n*************  test_2_where_question ******************"
        print "Where is the small cube?"
        sentence = Sentence("w_question", "place", 
                             [Nominal_Group(['the'],
                                            ['cube'],
                                            [['small',[]]],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present_simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['another_cube isOn ?concept']
        expected_result = ['shelf1']
        
        self.process(sentence , statement_query, expected_result)
    
    
    def test_3_what_question(self):
        print "\n*************  test_3_what_question ******************"
        print "What do you see?"
        sentence = Sentence("w_question", "thing", 
                             [Nominal_Group([],
                                            ['you'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['see'],
                                           [],
                                           'present_simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        #TODO:there might be severals action ID that are instances of See
        # ?Concept may hold several results 
        statement_query = ['* rdf:type See',
                           '* performedBy myself',
                           '* involves ?concept']
        expected_result = ['shelf1']
        
        self.process(sentence , statement_query, expected_result)
    
    def test_8_what_question(self):
        print "\n*************  test_8_what_question ******************"
        print "what is blue?"
        sentence = Sentence("w_question", "thing", 
                             [],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['blue_cube owl:sameAs ?concept']
        expected_result = ['blue_cube']        
        self.process(sentence , statement_query, expected_result) 
    
    def test_9_what_question_this(self):
        print "\n*************  test_9_what_question_this ******************"
        print "what is this?"
        sentence = Sentence("w_question", "thing", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['SPEAKER focusesOn ?concept']
        expected_result = ['another_cube']        
        self.process(sentence , statement_query, expected_result) 
    
    def test_10_what_question(self):
        print "\n*************  test_10_w_question ******************"
        print "what object is blue?"
        sentence = Sentence("w_question", "object", 
                             [],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['?concept owl:sameAs blue_cube']
        expected_result = ['blue_cube']        
        self.process(sentence , statement_query, expected_result)
    
    def test_11_what_question(self):
        print "\n*************  test_11_w_question ******************"
        print "what size is this?"
        sentence = Sentence("w_question", "size", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['another_cube hasSize ?concept']
        expected_result = ['small']        
        self.process(sentence , statement_query, expected_result)
    
    def test_12_what_question(self):
        print "\n*************  test_12_what_question ******************"
        print "what color is the blue_cube?"
        sentence = Sentence("w_question", "color", 
                             [Nominal_Group(['the'],
                                            ['blue_cube'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['blue_cube hasColor ?concept']
        expected_result = ['blue']        
        self.process(sentence , statement_query, expected_result)
    
    def test_13_who_question(self):
        print "\n*************  test_13_who_question ******************"
        print "who is the SPEAKER?"
        sentence = Sentence("w_question", "people", 
                             [Nominal_Group(['the'],
                                            ['SPEAKER'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['SPEAKER owl:sameAs ?concept']
        expected_result = ['SPEAKER']        
        self.process(sentence , statement_query, expected_result)
    
    def test_14_who_question(self):
        print "\n*************  test_14_who_question ******************"
        print "who sees Patrick?"
        sentence = Sentence("w_question", "people", 
                             [],                                         
                             [Verbal_Group(['see'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          ['Patrick'],
                                                          [],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['* performedBy ?concept',
                           '* rdf:type See',
                           '* involves SPEAKER']
                           
        expected_result = ['id_danny']        
        self.process(sentence , statement_query, expected_result)
    
    
    def test_15_who_question(self):
        print "\n*************  test_15_who_question ******************"
        print "who does Danny give the small cube?"
        sentence = Sentence("w_question", "people", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['give'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],
                                                          ['cube'],
                                                          [['small',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['* performedBy id_danny',
                           '* rdf:type Give',
                           '* hasGoal ?concept'
                           '* actsOnObject another_cube']
                            
        expected_result = ['SPEAKER']        
        self.process(sentence , statement_query, expected_result)
   
    """
    def test_4_y_n_question(self):
        print "\n*************  test_4_y_n_question action verb******************"
        print "Did you get the blue cube?"
        sentence = Sentence("yes_no_question", "", 
                             [Nominal_Group([],
                                            ['you'],
                                            [''],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['get'],
                                           [],
                                           'past_simple',
                                           [Nominal_Group(['the'],
                                                          ['cube'],
                                                          ['blue'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['* rdf:type Get',
                           '* performedBy myself',
                           '* actsOnObject blue_cube']
        expected_result = True        
        self.process(sentence , statement_query, expected_result)
        
    
    def test_5_y_n_question(self):
        print "\n*************  test_5_y_n_question verb to be followed by complement******************"
          "Is the blue cube on the table?"
        sentence = Sentence("yes_no_question", "", 
                             [Nominal_Group(['the'],
                                            ['cube'],
                                            ['blue'],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['on'],
                                                                [Nominal_Group(['the'],
                                                                               ['table1'],
                                                                               [],
                                                                               [],
                                                                               [])])],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['blue_cube isOn table1']
        expected_result = True        
        self.process(sentence , statement_query, expected_result)
    
    
    def test_6_y_n_question(self):
        print "\n*************  test_6_y_n_question verb to be not followed by complement and sentence resolved******************"
        print "Is the cube blue?"
        sentence = Sentence("yes_no_question", "", 
                             [Nominal_Group(['the'],
                                            ['cube'],
                                            ['blue'],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = []
        expected_result = True        
        self.process(sentence , statement_query, expected_result)
        
    
    def test_7_y_n_question(self):
        print "\n*************  test_7_y_n_question verb to be ******************"
        print "Is my cube on the table1?"
        sentence = Sentence("yes_no_question", "", 
                             [Nominal_Group(['my'],
                                            ['cube'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['on'],
                                                                [Nominal_Group(['the'],
                                                                               ['table1'],
                                                                               [],
                                                                               [],
                                                                               [])])],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['another_cube isOn table1']
        expected_result = False        
        self.process(sentence , statement_query, expected_result) 
    
    
    
    
    
    
    def test_9_how_question(self):
        print "\n*************  test_9_how_question ******************"
        print "How is my car?"
        sentence = Sentence("w_question", "manner", 
                             [Nominal_Group(['my'],
                                            ['cube'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['?concept hasColor blue']
        expected_result = ['blue']        
        self.process(sentence , statement_query, expected_result) 
    """
        
    def process(self, sentence , statement_query, expected_result):
        sentence = dump_resolved(sentence, 'SPEAKER', 'myself')#TODO: dumped_resolved is only for the test of query builder
        res = self.qhandler.process_sentence(sentence)
        
        #Statements Built for querying Ontology
        logger.info("Query Statement ...")
        for s in self.qhandler._statements:
            logger.info("\t>>" + s)
        logger.info("--------------- >>\n")
        
        #Result from the ontology
        logger.info("Expected Result:" + str(expected_result))
        logger.debug("Result Found in the Ontology: " + str(self.qhandler._answer))
        
        #Response in sentence
        logger.info("************************************************")
        logger.info("* Factory: Sentence towards Verbalization .... *")
        logger.info("************************************************")
        
        res_factory = []
        if sentence.data_type == 'w_question':
            res_factory = self.sfactory.create_w_question_answer(sentence, self.qhandler._answer, self.qhandler._query_on_field)
            
        elif sentence.data_type == 'yes_no_question':
            res_factory = self.sfactory.create_yes_no_answer(sentence, self.qhandler._answer)
        else:
            pass
        
        for rep in res_factory:
            logger.debug(str(rep))
            #logger.debug(str(rep.flatten()))
        
        self.qhandler.clear_statements()
        self.assertEqual(res, expected_result)


class TestQuestionHandlerDialog(unittest.TestCase):
    """Tests the processing of question by the Dialog module.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = ResourcePool().ontology_server
        
        try:
            self.oro.add(['shelf1 rdf:type Shelf',
                        'table1 rdf:type Table', 
                        'table2 rdf:type Table', 
                        'table2 hasColor blue', 
                        'Banana rdfs:subClassOf Plant',
                        'y_banana rdf:type Banana',
                        'y_banana hasColor yellow',
                        'y_banana isOn shelf1',
                        'green_banana rdf:type Banana',
                        'green_banana hasColor green',
                        'green_banana isOn table2',
                        'myself focusesOn y_banana',
                        'myself rdfs:label "Jido"',
                        'myself sees id_tom',
                        'myself sees y_banana',
                        'id_tom rdf:type Human',
                        'id_tom rdfs:label "Tom"',
                        'id_tom isNexto myself',                        
                        ])
            
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

    def test_question1_where(self):

        logger.info("\n##################### test_question1_where ########################\n")
        
        ####
        stmt = "Where is the green banana?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        self.assertTrue(res)
    
        
    
    def test_question2_what(self):

        logger.info("\n##################### test_question2_what ########################\n")
        
        ####
        stmt = "What is yellow?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        self.assertTrue(res)
        
    
    def test_question3_what(self):
        logger.info("\n##################### test_question3_what ########################\n")
        
        stmt = "What object is yellow?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        self.assertTrue(res)
        
    def test_question4_what(self):    
        logger.info("\n##################### test_question4_what ########################\n")
        
        stmt = "What color is the banana that is on the table?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        self.assertTrue(res)
    
    def test_question5_what(self):    
        logger.info("\n##################### test_question5_what ########################\n")
        
        stmt = "What is this?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        self.assertTrue(res)

    
    def test_question6_who(self):

        logger.info("\n##################### test_question6_who ########################\n")
        
        ####
        stmt = "Who are you?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        self.assertTrue(res)
    
    def test_question7_who(self):
        logger.info("\n##################### test_question7_who ########################\n")
        
        stmt = "Who is the myself?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        self.assertTrue(res)
        
    def test_question8_who(self):
        logger.info("\n##################### test_question8_who ########################\n")
        
        question = "Who do you see?"

        res = self.dialog.test('myself', question)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        
        expected_query = [ 'myself sees ?*']
        
        self.assertTrue(check_results(res[0], expected_result))
        
        self.assertEquals(res[1][1], "I see Tom and the yellow banana that is on the self")
        
    def test_question9_who(self):
        logger.info("\n##################### test_question9_who ########################\n")
        
        stmt = "Who is Tom?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        self.assertEquals(res[1][1], "Tom is Tom")

    """ Breaks severly the unittesting. Need to fix it at least to have a nicer failure
    def test_question10(self):
        logger.info("\n##################### Check we resolve correctly the labels ########################\n")
        
        question = "What humans do you know?"
        ####
        
        ###
        res = self.dialog.test('SPEAKER', question)
        logger.info( ">> input: " + stmt)
        logger.info( "<< output statements: " + res)
        
        expected_query = [ 'myself knows ?*']
        
        self.assertTrue(check_results(res[0], expected_query))
        
        self.assertEquals(res[1][1], "I know Tom")
    """

def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQuestionHandler)
    suite.addTests( unittest.TestLoader().loadTestsFromTestCase(TestQuestionHandlerDialog))

    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())
