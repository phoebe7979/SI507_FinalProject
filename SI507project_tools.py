from bs4 import BeautifulSoup # need beautifulsoup for scraping
import requests, json # need these to access data on the internet and deal with structured data in my cache
from advanced_expiry_caching import Cache # use tool from the other file for caching
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, types, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, query
from sqlalchemy import create_engine
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.image import BboxImage
import urllib3 # to access image url captured from omdb
from urllib.request import urlopen
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox) # importing a function that helps display the image
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#Part 1: scraping from rotten tomatoes
#Part 2: REST API for OMDB
#Part 3: Creating class models for database



###############################################################################################
############# Webscrapting functions to get and cache all Rotten Tomatoes data ################
###############################################################################################

FILENAME = "rt_cache.json" # saved in variable with convention of all-caps constant

program_cache = Cache(FILENAME) # creating a cache

url = "https://www.rottentomatoes.com/franchise/marvel_cinematic_universe/"

data = program_cache.get(url)
if not data: # use the .get function from the Cache class to see if we can get this data from the cache -- do we already have data associated with this url? if not,
    # make a request to get the data from the internet -- all the junk at that page
    data = requests.get(url).text # get the text attribute from the Response that requests.get returns -- and save it in a variable. This should be a bunch of html and stuff
    #print(data) # to prove it - this will print out a lot

    # set data in cache:
    program_cache.set(url, data, expire_in_days=7) # new marvel movie is coming out so I want to have the scores updated at least every week

# now data stored in variable -- can do stuff with it, separate from the caching
soup = BeautifulSoup(data, "html.parser") # html.parser string argument tells BeautifulSoup that it should work in the nice html way

#print(soup.prettify()) # view the "pretty" version of everything in the BeautifulSoup instance

#print(soup.find_all("a")) # see if this works...
rtmovies = soup.find_all("div", {"data-franchise-type" : "movie"})

#now trying to get the name and year of the movies

title_list = []
movie_list = []


#Phase lists
phase1=[2008,2009,2010,2011,2012]
phase2=[2013,2014,2015]
phasee=[2016,2017,2018,2019]

for movie in rtmovies:
    new_movie = []
    title_year = movie.find("strong")
    title = title_year.find("a").text
    title_list.append(title)
    year = int(title_year.find("span").text[1:-1])
    scores = movie.find_all("span", {"class" : "meter-value"})
    if len(scores) >1:
        tomatometer = int(scores[0].text.replace(" ","")[1:-2])
        audiencescore = int(scores[1].text.replace(" ","")[1:-2])
    else:
        tomatometer = 0
        audiencescore = 0
    if year in phase1:
        phase = 'Phase 1'
    elif year in phase2:
        phase = 'Phase 2'
    else:
        phase = 'Phase 3'
    new_movie = [title, year, phase, tomatometer, audiencescore]
    movie_list.append(new_movie)


########################################################
############# REST API requests on OMdb ################
########################################################

# use function to create a unique identifier for cached data

try:
    cache_file = open(CACHE_FNAME, 'r')
    CACHE_DICTION = jason.loads(cache_file.read())
    cache_file.close()
except:
    CACHE_DICTION = {}


def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

CACHE_FNAME = "omdb_cached_data.json" # PROVIDED FOR YOU, DO NOT CHANGE



def get_omdb_data(str):
    baseurl = "http://www.omdbapi.com/"
    params_d = {}
    params_d['apikey'] = "d75ed2e1"
    params_d["type"] = "movie"
    params_d["t"] = str
    unique_ident = params_unique_combination(baseurl, params_d, private_keys=["apikey"])
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        response = requests.get(baseurl,params_d)
        CACHE_DICTION[unique_ident] = json.loads(response.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fileforw = open(CACHE_FNAME, 'w')
        fileforw.write(dumped_json_cache)
        fileforw.close()
        return CACHE_DICTION[unique_ident]

n = 0
for movie in title_list:
    omdb_result = get_omdb_data(movie)
    try:
        director = omdb_result['Director']
    except KeyError:
        director = "N/A"
    try:
        poster = omdb_result["Poster"]
    except KeyError:
        poster = ""
    try:
        imdbrating = int(float(omdb_result['imdbRating']) * 10)
    except:
        imdbrating = 0
    try:
        released = omdb_result['Released']
    except:
        released = 'N/A'
    movie_list[n].append(director)
    movie_list[n].append(poster)
    movie_list[n].append(imdbrating)
    movie_list[n].append(released)
    n += 1

#manually insert Marvel's The Avengers data because the name on Rotten Tomatoes does not match with IMDB
omdb_result = get_omdb_data("The Avengers")
movie_list[16][5] = omdb_result['Director']
movie_list[16][6] = omdb_result['Poster']
movie_list[16][7] = int(float(omdb_result['imdbRating']) * 10)
movie_list[16][8] = omdb_result['Released']

#change released dates from string to to_datetime
for movie in movie_list:
    datestr = movie[8]
    d = datetime.strptime(datestr, '%d %b %Y')
    strd = d.strftime('%Y-%m-%d')
    newd = datetime.strptime(strd, '%Y-%m-%d').date()
    movie[8] = newd
#    print(movie[8])




########################################################################
############# Writing API and Scraped data to CSV files ################
########################################################################




#open a csv file for all movies and start populating data into the files
#moviefn = open('movie.csv','w')
#moviefn.truncate()  #clearing all data on moviefn first in case I overwrite it

#for movie in movie_list:
#    moviefn.write('{},{},{},{},{},{},{}'.format(movie[0], movie[1], movie[]))
#    moviefn.write('\n')




##################################################
############# Flask Model Classes ################
##################################################
# Set up application
app = Flask(__name__)
app.debug = True
app.use_reloader = True #"reloads" the code whenever you make a change so that you don't have to manually restart the app to see changes.
app.config['SECRET_KEY'] = 'ldjsfhakjshwej'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./mcumovies.db' # location of the database
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy


Base = declarative_base()

class Phases(db.Model):
    Director = Column(String(250)) # Not trying to separate the director names
    __tablename__ = 'Phases'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Phase = Column(String(250))
    Intro = Column(String(250))

class Directors(db.Model):
    __tablename__ = 'Directors'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Director = Column(String(250))

class Movies(db.Model):
    __tablename__ = 'Movies'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(250))
    Year = Column(DateTime)
    Phaseid = Column(Integer, ForeignKey('Phases.Id')) # Creates a many to one relationship
    Directorid = Column(Integer, ForeignKey('Directors.Id')) # Not trying to separate the director names
    Tomatometer = Column(Integer)
    AudienceScore = Column(Integer)
    IMDBRating = Column(Integer)
    Poster = Column(String(250))
    Phases = relationship('Phases')
    Directors = relationship('Directors') # Necessary for that relationship to be used in our code

# Set up session
session = scoped_session(sessionmaker())



# Create an engine that stores data in the local directory's database
engine = create_engine('sqlite:///mcumovies.db', echo=False)


# Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
session.configure(bind=engine)

def init_db():
    # Drop all tables in the engine if needed for initialization. This is equivalent to "Delete Table" statements in raw SQL.
    # We'll leave this commented out initially, but if you wanted to drop everythign and 'reset' it every time, you might uncomment this.
    Base.metadata.drop_all(engine)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    # But, this won't overwrite existing tables -- it will simply create new ones if necessary.
    Base.metadata.create_all(engine)
    return engine # Returnign the engine makes it possible to use this function in other files (e.g. query files) to access the engine and use it

#################################################################
############# Create graph with matplotlib ######################
#################################################################
x = [] #timeline for the releases
y1 = [] #tomatometer
y2 = [] #audeince scores on Rotten Tomatoes
y3 = [] #imdb rating *10 (to normalize data with the above two scores)
y4 = [] #average rating point

for movie in movie_list:
    x.append(movie[8])
    y1.append(movie[3])
    y2.append(movie[4])
    y3.append(movie[7])
    y4.append((movie[3]+movie[4]+movie[7])/3)

plt.plot(x,y1, label='Tomatometer', color='tomato', linewidth=4)
plt.plot(x,y2, label='Audience Score', color='skyblue', linewidth=4)
plt.plot(x,y3, label='IMDb Rating', color='gold', linewidth=4)
plt.plot(x,y4, label='average score', marker = "o", markersize = 8, markerfacecolor='darkmagenta', color='lightgray', linewidth=4)



#http = urllib3.PoolManager()

# reference: http://rikunert.com/2017/05/18/star-trek-movies-ratings/

ax = plt.gca()
def add_image(ax_, url, xy, imzoom):
    f = urlopen(url)
    arr_img = plt.imread(f, format='jpg')
    imagebox = OffsetImage(arr_img, zoom=imzoom)
    imagebox.image.axes = ax_
    ab = AnnotationBbox(imagebox, xy, xybox=(0., 0.), boxcoords="offset points", pad=-0.5)  # hide box behind image
    ax_.add_artist(ab)
    return ax_

i = 0
for movie in movie_list:  # for each movie
    url = movie[6]
    add_image(ax, url, [x[i] , y4[i]], 0.15) # looping through x and y4 (average rating) for each movie
    i += 1

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


plt.xlabel('Released')
plt.ylabel('Rating')
plt.title('Marvel Cinematic Universe Movies Rating')
plt.legend()
plt.grid(color='gainsboro', linestyle='-', linewidth=0.5)

plt.show(block=False)
fig = plt.gcf()
fig.set_size_inches(36, 9)
fig.savefig('static/movierating.png', dpi=100)

#############################################################
############# Set up Flask application ######################
#############################################################


#routing for the main page and the total ratings
@app.route('/')
def index():
    moviesitem = Movies.query.all()
    num_movies = len(moviesitem)
    #name = moviesitem.Name
    return render_template('index.html', num_movies=num_movies, moviesitem = moviesitem)


#routing different phases
@app.route('/phase/<phaseid>/')
def htmlcontent(phaseid):
    phaseitem = Phases.query.filter_by(Id=phaseid).first()
    phasename = phaseitem.Phase
    phaseintro = phaseitem.Intro
    return render_template('phase.html', phaseitem = phaseitem, phasename = phasename, phaseintro = phaseintro)

#routing different movies
@app.route('/movie/<movieid>/')
def moviecontent(movieid):
    movieitem = Movies.query.filter_by(Id=movieid).first()
    moviename = movieitem.Name
    movieyear = movieitem.Year.date()
    movieimg = movieitem.Poster
    movietm = movieitem.Tomatometer
    movieas = movieitem.AudienceScore
    movieim = movieitem.IMDBRating
    moviedi = Directors.query.filter_by(Id=movieitem.Directorid).first()
    moviedirector = moviedi.Director
    return render_template('movie.html', movieitem = movieitem, moviedirector = moviedirector, moviename = moviename, movieyear = movieyear, movieimg = movieimg, movietm = movietm, movieas = movieas, movieim = movieim)


if __name__ == "__main__":
    app.run()
