#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib

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
#Authenticate register for staff
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
		# session['airlineName'] = data['airline_name']
		return redirect(url_for('staffHome'))
	else:
		error = "Invalid login or username"
		return render_template('staffLogin.html', error=error)
@app.route('/staffHome')
def staffHome():
	username = session['username']
	# airlineName = session['airlineName']
	# cursor = conn.cursor();
	# query = 'SELECT * FROM flight WHERE airline_name = %s'
	# cursor.execute(query, (airlineName))
	# data = cursor.fetchall()
	# cursor.close()
	return render_template('staffHome.html', username=username)

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
