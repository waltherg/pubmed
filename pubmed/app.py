from flask import Flask, render_template, request, url_for, redirect
from summarize import summarize
import requests
from lxml import etree
from bs4 import BeautifulSoup as BS

import cPickle as pickle
from time import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tldrmed.html')

@app.route('/<int:pmid>')
def get_summary(pmid=None):
    try:
        summary_time = time()
        summary, url = pickle.load(open('%d.summary' % pmid, 'r'))
        summary_time = time() - summary_time
        print('Retrieve pickled summary for PMID %d: %.4f s' % (pmid,
                                                                summary_time))
    except:
        summary_time = time()
        summary, url = make_summary(pmid)
        pickle.dump([summary, url], open('%d.summary' % pmid, 'w'))
        summary_time = time() - summary_time
        print('Remake & pickle summary for PMID %d: %.4f s' % (pmid,
                                                               summary_time))

    return render_template('tldrmed.html',
                           article_summary=summary,
                           article_url=url,
                           request_pmid=pmid)

def make_summary(pmid=None):
    r = requests.get('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
                       'elink.fcgi?dbfrom=pubmed&id=%d&cmd=prlinks'
                       '&retmode=json' % pmid)
    
    body = None
    if r.status_code == 200:
        xml = etree.fromstring(r.text)
        try:
            url = xml.xpath('//Url')[0].text
            full_text_r = requests.get(url)
            article = BS(full_text_r.text)
            paragraphs = article.findAll(['p'])
            body = ' '.join([p.text for p in paragraphs])
            summary = summarize(body, pmid)
        except:
            summary = ['PubMed provided no full text URL for PMID %d' %pmid]
            url = None

    return summary, url

@app.route('/search', methods=['POST', 'GET'])
def search():
    error = None
    if request.method == 'POST':
        pmid = request.form['pmid']
        return redirect('/'+pmid)
    else:
        return 'Method not available'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
