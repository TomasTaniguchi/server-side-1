from database.base import db_session
from flask import Flask, make_response, request
from werkzeug.datastructures import FileStorage
from flask_graphql import GraphQLView
from flask_sockets import Sockets
from graphql_ws.gevent import GeventSubscriptionServer, GeventConnectionContext
from schema import schema
from class_api.data_subcription_tk import PayloadSubTk
from template import render_graphiql
import os

# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__, static_folder='img_data')
app.debug = True

sockets = Sockets(app)


@app.route('/payload_subscription', methods=['POST'])
def payload_subscription():

    if request.method == 'POST':
        id = request.json['id']
        data = request.json
        PayloadSubTk.received_data(id, data)
    print(PayloadSubTk.payload_tickets)

    return 'hola', 200


@app.route('/img_data')
def save_img():
    return app.static_folder


@app.route('/graphiql')
def graphql_view():
    print("graphiql")
    return make_response(render_graphiql())


UPLOAD_FOLDER = 'profile_img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/upload_p_image", methods=['POST', 'GET'])
def upload_file():
    print(request.headers)
    file_name = request.headers['filename']
    FileStorage(request.stream).save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    return 'OK', 200


@sockets.route('/subscriptions')
def echo_socket(ws):
    subscription_server.handle(ws)
    return []

@sockets.route('/query')
def echo_socket(ws):
    context.handle(ws)
    return []

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    print(exception)


app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=False))

subscription_server = GeventSubscriptionServer(schema)
context = GeventConnectionContext(schema)
app.app_protocol = lambda environ_path_info: 'graphql-ws'

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
