import csv
from SI507project_tools import *
from sqlalchemy import create_engine
from sqlalchemy.orm import query
import datetime



init_db()

#####create a CSV file for directors#####

director_list = []

for movie in movie_list:
    if movie[5] not in director_list:
        director_list.append(movie[5])

for director in director_list:
    new_director = Directors(Director=director)
    session.add(new_director)
    session.commit()

#####create a csv file for phases#####

with open('phase.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        phase = row[0]
        intro = row[1]
        new_phase = Phases(Phase=phase, Intro=intro)
        session.add(new_phase)
        session.commit()

#####create movie class#####


for movie in movie_list:
    phasenum = session.query(Phases.Id).filter(Phases.Phase == movie[2])
    directornum = session.query(Directors.Id).filter(Directors.Director == movie[5])
    new_movie = Movies(Name=movie[0], Year = movie[8], Phaseid = phasenum, Directorid = directornum, Tomatometer = movie[3], AudienceScore = movie[4], IMDBRating = movie[7], Poster = movie[6])
    session.add(new_movie)
    session.commit()

csvfile.close()








#reference
#https://marvelcinematicuniverse.fandom.com/wiki/Phase_One
#https://marvelcinematicuniverse.fandom.com/wiki/Phase_Two
#https://marvelcinematicuniverse.fandom.com/wiki/Phase_Three
#https://marvelcinematicuniverse.fandom.com/wiki/Phase_Four
