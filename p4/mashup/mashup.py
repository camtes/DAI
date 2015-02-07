## -*- coding: utf-8 -*-
#
# Mashup
# Práctica 4 - DAI - Carlos Campos Fuentes
import web
from web.contrib.template import render_mako
import tweepy
from bson import json_util
import json

# Twitter
consumer_key = 'fj5732PSXLwStsBbs8XCyBndd'
consumer_secret = 'GRJKgyrDdSKi5OAj7ceke1m4xHS83GX6Wk2rHaac4zJVwFEIvo'
access_token = '14339674-qEeB1yzpA3QSWY16ApdVsxLP2ghooyLyHZK6vCbNk'
access_token_secret = 'PussjjvA6vv0DPDeN5WpVhnVFn2tJr3SDpfQKQE39aasL'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

web.config.debug = False

urls = ( '/', 'index',
         '/data', 'data')

#Plantillas
plantillas = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )
app = web.application(urls, locals())

class index:
    def GET(self):
        return plantillas.index()

class data:
    def GET(self):
        geo = web.input().geo
        tweets = tweepy.Cursor(api.search, geocode=geo).items(10)
        resp = {}
        cont = 0

        for tweet in tweets:
            resp[cont] = {'name': tweet.user.screen_name, 'tweet': tweet.text, 'date': tweet.created_at.strftime("%d-%m-%Y %H:%M"),
                        'coordinates': tweet.coordinates.get('coordinates')}
            cont += 1
        web.header('Content-Type', 'application/json')
        return json.dumps(resp)

if __name__ == "__main__":
    app.run()
