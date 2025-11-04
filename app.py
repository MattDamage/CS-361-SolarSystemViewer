from flask import Flask, render_template, request  
import requests
app = Flask(__name__)

cache = {}


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
    print("test" + name)
    # Most of my data is directly from JPL and their amazing open source APIs
    api_url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={name}"
    try:
        resp = requests.get(api_url, timeout=5)
        data = resp.json()
        obj = data.get('object', {})
        orbit = data.get('orbit', {})
        obj['orbit'] = orbit
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
