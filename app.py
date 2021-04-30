from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://hbmzaywehilgod:89890fbc289955b938bc289b2ea032b71b719e1d9f193da07f09926826794522@ec2-52-87-107-83.compute-1.amazonaws.com:5432/d32nn0e668sf2f?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=['POST'])
def success():
    if request.method == 'POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        
        if db.session.query(Data).filter(Data.email_==email).count()==0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email,height,average_height,count)
            return render_template("success.html")
    return render_template('index.html',text="Seems like we've got something from that email address already!")

if __name__=='__main__':
    app.debug=True
    app.run()