from flask import Flask, jsonify, request, Blueprint
from ..commands.create_evento import CreateEvento
from ..commands.get_evento import GetEvento
from ..commands.reset import Reset
from ..commands.create_deportista_evento import CreateDeportaistaEvento
from ..commands.get_deportista_evento import GetDeportistaEvento

eventos_blueprint = Blueprint('eventos', __name__)

@eventos_blueprint.route('/eventos', methods = ['POST'])
def create():
    evento = CreateEvento(request.get_json()).execute()
    return jsonify(evento), 201

@eventos_blueprint.route('/eventos/<id>', methods = ['GET'])
def show(id):
    """ Authenticate(auth_token()).execute() """
    evento = GetEvento(id).execute() 
    return jsonify(evento)

@eventos_blueprint.route('/eventos/ping', methods = ['GET'])
def ping():
    return 'pong'

@eventos_blueprint.route('/eventos/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

@eventos_blueprint.route('/eventos/user', methods = ['POST'])
def create_deportista_evento():
    deportista_evento = CreateDeportaistaEvento(request.get_json()).execute()
    return jsonify(deportista_evento), 201

@eventos_blueprint.route('/eventos/user/<id>', methods = ['GET'])
def show_deportista_evento(id):
    """ Authenticate(auth_token()).execute() """
    evento = GetDeportistaEvento(id).execute() 
    return jsonify(evento)


def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization