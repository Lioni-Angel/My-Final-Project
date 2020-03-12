"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from My_Final_Project import app 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact.pg')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='You have reached to the CONTACT page~',
        year=datetime.now().year,
        message='<3'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='You have reached to the ABOUT page~',
        year=datetime.now().year,
        message='Here, you can get to know everything the project' 
    ) 

@app.route('/DataBase')
def data():
    """Renders the about page."""
    return render_template(
        'data.html',
        title='My Data Base Page~ ',
        year=datetime.now().year,
        message='Here you can find a link for the 2018 FIFA World Cup Squads Data Base'
    )

@app.route('/photoAlbum')
def photoAlbum():
    """Renders the contact page."""
    return render_template(
        'photoAlbum.html',
        title='My Photo Album',
        year=datetime.now().year,
        message='warning: might be too cute'
    )


@app.route('/registar')
def registar():
    """Renders the contact page."""
    return render_template(
        'registar.html',
        title='Here you can easly registar for my website!',
        year=datetime.now().year,
        message='You just need to fill in the details' 
    )

