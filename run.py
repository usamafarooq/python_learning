from flask import Flask, session, render_template,request,redirect,url_for,jsonify
from flask.ext.session import Session
import pymysql
import json
import collections

conn=pymysql.connect(host="localhost",user="root",password="",db="python_crud")##Connection to MYSQL DB
c=conn.cursor()###Database cursor

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()

@app.route('/')##Main Route

def main():
	"""Loads the index.html which contains all the links"""
	if 'id' in session:
		query="SELECT * from task WHERE user_id=%s"
		param=session['id']
		c.execute(query,param)
		data=c.fetchall()
		return render_template('index.html', data = data)
	else:
		return redirect('/login')

@app.route('/logout')

def logout():
	session.clear()
	return redirect('/login')

@app.route('/register')###INSERT Form Route

def register():
	if 'id' not in session:
		session['message'] = ""
		return render_template('register.html')
	else:
		return redirect('/')

@app.route('/signup',methods=['POST','GET'])###Values insert function

def signup():
	"""This function will Gets the values from the FORM and Stored in the DataBase table"""
	if request.method=='POST':
		form = request.form
		username=request.form['username']
		email=request.form['email']
		password=request.form['password']
		query="SELECT * from users WHERE username=%s"
		param=username
		c.execute(query,param)
		if c.fetchone() is not None:
			session['message'] = "That username is already taken..."
			return render_template('register.html',form=form)
		else:
			query="SELECT * from users WHERE email=%s"
			param=email
			c.execute(query,param)
			if c.fetchone() is not None:
				session['message'] = "That Email is already taken..."
				return render_template('register.html',form=form)
			else:
				c.execute("""INSERT into users(username,email,password) VALUES (%s,%s,%s)""",(username,email,password))
				conn.commit()
				return redirect('/login')

@app.route('/login')###INSERT Form Route

def login():
	if 'id' not in session:
		session['message'] = ""
		return render_template('login.html')
	else:
		return redirect('/')

@app.route('/check_login',methods=['POST','GET'])

def check_login():
	if request.method=='POST':
		form = request.form
		email=request.form['email']
		password=request.form['password']
		sql = "select * from users where email = %s and password = %s"  
		c.execute(sql, (email, password))
		data = c.fetchone()
		if data is not None:
			session['id'] = data[0]
			return redirect('/')
		else:
			session['message'] = "Email and Password do not match"
			return render_template('login.html',form=form)

@app.route('/insert')###INSERT Form Route

def insert():
	if 'id' not in session:
		return redirect('/login')
	"""This Function will call the Insert Form which contains TextFields"""
	return render_template('insert.html')

@app.route('/create',methods=['POST','GET'])###Values insert function

def create():
	if 'id' not in session:
		return redirect('/login')
	"""This function will Gets the values from the FORM and Stored in the DataBase table"""
	if request.method=='POST':
		name1=request.form['name']##Getting values from the FORM
		c.execute("""INSERT into task(name,date,type,user_id) VALUES (%s,%s,%s,%s)""",(name1,request.form['date'],request.form['type'],session['id']))
		conn.commit()
		return redirect('/')

@app.route('/edit/<id>',methods=['POST','GET'])###Values insert function

def edit(id):
	if 'id' not in session:
		return redirect('/login')
	update_data=id
	query="SELECT * from task WHERE id=%s and user_id = %s"
	param=update_data
	c.execute(query,(param, session['id']))
	data1=c.fetchall()	
	return render_template('edit.html',data1=data1)

@app.route('/update_del', methods=['POST','GET'])###update values based on ID

def update_del():
	if 'id' not in session:
		return redirect('/login')
	"""It will update the values Based on the id given by the user"""
	if request.method=='POST':
		id=request.form['id']
		name=request.form['name']
		date=request.form['date']
		type=request.form['type']
		query="UPDATE task set name=%s,date=%s,type=%s where id=%s"
		par=(name,date,type,id)
		c.execute(query,par)
		return redirect('/')

@app.route('/delete/<id>',methods=['POST','GET'])##Delete Values based on ID
def delete(id):
	if 'id' not in session:
		return redirect('/login')
	delete1=id
	qry="DELETE from task where id=%s and user_id = %s"
	c.execute(qry, (delete1, session['id']))
	return redirect('/')

app.run()