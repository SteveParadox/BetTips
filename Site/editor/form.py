import json
import uuid
import os

from flask import Blueprint, render_template, request, jsonify

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired



class Post(FlaskForm):
    content = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class InFormTeam(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')



class Tips(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class HighGoalStats(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class Bothteamsscore(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class HighConcedingRate(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')




class sureOddsForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')



class championshipDrawForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class RandomPickForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    league = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')


class NotificationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    submit = SubmitField('Subscribe')