from mycroft import MycroftSkill, intent_handler

from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel

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
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            urls.append('https://www.youtube.com' + vid['href'])
        endurl=urls[0]

        yt = YouTube(endurl)
        #download opus stream and convert to mp3
        yt.streams.filter(audio_codec="opus").first().download(filename=str(vid['href']))
        pydub.AudioSegment.from_file("./"+str(vid['href'])+".webm").export("./"+str(vid['href'])+".mp3", format="mp3")   

        
        #return song url
       
        return (phrase, CPSMatchLevel.TITLE, {"track": endurl})

    def CPS_start(self, phrase, data):
        """ Starts playback.
            Called by the playback control skill to start playback if the
            skill is selected (has the best match level)
        """
        url = data['track']
        self.audioservice.play(url)


def create_skill():
    return YoutubeMusic()

