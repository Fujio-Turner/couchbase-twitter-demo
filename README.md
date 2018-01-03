# couchbase-twitter-demo
Putting Tweets into Couchbase via Sync Gateway

<img src="img/twitter-python-sync_gateway-couchbase.png">

# Get Your Twitter API Key and Token.

1. Open a web browser and go to https://apps.twitter.com/app/new

2. Sign in with your normal Twitter username and password if you are not already signed in.

3. Enter a name, description, and temporary website (e.g. http://coming-soon.com)
Read and accept the terms and conditions – note principally that you agree not to distribute any of the raw tweet data and to delete tweets from your collection if they should be deleted from Twitter in the future.

4a. Click "Create your Twitter application"
Click on the "API Keys" tab 

4b. Then click "Create my access token" Wait a minute or two and press your browser's refresh button (or ctrl+r / cmd+r)
You should now see new fields labeled "Access token" and "Access token secret" at the bottom of the page.
You now have a Twitter application that can act on behalf of your Twitter user to read data from Twitter.

# Download Python Twitter Library
http://www.tweepy.org/    source: https://github.com/tweepy/tweepy

This is a simple demo for getting tweets into Couchbase via Sync Gateway

5. Download the above tweepy repo to your local machine from (ABOVE) link.

6. Download and copy the sg-streaming.py (ABOVE) into the "examples" folder in tweepy download.

7. Insert your twitter keys & tokens in the sg-streaming.py that was created in step(4)
```
-# Go to http://apps.twitter.com and create an app.
-# The consumer key and secret will be generated for you after
consumer_key="..."
consumer_secret="..."

-# After the step above, you will be redirected to your app's page.
-# Create an access token under the the "Your access token" section
access_token="..."
access_token_secret="..."
```

# Couchbase Server & Sync Gateway

8.a Create a Bucket in Couchbase (OPTIONAL create the bucket with FULL EJECTION) 

8.b Create a user in Couchbase with password so sync gateway can access the bucket (FULL ADMIN user is the faster and easiest).


9.a Download (ABOVE) Sync Gateway config file "basic-couchbase-bucket-twitter.json"

9.b Update the config file with the bucket name , username and password. Then go to the folder that you downloaded Sync Gateway and start it with the config (BELOW).

```
# bin/sync_gateway /path/to/config/file/basic-couchbase-bucket-twitter.json
```


10a. Currently the twitter feed is filtered by "basketball" related tweets. You might want to change it to something more interesting to you. To change it just open sg-streaming.py and on the last line in the file and change the filter string (BELOW).
```
stream.filter(track=['basketball'],async=True)
```


10b. Start the python script to get tweets and insert them into Sync Gateway
```
# ./sg-streaming.py
```


# FTS
Below is an example of a Full Text Search Index on the tweets in Couchbase.
<img src="img/fts-twitter-cb-sync-gateway.png">



# Requirements

- Python 2.7.x
