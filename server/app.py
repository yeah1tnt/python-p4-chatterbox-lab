from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        message_serialized = [message.to_dict() for message in messages]

        response = make_response(jsonify(message_serialized),200)
        return response
    elif request.method == 'POST':
        body = request.get_json()
        message = Message(
            body = body.get('body'), 
            username = body.get('username'),
            )
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(jsonify(message_dict),200)

        return response
    

@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':

        message.body = request.get_json().get('body')

        db.session.add(message)
        db.session.commit()
        message_serialized = message.to_dict()
        response = make_response(jsonify(message_serialized),200)
        return response
    elif request.method == 'DELETE':

        db.session.delete(message)
        db.session.commit()
        response = make_response('',200)
        return response

if __name__ == '__main__':
    app.run(port=5555)
