from flask import Flask, render_template
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'disney'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

@app.route("/")
def index():
	# set up a cursor object whihc is what the sql object uses to connect and run queries
	cursor = mysql.connect().cursor()
	# execute our query
	cursor.execute("SELECT content FROM page_content WHERE page='home' AND location='header' AND status=1")
	header_text = cursor.fetchall()
	print header_text
	return render_template('index.html',header=header_text)

if __name__ == "__main__":
	app.run(debug=True)