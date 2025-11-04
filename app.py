from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from utils.bookmark import BookmarkManager


app = Flask(__name__)


# We use this to store queries results to avoid spamming the JPL servers with a ton of requets
search_cache = {}

bookmark_manager = BookmarkManager()

# Routes for Bookmarking

@app.route("/bookmark/add/<name>")
def add_bookmark(name):
    bookmark_manager.add_bookmark(name)
    return jsonify({"status": "success", "name": name})

@app.route("/bookmark/remove/<name>")
def remove_bookmark(name):
    bookmark_manager.remove_bookmark(name)
    return jsonify({"status": "success", "name": name})

@app.route("/bookmarks")
def get_bookmarks():
    return jsonify(bookmark_manager.list_bookmarks())

# Routes for my solar system viwer
@app.route('/')
def splash():
    return render_template('index.html')

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/bookmarksManager')
def bookmarks_page():
    bookmarks = bookmark_manager.load_bookmarks()
    
    return render_template("bookmarksManager.html", bookmarks=bookmarks)
   

@app.route('/object/<name>')
def object_page(name):
    print("test" + name)
    # Most of my data is directly from JPL and their amazing open source APIs
    api_url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={name}"
    try:
        obj = search_cache.get(name)
        print(obj)
    except Exception as e:
        print("API error:", e)
        obj = {}

    return render_template('object.html', obj=obj)


# In the future maybe move this to another page!
@app.route("/results")
def results_page():
    query = request.args.get("q", "")
    results = []

    if query:
        url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={query}"
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            
            
            if 'object' in data:
                obj = data['object']

                search_cache[data['object']['fullname']] = data
                print(search_cache[data['object']['fullname']])
                results.append({
                    "name": obj.get("fullname", obj.get("des", query)),
                    "designation": obj.get("des", ""),
                    "type": obj.get("orbit_class", ""),
                    "discovery": obj.get("discovery_date", ""),
                })
                
            # Satellites (if available)
            if 'satellites' in data:
                for sat in data['satellites']:
                    results.append({
                        "name": sat.get("name", sat.get("des", "Unknown")),
                        "designation": sat.get("des", ""),
                        "type": "Satellite",
                        "discovery": sat.get("discovery_date", ""),
                    })

        except Exception as e:
            print("API error:", e)
            results = []

    return render_template("results.html", query=query, results=results)



if __name__ == '__main__':
    app.run(debug=True)
