from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Crime, User, Category, Chat
from . import db
from datetime import datetime
from collections import defaultdict
from collections import Counter
from datetime import datetime
import folium
from geopy.geocoders import Nominatim
import requests
import random

views = Blueprint('views', __name__)


response= None
brac_location = [23.7725, 90.4253]
default_location= brac_location  
zoom_level = 14
searched_location = None 
m = folium.Map(location=default_location, zoom_start=zoom_level, tiles='cartodbdark_matter')
crime_locations= []

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    global crime_locations, m
    m = folium.Map(location=default_location, zoom_start=zoom_level, tiles='cartodbdark_matter')
    if request.method == 'POST':
        text = request.form['text']

        new_message = Chat(user_id=current_user.id, text=text)
        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for('views.home'))
   
    chats = Chat.query.all()
    crimes = Crime.query.all()
    categories = Category.query.all()
    for crime in crimes:
        crime.user = User.query.get(crime.user_id)
        if crime.location not in crime_locations:
            crime_locations.append(crime.location)

    return render_template("home.html", user=current_user, crimes=crimes, categories=categories, chats=chats)

@views.route('/stats', methods=['GET'])
@login_required
def stats():
    # Fetch all crimes
    crimes = Crime.query.all()
    location_filter = request.args.get('location', '')
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    else:
        start_date = datetime.min  
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        end_date = datetime.max 

    filtered_crimes = [
        crime for crime in crimes
        if (start_date <= crime.date <= end_date) and (location_filter == '' or crime.location == location_filter)
    ]

    location_counts = Counter([crime.location for crime in crimes])
    locations = list(location_counts.keys())
    counts = list(location_counts.values())

    return render_template('stats.html',
        user=current_user,
        locations=locations,
        counts=counts,
        location_filter=location_filter,
        crime_count=len(filtered_crimes),location_counts=location_counts, crimes=crimes)