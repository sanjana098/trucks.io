from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_pyfile('../config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class TruckOwner(db.Model):

	__tablename__ = 'truckOwners'
	id          = db.Column(db.Integer, primary_key=True)
	name        = db.Column(db.String(50))

	truck_details = db.relationship("Truck", backref="truckOwners")

	def __init__(self,name): 		
		self.name   = name

	def __repr__(self):
		return 'Owner %r'%self.name

class TruckModel(db.Model):
	__tablename__ = 'truckModel'
	id          = db.Column(db.Integer, primary_key=True)
	truck_model = db.Column(db.String(50))
	max_weight  = db.Column(db.Float, default = 0.0)
	max_volume  = db.Column(db.Float, default = 0.0)

	def __init__(self, truck_model, max_weight, max_volume):
		self.truck_model = truck_model
		self.max_weight  = max_weight
		self.max_volume  = max_volume

	def __repr__(self):
		return 'TruckModel %r %.2f %.2f'%(self.truck_model, self.max_weight, self.max_volume)

class Customer(db.Model):

	__tablename__ = 'customerDetails'
	id          = db.Column(db.Integer, primary_key=True)
	name        = db.Column(db.String(50))

	booking_request = db.relationship("BookingRequest", backref="customerDetails")

	def __init__(self,name): 		
		self.name   = name

	def __repr__(self):
		return 'Customer %r'%self.name
	

class Truck(db.Model):

	__tablename__ = 'truckDetails'
	id          = db.Column(db.Integer, primary_key=True)    # The truck number
	truck_model = db.Column(db.String(50))
	source      = db.Column(db.String(50))
	max_weight  = db.Column(db.Float, default = 0.0)
	max_volume  = db.Column(db.Float, default = 0.0)
	owner_id    = db.Column(db.Integer, db.ForeignKey('truckOwners.id'))

	plan   = db.relationship("JourneyPlan", backref="truckDetails")

	def __init__(self,truck_model,source, max_weight,max_volume,owner_id):
		self.truck_model = truck_model
		self.source      = source
		self.max_weight  = max_weight
		self.max_volume  = max_volume
		self.owner_id    = owner_id

	def __repr__(self):
		return 'Truck %r %r %.2f %.2f %d'%(self.truck_model, self.source, self.max_weight, self.max_volume, self.owner_id)


class BookingRequest(db.Model):

	__tablename__ = 'bookingRequests'
	id           = db.Column(db.Integer, primary_key=True)
	customer_id  = db.Column(db.Integer, db.ForeignKey('customerDetails.id')) 
	source       = db.Column(db.String(60))
	destination  = db.Column(db.String(60))
	item_desc    = db.Column(db.String(60))
	weight       = db.Column(db.Float, default=0.0)
	volume       = db.Column(db.Float, default=0.0)
	start_date   = db.Column(db.DateTime)
	end_date     = db.Column(db.DateTime)

	journeyPlan = db.relationship("JourneyPlan", backref="bookingRequests")

	def __init__(self,customer_id,source,destination,item_desc,weight,volume,start_date,end_date): 
		self.customer_id  = customer_id 
		self.source       = source     
		self.destination  = destination
		self.item_desc    = item_desc   
		self.weight       = weight     
		self.volume       = volume     
		self.start_date   = start_date  
		self.end_date     = end_date    

	def __repr__(self):
		return 'Booking Request %d %r %r %r %.2f %.2f %r %r'%(self.customer_id, self.source, self.destination, self.item_desc, self.weight, self.volume, self.start_date, self.end_date)


class JourneyPlan(db.Model):

	__tablename__ = 'journeyPlans'
	id          = db.Column(db.Integer, primary_key=True)
	booking_id  = db.Column(db.Integer, db.ForeignKey('bookingRequests.id')) 
	truck_id    = db.Column(db.Integer, db.ForeignKey('truckDetails.id'))
	destination = db.Column(db.String(60))
	weight      = db.Column(db.Float, default=0.0)
	volume      = db.Column(db.Float, default=0.0)
	start_date  = db.Column(db.DateTime)
	end_date    = db.Column(db.DateTime)
	price       = db.Column(db.Float, default=0.0)
	accepted    = db.Column(db.Boolean, default=0)

	def __init__(self,booking_id,truck_id,destination,weight,volume,start_date,end_date,price,accepted):
		self.booking_id  =  booking_id
		self.truck_id    =  truck_id
		self.destination =  destination
		self.weight      =  weight
		self.volume      =  volume
		self.start_date  =  start_date
		self.end_date    =  end_date
		self.price       =  price
		self.accepted    =  accepted

	def __repr__(self):
		return 'Journey Plan %d %d %r %.2f %.2f %s %s %.2f %d'%(self.booking_id, self.truck_id, self.destination, self.weight, self.volume, self.start_date, self.end_date, self.price, self.accepted)


if __name__ == '__main__':
	# db.create_all()
	# model = TruckModel('TataMini',1,450)
	# db.session.add(model)
	# db.session.commit()
	print("hi")