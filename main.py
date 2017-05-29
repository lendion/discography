#!/usr/bin/python
# -*- coding: utf-8 -*-

'''crawser used to get discography info of the internet'''

import requests
import os
import re
import click
import discogs_client
sorten = {}

@click.command()
@click.argument("path")
def main(path):
	i=0
	if not os.path.exists(path):
		print "invalid path"
		return
	dirs = os.walk(path, followlinks=False)
	for dir in dirs:
		for song in dir[2]:
			print song
			if song.endswith(".mp3"):
				song_name = symplafy(song)
				artist = disearch(song_name)
				if not artist in sorten.keys():
					sorten[artist] = []
				sorten[artist].append(os.path.join(dir[0], song))
				print song_name + " : " + artist
				print i
				i=i+1
	print "done with this 1"
	for folder in sorten:
		print folder
		if not os.path.exists(os.path.join(path, folder)):
			os.makedirs(os.path.join(path, folder))
		print "folder created!"
		for song_with_path in sorten[folder]:
			os.rename(song_with_path, os.path.join(path, folder, song_with_path.split("/")[-1]))
	print "done!"
def disearch(query):
	d = discogs_client.Client('ExampleApplication/0.1', user_token="uieEzItIYiInEuCChonMjAmdkKeNYYjXOGksorpF")
	results = d.search(query, type='release')
	results.pages
	try:
		artist = results[0].artists[0]
		return artist.name

	except:
		return "not found"

def symplafy(name): #remove any text within [] or () in song name
#	if "(" in name and ")" in name:
#		re.sub('\([^>]+\)', '', name)
#	if "[" in name and "]" in name:
#		re.sub('\[[^>]+\]', '', name)
#	not any better ##########################################
	try:
		name = name.split("-")[1]
	except:
		pass
	name = name.replace(".mp3", "")
	if name.startswith(" "):
		name = name[1:]
	if name.endswith(" "):
		name = name[:-1]
	return name

if __name__ == "__main__":
	if raw_input("are the song names are correct and symple [y/n]: ").lower() == "y":
		main()