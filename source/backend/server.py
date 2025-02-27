from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import  sessionmaker
from flask import Flask, jsonify



from source.config import database


app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Example business logic
    engine = create_engine(database.database_engine_string, echo=True)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return jsonify({"message": tables})

#@app.route('/api/process', methods=['POST'])
#def process_data():
    # Example business logic for processing data sent by frontend
    #data = request.json
    #result = {"processed_data": f"Processed: {data.get('value')}"}
    #return jsonify(result)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001)  # Backend server runs on port 5001
