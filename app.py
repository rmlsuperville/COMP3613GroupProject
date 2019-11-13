from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = "SWy5rY8sM1"
app.config['MYSQL_PASSWORD'] = "f5gU8huxAs"
app.config['MYSQL_DB'] = "SWy5rY8sM1"

mysql = MySQL(app)


@app.route('/')
def index():
	cur1 = mysql.connection.cursor()
	cur2 = mysql.connection.cursor()

	resultValue1 = cur1.execute("SELECT * FROM EmployeeInfo")
	resultValue2 = cur2.execute("SELECT * FROM EmployeeRecords")
	if resultValue1 > 0 and resultValue2 > 0:
	
		empInfo = cur1.fetchall()
		empRecords = cur2.fetchall()

		return render_template('index.html', empInfo=empInfo, empRecords=empRecords)
	else:
		return "<h1>Failure</h1>"
	

if __name__ == "__main__":
    app.run(debug=True)
