# importing libraries
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from Site import db



class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    __mapper_args__ = {
        'polymorphic_identity': 'prediction',
        'polymorphic_on': db.Column(db.String(50))
    }

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.content}', '{self.league}')"


class RandomPrediction(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'random_prediction'}


class HighScoring(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'high_scoring'}


class BettingTips(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'betting_tips'}


class InForm(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'in_form'}


class Bts(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'bts'}


class Championship(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'championship'}


class HighConceding(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'high_conceding'}


class SureOdds(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'sure_odds'}


class BetAgainst(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'bet_against'}


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())

    def __repr__(self):
        return f"Notification('{self.name}', '{self.email}')"

  
