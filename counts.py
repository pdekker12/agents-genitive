# -*- coding: utf-8 -*-


from collections import defaultdict


import io

def check_missing(part, complete):
    missing = []
    for entry in complete:
        if entry not in part:
            missing.append(entry)
    
    if len(missing) > 0:
        print "Missing:"
        for m in missing:
            print m
        



def collect_counts(sentences, interesting_list):
    construction = defaultdict(list)
    function = defaultdict(list)
    constr_func = defaultdict(lambda: defaultdict(list))
    
    qualitative_constr = defaultdict(list)
     
     
    # create dictionaries for each type
    genitive = []
    dative = []
    preposition = []

    ending_ins = 0
    ending_nar = 0
    ending_s = 0
    ending_ar = 0
    ending_a = 0

    #go through each sentence
    for sentence in sentences:
        possessor_in_sentence = False
        preposition_in_sentence = False
        dative_in_sentence = False
        sentence_words = [word for lemma,tag,word in sentence]
        possessee_candidates = list(sentence)
        sentence_string = " ".join(sentence_words)
        for pos in range(0,len(sentence)):
            lemma,tag,word = sentence[pos]
            lemma_cmp=lemma.encode('utf-8')
            ########## Detect only nouns ###########
            # Detect genitive nouns
            #if (len(tag) > 3 and tag[0] == "n" and tag[3]=="e"):
                #possessor_in_sentence = True
                #preceding_string = " ".join(sentence_words[:pos])
                #following_string = " ".join(sentence_words[pos+1:])
                #construction["gen_common_noun"].append((lemma,tag,preceding_string,word,following_string))
                #if lemma_cmp in interesting_list:
                    #construction["interesting_possessor"].append((lemma,tag,preceding_string,word,following_string))
            # Detect dative nouns
            #elif ((len(tag) > 3) and (tag[0]== "n") and (tag[3] == u"þ")):
                #possessor_in_sentence = True
                #preceding_string = " ".join(sentence_words[:pos])
                #following_string = " ".join(sentence_words[pos+1:])
                #construction["dat_common_noun"].append((lemma,tag,preceding_string,word,following_string))
                #if lemma_cmp in interesting_list:
                    #construction["interesting_possessor"].append((lemma,tag,preceding_string,word,following_string))
            # Detect preposition  nouns
            #elif (tag == "ae"
                #or tag ==u"aþ"
                #or tag == u"aþe"
                #or tag == u"aþm"):
                #possessor_in_sentence=True
                #preceding_string = " ".join(sentence_words[:pos])
                #following_string = " ".join(sentence_words[pos+1:])
                #construction["pre_common_noun"].append((lemma,tag,preceding_string,word,following_string))   
                #if lemma_cmp in interesting_list:
                    #construction["interesting_possessor"].append((lemma,tag,preceding_string,word,following_string))
            #else:
                ## Detect possessee if this is not a possessor, and
                ## there is another possessor in the sentence
                #if possessor_in_sentence:
                    #if lemma_cmp in interesting_list:
                        #preceding_string = " ".join(sentence_words[:pos])
                        #following_string = " ".join(sentence_words[pos+1:])
                        #construction["interesting_possessee"].append((lemma,tag,preceding_string,word,following_string))
            
            
            ########### Detect full constructions #################
            # Detect dative, where in some positions this dative can be found on an other position
            #if (u'þ' in tag):
                #if ((tag[0] == "n" and tag[3] == u"þ")
                    #or (tag[0] == "f" and tag[4] == u"þ")    # number dative
                    #or (tag[0] == "l" and tag[3] == u"þ")
                    #or (tag[0] == "g" and tag[3] == u"þ")
                    #or (tag[0] == "t" and tag[4] == u"þ")
                    #or (word == "og" and len(dative) > 0)): # 'og' may occur in dative, as second or later
                        ## TODO: look at excluding gen. pronoun "hans" from list
                        #dative.append((word,pos))
                #else:
                    ## If a dative has built up, it is now ended
                    #if len(dative) > 0:
                        #start_pos = dative[0][1]
                        #end_pos = dative[-1][1]
                        #dative_string = " ".join([word for word,pos in dative])
                        #preceding_string = " ".join(sentence_words[:start_pos])
                        #following_string = " ".join(sentence_words[end_pos+1:])
                        #construction["dat"].append((preceding_string,dative_string,following_string))
                        #dative = []

            if (u'þ' in tag):
                if ((tag[0] == "n" and tag[3] == u"þ")
                or (tag[0] == "f" and tag[4] == u"þ")
                or (tag[0] == "l" and tag[3] == u"þ")
                or (tag[0] == "g" and tag[3] == u"þ")
                or (tag[0] == "t" and tag[4] == u"þ")):
                    dative_in_sentence = True

            if dative_in_sentence:
                if ((tag == "ae"
                or tag == u"aþ"
                or tag == u"aþe"
                or tag == u"aþm")
                and (word in [u"til",u"í",u"á",u"af",u"frá",u"hjá",u"að"])):
                    preposition_in_sentence = True
                    preceding_string = " ".join(sentence_words[:pos-1])
                    following_string = " ".join(sentence_words[pos+1:])
                    construction["pre"].append((preceding_string,word, following_string))

            # Detect genitive
            ending = ""

            if len(tag) > 3 :
                if ((tag [0]== "n") and (tag[3]=="e") # noun genitive
                    or (tag[0] == "f" and tag[4]=="e")    # pronoun genitive
                    or (tag[0] == "l" and tag[3]=="e")    # adjective genitive
                    or (tag[0] == "g" and tag[3]=="e")    # article genitive
                    or (tag[0] == "t" and tag[4]=="e")    # number genitive
                    or (word == "og" and len(genitive) > 0)): # 'og' may occur in genitive, as second or later
                        # TODO: look at excluding gen. pronoun "hans" from list
                        genitive.append((word,pos))
                        possessee_candidates.remove((lemma,tag,word))
                        possessor_in_sentence = True

                        # count suffixes
                        if (word.endswith(("ins"))):
                            ending_ins += 1
                        elif (word.endswith(("nar"))):
                            ending_nar += 1
                        elif (word.endswith(("s"))):
                            ending_s += 1
                        elif (word.endswith(("ar"))):
                            ending_ar += 1
                        elif (word.endswith(("a"))):
                            ending_a += 1
                        if lemma_cmp in interesting_list:
                            construction["interesting_possessor"].append((lemma,tag,preceding_string,word,following_string))
                else:
                    # If a genitive has built up, it is now ended
                    if len(genitive) > 0:
                        start_pos = genitive[0][1]
                        end_pos = genitive[-1][1]
                        genitive_string = " ".join([word for word,pos in genitive])
                        preceding_string = " ".join(sentence_words[:start_pos])
                        following_string = " ".join(sentence_words[end_pos+1:])
                        construction["gen"].append((preceding_string,genitive_string,following_string))
                        genitive = []
            
            # if ((lemma == (u"til"|u"í"|u"á"|u"af"|u"frá"):
            #         preposition_in_sentence = True
            #         preposition.append((word,pos))
            #         start_pos = preposition[0][1]
            #         end_pos = preposition[-1][1]
            #         preposition_string = " ".join([word for word,pos in preposition])
            #         preceding_string = " ".join(sentence_words[:start_pos])
            #         following_string = " ".join(sentence_words[end_pos+1:])
            #         construction["pre"].append((preceding_string,preposition_string,following_string))
            #         preposition = []
            
            # Detect linking pronoun
            # First, find the linking pronoun itself
            if (lemma=="hann" and tag=="fpkee") or (lemma==u"hún" and tag=="fpvee"):
                if pos > 1:
                    prev_lemma, prev_tag, prev_word = sentence[pos-1]
                    prev2_lemma, prev2_tag, prev2_word = sentence[pos-2]
                    
                    # OPTION 1: 'Jans fiets zijn'
                    # Match 'Jans': personal noun, genitive
                    # Match 'fiets: non-genitive noun
                    if ((prev2_tag[0]=="n" and len(prev2_tag)==6 and prev2_tag[3]=="e") and
                    (prev_tag[0]=="n" and prev_tag[3] != "e")):
                        lp_string = " ".join([prev2_word,prev_word,word])
                        preceding_string = " ".join(sentence_words[:pos-2])
                        following_string = " ".join(sentence_words[pos+1:])
                        construction["linking_pronoun"].append((preceding_string,lp_string, following_string))
                        possessor_in_sentence = True
                        if prev2_word.encode('utf-8') in interesting_list:
                            # Jans = possessessor
                            preceding_string = " ".join(sentence_words[:pos-2])
                            following_string = " ".join(sentence_words[pos-1:])
                            construction["interesting_possessor"].append((preceding_string,prev2_word, following_string))
                            possessee_candidates.remove((prev2_lemma,prev2_tag,prev2_word))
                            
                        
                if pos > 0 and pos < len(sentence)-1:
                    prev_lemma, prev_tag, prev_word = sentence[pos-1]
                    next_lemma, next_tag, next_word = sentence[pos+1]
                    # OPTION 2: 'fiets zijn Jans'
                    # Match 'fiets: non-genitive noun
                    # Match 'Jans': personal noun, genitive
                    if ((prev_tag[0]=="n" and prev_tag[3] != "e") and
                    (next_tag[0]=="n" and len(next_tag)==6 and next_tag[3]=="e")):
                        lp_string = " ".join([prev_word,word,next_word])
                        preceding_string = " ".join(sentence_words[:pos-1])
                        following_string = " ".join(sentence_words[pos+2:])
                        construction["linking_pronoun"].append((preceding_string,lp_string, following_string))
                        possessor_in_sentence = True
                        if next_word.encode('utf-8') in interesting_list:
                            # Jans = possessessor
                            preceding_string = " ".join(sentence_words[:pos+1])
                            following_string = " ".join(sentence_words[pos+2:])
                            construction["interesting_possessor"].append((preceding_string,next_word, following_string))
                            possessee_candidates.remove((next_lemma,next_tag,next_word))
                    
                    # OPTION 3: 'Jans zijn fiets'
                    # Match 'fiets: non-genitive noun
                    # Match 'Jans': personal noun, genitive
                    if ((prev_tag[0]=="n" and len(prev_tag)==6 and prev_tag[3]=="e") and
                    (next_tag[0]=="n" and next_tag[3] != "e")):
                        lp_string = " ".join([prev_word,word,next_word])
                        preceding_string = " ".join(sentence_words[:pos-1])
                        following_string = " ".join(sentence_words[pos+2:])
                        construction["linking_pronoun"].append((preceding_string,lp_string, following_string))
                        possessor_in_sentence = True
                        if prev_word.encode('utf-8') in interesting_list:
                            # Jans = possessor
                            preceding_string = " ".join(sentence_words[:pos-1])
                            following_string = " ".join(sentence_words[pos:])
                            construction["interesting_possessor"].append((preceding_string,prev_word, following_string))
                            possessee_candidates.remove((prev_lemma,prev_tag,prev_word))
        
        # At end of sentence, look if there was a possessor in the sentence
        if possessor_in_sentence:
            # Add possessee candidates (everything in sentence that was not possessor)
            # which are in interesting_list
            for lemma,tag,word in possessee_candidates:
                lemma_cmp = lemma.encode('utf-8')
                if lemma_cmp in interesting_list:
                    pos = sentence.index((lemma,tag,word)) # Find real position in sentence
                    preceding_string = " ".join(sentence_words[:pos])
                    following_string = " ".join(sentence_words[pos+1:])
                    construction["interesting_possessee"].append((lemma,tag,preceding_string,word,following_string))
        # At end of sentence, look if there was a preposition in the sentence
        if preposition_in_sentence and dative_in_sentence:
             for lemma,tag,word in possessee_candidates:
                lemma_cmp = lemma.encode('utf-8')
                if lemma_cmp in interesting_list:
                    pos = sentence.index((lemma,tag,word)) # Find real position in sentence
                    preceding_string = " ".join(sentence_words[:pos])
                    following_string = " ".join(sentence_words[pos+1:])
                    construction["interesting_preposition"].append((lemma,tag,preceding_string,word,following_string))
    # Print genitive suffixes
    print "-ins: " + str(ending_ins)
    print "-nar: " + str(ending_nar)
    print "-s: " + str(ending_s)
    print "-ar: " + str(ending_ar)
    print "-a: " + str(ending_a)
    
    # Write to files
    io.write_construction_csv(construction["gen"], "Genitive",1000)
    io.write_construction_csv(construction["pre"], "Preposition",1000)
    io.write_construction_csv(construction["linking_pronoun"], "Linking_pronoun",1000)
    
    io.write_word_csv(construction["interesting_possessor"], "interesting_possessor",2000, sort_on_lemma=True)
    io.write_word_csv(construction["interesting_possessee"], "interesting_possessee",2000, sort_on_lemma=True)
    io.write_word_csv(construction["interesting_preposition"], "interesting_preposition",2000, sort_on_lemma=True)




if __name__ == "__main__":
    data = io.read_data("Saga")
    interesting_list = io.read_interesting_list("icelandic-interesting-modified.txt")
    collect_counts(data, interesting_list)
