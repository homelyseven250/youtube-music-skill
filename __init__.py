from mycroft import MycroftSkill, intent_handler

from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel


from mycroft.util.parse import match_one

import urllib.request
from bs4 import BeautifulSoup
from pytube import YouTube
import pydub

class YoutubeMusic(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('play.intent')
    def CPS_match_query_phrase(self, phrase):
        """ This method responds wether the skill can play the input phrase.
            The method is invoked by the PlayBackControlSkill.
            Returns: tuple (matched phrase(str),
                            match level(CPSMatchLevel),
                            optional data(dict))
                     or None if no match was found.
        """
        # Get match and confidence


        textToSearch = f'{phrase} clean'
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        names = []
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            urls.append('https://www.youtube.com' + vid['href'])
        
        for title in soup.findAll(attrs={'class':'video-title'}):
            names.append(title.text)
        
        track_dict = {}

        for x in len(urls):
            track_dict[names[x]] = urls[x]
        
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


def create_skill():
    return YoutubeMusic()

