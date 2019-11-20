from flask import Flask, request, render_template, session
from flask_mysqldb import MySQL

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
	result1 = cur1.execute("SELECT ID, JobID, Name, Address, Sex, PhoneNo FROM EmployeeInfo WHERE ID = {};". format(id))
	empRecord = cur1.fetchall()
	result2 = cur2.execute("SELECT * FROM EmployeeRecords WHERE EmployeeID = {};". format(id))
	if result2 > 0:
			empAttendance = cur2.fetchall()
			return render_template('executive.html', empRecord = empRecord, empAttendance=empAttendance)
	else:
		return render_template('executive.html', empRecord=empRecord , att_msg="No Attendance Results Found")


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
		"""if log_type == "":
			cur.execute("INSERT INTO EmployeeRecords (id, data) VALUES (%s, %s);", (maxid[0] + 1, insert))			
		cur.execute("INSERT INTO example (id, data) VALUES (%s, %s);", (maxid[0] + 1, insert))
		mysql.connection.commit()"""
		return render_template('manual_log.html', msg="valid",)# log_type=log_type)
	else:
		return render_template('manual_log.html', msg="invalid")



if __name__ == "__main__":
	app.run(debug=True)
