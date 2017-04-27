from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It\'s cooool'})

if __name__ == '__main__':
    app.run(debug=True)
    