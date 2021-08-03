from flask import Flask,render_template,request,redirect,url_for
from flask_httpauth import HTTPBasicAuth
import pandas as pd
import os


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
users = {
    "john": "hello",
    "susan": "bye"
}

filename = "tasks.csv"
if not os.path.isfile(filename):
	df = pd.DataFrame(columns = ['name','details', 'deadline'])
	df.to_csv(filename,index=False)


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username,password):
	if username in users:
		if  password == users[username]:
			return username

			
@app.route('/login_try',methods=["GET","POST"])
def login_try():
	form = request.form
	username = form["username"]
	password = form["password"]
	if type(verify_password(username,password)) == type(""):
		return view()
	else:
		return login()
	

	
@app.route('/login',methods=["GET","POST"])
def login():
	return render_template('/login.html')
	

@app.route('/',methods=["GET","POST"])
@auth.login_required
def home():
	return view()

	
@app.route('/view')
@auth.login_required
def view():
	df = pd.read_csv(filename)
	csv_data = list(df.values)
	return render_template('/view.html',data=csv_data)
	
	
@app.route('/add',methods=['GET','POST'])
@auth.login_required
def add():
	return render_template('/add.html')

@app.route('/add-task', methods = ['GET','POST'])
@auth.login_required
def add_into_csv():
	if request.method == "POST":
		form = request.form
		task_name = form["taskname"]
		task_details = form["taskdetails"]
		deadline = form["deadline"]
		df = pd.DataFrame([[task_name,task_details,deadline]])
		print(task_name,task_details,deadline)
		df.to_csv('tasks.csv',header=False,index=False,mode='a')
		temp = pd.read_csv(filename)
		csv_data = list(temp.values)
		print("here")
		return add_redirect()
	else:
		return "World"
	
@app.route('/view',methods=['GET','POST'])
def add_redirect():
	return redirect(url_for('view'))

	
@app.route('/update',methods=['GET','POST'])
@auth.login_required
def update():
	df = pd.read_csv(filename)
	csv_data = list(df.values)		
	return render_template('/update.html',data=csv_data,len=len(csv_data))	
	
@app.route('/update-item',methods=['GET','POST'])
@auth.login_required
def updateCsv():
	df = pd.read_csv(filename)
	csv_data = list(df.values)
	if request.method == "GET":
		id = request.args.get("item-id",default=0,type=int)
		globalId = id
		return render_template('/update-item.html',data=csv_data[id],id=id)
	elif request.method == "POST":
		task_name = request.form["taskname"]
		task_details = request.form["taskdetails"]
		deadline = request.form["deadline"]
		id = request.form["id"]
		
		csv_data.pop(int(id))
		csv_data.insert(int(id),[task_name,task_details,deadline])
		df2 = pd.DataFrame(csv_data,columns=["Name","Details","Deadline"])
		
		df2.to_csv("tasks.csv",mode='w',index=False)
		return update_redirect()

@app.route('/view', methods = ['GET','POST'])
def update_redirect():
	return redirect(url_for('view'))
		
@app.route('/delete', methods = ['GET','POST'])
@auth.login_required
def delete():
	df = pd.read_csv(filename)
	csv_data = list(df.values)
	return render_template('/delete.html',data=csv_data,len=len(csv_data))

@app.route('/delete-task', methods = ['GET','POST'])
@auth.login_required
def deleteTask():
	df = pd.read_csv(filename)
	csv_data = list(df.values)
	if request.method == "GET":
		id = request.args.get("item",default=-999,type=int)
		if id == -999:
			return render_template('/delete.html',data=csv_data,len=len(csv_data))
		else:		
			print(id)
			csv_data.pop(int(id))
			print(csv_data)
			df2 = pd.DataFrame(csv_data,columns=["Name","Details","Deadline"])
			df2.to_csv("tasks.csv",mode='w',index=False)	
			return delete_redirect()

@app.route('/view', methods = ['GET','POST'])
def delete_redirect():
	return redirect(url_for('view'))

app.run(debug = True, port=5000)