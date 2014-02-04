''' WHAT I WANNA DO
1) soup the page with all the top grossing films
2) grab the link for each titles
3) write those to a list
4) iterate through that list 
5) go to keyword page for each title
6) write keywords to a csv, add new column with movie name
7) do that for every movie 
8) download csv
'''

from bs4 import BeautifulSoup
import requests
import pprint
import csv
import re

# made URL a global variable so that i can use this bad boy again

URL = "http://www.imdb.com/search/title?at=0&sort=boxoffice_gross_us,desc&start=101&year=2013,2013"

# STEP 1: okay first up: a function that will get me the movies url so that i can get to the keywords page

def get_movies(url):
    reponse = requests.get(url)                            # just learned about 'response' -- kinda like console.log 
    soup = BeautifulSoup(reponse.text)                     # can give you info like "response.status_code" or "response.json"
    movies_list = []                                       # make a list now to append the titles and URLS later on
    url_list = soup.select('.title a[href*="title"]')


#STEP 2: okay now that we've got the urls, we need to do something useful with them. 
#each_url means nothing right now, its just a consistent handle for me to iterate on as i go through my urls
    
    for each_url in url_list:
        movie_title = each_url.text                     #okay so this gave us two URLS,
        if movie_title != 'X':                          #the good one we wanted but then a shitty one with "X" in it so line gets rid of the ones we dont want
            movie_url = each_url["href"] 
            movies_list.append(                         # We're creating a list of dictionaries now 
                    {
                "movie_title": movie_title,             # each dict has "movie_title" key and a "url" key
                "url":movie_url                         # we can use this to get the values out of each dict later on
                }
                )
    return movies_list

#STEP 3: okay we've got the clean URLS we want, now we've gotta get to the keywords page and soup the words

def get_keywords(url):
    keywords = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    tables = soup.find_all('table', class_='dataTable') #ok so there were two tables on the page, the one we want a BS amazon table so we had to be specific here
    table = tables[0]                                          # [0] gets the first element of the list "tables" 
    for tr in table.find_all('tr'):                     # beautifulsoup always returns a list when calling find_all
        for td in tr.find_all('td'):                    # even if there is only one element
            if not isinstance(td, unicode):             # "isinstance" just checks the type of the variable, wanted to make sure we dont get those blank table rows 
                keywords.append(td.text)                #here we appended the keywords to the empty list we created in line 45
    return keywords

#STEP 4: GOT THE GOODS, LETS DO THIS
#below is a handy function so that i can reuse get_movies and get_keywords in another script if i wanted to

if __name__ == '__main__':                              # __name__ is the name of the "current" file             
    movies = get_movies(URL)                            #thats always the filename unless im executing directly (i.e. python imdb.py)
    with open('movies_clean3.csv', 'w') as output:      # in wihch case __name__ will be "__main__". This helps with importing.
        csvwriter = csv.writer(output)                  # this is beautiful soup way of writing to a CSV
        for movie in movies:
            title = movie['movie_title']
            url = movie['url']
            keyword_link = 'http://www.imdb.com{}keywords/'.format(url) # had to format the link since they were relative links, 
            keywords = get_keywords(keyword_link)                       # at first i tried 'http://www.imdb.com' + url + 'keywords/' which worked but .format is cleaner
            csvwriter.writerow([title, keywords])
        if UnicodeEncodeError: #ugh unicode errors will follow you to your grave
            pass 
