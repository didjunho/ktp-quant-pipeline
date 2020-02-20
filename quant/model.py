from driver import db
# import sqlalchemy as db
from sqlalchemy.dialects.postgresql import JSON

# DONT THINK WE NEED THIS FILE

class Result(db.Model):
    __tablename__ = 'results'

    #id of the result we stored
    id = db.Column(db.Integer, primary_key=True)
    #url that we counted the words from
    url = db.Column(db.String())
    #full list of words that we counted
    result_all = db.Column(JSON)
    #list of words that we counted minus stop words 
    result_no_stop_words = db.Column(JSON)

    #will run the first time we create a new result
    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words
    
    #represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)
