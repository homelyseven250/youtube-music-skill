from __future__ import unicode_literals
import youtube_dl

from mycroft import MycroftSkill, intent_handler

from mycroft.skills.common_play_skill import *


from mycroft.util.parse import match_one

import urllib.request
from bs4 import BeautifulSoup





class YoutubeMusic(CommonPlaySkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    
    def CPS_match_query_phrase(self, phrase):
        """ This method responds wether the skill can play the input phrase.
            The method is invoked by the PlayBackControlSkill.
            Returns: tuple (matched phrase(str),
                            match level(CPSMatchLevel),
                            optional data(dict))
                     or None if no match was found.
        """
        
        urls = []
        titles = []
        track_dict = {}
        self.log.info(phrase)
        response = urllib.request.urlopen('https://www.youtube.com/results?search_query='+phrase.replace(" ", "%20"))

        soup = BeautifulSoup(response)    
        divs = soup.find_all("div", { "class" : "yt-lockup-content"})


        for i in divs:
            href= i.find('a', href=True)
            urls.append("https://www.youtube.com"+href['href'])
            titles.append(href.text)

        for x in range(0, len(urls)):
            track_dict[titles[x]] = urls[x]
        
        # Get match and confidence
        match, confidence = match_one(phrase, track_dict)
        # If the confidence is high enough return a match
        if confidence > 0.5:
            return (match, CPSMatchLevel.TITLE, {"track": match})
        # Otherwise return None
        else:
            return None

    def CPS_start(self, phrase, data):
        """ Starts playback.
            Called by the playback control skill to start playback if the
            skill is selected (has the best match level)
        """
        self.log.info(data)
        url = data['track']
        self.audioservice.play(url)


        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg)


        def my_hook(d):
            if d['status'] == 'finished':
                print('Done downloading, now converting ...')


        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=ZbZSe6N_BXs'])


def create_skill():
    return YoutubeMusic()

