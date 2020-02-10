from flask import Flask, render_template, redirect
import requests
from textblob import TextBlob


app = Flask(__name__)


@app.route("/")
def home():

    return redirect("/random_quote", code=302)

@app.route("/random_quote/")
def random_quote():

    quote = "Welcome! Click below to generate a quote and get an analysis!"

    return render_template('index.html', quote=quote)


@app.route("/generate_quote/", methods=['POST'])
# Function used to generate a quote
def generate_quote():

    output = requests.get("https://quote-garden.herokuapp.com/quotes/random").json()
    quote = output['quoteText']
    author = output['quoteAuthor']

    # perform sentiment analysis on the quote
    sentiment = sentiment_analysis(quote)

    if sentiment == "very positive":
        analysis = 'Yay! Our sentiment analysis detected your quote to be very positive! You must have great ' \
                   'luck today. Feel free to generate another quote!'

    elif sentiment == "positive":
        analysis = 'Yay! Our sentiment analysis detected your quote to be quite positive! You must have great ' \
                   'luck today. Feel free to generate another quote!'
    else:
        analysis = "Our sentiment analysis detected your quote to be neutral. Feel free to generate another quote!"

    return render_template('index.html', quote=quote, author=author, analysis=analysis)


# Function used to determine whether quote is positive, neutral, or negative
def sentiment_analysis(quote):
    obj = TextBlob(quote)
    sentiment = obj.sentiment.polarity

    if sentiment == 0:
        return "neutral"
    elif sentiment > 0:
        return "positive"
    elif sentiment > 0.5:
        return "very positive"
    else:
        return "negative"


if __name__ == "__main__":
    app.run(debug=True)
