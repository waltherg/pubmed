from flask import Flask, render_template, request, url_for, redirect
from summarize import summarize

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tldrmed.html')

@app.route('/<int:pmid>')
def get_summary(pmid=None):
    return summarize(None, pmid)

@app.route('/search', methods=['POST', 'GET'])
def search():
    error = None
    if request.method == 'POST':
        pmid = request.form['pmid']
        return redirect('/'+pmid)
    else:
        return 'Method not available'

if __name__ == '__main__':
    app.run(debug=True)
