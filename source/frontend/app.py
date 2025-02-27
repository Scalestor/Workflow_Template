from flask import Flask, jsonify, render_template
import time
#from flask_cors import CORS  # Enable CORS if needed

app = Flask(__name__)
#CORS(app)  # Allow cross-origin requests (optional)

@app.route("/")
def home():
    return render_template("index.html")  # Serve the HTML page

@app.route("/get-data")
def get_data():
    time.sleep(5)
    return jsonify({"message": "Hello from Flask, dynamically loaded!"})



if __name__ == "__main__":
    app.run(debug=True)
