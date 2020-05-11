"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from My_Final_Project import app 
from My_Final_Project.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines



from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError 


from My_Final_Project.Models.QueryFormStructure import QueryFormStructure 
from My_Final_Project.Models.QueryFormStructure import LoginFormStructure 
from My_Final_Project.Models.QueryFormStructure import UserRegistrationFormStructure 

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year
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
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\2018 FIFA World Cup Squads.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover') 

    return render_template(
        'data.html',
        title='My Data Base Page~ ',
        year=datetime.now().year,
        message='Here you can find a link for the 2018 FIFA World Cup Squads Data Base', 

        raw_data_table = raw_data_table
    )


@app.route('/registar', methods=['GET', 'POST'])
def registar():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()): 
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas'
        )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)): 
            flash('Login approved!') 
            #return redirect('<where to go if login is good!') 
        else:
            flash('Error in - Username and/or password') 
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas'
        )


@app.route('/query')
def query():
    
    return render_template(
        'query.html',
        title='You managed to reach my Query page~',
        year=datetime.now().year,
        message='Here you can find a graph'


    )

