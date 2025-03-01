from sqlalchemy import create_engine, inspect,text
from sqlalchemy.orm import  sessionmaker
from flask import Flask, jsonify,request



from source.config import database


app = Flask(__name__)

allowed_resources = ["data","tables"]

@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.url} 'Args' {request.args} 'Data' {request.data}")

@app.route('/api/<resource>', methods=["GET","POST"])
def handle_request(resource):
    if resource not in allowed_resources:
        return jsonify({"error": "Resource not found"}), 404

    if resource == "tables":
        engine = create_engine(database.database_engine_string, echo=True)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return jsonify({"message": tables})
    
    if resource == "data":
        engine = create_engine(database.database_engine_string, echo=True)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        look_for_table = request.json["table"]

        if look_for_table not in tables:
            return jsonify({"error": f"Table {look_for_table} not found. Expected {request.json}. Have tables {tables}"}), 404
        
        with engine.connect() as connection:
            query = text(f"SELECT COUNT(*) FROM {look_for_table} ")
            result = connection.execute(query).scalar()
            response = {"message": f"Data from query {query}" , "data":result}
            print(f"Message built: {response}")
            return jsonify(response)
        

   



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001)  # Backend server runs on port 5001
