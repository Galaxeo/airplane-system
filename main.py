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

def checkStaff():
	if 'userType' in session:
		if session['userType'] == 'staff':
			return True
	return False

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
		session['firstName'] = data['FirstName']
		session['userType'] = 'user'
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
	# query where we select all flights that the user has purchased and that have not happened yet
	query = 'SELECT * FROM flight as f, ticket as t, purchase as p WHERE p.email = %s AND p.TicketID = t.TicketID AND t.FlightNum = f.FlightNum AND f.departureTime > NOW()'
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
	cursor = conn.cursor()

	# Build the base query
	query = 'SELECT * FROM flight WHERE departureTime > NOW()'
	params = []
	if departureAirport:
		query += ' AND departureAirport = %s'
		params.append(departureAirport)
	if arrivalAirport:
		query += ' AND arrivalAirport = %s'
		params.append(arrivalAirport)
	if departureTime:
		query += ' AND DATE(departureTime) = %s'
		params.append(departureTime)
	if arrivalTime:
		query += ' AND DATE(arrivalTime) = %s'
		params.append(arrivalTime)
	cursor.execute(query, params)

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
# Return total spending by calculating sum of calculated price of tickets where ticket.ticketid = purchase.ticketid and purchase.email = email
@app.route('/userTotalSpending', methods=['GET', 'POST'])
def userTotalSpending():
	email = session['email']
	firstName = session['firstName']
	dateFrom = request.form['dateFrom']
	dateTo = request.form['dateTo']
	# If dateFrom and dateTo are empty, default to querying sum of all tickest that the user has purchased in the last 6 months
	if dateFrom == '' and dateTo == '':
		query = 'SELECT SUM(calculatedPrice) FROM ticket as t, purchase as p WHERE t.ticketID = p.TicketID AND p.email = %s AND p.purchaseTime BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND NOW()'
		cursor = conn.cursor();
		cursor.execute(query, (email))
		data = cursor.fetchall()
		return render_template('userHome.html', email=email, firstName=firstName, spending=data)
	# Query calculating sum of price of all tickets that the user has purchased between the given dates
	else: 
		query = 'SELECT SUM(calculatedPrice) FROM ticket as t, purchase as p WHERE t.ticketID = p.TicketID AND p.email = %s AND p.purchaseTime BETWEEN %s AND %s'
	cursor = conn.cursor();
	cursor.execute(query, (email, dateFrom, dateTo))
	data = cursor.fetchall()
	if (data):
		cursor.close()
		return render_template('userHome.html', email=email, firstName=firstName, spending=data, dateFrom=dateFrom, dateTo=dateTo)
	else:
		cursor.close()
		return render_template('userHome.html', email=email, firstName=firstName, message="No spending to show")

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
			return render_template('index.html', message="Staff member added successfully")
		except:
			error = "Please make sure that the fields are correct"
			return render_template('staffRegister.html', error = error)
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
		session['userType'] = 'staff'
		return redirect(url_for('staffHome'))
	else:
		error = "Invalid login or username"
		return render_template('staffLogin.html', error=error)

@app.route('/staffHome')
def staffHome():
	if not checkStaff():
		return redirect('badLogin.html')
	username = session['username']
	return render_template('staffHome.html', username=username)
@app.route('/staffShowFlights', methods=['GET', 'POST'])
# Show flights
def staffShowFlights():
	if not checkStaff():
		return redirect('badLogin.html')
	username = session['username']
	airlineName = session['airlineName']
	startDate = request.form['startDate']
	endDate = request.form['endDate']
	departureAirport = request.form['departureAirport']
	arrivalAirport = request.form['arrivalAirport']
	cursor = conn.cursor()

	# Build the base query
	query = 'SELECT * FROM flight WHERE AirlineName = %s'

	# Create a list to store the query parameters
	params = [airlineName]

	# Check if startDate and endDate are provided
	if startDate and endDate:
		query += ' AND DepartureTime BETWEEN %s AND %s'
		params.extend([startDate, endDate])

	# Check if departureAirport is provided
	if departureAirport:
		query += ' AND DepartureAirport = %s'
		params.append(departureAirport)

	# Check if arrivalAirport is provided
	if arrivalAirport:
		query += ' AND ArrivalAirport = %s'
		params.append(arrivalAirport)

	# If none of these fields are provided, show flights for the next 30 days
	query += ' AND DepartureTime BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)'
	# Add the ORDER BY clause
	query += ' ORDER BY DepartureTime'


	# Execute the query with the parameters
	cursor.execute(query, params)

	data = cursor.fetchall()
	cursor.close()
	return render_template('staffHome.html', username=username, data=data)
@app.route('/staffAddFlight', methods=['GET', 'POST'])
# Add flight
def staffAddFlight():
	if not checkStaff():
		return redirect('badLogin.html')
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
# View customers of a flight
@app.route('/staffViewCustomers', methods=['GET', 'POST'])
def staffViewCustomers():
	if not checkStaff():
		return redirect('badLogin.html')
	username = session['username']
	airlineName = session['airlineName']
	flightNum = request.form['flightNum']
	flights = request.form['flights']
	cursor = conn.cursor();
	# query that selects all customers that have purchased tickets for the given flight
	query = 'SELECT * FROM customer as c, ticket as t, purchase as p WHERE t.FlightNum = %s AND t.TicketID = p.TicketID AND p.email = c.email'
	cursor.execute(query, (flightNum))
	data = cursor.fetchall()
	cursor.close()
	return render_template('staffHome.html', username=username, customers=data, flightNum=flightNum)
# Change status of flight
@app.route('/staffChangeStatus', methods=['GET', 'POST'])
def staffChangeStatus():
	if not checkStaff():
		return redirect('badLogin.html')
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
	if not checkStaff():
		return redirect('badLogin.html')
	username = session['username']
	airlineName = session['airlineName']
	planeID = request.form['planeID']
	numSeats = request.form['numSeats']
	manufacturer = request.form['manufacturer']
	modelNum = request.form['modelNum']
	manufactureDate = request.form['manufactureDate']
	age = datetime.now().year - datetime.strptime(manufactureDate, '%Y-%m-%d').year
	cursor = conn.cursor()
	ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (planeID, airlineName, numSeats, manufacturer, modelNum, manufactureDate, age))
	conn.commit()
	cursor.close()
	return render_template('staffHome.html', username=username, message="Airplane added successfully")
# Add airport
@app.route('/staffAddAirport', methods=['GET', 'POST'])
def staffAddAirport():
	if not checkStaff():
		return redirect('badLogin.html')
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
	if not checkStaff():
		return redirect('badLogin.html')
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
	if not checkStaff():
		return redirect('badLogin.html')
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
	if not checkStaff():
		return redirect('badLogin.html')
	username = session['username']
	airlineName = session['airlineName']
	cursor = conn.cursor();
	# query that selects the customer with the most tickets bought
	query = 'SELECT * FROM customer as c, ticket as t, purchase as p, flight as f WHERE c.email = p.email AND p.TicketID = t.ticketID AND t.FlightNum = f.FlightNum AND f.AirlineName = %s GROUP BY c.email ORDER BY COUNT(*) DESC LIMIT 1'
	cursor.execute(query, (airlineName))
	customerData = cursor.fetchall()
	# query to select all flights that customer has taken
	query = 'SELECT * FROM flight as f, ticket as t, purchase as p WHERE p.email = %s AND p.TicketID = t.TicketID AND t.FlightNum = f.FlightNum'
	cursor.execute(query, (customerData[0]['Email']))
	flightData = cursor.fetchall()
	cursor.close()
	return render_template('staffHome.html', username=username, customer=customerData, customerFlights=flightData)
# Show earned revenue, this is done by calculating sum of calculated price of tickets where ticket.ticketid = purchase.ticketid and ticket.flightnum = flight.flightnum and flight.airlinename = airlineName
# TODO: Add date range and default last 30 days
@app.route('/staffShowRevenue', methods=['GET', 'POST'])
def staffShowRevenue():
	if not checkStaff():
		return redirect('badLogin.html')
	username = session['username']
	airlineName = session['airlineName']
	try:
		cursor = conn.cursor();
		# query sum of calculated price of all tickets that the airline has sold within the last 30 days by default
		query = 'SELECT SUM(calculatedPrice) FROM ticket as t, purchase as p, flight as f WHERE t.ticketID = p.TicketID AND t.FlightNum = f.FlightNum AND f.AirlineName = %s AND p.purchaseTime BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()'
		# second query sum of calculated price of all tickets that the airline has sold within last year
		query2 = 'SELECT SUM(calculatedPrice) FROM ticket as t, purchase as p, flight as f WHERE t.ticketID = p.TicketID AND t.FlightNum = f.FlightNum AND f.AirlineName = %s AND p.purchaseTime BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()'
		cursor.execute(query, (airlineName))
		data = cursor.fetchall()
		cursor.execute(query2, (airlineName))
		data2 = cursor.fetchall()
		cursor.close()
		return render_template('staffHome.html', username=username, monthly=data, yearly=data2)
	except: 
		return render_template('staffHome.html', username=username, message="No revenue to show/Other error?")

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
	session.pop('userType')
	session.pop('airlineName')
	return redirect('/')
		
@app.route('/userLogout')
def userLogout():
	session.pop('email')
	session.pop('firstName')
	session.pop('userType')
	return redirect('/')
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
