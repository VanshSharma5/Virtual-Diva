from ai import Ai
from buddy import Buddy
from threading import Thread
import pygame as pg

class Model(Ai, Buddy):
    def __init__(self, model : str = 'llama3.2', role : str = 'user', streamflag : bool = True, rate : int = 175, volume : float = 0.66, voice : int = 1, model_id : int = 1, sheet_id : int = 1 ):
        Ai.__init__(self, model=model, role=role, streamflag=streamflag, rate=rate, volume=volume, voice=voice)
        Buddy.__init__(self, model_id=model_id, sheet_id=sheet_id, )
        #self.istalking :bool = False


    def talk(self, content, buffersize : int = 8, printflag : bool = False):
        print("before ask")
        self.ask(content="say 3 magic words")
        print("after ask")
        #Thread(target=self.talk, args=('talk', 200, 15)).start()
        #print("after thtead ")
        #super().say(buffersize=buffersize, printflag=printflag)


def main():
    model = Model()
    model.set_model(0, 90, 200, 400, 0.98)
    while model.alive:
        for action in model.user_actions.get():
            print(action)
            if action.type == pg.QUIT:
                model.kill()
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            model.animate("fun")
            #t2 = Thread(target=model.animate, args=('talk', 200, 15))
            #t2.start()
            #model.say("3 magic Words", buffersize=8)

if __name__ == "__main__":
    main()