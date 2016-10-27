from flask import Flask, flash, render_template, request
from twitterhelper import TwitterAPI
import os

app=Flask(__name__)
SECRET_KEY=os.urandom(24)

app.secret_key=SECRET_KEY

twitter=TwitterAPI()

@app.route('/')
def home():
	try:
		tweet_text=None
	except Exception as e:
		print e
		tweet_text=None
	return render_template('tweet.html', tweet_text=tweet_text)

@app.route('/tweet', methods=['POST'])
def send_tweet():
	try:
		tweet_text=request.form.get('tweet')
		twitter.tweet(tweet_text)
		flash('Your tweet has been sent!')
	except Exception as e:
		print e
	return home()

if __name__=='__main__':
	app.run(debug=True, port=7090)