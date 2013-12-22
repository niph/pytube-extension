import sys
import os
import json
import urllib2
from pytube import YouTube
from string import find, replace

'''
Author: niph.sp
Email:
Description: Extension of Nic Ficanos pytube youtube downloader (https://github.com/ablanco/python-youtube-download)

Usage:

	1) copy single video urls from youtube into tracklist.txt
		empty rows may cause problems
	2) enter link of playlist when you are prompted for it
		note: can only download public playlists
	3) convert downloaded mp4 files from tmp/ folder with ffmpeg to mp3
'''


#please set your default music directory
musicLibary = "/Users/niph/Desktop"


def welcome():
    print "\nHello User, what Im supposed to do?\n"
    print "\r\t1) Download videos from tracklist.txt"
    print "\r\t2) Download videos from YouTube playlist"
    print "\r\t3) Convert mp4's from tmp/ folder"
    print "\r\t4) return 0"

    selection = int(raw_input("\nNow it's your turn: [1,2,3,4]: "))
    if selection == 1:
        download("tracklist.txt")
    elif selection == 2:
        getPlaylist()
    elif selection == 3:
        convert()
    elif selection == 4:
        os._exit(1)
    else:
        print "\nSorry could not match your input to an option\n"
        welcome()


def download(list):
    #read url of videos to download
    try:
        n = 0
        e = 0
        f = open(list, "r")
        rowcount = len(f.readlines())
        print str(rowcount) + " links in list....starting\n"
        data = [line.strip() for line in open(list, 'r')]
        while n <= rowcount:
            if len(data) >= 1:
                try:
                    yt = YouTube()
                    #download all videos contained in textfile
                    for item in data:

                        yt.url = item

                        #check if file already exists
                        cwd = os.path.dirname(os.path.realpath(__file__))
                        tmp = os.path.join(cwd, "tmp/")
                        fe = tmp + yt.filename + ".mp4"
                        if os.path.exists(fe) == False:
                            #assume there is atleast one mp4 file with 360p resolution
                            video = yt.get('mp4', '360p')
                            print "\r" + str(n) + " [+] downloading: " + yt.filename
                            #download into tmp folder
                            video.download('tmp/')
                            n += 1
                        else:
                            print "File [" + yt.filename + "] already exists, skipping dowload"
                            n += 1

                except any, e:
                    print "\n" + str(n) + " [-] could not download video: " + yt.filename
                    print "\rTry to download next video in list if theres any\n"
                    print e
                    n += 1
                    e += 1

            else:
                print "Textfile seems to be empty"
                os._exit(1)

    #print "\nDownloaded " + str((n - e)) + " videos of a total of " + str(n) + "\n" + str(e) + " errors occured"

    except any, e:
        print "Im sorry there occured an unhandeld exception."
        print e

    selection = raw_input("\n\nConvert Downloaded videos to mp3?: [Yn]: ")
    if selection == "n":
        os._exit(1)
    else:
        convert()


def convert():
    print "***ATTENTION*** all .mp4 files will be deleted"
    c = raw_input("\n\nInput subdirectory: ")
    if int(len(c)) == 0:
        target = musicLibary
    else:
        target = os.path.join(musicLibary, c)
        if os.path.exists(target) == False:
            mkdir = "mkdir " + target
            os.system(mkdir)


            #check again if target exists may user didn't change musicLibaryPath
    if os.path.exists(target) == True:
        cwd = os.getcwd()
        tmp = os.path.join(cwd, "tmp")
        files = [f for f in os.listdir(tmp)]

        #convert to mp3
        for item in files:
            if find(item, ".mp4", 0, len(item)) != -1:
                mp4 = os.path.join(tmp, item)
                mp3 = os.path.join(target, replace(item, ".mp4", ".mp3"))
                cmd = "ffmpeg -i \"" + mp4 + "\" -vn -ar 44100 -ac 2 -ab 192k -f mp3 \"" + mp3 + "\""
                os.system(cmd)
    else:
        print "musicLibary does not exist - please set correct path"
        os._exit(0)

    #delete mp4
    cmd = "rm *.mp4"
    #os.system(cmd)


def getPlaylist():
    try:
        pURL = raw_input("\n\nPlease enter playlist uid (e.g. PLB746A93F14AAFF58): ")
        #extract playlist id
        #if find(pURL,"&feature") == 1:
        #	pUID = pURL[pURL.index("&list=")+6:pURL.index("&feature=")]
        #else:
        #	pUID = pURL[pURL.index("&list=")+6:]

        itemPerPlaylist = 49
        print "retrieving playlist information"
        #count() of all videos in playlist
        pAPI = "http://gdata.youtube.com/feeds/api/playlists/" + str(pURL) + "/?v=2&alt=json&feature=plcp&max-results=" + str(itemPerPlaylist)
        data = urllib2.urlopen(pAPI).read()
        jMax = json.loads(data)
        totalResults = jMax.get("feed", {}).get("openSearch$totalResults", {}).get("$t", {})
        print "found " + str(totalResults) + " videos..."
        p = open("playlist.txt", "w")

        #json string can contain a maximum of 50 videos
        #https://developers.google.com/youtube/2.0/developers_guide_protocol_api_query_parameters
        while (totalResults % itemPerPlaylist) > 0:

            #get the proper values for max-results and start-index
            if (totalResults - itemPerPlaylist) >= (totalResults % itemPerPlaylist) and totalResults != 50:
                index = totalResults - itemPerPlaylist
                itemPerPlaylist = 50
            elif (totalResults == 50):
                index = 1
                itemPerPlaylist = 50
            else:
                index = 1
                itemPerPlaylist = totalResults % itemPerPlaylist
            #DEBUG: print "index:" + str(index) + " totalResults:" + str(totalResults) + " itemPerPlaylist:" + str(itemPerPlaylist)

            #fetch JSON into dictionary
            pAPI = "http://gdata.youtube.com/feeds/api/playlists/" + str(pURL) + "/?v=2&alt=json&feature=plcp&max-results=" + str(itemPerPlaylist) + "&start-index=" + str(index)
            print index
            data = urllib2.urlopen(pAPI).read()
            j = json.loads(data)
            totalResults -= itemPerPlaylist
            #extract all URL's from dictionary
            mediagroup = j.get("feed", {}).get("entry", {})
            for item in mediagroup:
                group = item.get("media$group", {}).get("media$content", [])
                for item in group:
                    #convert extracted urls to pytube readable link
                    string = str(item.get("url")) + "\n"
                    if string.find("rtsp://") == -1:
                        vUID = string[string.index("/v/") + 3:string.index("?version=")]
                        vURL = "http://www.youtube.com/watch?v=" + vUID + "\n"
                        p.write(vURL)
                        

        p.close()
        download("playlist.txt")
    except urllib2.HTTPError, e:
        print "\nCould not get playlist. Please check if playlist is public"
        print e

welcome()