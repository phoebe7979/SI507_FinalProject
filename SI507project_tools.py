from bs4 import BeautifulSoup # need beautifulsoup for scraping
import requests, json # need these to access data on the internet and deal with structured data in my cache
from advanced_expiry_caching import Cache # use tool from the other file for caching
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, query
from sqlalchemy import create_engine

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
    movie_list[n].append(director)
    movie_list[n].append(poster)
    movie_list[n].append(imdbrating)
    n += 1

#manually insert Marvel's The Avengers data because the name on Rotten Tomatoes does not match with IMDB
omdb_result = get_omdb_data("The Avengers")
movie_list[16][-3] = omdb_result['Director']
movie_list[16][-2] = omdb_result['Poster']
movie_list[16][-1] = int(float(omdb_result['imdbRating']) * 10)

print(movie_list)


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
Base = declarative_base()

class Phases(Base):
    __tablename__ = 'Phases'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Phase = Column(String(250))
    Intro = Column(String(250))

class Directors(Base):
    __tablename__ = 'Directors'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Director = Column(String(250)) # Not trying to separate the director names

class Movies(Base):
    __tablename__ = 'Movies'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(250))
    Year = Column(Integer)
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
engine = create_engine('sqlite:///mcumovies.sqlite', echo=False)


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
