from flask import Flask, render_template, request, url_for, redirect
from summarize import summarize
import requests
from lxml import etree
from bs4 import BeautifulSoup as BS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tldrmed.html')

@app.route('/<int:pmid>')
def get_summary(pmid=None):
    r = requests.get('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
                       'elink.fcgi?dbfrom=pubmed&id=%d&cmd=prlinks'
                       '&retmode=json' % pmid)
    
    body = None
    if r.status_code == 200:
        xml = etree.fromstring(r.text)
        try:
            url = xml.xpath('//Url')[0].text
        except:
            return('PubMed provided no fulltext URL for PMID %d' %pmid)
        full_text_r = requests.get(url)
        article = BS(full_text_r.text)
        paragraphs = article.findAll(['p'])
        body = ' '.join([p.text for p in paragraphs])

    return summarize(body, pmid)

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
