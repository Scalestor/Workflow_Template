from flask import Flask, jsonify, render_template,request
import requests


app = Flask(__name__)

@app.route("/")
def home():
    # Fetch data from the backend API (GET request)
    backend_url = 'http://localhost:5001/api/tables'
    response = requests.get(backend_url)
    data_from_backend = response.json()  # Get the JSON data

    # Render a template with the data from the backend
    return render_template('index.html', data=data_from_backend)

@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.url}")

@app.route("/get-tables", methods=['GET'])
def get_tables():
    backend_url = 'http://localhost:5001/api/tables'
    response = requests.get(backend_url)
    data_from_backend = response.json()["message"]  # Get the JSON data
    return jsonify(data_from_backend)

@app.route("/get-data", methods=['POST','GET'])
def get_data():
    if request.method == "GET":
        return jsonify({"error": "This endpoint only accepts POST requests"}), 405
    

    backend_url = 'http://localhost:5001/api/data'
    request_payload = request.get_json()  # Get JSON data from request body
    table_name = request_payload.get('table')  # Extract 'table' field

    # Get the response
    backend_response = requests.post(backend_url, json={"table": table_name})
    print(f"Backend response request: {backend_response}")
    print(f"Backend response request: {backend_response.text}")
    
    # Work with the response to generate the new response
    if backend_response.status_code == 200:
        message_from_backend = backend_response.json().get("message", "No message received")
        data_from_backend = backend_response.json().get("data", "No data received")

        return jsonify({"message": f"Message from backend {message_from_backend}.",
                        "data":data_from_backend
                        })
    else:
        return jsonify({"error": "Backend request failed"
                        , "status_code": backend_response.status_code
                        , "original_request" :table_name
                        ,"original_response":backend_response.json()
                        
                        }), 500




if __name__ == "__main__":
    app.run(debug=True)
