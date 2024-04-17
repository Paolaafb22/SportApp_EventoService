from flask import Flask, jsonify
from src.blueprints.evento import eventos_blueprint
from src.errors.errors import ApiError
from flask_cors import CORS
from src.dynamodb_evento import DynamoDbEvento

application = Flask(__name__)
application.register_blueprint(eventos_blueprint)
CORS(application)
dynamo_db_evento = DynamoDbEvento()
dynamo_db_evento.create_table()
## add comment
@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code
##
if __name__ == "__main__":
    application.run(host="0.0.0.0", port = 5002, debug = True)