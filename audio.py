import pyttsx3

class Audio:
    def __init__(self, rate : int = 175, volume : float = 0.66, voice : int = 1):
        self.engine = pyttsx3.init()
        self.rate = rate
        self.volume = volume
        self.voice = voice
        self.engine.setProperty('volume', volume)        # setting up volume level  between 0 and 1
        self.engine.setProperty('rate', rate)     # setting up new voice rate
        self.voices = self.engine.getProperty('voices')       # getting details of current voice
        self.engine.setProperty('voice', self.voices[self.voice].id)   # changing index, changes voices. 1 for female 0 for male
    
    def set_property(self, properties : dict ):
        try :
            for property, value in properties.items():
                self.engine.setProperty(property, self.voices[value]) if property == 'voice' else self.engine.setProperty(property, value)
        except Exception as e:
            print("The Invalid Property is given.")

    def text2speech(self, context : list[str], runAndWaitflag : bool = False):
        if not len(context) > 0 :
            self.engine.say("It seems,There Is Nothing to Say.")
            self.engine.runAndWait()

        #for line in context :
        self.engine.say(''.join(context))
        self.engine.runAndWait() if runAndWaitflag else None