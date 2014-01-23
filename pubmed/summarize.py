from nltk.tag import RegexpTagger, BigramTagger, UnigramTagger
from nltk.corpus import brown
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

brown_train = brown.tagged_sents()
unigram_tagger = UnigramTagger(brown_train)
bigram_tagger = BigramTagger(brown_train, backoff=unigram_tagger)

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
