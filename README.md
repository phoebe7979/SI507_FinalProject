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
2. Run `python SI507project_tools.py runserver
3. Open your browser, and access 127.0.0.1:5000

## How to use

1. Once you reach the site, you will be prsented with an image created using matplotlib.
2. Click on each phase link such as 'Phase 1', 'Phase 2', 'Phase 3' to see the introduction to different phase of the Infinity Saga. You can return to the home page by clicking on 'Back' button located at the bottom of the page.
3. Click 'Read more' on the home page for each movie to see individual movie release year and ratings.

## Routes in this application
- `/` -> this is the home page
- `/phase/<phaseid>/` -> this route displays each phase details
- `/movie/<movieid>/>' - > this route displays movie details


## How to run tests
1. Simply run the SI507project_tests.py file

## In this repository:
- screenshots
  - index.png
  - movie.png
  - phase.png
- static
  - rating.png
- templates
  - index.html
  - layout.html
  - movie.html
  - phase.html
- advanced_expiry_caching.py
- diagram.jpg
- insert_models.py
- mcumovies.db
- mcumovies.sqlite
- omdb_cached.data.json
- phase.csv
- README.md
- requirements.txt
- rt_cache.json
- SI507project_tests.py
- SI507project_tools.py


---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [x] Project is submitted as a Github repository
- [x] Project includes a working Flask application that runs locally on a computer
- [x] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [x] Includes a diagram of your database schema
- [x] Includes EVERY file needed in order to run the project
- [x] Includes screenshots and/or clear descriptions of what your project should look like when it is working (Please refer to the screenshots folder)

### Flask Application
- [x] Includes at least 3 different routes
- [x] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [x] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [x] Use of a new module (matplotlib)
- [ ] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [ ] A many-to-many relationship in your database structure
- [ ] At least one form in your Flask application
- [x] Templating in your Flask application (x)
- [ ] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [x] Sourcing of data using web scraping
- [x] Sourcing of data using web REST API requests
- [ ] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [x] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [x] I included a summary of my project and how I thought it went **in my Canvas submission**!
