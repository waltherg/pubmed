from flask import Flask, render_template
from summarize import summarize

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tldrmed.html')

@app.route('/<int:pmid>')
def get_summary(pmid=None):
    return summarize(None, pmid)

if __name__ == '__main__':
    app.run(debug=True)
