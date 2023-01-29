from flask import Flask, render_template, request
import praw
# from datetime import datetime

app = Flask(__name__)

# timestamp = 1555555555
# date_time = datetime.fromtimestamp(timestamp)
# formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_query = request.form["search_query"]
        matching_articles = search_articles(search_query)
        total_articles = len(matching_articles)
        return render_template("index.html", articles=matching_articles, total_articles=total_articles)
    return render_template("index.html")

def search_articles(search_query):
    reddit = praw.Reddit(client_id="f1ecYWIeukFQEEOPHjdtkA",
                         client_secret="KIbEIfhjYb1tfczA9sj3qlV95Fe7WA",
                         user_agent="praw_scraper_1.0")
    # subreddit_mapping = {"technews": "Tech News", "UkraineWarVideoReport": "Ukrain War Report","worldnews": "World News","ClimateNews": "Climate News","Coronavirus": "Covid 19 News","business": "Business News","Health": "Health News"}
    subreddit_mapping = {"technews": "Tech News", "UkraineWarVideoReport": "Ukrain War Report"}

    matching_articles = []
    for subreddit in subreddit_mapping.keys():
        subreddit = reddit.subreddit(subreddit)
        for submission in subreddit.new(limit=100):
            if search_query.lower() in submission.title.lower():
                matching_articles.append(
                    {"title": submission.title, "id": submission.id, "category":subreddit_mapping[submission.subreddit.display_name],
                     "score": submission.score, "url": submission.url, "author": submission.author}
                )
    return matching_articles


if __name__ == "__main__":
    app.run(debug=True)
