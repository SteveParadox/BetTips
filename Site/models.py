from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from Site import db

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

    prediction_type = db.Column(db.String(50))  # Add a column for the polymorphic identity

    __mapper_args__ = {
        'polymorphic_on': prediction_type,
        'polymorphic_identity': 'prediction'
    }

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.content}', '{self.league}')"


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    played = db.Column(db.Integer())
    won = db.Column(db.Integer())
    drawn = db.Column(db.Integer())
    lost = db.Column(db.Integer())
    gf = db.Column(db.Integer())
    ga = db.Column(db.Integer())
    gd = db.Column(db.Integer())
    points = db.Column(db.Integer())
    team_form = db.Column(db.Integer())
    win_rate = db.Column(db.Integer())
    loss_rate = db.Column(db.Integer())
    draw_rate = db.Column(db.Integer())
    performance_trend = db.Column(db.Integer())

    def __repr__(self):
        return f"Notification('{self.name}', '{self.email}')"

class InForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    win_percent = db.Column(db.Float())
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

class BettingTips(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String())
    competition = db.Column(db.String())
    prediction = db.Column(db.String())
    connfidence = db.Column(db.Float())
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

class HighScoring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String())
    league = db.Column(db.String())
    goal_scored = db.Column(db.String())
    scoring_rate = db.Column(db.Float())
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

class HighConceding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String())
    league = db.Column(db.String())
    goal_conceded = db.Column(db.String())
    conceding_rate = db.Column(db.Float())
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Bts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fixture = db.Column(db.String())
    league = db.Column(db.String())
    prediction = db.Column(db.Float())
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)


class RandomPrediction(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'random_prediction'}



class Championship(Prediction):
    __mapper_args__ = {'polymorphic_identity': 'championship'}



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



class TeamsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teams


team_schema = TeamsSchema()
teams_schema = TeamsSchema(many=True)
