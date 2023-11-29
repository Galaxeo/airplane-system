#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airport_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/userRegister')
def userRegister():
	return render_template('userRegister.html')

@app.route("/staffRegister")
def staffRegister():
	return render_template('staffRegister.html')

# ------ All user oriented routes ------ #
#Authenticate register for users
@app.route('/userRegisterAuth', methods=['GET', 'POST'])
def userRegisterAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	firstName = request.form['firstname']
	lastName = request.form['lastname']
	buildingNum= request.form['buildingNum']
	street = request.form['street']
	aptNum = request.form['aptNum']
	if aptNum == '':
		aptNum = None
	city = request.form['city']
	state= request.form['state']
	zipcode = request.form['zipcode']
	passportNumber = request.form['passportNumber']
	passportExpiration = request.form['passportExpiration']
	passportCountry = request.form['passportCountry']
	dateOfBirth = request.form['dateOfBirth']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('userRegister.html', error = error)
	else:
		try:
			ins = 'INSERT INTO customer VALUES(%s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s, %s)'
			cursor.execute(ins, (email, password, firstName, lastName, buildingNum, street, aptNum, city, state, zipcode, passportNumber, passportExpiration, passportCountry, dateOfBirth))
			conn.commit()
			cursor.close()
		except:
			error = "Please make sure that the fields are correct"
			return render_template('userRegister.html', error = error)
		return render_template('index.html')
# Authenticates login for users
@app.route('/userLoginAuth', methods=['GET', 'POST'])
def userLoginAuth():
	email = request.form['email']
	password = request.form['password']
	cursor = conn.cursor()
	query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
	cursor.execute(query, (email, password))
	data = cursor.fetchone()
	error = None
	if(data):
		session['email'] = email
		print(data)
		session['firstName'] = data['FirstName']
		return redirect(url_for('userHome'))
	else:
		error = "Invalid login or username"
		return render_template('userLogin.html', error=error)
@app.route('/userLogin')
def userLogin():
	return render_template('userLogin.html')
@app.route('/userHome')
def userHome():
	email = session['email']
	firstName = session['firstName']
	# cursor = conn.cursor();
	# query = 'SELECT * FROM flight WHERE status = "upcoming"'
	# cursor.execute(query)
	# data = cursor.fetchall()
	# cursor.close()
	return render_template('userHome.html', firstName=firstName)
# View user flights
@app.route('/userViewFlights', methods=['GET', 'POST'])
def userViewFlights():
	firstName = session['firstName']
	email = session['email']
	cursor = conn.cursor();
	# query where we select all flights that the user has purchased
	query = 'SELECT f.FlightNum, f.AirlineName, p.TicketID FROM flight as f, ticket as t, purchase as p WHERE p.email = %s AND p.TicketID = t.TicketID AND t.FlightNum = f.FlightNum'
	# query all flights
	# query = 'SELECT * FROM flight'
	cursor.execute(query, (email))
	data = cursor.fetchall()
	cursor.close()
	return render_template('userHome.html', firstName=firstName, flights=data)
# Search for flights with any of the given parameters
@app.route('/userSearchFlights', methods=['GET', 'POST'])
def userSearchFlights():
	firstName = session['firstName']
	departureAirport = request.form['departureAirport']
	arrivalAirport = request.form['arrivalAirport']
	departureTime = request.form['departureTime']
	arrivalTime = request.form['arrivalTime']
	cursor = conn.cursor();
	query = 'SELECT * FROM flight WHERE departureAirport = %s OR arrivalAirport = %s OR departureTime = %s OR arrivalTime = %s'
	cursor.execute(query, (departureAirport, arrivalAirport, departureTime, arrivalTime))
	data = cursor.fetchall()
	cursor.close()
	return render_template('userHome.html', firstName=firstName, searched=data)
# Purchase ticket
@app.route('/userPurchaseTicket', methods=['GET', 'POST'])
def userPurchaseTicket():
	# Use userhome.html as reference for inputs
	firstName = session['firstName']
	email = session['email']
	flightNum = request.form['flightNum']
	cardType = request.form['cardType']
	cardNum = request.form['cardNum']
	cardExp = request.form['cardExp']
	# check if card date is valid
	if datetime.strptime(cardExp, '%Y-%m-%d') < datetime.now():
		return render_template('userHome.html', firstName=firstName, message="Invalid card date")
	cardName = request.form['cardName']
	purchaseTime = datetime.now()
	ticketFirstName = request.form['firstName']
	lastName = request.form['lastName']
	dateOfBirth = request.form['dateOfBirth']
	# check if date of birth is before today
	if datetime.strptime(dateOfBirth, '%Y-%m-%d') > datetime.now():
		return render_template('userHome.html', firstName=firstName, message="Invalid date of birth")
	# available tickets are the ones that are not purchased
	query = 'SELECT * FROM ticket WHERE FlightNum = %s AND TicketID NOT IN (SELECT TicketID FROM purchase)'
	cursor = conn.cursor()
	cursor.execute(query, (flightNum))
	# if no tickets are available, return error
	if cursor.rowcount == 0:
		return render_template('userHome.html', firstName=firstName, message="No tickets available")
	# otherwise, purchase the ticket
	# calculated price is same as base price from flight for now
	else:
		data = cursor.fetchone()
		ticketID = data['TicketID']
		# fetch base price from flight
		query = 'SELECT basePrice FROM flight WHERE FlightNum = %s'
		cursor.execute(query, (flightNum))
		price = cursor.fetchone()['basePrice']
		ins = 'INSERT INTO purchase VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'
		cursor.execute(ins, (ticketID, email, cardType, cardNum, cardExp, cardName, purchaseTime, price, ticketFirstName, lastName, dateOfBirth))
		conn.commit()
		cursor.close()
		return render_template('userHome.html', firstName=firstName, message="Ticket purchased successfully")
# Cancel ticket
@app.route('/userCancelTicket', methods=['GET', 'POST'])
def userCancelTicket():
	firstName = session['firstName']
	email = session['email']
	ticketID = request.form['ticketID']
	cursor = conn.cursor()
	query = 'DELETE FROM purchase WHERE TicketID = %s AND email = %s'
	cursor.execute(query, (ticketID, email))
	conn.commit()
	cursor.close()
	return render_template('userHome.html', firstName=firstName, message="Ticket cancelled successfully")
# Show previous flights
@app.route('/userRatingsTable', methods=['GET', 'POST'])
def userShowPreviousFlights():
	email = session['email']
	firstName = session['firstName']
	cursor = conn.cursor();
	# query that selects all flights that the user has purchased and that have already happened
	query = 'SELECT * FROM flight as f, ticket as t, purchase as p WHERE p.email = %s AND p.TicketID = t.TicketID AND t.FlightNum = f.FlightNum AND f.arrivalTime < NOW()'
	cursor.execute(query, (email))
	data = cursor.fetchall()
	cursor.close()
	return render_template('userHome.html', email=email, firstName=firstName, ratings=data)
# User clicks on give rating button, redirects to rating page with flightNum and email parameters
@app.route('/userGiveRating', methods=['GET', 'POST'])
def userGiveRating():
	email = session['email']
	firstName = session['firstName']
	flightNum = request.form['flightNum']
	return render_template('userRatings.html', email=email, firstName=firstName, flightNum=flightNum)
# User submits rating
@app.route('/userSubmitRating', methods=['GET', 'POST'])
def userSubmitRating():
	email = session['email']
	firstName = session['firstName']
	flightNum = request.form['flightNum']
	rating = request.form['rating']
	comment = request.form['comment']
	cursor = conn.cursor()
	ins = 'INSERT INTO rating VALUES(%s, %s, %s, %s)'
	cursor.execute(ins, (email, rating, flightNum, comment))
	conn.commit()
	cursor.close()
	return render_template('userHome.html', email=email, firstName=firstName, message="Rating submitted successfully")

# ------ All staff oriented routes ------ #
# Authenticate register for staff
@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffRegisterAuth():
	username = request.form['username']
	password = request.form['password']
	airlineName = request.form['airlineName']
	firstName = request.form['firstname']
	lastName = request.form['lastname']
	dateOfBirth = request.form['dateOfBirth']
	cursor = conn.cursor()
	query = 'SELECT * FROM airlinestaff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists"
		return render_template('staffRegister.html', error = error)
	else:
		try:
			ins = 'INSERT INTO airlinestaff VALUES(%s, MD5(%s), %s, %s, %s, %s)'
			cursor.execute(ins, (username, password, airlineName, firstName, lastName, dateOfBirth))
			conn.commit()
			cursor.close()
		except:
			error = "Please make sure that the fields are correct"
			return render_template('staffRegister.html', error = error)
		return render_template('index.html')
@app.route('/staffLogin')
def staffLogin():
	return render_template('staffLogin.html')
# Authenticates login for staff
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = 'SELECT * FROM airlinestaff WHERE username = %s and password = md5(%s)'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	error = None
	if(data):
		session['username'] = username
		session['airlineName'] = data['AirlineName']
		return redirect(url_for('staffHome'))
	else:
		error = "Invalid login or username"
		return render_template('staffLogin.html', error=error)

@app.route('/staffHome')
def staffHome():
	username = session['username']
	return render_template('staffHome.html', username=username)
@app.route('/staffShowFlights', methods=['GET', 'POST'])
# Show flights
def staffShowFlights():
	username = session['username']
	airlineName = session['airlineName']
	cursor = conn.cursor();
	query = 'SELECT * FROM flight WHERE AirlineName = %s'
	cursor.execute(query, (airlineName))
	data = cursor.fetchall()
	cursor.close()
	return render_template('staffHome.html', username=username, data=data)
@app.route('/staffAddFlight', methods=['GET', 'POST'])
# Add flight
def staffAddFlight():
	username = session['username']
	airlineName = session['airlineName']
	flightNum = request.form['flightNum']
	departureTime = request.form['departureTime']
	departureAirport = request.form['departureAirport']
	arrivalTime = request.form['arrivalTime']
	arrivalAirport = request.form['arrivalAirport']
	basePrice = request.form['basePrice']
	status = request.form['status']
	planeID = request.form['planeID']
	try:
		cursor = conn.cursor()
		ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (airlineName, flightNum, departureTime, departureAirport, arrivalTime, arrivalAirport, basePrice, status, planeID))
		conn.commit()
		cursor.close()
	except:
		return render_template('staffHome.html', username=username, message="Please make sure that the fields are correct")
	return render_template('staffHome.html', username=username, message="Flight added successfully")
# Change status of flight
@app.route('/staffChangeStatus', methods=['GET', 'POST'])
def staffChangeStatus():
	username = session['username']
	airlineName = session['airlineName']
	flightNum = request.form['flightNum']
	status = request.form['status']
	cursor = conn.cursor()
	query = 'UPDATE flight SET status = %s WHERE AirlineName = %s AND flightNum = %s'
	cursor.execute(query, (status, airlineName, flightNum))
	conn.commit()
	cursor.close()
	return render_template('staffHome.html', username=username, message="Flight status changed successfully")
# Add airplane
@app.route('/staffAddAirplane', methods=['GET', 'POST'])
def staffAddAirplane():
	username = session['username']
	airlineName = session['airlineName']
	planeID = request.form['planeID']
	numSeats = request.form['numSeats']
	manufacturer = request.form['manufacturer']
	modelNum = request.form['modelNum']
	manufactureDate = request.form['manufactureDate']
	age = request.form['age']
	cursor = conn.cursor()
	ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (planeID, airlineName, numSeats, manufacturer, modelNum, manufactureDate, age))
	conn.commit()
	cursor.close()
	return render_template('staffHome.html', username=username, message="Airplane added successfully")
# Add airport
@app.route('/staffAddAirport', methods=['GET', 'POST'])
def staffAddAirport():
	username = session['username']
	airlineName = session['airlineName']
	airportCode = request.form['airportCode']
	airportName = request.form['airportName']
	airportCity = request.form['airportCity']
	airportState = request.form['airportState']
	numTerminals = request.form['numTerminals']
	type = request.form['type']
	try:
		cursor = conn.cursor()
		ins = 'INSERT INTO airport VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (airportCode, airportName, airportCity, airportState, numTerminals, type))
		conn.commit()
		cursor.close()
		return render_template('staffHome.html', username=username, message="Airport added successfully")
	except:
		return render_template('staffHome.html', username=username, message="Please make sure that the fields are correct")
# Show all ratings
@app.route('/staffShowRatings', methods=['GET', 'POST'])
def staffShowRatings():
	username = session['username']
	airlineName = session['airlineName']
	cursor = conn.cursor();
	query = 'SELECT * FROM rating as r, flight as f WHERE r.FlightNum = f.flightNum AND AirlineName = %s'
	cursor.execute(query, (airlineName))
	data = cursor.fetchall()
	cursor.close()
	return render_template('staffHome.html', username=username, ratings=data)
# Schedule maintenance
@app.route('/staffScheduleMaintenance', methods=['GET', 'POST'])
def staffScheduleMaintenance():
	username = session['username']
	maintenanceID = request.form['maintenanceID']
	planeID = request.form['planeID']
	startTime = request.form['start']
	endTime = request.form['end']
	try:
		cursor = conn.cursor()
		ins = 'INSERT INTO maintenance VALUES(%s, %s, %s, %s)'
		cursor.execute(ins, (planeID, maintenanceID, startTime, endTime))
		conn.commit()
		cursor.close()
		return render_template('staffHome.html', username=username, message="Maintenance scheduled successfully")
	except:
		return render_template('staffHome.html', username=username, message="Please make sure that the fields are correct")
# Show the most frequent customer (most tickets bought)
@app.route('/staffShowFrequent', methods=['GET', 'POST'])
def staffShowFrequentCustomer():
	username = session['username']
	airlineName = session['airlineName']
	cursor = conn.cursor();
	# query that selects the customer with the most tickets bought
	query = 'SELECT * FROM customer as c, ticket as t, purchase as p, flight as f WHERE c.email = p.email AND p.TicketID = t.ticketID AND t.FlightNum = f.FlightNum AND f.AirlineName = %s GROUP BY c.email ORDER BY COUNT(*) DESC LIMIT 1'
	cursor.execute(query, (airlineName))
	data = cursor.fetchall()
	cursor.close()
	return render_template('staffHome.html', username=username, customer=data)
# Show earned revenue, this is done by calculating sum of calculated price of tickets where ticket.ticketid = purchase.ticketid and ticket.flightnum = flight.flightnum and flight.airlinename = airlineName
@app.route('/staffShowRevenue', methods=['GET', 'POST'])
def staffShowRevenue():
	username = session['username']
	airlineName = session['airlineName']
	try:
		cursor = conn.cursor();
		query = 'SELECT SUM(calculatedPrice) FROM ticket as t, purchase as p, flight as f WHERE t.ticketID = p.TicketID AND t.FlightNum = f.FlightNum AND f.AirlineName = %s'
		cursor.execute(query, (airlineName))
		data = cursor.fetchall()
		cursor.close()
		return render_template('staffHome.html', username=username, revenue=data)
	except: 
		return render_template('staffHome.html', username=username, message="No revenue to show/Other error?")

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/showFlights', methods=['GET', 'POST'])
def showFlights():
	cursor = conn.cursor();
	query = 'SELECT * FROM `flight`'
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	return render_template('index.html', data=data)

@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor();
    # query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    # cursor.execute(query, (username))
    # data1 = cursor.fetchall() 
    # for each in data1:
    #     print(each['blog_post'])
    # cursor.close()
    return render_template('home.html', username=username)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
@app.route('/userLogout')
def userLogout():
	session.pop('email')
	session.pop('firstName')
	return redirect('/')
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
