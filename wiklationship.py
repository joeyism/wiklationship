import wikipedia
import spacy
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

global nlp 
nlp = spacy.load("en")
pool = ThreadPool(4)

def noun_is_in_sentence(input_noun, sentence):
    sentence = nlp(sentence)
    for noun in sentence.noun_chunks:
        if input_noun == noun.text:
            return True
    return False

def match_word_with_sentences(sentences, word):
    print (word)
    matched_sentences = []
    for sentence in sentences:
        if noun_is_in_sentence(word, sentence):
            matched_sentences.append(sentence)
    return (word, matched_sentences)
        

def get_noun_and_sentence_from_page(parent_entity):
    parent_wikipedia = wikipedia.page(parent_entity)

    doc = nlp(unicode(parent_wikipedia.content))
    sentences = [sent.string.strip() for sent in doc.sents]

    func = partial(match_word_with_sentences, sentences)
    word_sentences = pool.map(func, parent_wikipedia.links)
    
    word_dict = dict(word_sentences)
    return word_dict

parent_entity = "Toronto Raptors"
print (get_noun_and_sentence_from_page(parent_entity))
