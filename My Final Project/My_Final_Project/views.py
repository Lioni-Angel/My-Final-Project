"""
Routes and views for the flask application.
"""

import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


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
from My_Final_Project.Models.QueryFormStructure import QueryForm

from flask_bootstrap import Bootstrap

#כל אלו הם סיפריות שהוספתי, ועשיתי אימפורטים ("הבאתי" אותם, ו"קראתי להם" גם בשמות קצרים ונוחים יותר), כתבתי אותם בכדי שנוכל להפעיל פקודות מסויימות 

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines()
bootstrap = Bootstrap(app)



@app.route('/')
@app.route('/home')
#זה הכתובת של הדף, מתוך האתר שלי
def home(): 
 #layoutכלומר, שזה "לוקח" את השם של איך שקראתי לדף זה בדף ה

    """Renders the home page."""

    return render_template(
        'index.html',
 #כלומר שזה פותח את הדף שקראתי לו בשם זה(מתוך הטמפלייטס) י
        title='Home Page', 
 #הכותרת של הדף
        year=datetime.now().year
 #הזמן של התוכנה
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='You have reached to the CONTACT page~',
        year=datetime.now().year,
        message=''
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='You have reached to the ABOUT page~',
        year=datetime.now().year,
        message='Here, you can get to know everything about the project' 
    ) 

@app.route('/DataBase')
def data():
    """Renders the about page."""
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\2018 FIFA World Cup Squads.csv'))
    #זה גורם "להציב" את הדאטא, וגם עשינו לה אימפורט, כלומר "הבאנו/קראנו" לו, ומציבים שהדאטא הזה יהיה בשם חדש, קצר ונוח יותר
    raw_data_table = df.to_html(classes = 'table table-hover') 
    #הפקודה שדרכה אני ללא בטוחה..

    return render_template(
        'data.html',
        title='My Data Base Page~ ',
        year=datetime.now().year,
        message='Here you can find a link for the 2018 FIFA World Cup Squads Data Base', 

        raw_data_table = raw_data_table
        #אותה הפקודה
    )


@app.route('/registar', methods=['GET', 'POST'])
def registar():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()): 
        #אם 
        if (not db_Functions.IsUserExist(form.username.data)):
            #אז ש
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            return redirect('query')
            #אם שני סעיפי ה if .query מתממשים/נכונים/קורים, אז מוחזרת הודעה שמודה על ההרשמה, ונפתח דף ה
        


        else: 
         #ואם זה לא נכון/קורה/מתממש, כלומר, שכבר יש משתמש שכזה, אז:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            #מופיעה הודעה שמודיעה שכבר קיים המשתמש הזה
            form = UserRegistrationFormStructure(request.form)
            #queryוניתנת גישה אל דף ה

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
            
            return redirect('query')


        else: 
            flash('Error in - Username and/or password') 
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas'
        )


@app.route('/query', methods = ['GET' , 'POST'])
def query():

    form = QueryForm()
    chart = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\2018 FIFA World Cup Squads.csv')) 
    s = set(df['Team'].to_list())
    l = list(s)
    l = list(zip(l,l))
    form.countries.choices = l

    if request.method == 'POST':
        countries_list = form.countries.data
        df = df[['Team' , 'Caps', 'Goals', 'Age']]
        df = df.groupby('Team').mean()
        df = df.loc[countries_list]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.4)
        df.plot(kind = 'bar', ax = ax)
        chart = plot_to_img(fig)

    return render_template(
        'query.html',
        title='You managed to reach my Query page~',
        year=datetime.now().year,
        message='Here you can find the graph', 
        form = form,
        chart = chart

    )

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String