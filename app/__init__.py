from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

@app.route('/listModels', methods=['GET'])
def listModel():
	query = TruckModel.query.all()
	result = []
	for q in query:
		r = {}
		r['id'] = q.id
		r['truck_model'] = q.truck_model
		r['max_weight']  = q.max_weight
		r['max_volume']  = q.max_volume
		result.append(r)

	return jsonify({'response' : result})

@app.route('/addTruck', methods=['POST'])
def addTruck():
	q   = request.get_json()
	res = TruckModel.query.filter_by(truck_model = q['truck_model'], max_weight = q['max_weight'], max_volume = q['max_volume'])

	if res.count() != 0:
		return jsonify({'response' : 'Duplicate entry'})

	r = TruckModel(q['truck_model'],q['max_weight'],q['max_volume'])
	db.session.add(r)
	db.session.commit()
	return jsonify({'response' : 'Added'})

if __name__ == '__main__':
	app.run(debug=True)
    