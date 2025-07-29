import os
import sys
import pandas as pd

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

bp = Blueprint('home', __name__, url_prefix='/') 

@bp.route('/', methods=['GET'])
def home():
    return render_template('home/home.html')