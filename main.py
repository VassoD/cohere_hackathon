from flask import Flask, render_template, request, jsonify
import praw
from flask import jsonify
from threading import Thread
import datetime
from config import API_KEY
import cohere 

co = cohere.Client(API_KEY)

app = Flask(__name__)

from cohere.classify import Example

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

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        search_query = request.form["search_query"]
        matching_articles, prediction = search_articles(search_query)
        total_articles = len(matching_articles)
        return render_template("home.html", articles=matching_articles, total_articles=total_articles, prediction=prediction)
    return render_template("home.html")

def search_articles(search_query):
    reddit = praw.Reddit(client_id="f1ecYWIeukFQEEOPHjdtkA",
                         client_secret="KIbEIfhjYb1tfczA9sj3qlV95Fe7WA",
                         user_agent="praw_scraper_1.0")
    # subreddit_mapping = {"technews": "Tech News", "UkraineWarVideoReport": "Ukrain War Report","worldnews": "World News","ClimateNews": "Climate News","Coronavirus": "Covid 19 News","business": "Business News","Health": "Health News"}
    subreddit_mapping = {"technews": "Tech News","Coronavirus": "Covid 19 News"} 

    matching_articles = []
    prediction = ""
    for subreddit in subreddit_mapping.keys():
        subreddit = reddit.subreddit(subreddit)
        for submission in subreddit.new(limit=100):
            if search_query.lower() in submission.title.lower():
                response = co.classify(
                    model='large',
                    inputs=[submission.title],
                    examples=examples
                )
                for classification in response.classifications:
                    prediction = classification.prediction
                if prediction == "positive":
                    date = datetime.datetime.fromtimestamp(submission.created_utc)
                    formatted_date = date.strftime("%d-%m-%Y %H:%M:%S")
                    matching_articles.append(
                        {"title": submission.title, "id": submission.id, "category": subreddit_mapping[submission.subreddit.display_name],
                         "score": submission.score, "url": submission.url, "date": formatted_date}
                    )
                    # return jsonify({'prediction': prediction})
    return matching_articles, prediction

@app.route("/ethics")
def ethics():
    return render_template("ethics.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/manifesto")
def manifesto():
    return render_template("manifesto.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
