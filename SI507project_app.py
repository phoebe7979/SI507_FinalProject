from flask import Flask, render_template, session, redirect, url_for
from sqlalchemy import Column, ForeignKey, Integer, String, Float, types, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, query
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from SI507project_tools import *


# Set up application
app = Flask(__name__)
app.debug = True
app.use_reloader = True #"reloads" the code whenever you make a change so that you don't have to manually restart the app to see changes.
app.config['SECRET_KEY'] = 'ldjsfhakjshwej'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./mcumovies.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # For database use
session = db.session

#routing for the main page and the total ratings
@app.route('/')
def index():
    allmovies = Movies.query.all()
    num_movies = len(allmovies)
    return render_template('index.html', num_movies=num_movies)


#routing different phases
@app.route('/phase/<phaseid>/')
def htmlcontent():
    phaseitem = Phases.query.filter_by(Id=phaseid).first()
    phasename = phaseitem.Phase
    phaseintro = phaseitem.Intro
    return render_template('phase.html', phasename = phasename, phaseintro = phaseintro)



if __name__ == "__main__":
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run()
