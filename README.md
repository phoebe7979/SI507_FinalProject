# Marvel Cinematic Universe Database

Name

[Link to this repository](https://github.com/phoebe7979/SI507_FinalProject)

---

## Project Description

This application displays a list of Marvel Cinematic Universe (MCU) movies information.
Users will be able to check each MCU movie's name, image, director, and ratings.
Using Matplotlib, the movie will also display the ratings from imdb, Tomatometer, and Rotten Tomato audience score in order to see which one is the highest rated movie.


## How to run

1. Install all requirements with `pip install -r requirements.txt'
2. Run `python programname.py runserver
3. Open your browser, and access 127.0.0.1:5000

## How to use

1. Once you reach the site, you will be prsented with a list of MCU movies.
2. Click on 'Browse by phase' to see movies that belongs to the different phase of the Infinity Saga.
3. A screenshot of it is like (need to insert image)

## Routes in this application
- `/` -> this is the home page
- `/<movie>` -> this route displays each movie details
- `/<phase> -> this route displays movies that belongs to the different phase of the saga
- `/rating -> this route displays a visualized data of the ratings for each MCU movie

## How to run tests
1. First... (e.g. access a certain directory if necessary)
2. Second (e.g. any other setup necessary)
3. etc (e.g. run the specific test file)
NOTE: Need not have 3 steps, but should have as many as are appropriate!

## In this repository:
- Directory Name
  - File in directory
  - File in directory
- File name
- File name

---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [x] Project is submitted as a Github repository
- [ ] Project includes a working Flask application that runs locally on a computer
- [x] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [ ] Includes a sample .sqlite/.db file
- [x] Includes a diagram of your database schema
- [ ] Includes EVERY file needed in order to run the project
- [ ] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [ ] Includes at least 3 different routes
- [ ] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [ ] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [ ] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [ ] Use of a new module (x)
- [ ] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [ ] A many-to-many relationship in your database structure
- [ ] At least one form in your Flask application (x)
- [ ] Templating in your Flask application (x)
- [ ] Inclusion of JavaScript files in the application
- [ ] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [x] Sourcing of data using web scraping
- [x] Sourcing of data using web REST API requests
- [ ] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [ ] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!
