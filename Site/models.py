# importing libraries
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from Site import db



class RandomPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"RandomPrediction('{self.content}', '{self.league}')"
  


class HighScoring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"HighScoring('{self.content}', '{self.league}')"
  

class BettingTips(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"BettingTips('{self.content}', '{self.league}')"


class InForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"InForm('{self.content}', '{self.league}')"



class Bts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Bts('{self.content}', '{self.league}')"


class Championship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Championship('{self.content}', '{self.league}')"




class HighConceding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"HighConceding('{self.content}', '{self.league}')"



class SureOdds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"SureOdds('{self.content}', '{self.league}')"
  


  
class BetAgainst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    dateUploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"BetAgainst('{self.content}', '{self.league}')"
  

    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    def __repr__(self):
        return f"BetAgainst('{self.name}', '{self.email}')"
  