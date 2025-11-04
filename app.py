from flask import Flask, render_template, request  

app = Flask(__name__)


# Routes for my solar system viwer
@app.route('/')
def splash():
    return render_template('index.html')

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/bookmarks')
def bookmarks_page():
    return render_template('bookmarks.html')

@app.route('/object/<name>')
def object_page(name):
    return render_template('object.html', name=name)

@app.route("/results")
def results_page():
    query = request.args.get("q")
    search_results = [] 
    return render_template("results.html", query=query, results=search_results)


if __name__ == '__main__':
    app.run(debug=True)
