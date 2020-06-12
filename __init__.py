from mycroft import MycroftSkill, intent_file_handler


class YoutubeMusic(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('music.youtube.intent')
    def handle_music_youtube(self, message):
        self.speak_dialog('music.youtube')


def create_skill():
    return YoutubeMusic()

