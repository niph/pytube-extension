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
musicLibary = "/media/niph/data1/music"


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
        f = open(list,"r")
        rowcount = f.readlines()
        data = [line.strip() for line in open(list, 'r')]
        while n <= rowcount:
            if len(data) >= 1:
                try:
                    yt = YouTube()
                    #download all videos contained in textfile
                    for item in data:
                        yt.url = data[n]#item

                        #check if file already exists
                        fe = "tmp/" + yt.filename + ".mp4"
                        if os.path.exists(fe) == False:
                            #assume there is atleast one mp4 file with 360p resolution
                            video = yt.get('mp4', '360p')
                            print "\rdownloading: " + yt.filename
                            #download into tmp folder
                            video.download('tmp/')
                            n += 1
                        else:
                            print "File [" + yt.filename + "] already exists, skipping dowload"
                            print n
                            n += 1

                except:
                    print "\ncould not download video: " + yt.filename
                    print "\rTry to download next video in list if theres any"
                    print n
                    n += 2
                    e += 1

            else:
                print "tracklist.txt seems to be empty"
                os._exit(1)

    #print "\nDownloaded " + str((n - e)) + " videos of a total of " + str(n) + "\n" + str(e) + " errors occured"

    except:
        print "Im sorry there occured an unhandeld exception."

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
        print "musicLibary does not exist - pleace set correct path"
        os._exit(0)

    #delete mp4
    cmd = "rm *.mp4"
    print cmd


def getPlaylist():
    pURL = raw_input("\n\nPlease enter playlist uid (e.g. PL81676A3E85BD3833): ")
    #extract playlist id
    #if find(pURL,"&feature") == 1:
    #	pUID = pURL[pURL.index("&list=")+6:pURL.index("&feature=")]
    #else:
    #	pUID = pURL[pURL.index("&list=")+6:]

    #get json string from playlist
    pAPI = "http://gdata.youtube.com/feeds/api/playlists/" + str(pURL) + "/?v=2&alt=json&feature=plcp"
    data = urllib2.urlopen(pAPI).read()

    j = json.loads(data)
    p = open("playlist.txt", "w")

    #get url's of all videos
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


welcome()
		



































