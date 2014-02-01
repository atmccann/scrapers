'''
1) soup the page
2) grab the dropdown box full of team URLS
3) write to a list
4) iterate through that list
5) write to a csv, add a new column with the team name
6) do that 120 times
7) download csv
'''

from bs4 import BeautifulSoup
import urllib
import urllib2
import pprint
import csv

players = []
url_list = []
teams_list = []
indiv_url = []
all_players = []
players_list = []

#grab first url. tell it to soup. find everything with class "select-box" and write contents to a list
url = "http://espn.go.com/college-football/team/roster/_/id/12/arizona-wildcats"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
'''when you tried just find_all before, it dumped the
whole enchilada into a list with
only one item, which sucks. you want a list
where each item is a discrete option tag, so
you made a nested statement like this.'''
url_list = soup.find(class_="select-box").find_all("option")
print url_list

''' this is what iterating means: a for loop means that you can
act on shit in a way you define on EVERY ITEM IN A LIST. the
for loop is smart enough to see a list, know to do something
to every item in a list, so grab what's between the commas in a list
and manhandle it. each_url just refers to a placeholder while
you iterate on. each_url means nothing, its just a consistent handle for
you to grab. it stands for "each item on a list," and you just need to
consistently refer to it as such'''

'''also remember the dict lesson, since we learned
that's how BS4 stores things. its smart.'''
for each_url in url_list:
      
    team_name = each_url.text #define what you're looking for in name and url; name is the .text modifier,
    print each_url
    #which means take between the tags, and url is whatever comes after the "value=" thingy in the option tag
    team_url = each_url["value"]
    teams_list.append({"team_name":team_name,"url":team_url})
    #what you're doing here is creating a list of ~180 dictionaries; each dict has a name and a url. nesting
    #dicts within a list

#why did i put this outside the loop? well, think of anything outside the loop as
#"things i have to only once." anything insid  a loop will be iterated on forever, til the condition runs out
teams_list = teams_list[2:] #first two teams are junk, skip those 

'''same thing here, each_team is just a placeholder'''
for each_team in teams_list:
    indiv_url = each_team["url"]
    team_page = urllib2.urlopen(indiv_url)
    souped_team_page = BeautifulSoup(team_page)
    all_rows = souped_team_page.find_all("tr")
      #find_all is a function, and thus needs to act on a var. your var here
    #is "row," but row doesn't exist yet. you have to create the var before
    #you, you know, do anything with it. like find_all
           
    #what we did here before was just grab the TD's; its like telling python
    #to grab all the salami in the sandwich while leaving the bread. now you
    #have a pile of salami but no sandwiches. so instead we grabbed TRs, which are the bread that contains the TDs
    
    all_rows = all_rows[2:] #remember you had to skip the first few items? same thing here, since the
    #first few rows are junk. headers, and random labels and such. 
    
    for row in all_rows:
        current_row = row.find_all("td")
     #the variables we care about, grabbed by the order it comes in the list that's made up of the tds
        number = current_row[0].text
        name = current_row[1].text
        pos = current_row[2].text
        height = current_row[3].text
        weight = current_row[4].text
        hometown = current_row[6].text

    #the explicit names we're writing are called dictionary "keys", the ones in quotes
    #this tells python: in this dic for the current player, create a key called number assigning it
    #teh variable we called number right above
        
        current_player = {"number":number,
                          "name":name,
                          "pos":pos,
                          "height":height,
                          "weight":weight,
                          "team_name": each_team["team_name"],
                          "hometown":hometown} #IMPORTANT: each_team is where our loop started;
                                        #it's our placeholder that we can iterate through. we have to tell python
                                        #something thats iterable
        players_list.append(current_player)
 


  


#now for the csv shitfight


with open("C:\Python27\ArcGIS10.2\players.csv", "wb") as players_csv: #player_csv is just the name for our csv.
    writer = csv.writer(players_csv)
    for each_player in players_list:
        try:
            writer.writerow([each_player["name"],
                        each_player["number"],
                        each_player["pos"],
                        each_player["weight"],
                        each_player["height"],
                        each_player["team_name"],
                        each_player["hometown"]])
        except UnicodeEncodeError: #ugh unicode errors will follow you to your grave
            pass 
