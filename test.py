from ai import Ai
from buddy import Buddy
import pygame as pg
import threading as td

def test1():
    model1 = Buddy()
    ai = Ai()

    model1.set_model(0, 90, 200, 400, 0.98)
    while model1.alive:
        for action in model1.user_actions.get():    
            if action.type == pg.QUIT:
                model1.kill()

        keys = pg.key.get_pressed()
        
        if keys[pg.K_UP]:
            model1.animate('fun', loop = 3)
        elif keys[pg.K_RIGHT]:
            ai.ask("3 magic Words")
            t2 = td.Thread(target=model1.animate, args=('talk', 200, 25))
            t2.start()
            ai.say("3 magic Words", buffersize=8)
            #t1.daemon = True
            #t2.daemon = True
        elif keys[pg.K_LEFT]:
            model1.animate('emberass', loop = 3)
        elif keys[pg.K_DOWN]:
            model1.animate('anger', loop = 2, animation_time=200)
        else:
            model1.animate()

    t2.join()

if __name__ == "__main__":
    test1()