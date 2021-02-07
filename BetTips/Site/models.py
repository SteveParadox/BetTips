# importing libraries
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from Site import db



class RandomPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"RandomPrediction('{self.content}', '{self.publicId}')"
  


class HighScoring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"HighScoring('{self.content}', '{self.publicId}')"
  

class BettingTips(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"BettingTips('{self.content}', '{self.publicId}')"


class InForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"InForm('{self.content}', '{self.publicId}')"



class Bts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Bts('{self.content}', '{self.publicId}')"


class Championship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Championship('{self.content}', '{self.publicId}')"




class HighConceding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"HighConceding('{self.content}', '{self.publicId}')"



class SureOdds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"SureOdds('{self.content}', '{self.publicId}')"
  


  
class BetAgainst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"BetAgainst('{self.content}', '{self.publicId}')"
  