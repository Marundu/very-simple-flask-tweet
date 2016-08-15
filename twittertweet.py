from flask import Flask, render_template, request
from twitterhelper import TwitterAPI

app=Flask(__name__)

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
	except Exception as e:
		print e
		#tweet_text=None
	return home()#render_template('tweet.html', tweet_text=tweet_text)

if __name__=='__main__':
	app.run(debug=True, port=7090)