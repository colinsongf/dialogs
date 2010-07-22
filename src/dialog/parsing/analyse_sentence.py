#!/usr/bin/python
# -*- coding: utf-8 -*-
# SVN:rev202 + PythonTidy

"""
 Created by Chouayakh Mahdi                                                       
 25/06/2010                                                                       
 The package contains functions to analyse all sentence of a utterance            
 Functions:                                                                       
    dispatching : to distribute the sentence                                      
    w_quest_where : to process many different type of where question                
    w_quest_what  : to process many different type of what question                 
    w_quest_quant : to process many different type of how question
    w_quest_how : to process many different type of how question                    
    condi_sentence : to process the conditional sentence                           
    w_quest_whose : to process many different type of whose question   
    w_quest_whom : to process whom question
    y_n_ques : to process the yes or no question from of a sentence                 
    other_sentence : to process the other from of a sentence                        
    sentences_analyzer : is the basic function of parsing                         
"""
from sentence import *
from resources_manager import ResourcePool
import analyse_nominal_group
import analyse_nominal_structure
import analyse_verb
import analyse_verbal_structure
import other_functions


"""
Statement of lists
"""
modal_list=['must', 'should', 'may', 'might', 'can', 'could', 'shall']
det_dem_list=['this', 'there', 'these']
what_ques_list=[('time','time',2),('color','color',2),('size','size',2),('object','object',2)]
how_ques_list=[('old','age',2),('long','duration',2),('often','frequency',2),('far','distance',2),('soon','time',2)]

"""
We have to read all words that sentence can begin with                           
"""
frt_wd = ResourcePool().sentence_starts



def dispatching(sentence):
    """
    This function distributes the sentence according to:                             
    Their functionality and their type                                               
    Input=sentence, beginning sentence list          Output=class Sentence           
    """

    if len(sentence)>0:
        
        #For interjection
        if sentence[len(sentence)-1]=='!':
            return Sentence('interjection', '', [], [])

        #When others
        for x in frt_wd:
            #If we find a knowing case
            if sentence[0]==x[0]:


                #For
                if x[1] == '0':
                    return Sentence('start', '', [], [])

                #It's a w_question
                if x[1] == '1':

                    #For 'when'
                    if x[2]=='1':
                        #If we remove the first word => it becomes like y_n_question
                        return y_n_ques('w_question', 'date', sentence[1:])

                    #For 'where'
                    elif x[2]=='2':
                        return w_quest_where('w_question', 'place', sentence)

                    #For 'what'
                    elif x[2]=='3':

                        #We have different type of question with 'what'
                        for z in what_ques_list:
                            if sentence[1]==z[0]:
                                return y_n_ques('w_question', z[1], sentence[z[2]:])

                        #Here we have to use a specific processing for 'type' and 'kind'
                        if sentence[1]=='type' or sentence[1]=='kind':
                            #We start by processing the end of the sentence like a y_n_question
                            return y_n_ques('w_question', 'classification'+'+'+sentence[3],sentence[4:])

                        #For other type of 'what' question
                        else:
                            return w_quest_what('w_question', sentence, 2)

                    #For 'how'
                    elif x[2]=='4':
                        
                        #We have different type of question with 'how'
                        for z in how_ques_list:
                            if sentence[1]==z[0]:
                                return y_n_ques('w_question', z[1], sentence[z[2]:])

                        if sentence[1]=='many' or sentence[1]=='much' :
                            return w_quest_quant('w_question', 'quantity', sentence)
                        
                        elif sentence[1]=='about':
                            #We replace 'about' by 'is' to have a y_n_question
                            sentence[1]='is'
                            return y_n_ques('w_question', 'invitation', sentence[1:])

                        #For other type of 'how' question
                        else:
                            return w_quest_how('w_question', sentence)

                    #For 'why'
                    elif x[2]=='5':
                        return y_n_ques('w_question', 'reason', sentence[1:])

                    #For 'whose'
                    elif x[2]=='6':
                        return w_quest_whose('w_question', 'owner', sentence)

                    #For 'who'
                    elif x[2]=='7':
                        return y_n_ques('w_question', 'people', sentence[1:])

                    #For 'which'
                    elif x[2]=='8':
                        return other_sentence('w_question', 'choice', sentence[1:])
                    
                    #For 'to whom'
                    elif x[2]=='9':
                        return w_quest_whom('w_question', 'people', sentence[1:])

                #It's a y_n_question
                elif x[1] == '2':
                    return y_n_ques('yes_no_question', '', sentence)

                #It's a conditional sentence
                elif x[1]=='3':
                    return condi_sentence(sentence)

                #Agree
                elif x[1]=='4':
                    return Sentence('agree', '', [], [])

                #Disagree
                elif x[1]=='5':
                    return Sentence('disagree', '', [], [])

                #It's a y_n_question
                elif x[1]=='6':
                    return Sentence('gratulation', '', [], [])

        #It's a statement or an imperative sentence
        if sentence[len(sentence)-1]=='?':
            return other_sentence('yes_no_question', '', sentence)
        else:
            return other_sentence('', '', sentence)

    #Default case
    return []



def w_quest_where(type, request, stc):
    """
    This function process many different type of where question                       
    Input=type and requesting of sentence, the sentence      Output=class Sentence   
    """

    #If there is 'form' at the end => question about the origin
    if stc[len(stc)-1]=='from' or (stc[len(stc)-1]=='?' and stc[len(stc)-2]=='from'):

        #If we remove the first word => it becomes like y_n_question
        return y_n_ques(type, 'origin', stc[1:])
    else:
        #If we remove the first word => it becomes like y_n_question
        return y_n_ques(type, request, stc[1:])



def w_quest_what(type, sentence,sbj_pos):
    """
    This function process many different type of what question                        
    Input=type of sentence, the sentence and position of subject                      
    Output=class Sentence                                                            
    """
    
    #We start with a processing with the function of y_n_question's case
    analysis=y_n_ques(type, 'thing',sentence[sbj_pos-1:])
    
    #The case when we have 'happen'
    if analysis.sv[0].vrb_main[0].endswith('happen'):
        analysis.aim='situation'

    #The case when we have 'think'
    elif analysis.sv[0].vrb_main[0].endswith('think+of') or analysis.sv[0].vrb_main[0].endswith('think+about'):
        analysis.aim='opinion'

    #The case when we have 'like' + conditional
    elif analysis.sv[0].vrb_main[0].endswith('like') and not(analysis.sv[0].vrb_tense.endswith('conditional')):
        analysis.aim='description'

    #The case when we have 'do' + ing form
    elif analysis.sv[0].vrb_main[0].endswith('do') and analysis.sv[0].i_cmpl!=[] and analysis.sv[0].i_cmpl[0].nominal_group[0].noun[0].endswith('ing'):
        analysis.aim='explication'

    return analysis



def w_quest_quant(type, request, sentence):
    """
    This function process many different type of quantity question                    
    Input=type and requesting of sentence, the sentence and beginning sentence list  
    Output=class Sentence                                                            
    """

    for j in frt_wd :
        if sentence[2]==j[0]:
            if j[1]=='2':
                #This case is the same with y_n_question
                return y_n_ques(type, request,sentence[2:])

    analysis=y_n_ques(type, request,sentence[3:])

    #There is not sn in the sentence
    if analysis.sn==[]:
        analysis.sn=[Nominal_Group(['a'],[sentence[2]],[],[],[])]

    #There is not direct object in the sentence
    else:
        analysis.sv[0].d_obj=[Nominal_Group(['a'],[sentence[2]],[],[],[])]
    
    return analysis



def w_quest_how(type, sentence):
    """
    This function process many different type of how question                         
    Input=type of sentence, the sentence      Output=class Sentence                  
    """
    
    analysis=y_n_ques(type, 'manner', sentence[1:])

    #The case when we have 'do' + ing form
    if analysis.sv[0].vrb_main[0].endswith('like'):
        analysis.aim='opinion'
    return analysis



def condi_sentence(sentence):
    """
    This function process the conditional sentence
    Input=sentence                                          Output=class Sentence    
    """

    #We recover the conditional sentence
    conditional_sentence=sentence[1:sentence.index(';')]

    #We perform the 2 processing
    analysis=other_sentence('statement', '', sentence[sentence.index(';')+1:])
    analysis.sv[0].vrb_sub_sentence=[other_sentence('subsentence', 'if', conditional_sentence)]

    return analysis



def w_quest_whose(type, request, sentence):
    """
    This function process many different type of whose question                       
    Input=type and requesting of sentence and the sentence                           
    Output=class Sentence                                                           
    """

    #init
    vg=Verbal_Group(['be'], [],'', [], [], [], [] ,'affirmative',[])
    analysis=Sentence(type, request, [], [])


    #We replace 'whose' by 'that' to have a nominal group
    sentence[0]='that'

    #We recover the subject
    sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)

    if sentence[1]=='not':
        vg.state='negative'

    analysis.sv=[vg]
    return analysis



def w_quest_whom(type, request, sentence):
    """
    This function process whom question                                            
    Input=type and requesting of sentence and the sentence
    Output=class Sentence                                                            
    """
    
    #It is the same with yes or no question
    analysis=y_n_ques(type, request, sentence)
    
    #We have to add 'to' to the verb
    analysis.sv[0].vrb_main[0]=analysis.sv[0].vrb_main[0]+'+to'
    
    return analysis



def y_n_ques(type, request, sentence):
    """
    This function process the yes or no question from of a sentence
    Input=type and requesting of sentence and the sentence                           
    Output=class Sentence                                                            
    """
    
    #init
    vg=Verbal_Group([], [],'', [], [], [], [] ,'affirmative',[])
    analysis=Sentence(type, request, [], [])
    modal=[]

    #We recover the auxiliary 
    aux=sentence[0]
    
    #We have to know if there is a modal
    for m in modal_list:
        if aux==m:
            modal=aux

    #If we have a negative form
    if sentence[1]=='not':
        vg.state='negative'
        #We remove 'not'
        sentence=sentence[:1]+ sentence[2:]

    #Wrong is a noun but not followed by the determinant
    if sentence[1]=='wrong' and request=='thing':
        analysis.sn=[Nominal_Group([],[],['wrong'],[],[])]
        sentence=[sentence[0]]+sentence[2:]
    
    #In this case we have an imperative sentence
    elif analyse_nominal_group.find_sn_pos(sentence, 1)==[] and type!='w_question':
        #We have to reput the 'not'
        if vg.state=='negative':
            sentence=sentence[:1]+['not']+sentence[1:]
        return other_sentence(type, request, sentence)

    #We delete the auxiliary
    sentence=sentence[1:]
    
    #We recover the subject
    sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)
    
    #If there is one element => it is an auxiliary => verb 'be'
    if len(sentence)==0:
        vg.vrb_tense = analyse_verb.find_tense_statement(aux, vg.vrb_adv)
        vg.vrb_main=['be']
    else:
        
        vg.vrb_adv=analyse_verbal_structure.find_vrb_adv(sentence)
        vg.vrb_tense = analyse_verb.find_tense_question(sentence, aux, vg.vrb_adv)

        #We process the verb
        verb=analyse_verb.find_verb_question(sentence, vg.vrb_adv, aux, vg.vrb_tense)
        verb_main=analyse_verb.return_verb(sentence, verb, vg.vrb_tense)
        vg.vrb_main=[other_functions.convert_to_string(verb_main)]
        
        #We delete the verb if the aux is not the verb 'be'
        if vg.vrb_main!=['be']:
            sentence= sentence[sentence.index(verb[0])+len(verb_main):]
        
        #In case there is a state verb followed by an adjective
        if vg.vrb_main[0]=='be' and analyse_nominal_group.adjective_pos(sentence,0)-1!=0:
            pos=analyse_nominal_group.adjective_pos(sentence,0)
            vg.d_obj=[Nominal_Group([],[],sentence[:pos-1],[],[])]
            sentence=sentence[pos:]
        
        #Here we have special processing for different cases
        if sentence!=[]:
            #For 'what' descrition case
            if sentence[0]=='like' and aux!='would':
                vg.vrb_main=['like']
                sentence=sentence[1:]

            #For 'how' questions with often
            elif sentence[0].endswith('ing'):
                vg.vrb_main[0]=vg.vrb_main[0]+'+'+sentence[0]
    
        #We recover the conjunctive subsentence
        sentence=analyse_verbal_structure.process_conjunctive_sub(sentence, vg)
        
        #It verifies if there is a secondary verb
        sec_vrb=analyse_verbal_structure.find_scd_vrb(sentence)
        if sec_vrb!=[]:
            sentence=analyse_verbal_structure.process_scd_sentence(sentence, vg, sec_vrb)
            
        #We recover the subsentence
        sentence=analyse_verbal_structure.process_subsentence(sentence, vg)
        
        #Process relative changes
        sentence=analyse_verbal_structure.correct_i_compl(sentence,vg.vrb_main[0])
        
        #We recover the direct, indirect complement and the adverbial
        sentence=analyse_verbal_structure.recover_obj_iobj(sentence, vg)
    
        #We have to take off adverbs form the sentence
        sentence=analyse_verbal_structure.find_adv(sentence, vg)

    #We perform the processing with the modal
    if modal!=[]:
        vg.vrb_main=[modal+'+'+vg.vrb_main[0]]
    
    #If there is a forgotten*
    vg.vrb_adv=vg.vrb_adv+analyse_verbal_structure.find_vrb_adv (sentence)
    
    analysis.sv=[vg]
    return analysis



def other_sentence(type, request, sentence):
    """
    This function process the other from of a sentence                                
    Input=type and requesting of sentence and the sentence                               
    Output=class Sentence                                                            
    """
    
    #init
    vg=Verbal_Group([], [],'', [], [], [], [] ,'affirmative',[])
    analysis=Sentence(type, request, [], [])
    modal=[]
    
    #We have to add punctuation if there is not
    if sentence[len(sentence)-1]!='.' and sentence[len(sentence)-1]!='?' and sentence[len(sentence)-1]!='!':
        sentence=sentence+['.']
            
    #We search the subject
    sbj=analyse_nominal_group.find_sn_pos(sentence, 0)
    if sbj!=[] or type=='relative' :
        #If we haven't a data type => it is a statement
        if type=='':
            analysis.data_type='statement'

        
        #We have to separate the case using these, this or there
        for p in det_dem_list:
            
            if p==sentence[0] and analyse_verb.infinitive([sentence[1]], 'present simple')==['be']:
                #We recover this information and remove it
                analysis.sn=[Nominal_Group([p],[],[],[],[])]
                sentence=sentence[1:]
        
        if analysis.sn==[]:
            #We recover the subject
            sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)
        
        #We have to know if there is a modal
        for m in modal_list:
            if sentence[0]==m:
                modal=sentence[0]
                
        #We must take into account all possible cases to recover the sentence's tense
        if len(sentence)>1 and sentence[1]=='not':
            vg.state='negative'

            #Before the negative form we have an auxiliary for the negation
            if sentence[0]=='do' or sentence[0]=='does' or sentence[0]=='did' :
                vg.vrb_tense = analyse_verb.find_tense_statement([sentence[0]], [])
                sentence=sentence[2:]
                vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
            
            #There is a modal
            elif modal!=[]:
                sentence=[sentence[0]]+sentence[2:]
                vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
                vg.vrb_tense = analyse_verb.find_tense_statement(sentence, vg.vrb_adv)

            else:
                #We remove 'not' and find the tense
                sentence=sentence[:1]+ sentence[2:]
                vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
                vg.vrb_tense = analyse_verb.find_tense_statement(sentence, vg.vrb_adv)
        
        #For the affirmative processing
        else:
            vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
            vg.vrb_tense = analyse_verb.find_tense_statement(sentence, vg.vrb_adv)
        
        verb=analyse_verb.find_verb_statement(sentence,vg.vrb_adv, vg.vrb_tense)
        verb_main=analyse_verb.return_verb(sentence, verb, vg.vrb_tense)
        vg.vrb_main=[other_functions.convert_to_string(verb_main)]
        
        #We delete the verb
        sentence= sentence[sentence.index(verb[0])+len(verb_main):]
        
        #In case there is a state verb followed by an adjective
        if vg.vrb_main[0]=='be' and analyse_nominal_group.adjective_pos(sentence,0)-1!=0:
            pos=analyse_nominal_group.adjective_pos(sentence,0)
            vg.d_obj=[Nominal_Group([],[],sentence[:pos-1],[],[])]
            sentence=sentence[pos:]
            
        #We perform the processing with the modal
        if modal!=[]:
            vg.vrb_main=[modal+'+'+vg.vrb_main[0]]

    #This is a imperative form
    else:
        #re-init
        analysis.data_type='imperative'
        vg.vrb_tense='present simple'

        #Negative form
        if sentence[1]=='not':
            sentence=sentence[sentence.index('not')+1:]
            vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
            vg.state='negative'
        else:
            vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)

        #We process the verb
        verb=[sentence[0+len(vg.vrb_adv)]]
        vg.vrb_main=[other_functions.convert_to_string(analyse_verb.return_verb(sentence, verb, vg.vrb_tense))]
        
        #We delete the verb
        sentence= sentence[sentence.index(verb[0])+len(verb):]
    
    #We recover the conjunctive subsentence
    sentence=analyse_verbal_structure.process_conjunctive_sub(sentence, vg)
    
    #It verifies if there is a secondary verb
    sec_vrb=analyse_verbal_structure.find_scd_vrb(sentence)
    if sec_vrb!=[]:
        sentence=analyse_verbal_structure.process_scd_sentence(sentence, vg, sec_vrb)
        
    #We recover the subsentence
    sentence=analyse_verbal_structure.process_subsentence(sentence, vg)
        
    #Process relative changes
    sentence=analyse_verbal_structure.correct_i_compl(sentence,vg.vrb_main[0])
        
    #We recover the direct, indirect complement and the adverbial
    sentence=analyse_verbal_structure.recover_obj_iobj(sentence, vg)
    
    #We have to take off abverbs form the sentence
    sentence=analyse_verbal_structure.find_adv(sentence, vg)
    
    #If there is a forgotten*
    vg.vrb_adv=vg.vrb_adv+analyse_verbal_structure.find_vrb_adv (sentence)
    
    analysis.sv=[vg]
    return analysis



def sentences_analyzer(sentences):
    """
    This function is the basic function of parsing                                   
    Input=list of sentences and beginning sentence list                              
    Output=list of class Sentence                                                    
    """

    #init
    class_sentence_list=[]

    #We process all sentences of the list
    for i in sentences:
        
        #We have to add punctuation if there is not
        if i[len(i)-1]!='.' and i[len(i)-1]!='?' and i[len(i)-1]!='!':
            i=i+['.']
        
        class_sentence_list=class_sentence_list+[dispatching(i)]

    return class_sentence_list
