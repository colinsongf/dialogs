#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from helpers import colored_print

from interpretation.statements_builder import StatementBuilder, StatementSafeAdder

"""This module implements ...

"""

class ContentAnalyser:
    def __init__(self):
        self.builder = StatementBuilder()
        self.safeAdder = StatementSafeAdder()
        
    def analyse(self, sentence, current_speaker):
        """analyse an imperative or statement data_type sentence"""
        if sentence.data_type in ['imperative', 'statement']:
            logging.debug("Processing the content of an imperative or statement data_type sentence")
            return self.process_sentence(sentence, current_speaker)
        

            
    def process_sentence(self, sentence, current_speaker):
        self.builder.set_current_speaker(current_speaker)
        stmts = self.builder.process_sentence(sentence)
        
        logging.info("Generated statements: ")
        for s in stmts:
            logging.info(">> " + colored_print(s, None, 'magenta'))
        
        logging.info("Adding New statements in Ontology")
        self.safeAdder.safeAdd(stmts)
        
        return stmts

    

def unit_tests():
    """This function tests the main features of the class ContentAnalysis"""
    print("This is a test...")

if __name__ == '__main__':
    unit_tests()
