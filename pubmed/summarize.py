from nltk.tag import RegexpTagger, BigramTagger, UnigramTagger
from nltk.corpus import brown
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

import cPickle as pickle

from time import time

brown_train = brown.tagged_sents()

try:
    unigram_time = time()
    unigram_tagger = pickle.load(open('unigram.object', 'r'))
    unigram_time = time() - unigram_time
    print('Loaded pickled unigram tagger: %.4f s' % unigram_time)
except:
    unigram_time = time()
    unigram_tagger = UnigramTagger(brown_train)
    pickle.dump(unigram_tagger, open('unigram.object', 'w'))
    unigram_time = time() - unigram_time
    print('Retrained and pickled unigram tagger: %.4f s' % unigram_time)

try:
    bigram_time = time()
    bigram_tagger = pickle.load(open('bigram.object', 'r'))
    bigram_time = time() - bigram_time
    print('Loaded pickled bigram tagger: %.4f s' % bigram_time)
except:
    bigram_time = time()
    bigram_tagger = BigramTagger(brown_train, backoff=unigram_tagger)
    pickle.dump(bigram_tagger, open('bigram.object', 'w'))
    bigram_time = time() - bigram_time
    print('Retrained and pickled bigram tagger: %.4f s' % bigram_time)

def summarize(body, pmid):
    if not body:
        return('No summary avialable for PMID %d' % pmid)

    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['et al', 'i.e', 'e.g', 'ref', 'c.f',
                                    'fig', 'Fig', 'Eq', 'eq', 'eqn', 'Eqn'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_splitter.tokenize(body)
    
    tagged = []
    for sentence in sentences:
        tagged.append(bigram_tagger.tag(sentence.split()))
    
    summary = []
    for sentence in tagged:
        for (word, tag) in sentence:
            if tag == 'PPSS' and word.lower() == 'we':
                summary.append(' '.join(nltk.tag.untag(sentence)))

    summary_string = ''
    for s in summary:
        summary_string += s+'\n'

    return summary_string
