from bs4 import BeautifulSoup # need beautifulsoup for scraping
import requests, json # need these to access data on the internet and deal with structured data in my cache
from advanced_expiry_caching import Cache # use tool from the other file for caching

FILENAME = "nytimes_sample_cache.json" # saved in variable with convention of all-caps constant

program_cache = Cache(FILENAME) # create a cache -- stored in a file of this name

url = "https://www.nytimes.com/column/trilobites" #url can act as identifier for caching in a scraping situation -- it IS frequently unique here, unlike in query requests

data = program_cache.get(url)
if not data: # use the .get function from the Cache class to see if we can get this data from the cache -- do we already have data associated with this url? if not,
    # make a request to get the data from the internet -- all the junk at that page
    data = requests.get(url).text # get the text attribute from the Response that requests.get returns -- and save it in a variable. This should be a bunch of html and stuff
    #print(data) # to prove it - this will print out a lot

    # set data in cache:
    program_cache.set(url, data, expire_in_days=1) # just 1 day here because news site / for an example in class

# now data stored in variable -- can do stuff with it, separate from the caching
soup = BeautifulSoup(data, "html.parser") # html.parser string argument tells BeautifulSoup that it should work in the nice html way

#print(soup.prettify()) # view the "pretty" version of everything in the BeautifulSoup instance

#print(soup.find_all("a")) # see if this works...

# All the list items on the page
list_items =  soup.find_all("li")
# print(list_items) # to see
for item in list_items:
    item.find("h2") # Find in that Tag element an h2 value, which from inspection appears to contain a bunch of information about articles relevant to this page about Trilobites
    if item.text.startswith("Image"): # Noticed that all the text starts with "Image" that is interesting to me, but I don't actually want the Image text -- that must come from some fancy way of putting the page together, I just want to capture and print out the text
        print(item.text[len("Image"):], "\n")

# But despite running this many times to change it, the MAIN URL that is captured at the top -- and any other URL you choose to do program_cache.set on -- will be cached and, when accessed in some way with program_cache.get later -- will be usable without making a new request to hit the page, at least until the expiry time is over.
