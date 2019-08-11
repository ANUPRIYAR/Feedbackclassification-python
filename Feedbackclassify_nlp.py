from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import nltk
from autocorrect import spell
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from nltk.stem.porter import PorterStemmer
import ast


def update_tags(list):
    """
    Function : Input is a cleaned list of words in each sentence along with its
    synonyms and is checked if a specific words or its synonyms is found in the
    input, then a tag is attached.
    param list: list of words in a sentence
    """
    Feedback_Tag=[]
    for word in list:
        if word in synonymns_slow and "Performance issue" not in Feedback_Tag:
            Feedback_Tag.append("Performance issue")
        elif word in synonymns_Complicated_ui and "Complicated UI" not in Feedback_Tag:
            Feedback_Tag.append("Complicated UI")
        elif word in synonymns_Ineffective_sw and "Ineffective software solution" not in Feedback_Tag:
            Feedback_Tag.append("Ineffective software solution")
    ofile=open("output.txt","a")
    print(Feedback_Tag)
    ofile.write(str(Feedback_Tag))
    ofile.write("\n")
    return



def clean_func(list):
    """
    Function : It takes the sentence as the input and corrects spellings
    errors and convert the words to its base form
    param list: list of sentences
    return: Cleaned sentences
    """
    # lemmatizer object to converts words to its base form such us 'caring' to
    # 'Care'
    lemmatizer = WordNetLemmatizer()
    # SpellChecker object correct the basic spellings of the words
    spell = SpellChecker()
    clean_list = []
    for word in list:
        word = spell.correction(word)
        # word = porter_stemmer.stem(word)
        word = lemmatizer.lemmatize(word)
        clean_list.append(word)
    return clean_list


def synonymns(list):
    """
    Function : Creates a list of commonly found synonyms for a word
    param :list of words
    return: synonyms of all words in the list is added back to the input list
    """
    synonymns_list=[]
    for word in list:
        for syn in wordnet.synsets(word):
         for name in syn.lemma_names():
            synonymns_list.append(name)
    return synonymns_list

def antonymns(word):
    """
    Function : To derive the antonym of a word
    param : a word
    return: Antonym of the given word
    """
    antonyms_list=[]
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms_list.append(l.antonyms()[0].name())
    return antonyms_list


def decode_negative(list):
    """
    Function : Words with not, never preceding a adjective will be replaced
     with the antonym of adjective.
    param list: List of words
    return: List of words with no negations
    """
    neg_keywords=[]
    for i in range(0,len(list)):
        if list[i] in ["not","never"]:
             neg_keywords.append(antonymns(list[i+1]))
             neg_keywords = str(neg_keywords).replace('[[', '[').replace(']]', ']')
    neg_keywords=ast.literal_eval(neg_keywords)
    return neg_keywords


open('output.txt', 'w').close()
synonymns_slow = synonymns(["slow","slowly","slowness"])
synonymns_Complicated_ui = synonymns(["complex","confusing","ui","awful","cumbersome","clunky","fail"])
synonymns_Ineffective_sw = synonymns(["ineffective","worst","hard","fail"])


ifile= open('Input.txt','r')
for line in ifile.readlines():
    text = line
    print("text: %s" %text)

    # Converts string into list
    word_sent = word_tokenize(text.lower())
    print("word_sent: %s" %word_sent)

    # Makes a list of all the stop words plus punctuation symbols in english
    # language
    list_stopwords = list(stopwords.words('english') + list(punctuation))

    # Removes the stop words plus punctuation symbols from the our text
    final_words= []
    for word in word_sent:
        word = spell(word)
        if word not in list_stopwords:
            final_words.append(word)

    print("final_words after removing stopwords: %s" %final_words)

    # Tags the verb form to each word
    postag_finalwords = nltk.pos_tag(final_words)
    print(postag_finalwords)
    keyword=[]


    # We are only picking up the words with tags of interest.
    # ####TAGS####
    # RB - adverbs/ ;JJ	adjective ; JJR	adjective, comparative 'bigger' ;
    # JJS adjective, superlative 'biggest' ; RBR adverb, comparative better;
    # RBS adverb, superlative best ; VBD verb, past tense took ; NN	noun ;
    # VB verb ;
    for word in postag_finalwords:
        if word[1] in ('RB', 'JJ', 'JJS', 'JJR', 'RBR', 'RBS', 'VBD','NN','VB'):
             keyword.append(word[0])
    print("Keyword: %s" %keyword)
    keyword = clean_func(keyword)
    print("clean keyword: %s" % keyword)

    for i in range(0,len(keyword)):
        print(keyword[i])
        if keyword[i] in ["not","never"]:
           keyword = decode_negative(keyword)
           break
    update_tags(keyword)
