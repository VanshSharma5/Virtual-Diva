from audio import Audio
from writer import Writer
from ollama import chat
#from time import sleep
import pygame as pg

class Ai(Audio, Writer):
    def __init__(self, model : str = 'llama3.2', role : str = 'user', streamflag : bool = True, rate : int = 175, volume : float = 0.66, voice : int = 1): 
        Audio.__init__(self, rate=rate, volume=volume, voice=voice)
        Writer.__init__(self)
        self.model : str = model
        self.role : str = role
        self.streamflag : bool = streamflag
        self.stream = None
        self.content : str 
        self.counter = 1
        self.buffer : list[str] = []
        self.block : list[str] = []

    def ask(self, content : str ):
        self.content = content
        self.stream = chat(
            model = self.model ,
            messages = [ {
                'role': self.role,
                'content': self.content,
            } ],
            stream=self.streamflag,
        )

    def say(self, speechflag : bool = True, printflag : bool = False, buffersize = 1):
        for chunk in self.stream:
            print(chunk['message']['content'], end = '', flush = True) if printflag else None
            #print(chunk, flush = True)
            self.buffer.append(chunk['message']['content'])
            if self.counter <= buffersize and chunk['message']['content'] != '' and chunk['message']['content'] != '\n':
                self.counter += 1
            else:
                self.counter = 1
                super().text2speech(self.buffer, runAndWaitflag=True) if speechflag else None
                self.block.append(''.join(self.buffer))
                self.buffer.clear()
        return ''.join(self.block)

    def texts(self, content : str | None, In : str, *, app : str, parameter : str):
        if In == 'file':
            super().write_in_file( 'my_ai_response.txt', content=content)
        elif In == 'app':
            super().open_app(app = app, parameter=parameter)
            #print(self.block)
            super().type(content)



'''def main():
    model1 = Ai()
    model1.set_model(0, 90, 200, 400, 0.98)
    model1.ask("say 3 magic words")
    model1.say(printflag=True)
    while model1.alive:
        for action in model1.user_actions.get():    
            if action.type == pg.QUIT:
                model1.kill()

        keys = pg.key.get_pressed()
        
        if keys[pg.K_UP]:
            model1.animate('fun', loop = 3)
        elif keys[pg.K_RIGHT]:
            model1.animate('anger', loop = 2)
        elif keys[pg.K_LEFT]:
            model1.animate('emberass', loop = 3)
        elif keys[pg.K_DOWN]:
            model1.animate('talk', loop = 2, animation_time=250)
        else:
            model1.animate()


if __name__ == "__main__":
    main()

'''
if __name__ == '__main__':
    ai = Ai()
    ai.set_property({'volume' : 1})
    ai.ask("say 2 line poem",)
    response = ai.say(printflag=True, speechflag = True, buffersize=8)
    ai.texts(content = response, In = 'app',app = 'notepad', parameter = 'aitext.txt')