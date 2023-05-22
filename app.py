from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pda_db'

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/home")
def home_page():
    return render_template('home.html')

#----------------------------
    
# sendgrid integration
def mailtest_registration(to_email):
	message = Mail(
	from_email='mrrookie1221@gmail.com',
	to_emails= to_email,
    subject=' Registration Successfull ! ',
    html_content='<strong> You have successfully registered as user. Please Login using your Username and Password to donate/request for Plasma. </strong>')
	try:
		sg = SendGridAPIClient('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')
		response = sg.send(message)
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
		print(e)

#for donor
def mailtest_donor(to_email):		
    message = Mail(
    from_email='mrrookie1221@gmail.com', 
    to_emails= to_email,
    subject=' Thankyou for Registering as Donor ! ',
    html_content='<strong> Every donor is an asset to the nation who saves peoples lives, and you are one of them.We appreciate your efforts. Thank you !! </strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

#for request

def mailtest_request(to_email):
    message = Mail(
    from_email='mrrookie1221@gmail.com',
    to_emails= to_email,
    subject=' Request Submitted ! ',
    html_content='<strong> Your request has been successfully submitted. Please be patient, your requested donor will get back to you soon. </strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

#for request sending to donor

def mailtest_requesttodonor(to_email, hospitalname, recname, recmobile, recmail, recage, recarea, reccity, recdistrict): 
    message = Mail(
    from_email='mrrookie1221@gmail.com',
    to_emails= to_email,
    subject=' Requesting Plasma ',
    html_content='<strong> Your registration has been requested by a recipient. Name : {} , Age : {} , Mobile No : {} , Email : {} , Hospital Name : {} , Address : {} .</strong>'.format(recname,recage,recmobile,recmail,hospitalname,recarea + " , "+ reccity + " , "+recdistrict))
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
#----------------------------

    
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' :
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM loginregister WHERE username = % s AND password = % s', (username, password))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['username']
			session['username'] = account['username']
			msg = 'Logged in successfully !'  
			return render_template('user_profile.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

# After login
@app.route('/afterlogin')
def afterlogin():
    return render_template("user_profile.html")

@app.route('/signin', methods =['GET', 'POST'])
def signin():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'usermail' in request.form and 'usercontact' in request.form and 'password' in request.form :
		username = request.form['username']
		usermail = request.form['usermail']
		usercontact = request.form['usercontact']
		password = request.form['password']
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM loginregister WHERE usermail = % s', (usermail, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', usermail):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not usermail:
			msg = 'Please fill out the form !'
		else:
			mailtest_registration(usermail)
			cursor.execute('INSERT INTO loginregister VALUES (% s, % s, % s, % s)', (username, usermail, usercontact, password))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('signin.html', msg = msg)


@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/adddonor",methods = ['POST','GET'])
def adddonor():
	if request.method == 'POST':
		name = request.form['name']
		mobile = request.form['mobile']
		email = request.form['email']
		age = request.form['age']
		gender = request.form['gender']
		blood = request.form['blood']
		area = request.form['area']
		city = request.form['city']
		district = request.form['district']

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM donor WHERE email = % s', (email, ))
		account = cursor.fetchone()
		if account:
			cursor.execute('SELECT * FROM donor')
			data = cursor.fetchall()
			return render_template("donor.html", donor2 = data, msg="You are already a member, please login using your details")
			#return render_template('donor.html', msg="You are already a member, please login using your details")
		else:
			mailtest_donor(email)
			cursor.execute('INSERT INTO donor VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s)', (name, mobile, email, age, gender, blood, area, city, district))
			mysql.connection.commit()
		return render_template('success.html', msg="You have successfully registered !")

#-----------------------------------------------------------------------------------------

@app.route('/donorlist')
def donorlist():
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM donor')
		data = cursor.fetchall()
		return render_template("donor.html", donor2 = data)

#----------------------------------------------------------------------------

@app.route("/request_page", methods = ['GET','POST'])
def request_page():
	msg = ''
	if request.method == 'POST' :
		drmail = request.form['drmail']
		hospitalname = request.form['hospitalname']
		recname = request.form['recname']
		recmobile = request.form['recmobile']
		recmail = request.form['recmail']
		recage = request.form['recage']
		recgender = request.form['recgender']
		recbloodgroup = request.form['recbloodgroup']
		recarea = request.form['recarea']
		reccity = request.form['reccity']
		recdistrict = request.form['recdistrict']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		mailtest_requesttodonor(drmail,hospitalname, recname, recmobile, recmail, recage, recarea, reccity, recdistrict)
		mailtest_request(recmail)
		cursor.execute('INSERT INTO request VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (drmail, hospitalname, recname, recmobile, recmail, recage, recgender, recbloodgroup, recarea, reccity, recdistrict))
		mysql.connection.commit()
		msg = 'Your request has been submitted!'
		return render_template('request.html', msg = msg)
	
	elif request.method == 'POST':
			msg = 'Please fill out the form !'
	return render_template('request.html', msg = msg)
#-----------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run( debug=True, port=5000 )