from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from validationSchema import *
from jsonschema import validate
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

	try:
		validate(q, truck_schema)
	except:
		return jsonify(success= False, errors= 'Invalid parameters')
		
	res = TruckModel.query.filter_by(truck_model = q['truck_model'], max_weight = q['max_weight'], max_volume = q['max_volume'])

	if res.count() != 0:
		return jsonify(success= False, errors= 'Duplicate Entry')

	r = TruckModel(q['truck_model'],q['max_weight'],q['max_volume'])
	db.session.add(r)
	db.session.commit()
	
	return jsonify(success = True)



@app.route('/api/book', methods=['POST'])
def bookingRequest():

	q  = request.get_json()

	try:
		validate(q, booking_schema)
	except:
		return jsonify(success= False, errors= 'Invalid parameters')

	res = BookingRequest.query.filter_by(source = q['source'], destination = q['destination'], item_desc = q['item_desc'], weight = q['weight'], volume = q['volume'], start_date = q['start_date'], end_date = q['end_date'])

	if res.count() != 0:
		return jsonify(success= False, errors= 'Duplicate Entry')

	r = BookingRequest(q['source'],q['destination'],q['item_desc'],q['weight'],q['volume'],q['start_date'],q['end_date'])
	db.session.add(r)
	db.session.commit()

	return jsonify(success = True)



@app.route('/api/truck/location', methods=['POST'])
def findLastDestination():
	q = request.get_json()
	truck_id =q['truck_id']
	try:
		validate(q, truck_location_schema)
	except:
		return jsonify(success= False, errors= 'Invalid parameters')
	res = JourneyPlan.query.order_by(JourneyPlan.id.desc()).filter_by(accepted = 1).filter( JourneyPlan.end_date <= datetime.now()).first()
	
	if res == None:
		res = Truck.query.filter_by(id = truck_id)
		if res.count() != 0:
			return jsonify({'location' : res[0].source })
		
		return jsonify(success= False, errors= 'Truck not found')

	return jsonify({ 'location' : res[0].destination})


@app.route('/api/list/plans', methods=['POST'])
def listPlans():
	q = request.get_json()
	user_id    = q['user_id']
	booking_id = q['booking_id']

	print(type(q))

	try:
		validate(q, plan_schema)
	except:
		return jsonify(success= False, errors= 'Invalid parameters')

	res = BookingRequest.query.filter_by(id = booking_id, customer_id = user_id)
	print(BookingRequest.query.all())

	if res.count() == 0:
		return jsonify(success = False, errors = 'Make sure you have logged in.')

	res = JourneyPlan.query.filter_by(booking_id = booking_id)
	result = []

	for r in res:
		a = {}
		# a['id'] = q.id
		a['booking_id']  = r.booking_id  
		a['plan_type']   = r.plan_type    
		a['truck_id']    = r.truck_id      
		a['source']      = r.source          
		a['destination'] = r.destination
		a['weight']      = r.weight          
		a['volume']      = r.volume          
		a['start_date']  = r.start_date  
		a['end_date']    = r.end_date      
		a['price']       = r.price            
		a['accepted']    = r.accepted      
		result.append(a)

	return jsonify({'response' : result})
		
@app.route('/api/plan/select', methods=['POST'])
def selectPlan():
	plan = request.get_json()

	try:
		validate(plan, plan_id_schema)
	except:
		return jsonify(success= False, errors= 'Invalid parameters')

	q = JourneyPlan.query.filter_by(id = plan['plan_id'])

	if q.count() == 0:
		return jsonify(success = False, errors = 'No such plan id exists')
		

	confirmed = JourneyPlan.query.filter_by(booking_id = q[0].booking_id, accepted = 1).count()

	if confirmed:
		return jsonify({'response': 'Plan confirmed for this booking already.' })

	q[0].accepted = 1
	db.session.commit()

	return jsonify(success = True)
	

if __name__ == '__main__':
	app.run(debug=True)
