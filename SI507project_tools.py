from bs4 import BeautifulSoup # need beautifulsoup for scraping
import requests, json # need these to access data on the internet and deal with structured data in my cache
from advanced_expiry_caching import Cache # use tool from the other file for caching

#12-50 scrraping from rotten tomatoes
#


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

for movie in rtmovies:
    title_year = movie.find("strong")
    title = title_year.find("a").text
    title_list.append(title)
    year = title_year.find("span").text[1:-1]
    scores = movie.find_all("span", {"class" : "meter-value"})
    if len(scores) >1:
        tomatometer = scores[0].text.replace(" ","")[:-1]
        audiencescore = scores[1].text.replace(" ","")[:-1]
    else:
        tomatometer = "0"
        audiencescore = "0"

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


for movie in title_list:
    omdb_result = get_omdb_data(movie)
    try:
        director = omdb_result['Director']
    except KeyError:
        director = ""
    try:
        poster = omdb_result["Poster"]
    except KeyError:
        poster = ""
    try:
        imdbrating = omdb_result['imdbRating']
    except KeyError:
        imdbrating = "0"
    
