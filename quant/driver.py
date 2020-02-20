from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy (?) not sure which ones correct
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os
import quant


app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
#not sure what this doing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#this line wasnt working and i didnt know why, but rn model.py is useless
#from quant.model import Result


class StonksModel(db.Model):
    __tablename__ = 'stocks'

    #modified these to fit our schema
    #apparently db.Integer by itself creates a serial so i think were good
    uid = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.VARCHAR(length=250))
    timestamp = db.Column(db.TIMESTAMP())
    price = db.Column(db.DECIMAL())
    volume = db.Column(db.DECIMAL())

    #will run the first time we create a new result
    def __init__(self, ticker, timestamp, price, volume):
        self.ticker = ticker
        self.timestamp = timestamp
        self.price = price
        self.volume = volume

    #represents object when we query for it
    def __repr__(self):
        return '<ticker {}>'.format(self.ticker)


#@app.route('/')
#def hello():
#    return "Hello World!"
#
#
#@app.route('/<name>')
#def hello_name(name):
#    return "Hello {}!".format(name)

#this allows us to create one stonk or retrieve all stonks
#im not sure what we are trying to do specifically w this api so i left it at this for now
#USAGE- GET [host:port]/stocks
@app.route('/stocks', methods=['POST', 'GET'])
def handle_stonks():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_stonk = StonksModel(ticker=data['ticker'],
                                    timestamp=data['timestamp'],
                                    price=data['price'],
                                    volume=data['volume'])
            db.session.add(new_stonk)
            db.session.commit()
            return "Stonk {} has been birthed.".format(new_stonk.ticker)
        else:
            return "error: The request payload is not in JSON format"
    elif request.method == 'GET':
        #should return all stonks,query all is a function by sql alchemy
        stonks = StonkModel.query.all()
        res = [
        {
            "ticket": stonk.ticket,
            "timestamp": stonk.timestamp,
            "price": stonk.price,
            "volume": stonk.volume
        } for stonk in stonks]
        return "count: " + str(len(results)) + " cars: " + str(results)

#USAGE - i.e. GET [host:port]/stocks/42069
#gets/udpates/deletes a stonk
#idk if its actually stock_uid, i dont think it matters
@app.route('/stocks/<stock_uid>', methods=['POST', 'GET'])
def handle_stonks(stock_uid):
    stonk = StonkModel.query.get_or_404(stock_uid)
    if request.method == 'GET':
        res = {
            "ticket": stonk.ticket,
            "timestamp": stonk.timestamp,
            "price": stonk.price,
            "volume": stonk.volume
        }
        return "Success, stonk: " + str(res)
    elif request.method == 'PUT':
        data = request.get_json()
        stonk.ticker=data['ticker']
        stonk.timestamp=data['timestamp']
        stonk.price=data['price']
        stonk.volume=data['volume']
        db.session.add(stonk)
        db.session.commit()
        return "Stonk {} updated successfully".format(stonk.ticker)
    elif request.method == 'DELETE':
        db.session.delete(stonk)
        db.sesion.commit()
        return "Stonk {} deleted successfully.".format{stonk.ticker}

#our file name is fine right?
if __name__ == '__main__':
    app.run()
