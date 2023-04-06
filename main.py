from flask import Flask, render_template, request
import praw
# from flask import jsonify
# from threading import Thread
import datetime
import os
# from config import API_KEY
import cohere 

API_KEY = os.environ.get("API_KEY")
co = cohere.Client(API_KEY)

app = Flask(__name__)

from cohere.responses.classify import Example


examples = [
  Example("The order came 5 days early", "positive"), 
  Example("The item exceeded my expectations", "positive"), 
  Example("I ordered more for my friends", "positive"), 
  Example("I would buy this again", "positive"), 
  Example("I would recommend this to others", "positive"), 
  Example("The package was damaged", "negative"), 
  Example("The order is 5 days late", "negative"), 
  Example("The order was incorrect", "negative"), 
  Example("I want to return my item", "negative"), 
  Example("The item\'s material feels low quality", "negative"), 
  Example("The product was okay", "neutral"), 
  Example("I received five items in total", "neutral"), 
  Example("I bought it from the website", "neutral"), 
  Example("I used the product this morning", "neutral"), 
  Example("The product arrived yesterday", "neutral"),
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/ethics")
def ethics():
    return render_template("ethics.html")

@app.route("/newsboy", methods=["GET", "POST"])
def newsboy():
    if request.method == "POST":
        search_query = request.form["search_query"]
        matching_articles, prediction = search_articles(search_query)
        total_articles = len(matching_articles)
        return render_template("newsboy.html", articles=matching_articles, total_articles=total_articles, prediction=prediction, spinner=True)
    return render_template("newsboy.html")

def search_articles(search_query):
    #code to get the Reddit instance and subreddit_mapping
    reddit = praw.Reddit(client_id="f1ecYWIeukFQEEOPHjdtkA",
                         client_secret="KIbEIfhjYb1tfczA9sj3qlV95Fe7WA",
                         user_agent="praw_scraper_1.0")
    # subreddit_mapping = {"technews": "Tech News","Coronavirus": "Covid 19 News"} 
    subreddit_mapping = {"technews": "Tech News", "UkraineWarVideoReport": "Ukraine War Report","worldnews": "World News","ClimateNews": "Climate News","Coronavirus": "Covid 19 News","business": "Business News","Health": "Health News"}
    matching_articles = []
    prediction = co.classify(model='large', inputs=[search_query], examples=examples).classifications[0].prediction
    
    # some examples from each category but not enough (We will need datasets for later to do the prediction of the user's search query into a category)
    tech_keywords = ['technology', 'tech', 'mobiles', 'mobile', 'electronics', 'apple', 'samsung', 'huawei', 'gadget', 'smartphone', 'vr', 'augmented reality', 'ar', 'wearables'
                    'computer', 'tablets', 'tablet', 'innovation', 'innovative', 'devices', 'device', 'internet of things', 'iot', 'virtual reality', 'ar',
                    'cyber security', 'artificial', 'ai', 'big data', 'blockchain', 'cloud computing',
                    'data center', 'machine', 'internet', '5g', 'robotics', 'drones', 'chatgpt', 'cohere']
    business_keywords = ['business', 'economy', 'finance', 'banks', 'banks', 'investment', 'market', 'stock', 'startup', 'entrepreneurship', 'mergers', 'acquisitions', 'corporation', 'industry', 'commercial', 'trade', 'money', 'euro']
    health_keywords = ['health', 'medicine', 'disease', 'medical', 'hospital', 'doctor', 'virus', 'vaccine', 'cure', 'illness', 'symptoms', 'diseases', 'medical treatment', 'medical research', 'healthcare', 'pharmaceutical', 'drugs']
    ukraine_keywords = ['ukraine', 'russia', 'war', 'politics', 'government', 'ukrainian', 'kiev', 'crimea']
    worldnews_keywords = ['world', 'worldnews', 'countries', 'international', 'global', 'events', 'affairs', 'foreign', 'headlines']
    climateNews_keywords = ['climate', 'climate change', 'global warming', 'environment', 'environmental']
    covid_keywords = ['covid', 'covid19', 'coronavirus', 'pandemic', 'virus', 'vaccine', 'corona']

    subreddits_to_search = []
    if any(word in search_query.lower() for word in tech_keywords):
        subreddits_to_search.append('technews')
    if any(word in search_query.lower() for word in business_keywords):
        subreddits_to_search.append('business')
    if any(word in search_query.lower() for word in health_keywords):
        subreddits_to_search.append('Health')
    if any(word in search_query.lower() for word in ukraine_keywords):
        subreddits_to_search.append('UkraineWarVideoReport')
    if any(word in search_query.lower() for word in ukraine_keywords):
        subreddits_to_search.append('UkraineWarVideoReport')
    if any(word in search_query.lower() for word in worldnews_keywords):
        subreddits_to_search.append('worldnews')
    if any(word in search_query.lower() for word in climateNews_keywords):
        subreddits_to_search.append('ClimateNews')
    if any(word in search_query.lower() for word in covid_keywords):
        subreddits_to_search.append('Coronavirus')

    # for subreddit in subreddit_mapping.keys():
    #     subreddit = reddit.subreddit(subreddit)
    for subreddit in subreddits_to_search:
        subreddit = reddit.subreddit(subreddit)
        for submission in subreddit.new(limit=15):
            response = co.classify(
                model='large',
                inputs=[submission.title],
                examples=examples
            )
            for classification in response.classifications:
                   article_prediction = classification.prediction
            if article_prediction == prediction:
                date = datetime.datetime.fromtimestamp(submission.created_utc)
                formatted_date = date.strftime("%d-%m-%Y %H:%M:%S")
                matching_articles.append(
                    {"title": submission.title, "id": submission.id, "category": subreddit_mapping[submission.subreddit.display_name],
                     "score": submission.score, "url": submission.url, "date": formatted_date}
                )
    return matching_articles, prediction

@app.route("/manifesto")
def manifesto():
    return render_template("manifesto.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")



if __name__ == "__main__":
    app.run(debug=True)
