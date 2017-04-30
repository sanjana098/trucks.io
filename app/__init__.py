from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_inputs.validators import JsonSchema
from datetime import datetime
from models import *

app = Flask(__name__)

@app.route('/api/list/models', methods=['GET'])
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



@app.route('/api/add/truck', methods=['POST'])
def addTruck():

	q   = request.get_json()
	res = TruckModel.query.filter_by(truck_model = q['truck_model'], max_weight = q['max_weight'], max_volume = q['max_volume'])

	if res.count() != 0:
		return jsonify(success= False, errors= 'Duplicate Entry')

	r = TruckModel(q['truck_model'],q['max_weight'],q['max_volume'])
	db.session.add(r)
	db.session.commit()
	
	return jsonify({'response' : 'Added'})
	# return jsonify(success = True)



@app.route('/api/book', methods=['POST'])
def bookingRequest():

	q  = request.get_json()
	res = BookingRequest.query.filter_by(source = q['source'], destination = q['destination'], item_desc = q['item_desc'], weight = q['weight'], volume = q['volume'], start_date = q['start_date'], end_date = q['end_date'])

	if res.count() != 0:
		return jsonify(success= False, errors= 'Duplicate Entry')

	r = BookingRequest(q['source'],q['destination'],q['item_desc'],q['weight'],q['volume'],q['start_date'],q['end_date'])
	db.session.add(r)
	db.session.commit()

	return jsonify({'response' : 'Added'})



@app.route('/api/truck/location', methods=['POST'])
def findLastDestination():

	truck_id = request.json('truck_id')
	res = JourneyPlan.query.order_by(JourneyPlan.id.desc()).filter_by(accepted = 1, end_date < datetime.now()).first()
	
	if res.count() == 0:
		res = Truck.query.filter_by(id = truck_id)
		if res.count != 0:
			return jsonify({'current_location' : res[0].source })
		
		return jsonify(success= False, errors= 'Not found')

	return jsonify({ 'location' : res[0].destination})


if __name__ == '__main__':
	app.run(debug=True)
    