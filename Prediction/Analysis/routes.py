from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework
import uuid 
from ..models import  Teams, InForm, Bts, BettingTips, HighScoring, HighConceding
from Prediction import db, app 
import datetime

# registering blueprint 
analysis = Blueprint('analysis', __name__)

