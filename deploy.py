from flask import Flask, request, render_template, session
from flask_mysqldb import MySQL
from datetime import datetime
import pytz

app = Flask(__name__)

app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = "SWy5rY8sM1"
app.config['MYSQL_PASSWORD'] = "f5gU8huxAs"
app.config['MYSQL_DB'] = "SWy5rY8sM1"

mysql = MySQL(app)

app.secret_key = "p2n3ryen2yyp932y32#@kkj3209"

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login', methods=["GET","POST"])
def login():
	if request.method == "POST":
		uname = request.form['uname']
		passw = request.form['passw']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM EmployeeInfo WHERE ID = {} AND Password = '{}'; ". format(uname, passw))
		if result > 0:
			session['name'] = uname
			return render_template('index.html')
		else:
			return render_template('login.html', msg="invalid")
	else:
		return render_template('login.html')


@app.route('/logout')
def logout():
	session.clear()
	return render_template('index.html')



@app.route('/employees')
def employees():
	cur1 = mysql.connection.cursor()
	cur2 = mysql.connection.cursor()
	resultValue1 = cur1.execute("SELECT * FROM EmployeeInfo")
	resultValue2 = cur2.execute("SELECT * FROM EmployeeRecords")
	if resultValue1 > 0 and resultValue2 > 0:
		empInfo = cur1.fetchall()
		empRecords = cur2.fetchall()
		return render_template('employees.html', empInfo=empInfo, empRecords=empRecords)
	else:
		return "<h1>Failure in retrieving data</h1>"

@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/register_emp', methods=['POST'])
def register_emp():
	email=request.form['u_email']
	password=request.form['passw']
	jobID=request.form['jobID']
	name=request.form['uname']
	address=request.form['address']
	sex=request.form['sex_type']
	phone=request.form['phone']

	cur = mysql.connection.cursor()

	try:
		cur.execute("SELECT ID FROM EmployeeInfo  ORDER BY ID DESC;")
		empRecords = cur.fetchall()
		emp_Latest = int(empRecords[0][0])
		emp_Latest = emp_Latest + 1	
		cur.execute("INSERT INTO EmployeeInfo VALUES (%s, %s, %s, %s, %s, %s, %s);", (emp_Latest, jobID, name, address, sex, phone, password))
		mysql.connection.commit()
		cur.close()
		return render_template('register.html', type="success", msg="Employee successfully registered")
	except:
		mysql.connection.rollback()
		return render_template('register.html', type="notice", msg="Error in registering data")
	


@app.route('/employee_search', methods=['POST'])
def employee_search():
	empID = request.form['empId']
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM EmployeeRecords WHERE EmployeeID = {};". format(empID))
	if result > 0:
		empRecord = cur.fetchall()
		return render_template('employee.html', empRecord=empRecord)
	else:
		return "<h1>Failure in retrieving data</h1>"


@app.route('/executive')
def executive():
	cur = mysql.connection.cursor()
	resultValue = cur.execute("SELECT * FROM EmployeeInfo")
	if resultValue > 0:
		empRecords = cur.fetchall()
		return render_template('executive.html', empRecords=empRecords)
	else:
		return render_template('executive.html')



@app.route('/employee_search_exec', methods=['POST'])
def employee_search_exec():
	search_type = request.form['search_type']
	empDetails = request.form['empDetails']
	cur = mysql.connection.cursor()
	if search_type == "empId":
		empDetails = int(empDetails)
		result = cur.execute("SELECT ID, JobID, Name, Address, Sex, PhoneNo FROM EmployeeInfo WHERE ID = {};". format(empDetails))
		if result > 0:
			empRecord = cur.fetchall()
			return render_template('executive.html', empRecord=empRecord)
	if search_type == "empName":
		result = cur.execute("SELECT ID, JobID, Name, Address, Sex, PhoneNo FROM EmployeeInfo WHERE Name = '{}';". format(empDetails))
		if result > 0:
			empRecord = cur.fetchall()
			return render_template('executive.html', empRecord=empRecord)
	return render_template('executive.html', emp_msg="No Results Found")


@app.route('/employee_attendance_info/<int:id>')
def employee_attendance_info(id):
	cur1 = mysql.connection.cursor()
	cur2 = mysql.connection.cursor()
	cur1.execute("SELECT ID, JobID, Name, Address, Sex, PhoneNo FROM EmployeeInfo WHERE ID = {};". format(id))
	empInfo = cur1.fetchall()
	result2 = cur2.execute("SELECT * FROM EmployeeRecords WHERE EmployeeID = {};". format(id))
	if result2 > 0:
			empAttendance = cur2.fetchall()
			return render_template('executive.html', empInfo = empInfo, empAttendance=empAttendance)
	else:
		return render_template('executive.html', empInfo = empInfo, att_msg="No Attendance Results Found")


@app.route('/manual_log')
def manual_log():
	return render_template('manual_log.html')


@app.route('/input_log', methods=['POST'])
def input_log():
	empID = request.form['empId']
	log_type = request.form['log_type']
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM EmployeeInfo WHERE ID = {};". format(empID))
	if result > 0:
		if log_type == "in":
			result = cur.execute("SELECT EmployeeID FROM EmployeeStatus WHERE EmployeeID = {};". format(empID))
			if result > 0:
				return render_template('manual_log.html', type="notice", msg="You have already clocked-in")
			else:
				try:
					dt_utcnow = datetime.now(tz=pytz.UTC)
					timestamp = dt_utcnow.astimezone(pytz.timezone('Canada/Atlantic')).strftime('%Y-%m-%d %H:%M:%S')
					cur.execute("INSERT INTO EmployeeStatus (EmployeeID, TimeIn) VALUES (%s, %s);", (empID, timestamp))
					mysql.connection.commit()
					cur.close()
					return render_template('manual_log.html', type="success", msg="Successfully submitted")
				except:
					mysql.connection.rollback()
					return render_template('manual_log.html', type="notice", msg="Error in inserting data")
		if log_type == "out":
			if cur.execute("SELECT EmployeeID FROM EmployeeStatus WHERE EmployeeID = {};". format(empID)) > 0:
				empRecord = cur.fetchone()
				empID = empRecord[0]
				try:
					dt_utcnow = datetime.now(tz=pytz.UTC)
					timestamp = dt_utcnow.astimezone(pytz.timezone('Canada/Atlantic')).strftime('%Y-%m-%d %H:%M:%S')
					cur.execute("UPDATE EmployeeStatus SET timeOut = %s WHERE EmployeeID = %s;", (timestamp, empID))
					mysql.connection.commit()
					cur.close()
					return render_template('manual_log.html', type="success", msg="Successfully submitted")
				except:
					mysql.connection.rollback()
					return render_template('manual_log.html', type="notice", msg="Error in updating data")
			else:
				return render_template('manual_log.html', type="notice", msg="You have not clocked-in for the day")
	else:
		return render_template('manual_log.html', type="notice", msg="Invalid Employee Credentials!")



if __name__ == "__main__":
	app.run(debug=True)
