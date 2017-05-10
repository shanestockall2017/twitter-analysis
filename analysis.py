##########################################################
####################### IMPORTS ##########################
##########################################################
import re
import twitter
import sys
from textblob import textblob


##########################################################
################### GLOBAL VARIABLES #####################
##########################################################

API_KEY = ""
SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
API_INSTANCE = None


##########################################################
################### CLASS DEFINITION #####################
##########################################################

class Person:
	def __init__(self):
		self.influence = 0
		self.handle = ""


##########################################################
######################## METHODS #########################
##########################################################

# authenticates with twitter API
def twitter_api():
	API_INSTANCE = twitter.Api(consumer_key =       API_KEY,
					  		   consumer_secret =    SECRET,
					  		   access_token_key =   ACCESS_TOKEN,
					  		   access_token_secret = ACCESS_TOKEN_SECRET)

	print api.VerifyCredentials()

# gets a list of followers, given a person
def get_network(person):
	api = API_INSTANCE

	network = api.GetFriends()

	return network

# gets a list of tweets, given a person
def get_tweets(person):
	api = API_INSTANCE

	list_tweets = api.GetUserTimeline(screen_name=person)

	return list_tweets

# analyzes a person's network to determine their influence, given a person
def get_influence(person):
	avg_retweets = 1
	avg_favorites = 1
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

	influence = 0.1 * network_size + avg_favorites + avg_favorites

	return influence


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

def ordered_list_of_people_in_network(person):
	list_of_people = []
	network = get_network(person)

	for person in network:
		p = Person()
		p.handle = person
		p.influence = get_influence(person)
		list_of_people.append(p)

def main():
	API_INSTANCE = twitter_api()


	ordered_list_of_people_in_network(sys.argv[1])
# gets the sentiment of a tweet, given a particular tweet
# def get_tweet_sentiment(tweet):