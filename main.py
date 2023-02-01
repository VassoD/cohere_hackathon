from flask import Flask, render_template, request
import praw
# from datetime import datetime
from flask import jsonify
from threading import Thread

app = Flask(__name__)

import cohere
from cohere.classify import Example


co = cohere.Client('q0NrIwmw78Qt3IegCK71Hrnp3JU131ilq3UWtcpP') # This is your trial API key)
examples=[Example("Nationwide ban on TikTok inches closer to reality", "negative"), Example("Chinas 2022 smartphone shipments the lowest in 10 years - research firm", "negative"), Example("Bitwarden password vaults targeted in Google ads phishing attack", "negative"), Example("Smart ovens do really dumb stuff to check for Wi-Fi  Pinging search services in the US, China, Russia perhaps not ideal for privacy", "negative"), Example("Intels historic collapse erases $8 billion from market value  Reuters", "negative"), Example("Some auto insurers are refusing to cover certain Hyundai and Kia models", "negative"), Example("U.S. Department of Justice files lawsuit alleging Google is anticompetive", "negative"), Example("Mac Pro Enthusiasts Raise Concerns Over Upgrade Limitations of Apple Silicon", "negative"), Example("Dutch hacker steals data from virtually entire population of Austria", "negative"), Example("Microsoft set to face EU antitrust probe over video calls", "negative"), Example("Google to make changes to Android business terms in India after antitrust blow", "negative"), Example("Waymo lays off staff as Alphabet announces 12,000 job cuts", "negative"), Example("Microsoft announces $52.7 billion in Q2 revenue amid plans to layoff 10,000 workers  Engadget", "negative"), Example("Microsoft cloud outage hits users around the world", "negative"), Example("Internet Archive takes down upload of BBC’s Modi documentary", "negative"), Example("Amazon Workers Set for Unprecedented UK Strike on Wednesday", "negative"), Example("‘Robots are treated better’: Amazon warehouse workers stage first-ever strike in the UK", "negative"), Example("Riot Games: League of Legends Source Code and Anti-Cheat Stolen", "negative"), Example("Appliance makers sad that 50% of customers won’t connect smart appliances", "negative"), Example("I cried all night: Millions of Chinese lose access to World of Warcraft and other hit games  CNN Business", "negative"), Example("FBI accuses North Korean government hackers of stealing $100M in Harmony bridge theft", "negative"), Example("ClearSpace raises $29 million ahead of first debris removal mission", "neutral"), Example("Ford cuts price on Mustang Mach-E after Tesla trims prices", "neutral"), Example("LG says its in talks with Tesla to supply batteries from Arizona factory", "neutral"), Example("Microsoft, GitHub, and OpenAI ask court to throw out AI copyright lawsuit", "neutral"), Example("Apple expanding China’s website warnings for users in Hong Kong", "neutral"), Example("Japan, Netherlands to join U.S. in restricting chip equipment exports to China-Bloomberg", "neutral"), Example("Metal robot can melt its way out of tight spaces to escape", "neutral"), Example("Under increasing pressure in the US, ByteDance and TikTok shift their strategy for dealing with officials by going on the offense and speaking out publicly", "neutral"), Example("After inking its OpenAI deal, Shutterstock rolls out a generative AI toolkit to create images based on text prompts", "neutral"), Example("AstroForge Plans First Private Asteroid Mining Mission", "neutral"), Example("Acura will sell its EVs exclusively online starting in 2024  Engadget", "neutral"), Example("Recyclable mobile phone batteries a step closer with rust-busting invention", "positive"), Example("Zelda: A Link to the Past can now be compiled on Windows and Nintendo Switch", "positive"), Example("Scientists at Salesforce develop proteins with AI that can eat trash", "positive"), Example("Stanford introduces DetectGPT to help educators fight back against ChatGPT", "positive"), Example("An ALS patient set a record for communicating via a brain implant: 62 words per minute", "positive"), Example("Everybody is cheating: Why this teacher has adopted an open ChatGPT policy", "positive"), Example("Mercedes-Benz is the first to bring Level 3 automated driving to the US", "positive"), Example("OpenAI has hired an army of contractors to make basic coding obsolete", "positive"), Example("Canonical Announces General Availability of Ubuntu Pro, Free for Up to 5 PCs - 9to5Linux", "positive"), Example("ChatGPT bot passes US law school exam", "positive"), Example("U.S. says it hacked the hackers to bring down ransomware gang", "positive"), Example("With new funding, Atomic AI envisions RNA as the next frontier in drug discovery", "positive"), Example("With Nvidia Eye Contact, you’ll never look away from a camera again", "positive"), Example("US Marines Defeat DARPA Robot by Hiding Under a Cardboard Box", "positive"), Example("Researchers look a dinosaur in its remarkably preserved face", "positive"), Example("Crypto Infrastructure Firm Blockstream Raises $125M for Bitcoin Mining The company will use the funds to expand its bitcoin mining facilities amid strong demand for hosting.", "positive"), Example("Google CEO Sundar Pichai says he will take less pay this year as he joins JPMorgan’s Jamie Dimon and Apple’s Tim Cook in taking a compensation hit", "positive"), Example("Nvidia CEO says AI will need regulation, social norms", "positive")])


# timestamp = 1555555555
# date_time = datetime.fromtimestamp(timestamp)
# formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        search_query = request.form["search_query"]
        matching_articles = search_articles(search_query)
        total_articles = len(matching_articles)
        return render_template("home.html", articles=matching_articles, total_articles=total_articles)
    return render_template("home.html")

def search_articles(search_query):
    reddit = praw.Reddit(client_id="f1ecYWIeukFQEEOPHjdtkA",
                         client_secret="KIbEIfhjYb1tfczA9sj3qlV95Fe7WA",
                         user_agent="praw_scraper_1.0")
    # subreddit_mapping = {"technews": "Tech News", "UkraineWarVideoReport": "Ukrain War Report","worldnews": "World News","ClimateNews": "Climate News","Coronavirus": "Covid 19 News","business": "Business News","Health": "Health News"}
    subreddit_mapping = {"technews": "Tech News"}
    matching_articles = []
    for subreddit in subreddit_mapping.keys():
        subreddit = reddit.subreddit(subreddit)
        for submission in subreddit.new(limit=100):
            if search_query.lower() in submission.title.lower():
                #check the sentiment of this article
                inputs=[submission.title]
                response = co.classify(
                    model='large',
                    inputs=inputs,
                    examples=examples)
                #pulls out the dictionary of classifications
                class = response.classifications['classifications']
                #find the first output
                class1 = class[0]
                
                #pulls the sentiment from the dictionary of first output 
                sentiment = class1['prediction']
                
                #if this sentiment is what the user has typed in the search query
                
                if sentiment in search_query.lower():
                    
                    #then add the matching article 
                    
                    matching_articles.append(
                        {"title": submission.title, "id": submission.id, "category":subreddit_mapping[submission.subreddit.display_name],
                         "score": submission.score, "url": submission.url, "author": submission.author}
                    )
    return matching_articles


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
