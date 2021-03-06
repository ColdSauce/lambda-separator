#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import os
from os import system, remove
import twilio.twiml
import soundcloud
import Queue

from flask import Flask, request
app = Flask(__name__)

queue_of_eternal_light = Queue.Queue()
SOUND_CLOUD_CLIENT_ID = os.environ.get("CLIENT_ID")
SOUND_CLOUD_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USERNAME = os.environ.get("SOUNDCLOUD_USER_NAME")
PASSWORD = os.environ.get("SOUNDCLOUD_PASSWORD")

client = soundcloud.Client(client_id = SOUND_CLOUD_CLIENT_ID,
                           client_secret = SOUND_CLOUD_CLIENT_SECRET,
                           username= USERNAME,
                           password=PASSWORD)

def enqueue_song(songName):
	global queue_of_eternal_light
	queue_of_eternal_light.put(songName)
	
def play_song(songName):
	tracks = client.get('/tracks',charset="utf-8",q=songName )
	stream_url = client.get(tracks[0].stream_url, allow_redirects=False)
	urllib.urlretrieve(stream_url.location, "tmp/song.mp3")
	system("mpg321 tmp/song.mp3 &")

@app.route("/playSound")
def playSound():
	return skip();
	

@app.route("/", methods=['POST'])
def twilioIndex():
	resp = twilio.twiml.Response()
	songName = str(request.form.get('Body'))
	if songName == "skip":
		skip()
	enqueue_song(songName)
	

@app.route("/skip")
def skip():
	global queue_of_eternal_light
	system("pkill mpg321")
	song_gotten = ""
	if not queue_of_eternal_light.empty():
		song_gotten = queue_of_eternal_light.get()
		play_song(queue_of_eternal_light.get())
	return "Now playing:" + str(song_gotten) + "\nIn the queue:" + str(queue_of_eternal_light)

@app.route("/song/", methods=['POST'])
def index():
	#enqueue_song(songName)
        content = request.json
	return str(content)

if __name__ == "__main__":
	app.run('0.0.0.0', port = 7573, debug=True)
	system("python player.py")

