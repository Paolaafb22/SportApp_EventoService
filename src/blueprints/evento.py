from flask import Flask, jsonify, request, Blueprint
from ..commands.create_evento import CreateEventos
from ..commands.get_evento import GetEvento
from ..commands.reset import Reset

eventos_blueprint = Blueprint('eventos', __name__)

@eventos_blueprint.route('/eventos', methods = ['POST'])
def create():
    user = CreateEventos(request.get_json()).execute()
    return jsonify(user), 201

@eventos_blueprint.route('/eventos/<id>', methods = ['GET'])
def show(id):
    """ Authenticate(auth_token()).execute() """
    evento = GetEvento(id).execute() 
    return jsonify(evento)

@eventos_blueprint.route('/', methods = ['GET'])
def ping():
    return 'pong'

@eventos_blueprint.route('/eventos/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization