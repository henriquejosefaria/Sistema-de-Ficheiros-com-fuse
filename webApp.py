from flask import Flask, render_template, url_for, flash, redirect, json, request
import time
from flask_pymongo import PyMongo
import random, os, time

# bibliotecas usadas para enviar o email com o código secreto
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


app= Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["MONGO_URI"] = "mongodb://localhost:27017/fuse"
mongo = PyMongo(app)
user_id = -1


@app.route("/")
def Server():
	return render_template("directoryHome.html", title="personalHome")

@app.route("/acess", methods=['GET','POST'])
def acess():
	global user_id
	if request.method == 'POST': 		
		username = request.form['email']
		# verifca se email é válido e user tem permissão para entrar
		if mongo.db.users.find({"username": username}).count() > 0:
			# encontra dados do utilizador
			file = mongo.db.users.find_one({"username":username})
			email = file["email"]
			user_id = file["userId"]
			# prepara e envia email com código secreto
			msg = MIMEMultipart()
			code = str(random.randint(100000,1000000))
			message = "Thank you  for using our services !!\n\n Requested code: "+ code
			password = "workaholics2020"
			msg['From'] = "workaholicsTS2020@gmail.com"
			msg['To'] = email
			msg['Subject'] = "Requested code"
			# add in the message body
			msg.attach(MIMEText(message, 'plain'))
			#create server
			server = smtplib.SMTP('smtp.gmail.com: 587')
			server.starttls()
			# Login Credentials for sending the mail
			server.login(msg['From'], password)
			# send the message via the server.
			server.sendmail(msg['From'], msg['To'], msg.as_string())
			server.quit()
			mongo.db.validCodes.insert({"userId": user_id , "code": code})
			return render_template("verify.html", title="verify",time = time.time())
		else:
			flash("Email inserido está errado!!", "fail")
			return render_template("directoryHome.html", title="personalHome")


@app.route("/verify/<timestr>", methods=['GET','POST'])
def verify(timestr):
	global user_id
	if request.method == 'POST': 		
		text = request.form['verify']
		print("dif => ",(time.time() - float(timestr)))
		# User Válido se inserir password dentro de 1 minuto
		if mongo.db.validCodes.find({"userId": user_id, "code": text}).count() > 0 and (time.time() - float(timestr)) <= 60:
			flash("You have Autenticated successfully!!","success")
			mongo.db.validCodes.remove({"userId":user_id, "code": text})
			mongo.db.log.insert({"userId": user_id, "time": time.time(), "acess": "valid"})
			return render_template("verify.html", title="verify",time = "-1")
		elif (time.time() - float(timestr)) > 60:
			#Qualquer valor que dê deve ser removido
			mongo.db.validCodes.remove({"userId": user_id})
			flash("You took to long to inser the code. BE FASTER NEXT TIME!!","fail")
			return render_template("directoryHome.html", title="personalHome")
		else:
			flash("You inserted a wrong code. Try again fast!!","fail")
			return render_template("verify.html", title="verify",time = timestr)

if __name__ == "__main__":
	app.run(debug=True)
