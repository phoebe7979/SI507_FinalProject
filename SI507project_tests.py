from SI507project_tools import *
import unittest

#The following test is used to see if the webscraping works for rotten tomatoes
class TestSourcedMovieData(unittest.TestCase):
     def test_movie_namelist(self):       #testing that the list of movies scraped from rotten tomatoes are populated with movie titles
        self.assertIn('Captain Marvel', title_list)
     def test_tomatometer(self):     # making sure the tomatometer is there
        self.assertTrue(tomatometer)
     def test_audiencescore(self):     # making sure the audiencescore is there
        self.assertTrue(audiencescore)
     def test_director(self):     # making sure the director is there
        self.assertTrue(director)
     def test_poster(self):     # making sure the posterurl is there
        self.assertTrue(poster)





if __name__ == "__main__":
    unittest.main(verbosity=2)











unittest.main(verbosity=2)
