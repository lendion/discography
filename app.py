#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import click
import discogs_client

'''crawler used to get discography info of the internet'''

sorted_songs = {}


@click.command()
@click.argument("path")
def main(path):
	i = 0
	if not os.path.exists(path):
		print "invalid path"
		return
	dirs = os.walk(path, followlinks=False)
	for DIR in dirs:
		for song in DIR[2]:
			print song
			if song.endswith(".mp3"):
				song_name = symplafy(song)
				artist = disearch(song_name)
				if artist not in sorted_songs.keys():
					sorted_songs[artist] = []
				sorted_songs[artist].append(os.path.join(DIR[0], song))
				print song_name + " : " + artist
				print i
				i += 1
	print "done with this 1"
	for folder in sorted_songs:
		print folder
		if not os.path.exists(os.path.join(path, folder)):
			os.makedirs(os.path.join(path, folder))
		print "folder created!"
		for song_with_path in sorted_songs[folder]:
			os.rename(song_with_path, os.path.join(path, folder, song_with_path.split("/")[-1]))
	print "done!"


def disearch(query):
	d = discogs_client.Client('ExampleApplication/0.1', user_token="uieEzItIYiInEuCChonMjAmdkKeNYYjXOGksorpF")
	results = d.search(query, type='release')
	try:
		artist = results[0].artists[0]
		return artist.name

	except IndexError:
		return "not found"


def symplafy(name):  # remove any text within [] or () in song name
	if "-" in name:
		name = name.split("-")[1]
	name = name.replace(".mp3", "")
	if name.startswith(" "):
		name = name[1:]
	if name.endswith(" "):
		name = name[:-1]
	return name

if __name__ == "__main__":
	if raw_input("are the song names are correct and simple [y/n]: ").lower() == "y":
		main()
