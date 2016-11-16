from flask import Flask, flash, g, redirect, request, session, render_template, url_for
from flask_oauth import OAuth

import os
import twitterconfig

from twitterhelper import TwitterAPI

DEBUG=True

app=Flask(__name__)
app.debug=DEBUG
app.secret_key=os.urandom(24)
oauth=OAuth()

t_api=TwitterAPI()

twitter=oauth.remote_app('twitter',
	base_url = 'https://api.twitter.com/1.1/',
	request_token_url='https://api.twitter.com/oauth/request_token',
	access_token_url='https://api.twitter.com/oauth/access_token',
	authorize_url='https://api.twitter.com/oauth/authenticate',
	consumer_key=twitterconfig.consumer_key,
	consumer_secret=twitterconfig.consumer_secret
)

@twitter.tokengetter
def get_twitter_token(token=None):
	return session.get('twitter_token')

@app.route('/')
def home():
	access_token=session.get('access_token')
	if access_token is None:
		return render_template('index.html')
		return redirect(url_for('login'))

	access_token=access_token[0]

	try:
		tweet_text=None
		resp=twitter.post('statuses/update.json', data={'status': tweet_text})
	except Exception as e:
		print e
		tweet_text=None
	return render_template('tweet.html', tweet_text=tweet_text)

@app.route('/tweet', methods=['POST'])
def send_tweet():
	try:
		tweet_text=request.form.get('tweet')
		t_api.tweet(tweet_text)
		flash('Your tweet has been sent!')
	except Exception as e:
		print e
	return render_template('tweet.html')

@app.route('/login')
def login():
	return twitter.authorize(callback=url_for('oauth_authorized',
		next=request.args.get('next') or request.referrer or None))

@app.route('/logout')
def logout():
	session.pop('screen_name', None)
	flash('You were signed out.')
	return redirect(request.referrer or url_for('index'))

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
	next_url=request.args.get('next') or url_for('send_tweet')

	if resp is None:
		flash(u'You denied the request to sign in')
		return redirect(next_url)

	access_token=resp['oauth_token']
	session['access_token']=access_token
	session['screen_name']=resp['screen_name']

	session['twitter_token']=(
		resp['oauth_token'],
		resp['oauth_token_secret']
		)

	return redirect(url_for('home'))

if __name__=='__main__':
	app.run(port=7091)