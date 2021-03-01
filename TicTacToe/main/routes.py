from flask import Blueprint,render_template,request,current_app
from random import random
main=Blueprint("main",__name__)

@main.route("/")
@main.route("/home")
def home():
    verified=True if request.cookies.get("user",False) else False
    return render_template("index.html" ,random=random(),verified=verified)

@main.route("/newuser",methods=["POST","GET"])
def newUser():
    if request.method=="GET":
        resp=current_app.response_class(status=200)  
        resp.set_cookie("user","true");
        return resp
