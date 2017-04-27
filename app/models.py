from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_pyfile('../config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class TruckOwnerDetails(db.Model):

	__tablename__ = 'truckOwners'
	id          = db.Column(db.Integer, primary_key=True)
	name        = db.Column(db.String(50))

	truckDetails = db.relationship("TruckDetails", backref="truckOwners")

	def __init__(self,id,name):
		self.id     = id 		
		self.name   = name

	def __repr__(self):
		return 'Owner %r'%self.name


class CustomerDetails(db.Model):

	__tablename__ = 'customerDetails'
	id          = db.Column(db.Integer, primary_key=True)
	name        = db.Column(db.String(50))

	bookingRequests = db.relationship("BookingRequest", backref="customerDetails")

	def __init__(self,id,name):
		self.id     = id 		
		self.name   = name

	def __repr__(self):
		return 'Customer %r'%self.name
	

class TruckDetails(db.Model):

	__tablename__ = 'truckDetails'
	id         = db.Column(db.Integer, primary_key=True)    # The truck number
	truckModel = db.Column(db.String(50))
	maxWeight  = db.Column(db.Float, default = 0.0)
	maxVolume  = db.Column(db.Float, default = 0.0)
	ownerId    = db.Column(db.Integer, db.ForeignKey('truckOwners.id'))

	plan   = db.relationship("JourneyPlans", backref="truckDetails")

	def __init__(self,id,truckModel,maxWeight,maxVolume,ownerId):
		self.id         = id 
		self.truckModel = truckModel
		self.maxWeight  = maxWeight
		self.maxVolume  = maxVolume
		self.ownerId    = ownerId

	def __repr__(self):
		return 'Truck %r %.2f %.2f %d'%(self.truckModel, self.maxWeight, self.maxVolume, self.ownerId)


class BookingRequest(db.Model):

	__tablename__ = 'bookingRequests'
	id          = db.Column(db.Integer, primary_key=True)
	customerId  = db.Column(db.Integer, db.ForeignKey('customerDetails.id')) 
	source      = db.Column(db.String(60))
	destination = db.Column(db.String(60))
	itemDesc    = db.Column(db.String(60))
	weight      = db.Column(db.Float, default=0.0)
	volume      = db.Column(db.Float, default=0.0)
	startDate   = db.Column(db.DateTime)
	endDate     = db.Column(db.DateTime)

	journeyPlans = db.relationship("JourneyPlans", backref="bookingRequests")

	def __init__(self,id,customerId,source,destination,itemDesc,weight,volume,startDate,endDate):
		self.id     = id 
		self.customerId  = customerId 
		self.source      = source     
		self.destination = destination
		self.itemDesc    = itemDesc   
		self.weight      = weight     
		self.volume      = volume     
		self.startDate   = startDate  
		self.endDate     = endDate    

	def __repr__(self):
		return 'Booking Request %d %r %r %r %.2f %.2f %r %r'%(self.customerId, self.source, self.destination, self.itemDesc, self.weight, self.volume, self.startDate, self.endDate)


class JourneyPlans(db.Model):

	__tablename__ = 'journeyPlans'
	id          = db.Column(db.Integer, primary_key=True)
	bookingId   = db.Column(db.Integer, db.ForeignKey('bookingRequests.id')) 
	truckId     = db.Column(db.Integer, db.ForeignKey('truckDetails.id'))
	destination = db.Column(db.String(60))
	weight      = db.Column(db.Float, default=0.0)
	volume      = db.Column(db.Float, default=0.0)
	startDate   = db.Column(db.DateTime)
	endDate     = db.Column(db.DateTime)
	price       = db.Column(db.Float, default=0.0)
	accepted    = db.Column(db.Boolean, default=0)

	def __init__(self,id,bookingId,truckId,destination,weight,volume,startDate,endDate,price,accepted):
		self.id          =  id 
		self.bookingId   =  bookingId
		self.truckId     =  truckId
		self.destination =  destination
		self.weight      =  weight
		self.volume      =  volume
		self.startDate   =  startDate
		self.endDate     =  endDate
		self.price       =  price
		self.accepted    =  accepted

	def __repr__(self):
		return 'Journey Plans %d %d %r %.2f %.2f %s %s %.2f %d'%(self.bookingId, self.truckId, self.destination, self.weight, self.volume, self.startDate, self.endDate, self.price, self.accepted)


if __name__ == '__main__':
	db.create_all()
	# a = CustomerDetails(id= 2, name = 'Sanju')
	# db.session.add(a)
	# db.session.commit()

	q = CustomerDetails.query.all()
	print(q[1].id)