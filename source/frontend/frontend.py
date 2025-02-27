from flask import Flask, jsonify, render_template
import requests


app = Flask(__name__)

@app.route("/")
def home():
    # Fetch data from the backend API (GET request)
    backend_url = 'http://localhost:5001/api/data'
    response = requests.get(backend_url)
    data_from_backend = response.json()  # Get the JSON data

    # Render a template with the data from the backend
    return render_template('index.html', data=data_from_backend)
   
@app.route("/get-data")
def get_data():
    backend_url = 'http://localhost:5001/api/data'
    response = requests.get(backend_url)
    data_from_backend = response.json()  # Get the JSON data

    return jsonify({"message": f"Hello from Flask, dynamically loaded! {data_from_backend}"})



if __name__ == "__main__":
    app.run(debug=True)
