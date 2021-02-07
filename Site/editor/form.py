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