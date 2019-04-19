import unittest


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

class Testing_Movie(unittest.TestCase):
     def test_init(self):
        captainmarvel = Movie('Captain Marvel')
        self.assertTrue(vaptainmarvel.imdbRating)














unittest.main(verbosity=2)
