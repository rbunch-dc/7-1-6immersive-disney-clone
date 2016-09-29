from flask import Flask, render_template, request, redirect, session  #include Flask class, render_template, and request from teh flask module
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'disney'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

#Make one connection and use it over, and over, and over...
conn = mysql.connect()
# set up a cursor object whihc is what the sql object uses to connect and run queries
cursor = conn.cursor()

# Sessions require a secret_key to try and protect the var
app.secret_key = 'HSDG#$%T34t35t3tREGgfsDG34t34543t3455fdsfgdfsgd'

@app.route("/")
def index():
	# execute our query
	cursor.execute('''SELECT content FROM page_content WHERE page='home' AND location='header' AND status=1''')
	header_text = cursor.fetchall()
	# a_list = j(header_text)
	# cursor.exectue('SELECT...')
	# cursor.execute('''SELECT content FROM page_content WHERE page='home' AND location='header' AND status=1''')
	# left_stuff = cursor.fetchall()
	# Write a queryt that will pull the three main fields for all rows that have page as home, and left_block as location. Alsp, make sure they are publisehd (status = 1)
	left_block_query = "SELECT header_text,content,image_link FROM page_content WHERE page = 'home' AND location = 'left_block' AND status = 1 ORDER BY priority asc"
	# Run the query
	cursor.execute(left_block_query)
	# Turn the query into something Python can use via fetchall
	data = cursor.fetchall()
	# print header_text
	return render_template('index.html',
		header=header_text,
		# Add a new variable "left_data" to be used in the template
		left_data = data
	)

# Make a new route called admin
@app.route('/admin')
# Define the method for the new route admin
def admin():
	# return request.args.get('message')
	# get the variable "message" out of the qery if it exists...
	if request.args.get('message'):
		# return teh template with the var
		return render_template('admin.html',
			message = "Login Failed"
		)
		# otherwise, just return the tempalte
	else:
		return render_template('admin.html')

@app.route('/logout')
def logout():
	# Nuke their session vars. This will end the session which is waht we use to let them into the portal
	session.clear()	
	return redirect('/admin?message=LoggedOut')

# Make a new route called admin_submit. Add method POST so that the form can get here.
@app.route('/admin_submit', methods=['GET', 'POST'])
# Define the method for the new route admin_submit
def admin_submit():
	# print request.form
	# return request.form['username'] + ' ---- ' + request.form['password']
	if request.form['username'] == 'admin' and request.form['password'] == 'admin':
		# You may proceed
		# But before oyu do... let me give you a ticket!
		session['username'] = request.form['username']
		return redirect('/admin_portal')
	else:
		return redirect('/admin?message=login_failed')

@app.route('/admin_portal')
def admin_portal():
	# Session variable "username" exits... proceed.
	# Make sure to check if it's in teh dictaionry rather than just "if"
	if 'username' in session:
		home_page_query = "SELECT header_text,content,image_link,location,id FROM page_content WHERE page = 'home' AND status = 1"
		# Run the query
		cursor.execute(home_page_query)
		# Turn the query into something Python can use via fetchall
		data = cursor.fetchall()		
		return render_template('admin_portal.html',
			# Data is what it is here, home_page_content is what it is to the template
			home_page_content = data
		)
	# You have no ticket. No soup for you
	else:
		return redirect('/admin?message=YouMustLogIn')

@app.route('/admin_update', methods=['POST'])
def admin_update():
	# FIRST... do you belong here?
	if 'username' in session:
		# OK, they are logged in. I will insert your stuff...
		body = request.form['body_text']
		header = request.form['header']
		image = request.form['image']

		# set up a cursor object whihc is what the sql object uses to connect and run queries
		# cursor = mysql.connect().cursor()

		# execute our query
		query = "INSERT INTO page_content VALUES (DEFAULT, 'home', '"+body+"', 1,1,'left_block', NULL, '"+header+"', '"+image+"')"
		# print query
		cursor.execute(query)
		conn.commit()
		return redirect('/admin_portal?success=Added')
	# You have no ticket. No soup for you
	else:
		return redirect('/admin?message=YouMustLogIn')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
	if request.method == 'GET':
		# Write a query that gets the row with the matching id
		query = "SELECT header_text,content,image_link,id,status,priority FROM page_content WHERE id = %s" % id
		print query	
		cursor.execute(query)
		data = cursor.fetchone()
		return render_template('edit.html',
			data = data
		)
	else:
		# Do the post stuff

if __name__ == "__main__":
	app.run(debug=True)