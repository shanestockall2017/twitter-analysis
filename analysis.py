##########################################################
####################### IMPORTS ##########################
##########################################################
import re
import twitter
import sys
import plotly.plotly as plotly
import networkx as nx
from plotly.graph_objs import *

#from textblob import textblob


##########################################################
################### GLOBAL VARIABLES #####################
##########################################################

API_KEY = ""
SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
API_INSTANCE = twitter.Api(consumer_key =       API_KEY,
					  		   consumer_secret =    SECRET,
					  		   access_token_key =   ACCESS_TOKEN,
					  		   access_token_secret = ACCESS_TOKEN_SECRET)

USERS = ['@shanestockall']

LANGUAGES = ['en']



##########################################################
################### CLASS DEFINITION #####################
##########################################################

class Person:
	def __init__(self):
		self.influence = 0
		self.handle = ""
		self.avg_favorites = 0
		self.avg_retweets = 0


##########################################################
######################## METHODS #########################
##########################################################

# gets a list of followers, given a person
def get_network(person):
	network = API_INSTANCE.GetFriends(screen_name=person)

	return network

# gets a list of tweets, given a person
def get_tweets(person):
	api = API_INSTANCE

	list_tweets = api.GetUserTimeline(screen_name=person)

	return list_tweets

def get_num_favorites(tweet):
	if tweet.favorite_count: 
		return int(tweet.favorite_count)
	else:
		return 0

def get_num_retweets(tweet):
	if tweet.retweet_count:
		return int(tweet.retweet_count)
	else:
		return 0

# analyzes a person's network to determine their influence, given a person
def get_influence(person):
	avg_retweets = 0
	avg_favorites = 0
	num_favorites = 0
	num_retweets = 0
	influence = 0

	network = get_network(person)

	network_size = float(len(network))

	tweets = get_tweets(person)

	num_tweets = float(len(tweets))


	for tweet in tweets:
		num_favorites += get_num_favorites(tweet)
		num_retweets += get_num_retweets(tweet)

	avg_retweets = float(num_retweets) / num_tweets
	avg_favorites = float(num_favorites) / num_tweets

	#this is really not a good metric of influence.
	#avg_retweets also includes things like celeb retweets, so inflation is a thing
	influence = 0.1 * network_size + avg_retweets + avg_favorites

	return influence, avg_retweets, avg_favorites

'''
# looks through a persons followers/following to find the most influential person
def most_influential_in_network(person):
	highest_influence = 0
	most_influential_person = None
	network = get_network(person)

	for person in network:
		influence = get_influence(person)

		if influence > highest_influence:
			highest_influence = influence
			most_influential_person = person


	return most_influential_person, highest_influence

# looks through 2 levels of followers/following to find the most influential person
def most_influential_in_extended_network(person):
	highest_influence = 0
	most_influential_person = None
	network = get_network(person)
	extended_network = network

	for person in network:
		extended_network += get_network(person)

	for person in extended_network:
		influence = get_influence(person)

		if influence > highest_influence:
			highest_influence = influence
			most_influential_person = person

	return most_influential_person, highest_influence
'''

#rip api limits
def ordered_list_of_people_in_network(person):
	list_of_people = []
	network = get_network(person)

	for person in network:
		p = Person()
		p.handle = person
		p.influence, p.avg_retweets, p.avg_favorites = get_influence(person)
		list_of_people.append(p)

	list_of_people.sort(key=lambda x: x.influence, reverse=True)

	return list_of_people

'''
def main():
	print API_INSTANCE.VerifyCredentials()

	list_of_people = ordered_list_of_people_in_network('@shanestockall')

	f = open("people.txt", "w+")

	for person in list_of_people:
		write_string = "username: " + str(person.handle) + "influence: " + str(person.influence) + "average RT: " + str(person.avg_retweets) + "average favorites: " + str(person.avg_favorites) + "\n"
		print write_string
		f.write(write_string)

	f.close()


if __name__ == "__main__":
	main()

# gets the sentiment of a tweet, given a particular tweet
# def get_tweet_sentiment(tweet):
'''
