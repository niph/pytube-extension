pytube-extension
================

Author: niph.sp

Email: niph.dev@gmail.com

Description: Extension of Nic Ficanos pytube youtube downloader (https://github.com/ablanco/python-youtube-download). Converts downloaded mp4s with ffmpeg to mp3

Install: 
================

	1) clone Nic Ficanos repository and run setup.py
	2) open download.py and edit path to your music libary
	3) chmod u+x download.py
	4) python download.py

Usage:
================

	1) copy single video urls from youtube into tracklist.txt 
		empty rows may cause problems
	2) enter link of playlist when you are prompted for it
		note: can only download public playlists (still in alpha state)
	3) convert downloaded mp4 files from tmp/ folder with ffmpeg to mp3
