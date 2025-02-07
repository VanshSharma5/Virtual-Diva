import pygame as pg
from win32api import GetSystemMetrics, RGB
from win32con import GWL_EXSTYLE, LWA_COLORKEY, SM_CXSCREEN, WS_EX_LAYERED, HWND_TOPMOST, SM_CYSCREEN, WS_EX_TOPMOST
from win32gui import SetWindowLong, SetLayeredWindowAttributes, GetWindowLong, SetWindowPos
from settings import *
from sys import exit
from typing import List, Tuple, Union

class SpriteSheet:
    def __init__(self, sheet_id: int,sprite_size: Tuple[int, int] = (85, 100), spacing: Tuple[int, int] = (0, 0), scale: Tuple[int, int]= None) -> None:
        """Initialize the spritesheet.

        Args:
            filepath (Path): Path to the spritesheet image file.
            sprite_size (Tuple[int, int]): Width and height of each sprite in the sheet.
            spacing (Tuple[int, int], optional): Spacing between each sprite (row spacing, column spacing). Defaults to (0, 0).
            scale (Tuple[int, int], optional): Rescale each sprite to the given size. Defaults to None.
        """
        self._sheet = pg.image.load(SHEET[sheet_id]).convert_alpha()
        self._sprite_size = sprite_size
        self._spacing = spacing
        self._scale = scale

    def get_sprite(self, loc: Tuple[int, int], colorkey: Union[pg.Color, int, None] = None) -> pg.Surface:
        """Load a specific sprite from the spritesheet.

        Args:
            loc (Tuple[int, int]): Location of the sprite in the sheet (row, column).
            colorkey (Union[pg.Color, int, None], optional): Color to be treated as transparent. Defaults to None.

        Returns:
            pg.Surface: The sprite image.
        """
        x = loc[1] * (self._sprite_size[0] + self._spacing[0])
        y = loc[0] * (self._sprite_size[1] + self._spacing[1])

        rect = pg.Rect(x, y, *self._sprite_size)
        image = pg.Surface(self._sprite_size, pg.SRCALPHA).convert_alpha()
        image.blit(self._sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)

        if self._scale:
            image = pg.transform.scale(image, self._scale)
        
        return image

    def get_sprites(self, locs: List[Tuple[int, int]], colorkey: Union[pg.Color, int, None] = None) -> List[pg.Surface]:
        """Load multiple sprites from the spritesheet.

        Args:
            locs (List[Tuple[int, int]]): List of locations of the sprites in the sheet (row, column).
            colorkey (Union[pg.Color, int, None], optional): Color to be treated as transparent. Defaults to None.

        Returns:
            List[pg.Surface]: List of sprite images.
        """
        return [self.get_sprite(loc, colorkey) for loc in locs]

class Expression(SpriteSheet):
    def __init__(self, sheet_id: int  = 1):
        super().__init__(sheet_id=sheet_id, sprite_size = (85, 100), spacing=(1, -3), scale = (80, 160) ) # 680x300: 8x3
        self.expressions = {
            'fun' : [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)],
            'anger' : [ (1, 0), (1, 6), (1, 0), (1, 6), (1, 0), (1, 6), (1, 2), (1, 0), (1, 2), (1, 3), (1, 2), (1, 3), (1, 2), (1, 3), (1, 2), (1, 3), (0, 5), (1, 5), (0, 5), (1, 5), (0, 5), (1, 5),],
            'emberass' : [(0, 1), (1, 1), (2, 1), (1, 6), (1, 7), (2, 5), (1, 4), (0, 1)],
            'talk' : [(1, 1), (1, 6), (1, 0), (1, 6), (1, 0), (1, 1), (1, 6), (1, 0), (1, 6), (1, 0)],

        }
        self.animations = {
            'fun' : []
        }
        self.create_animation()

    def add_expression(self, name : str, *expression_sequense ):
        '''
        expression_sequense = [(x0, y0), (x1, y1), ..............]
        '''        
        self.expressions[name] = expression_sequense
        self.create_animation(name)
    
    def create_animation(self, expression : str = None):
        if expression:
            self.animations[expression] = []
            self.animations[expression] = self.get_sprites(self.expressions[expression])
        else:
            for expression in self.expressions:
                self.create_animation(expression)
        
class Buddy(Expression):
    def __init__(self, model_id : int = 1, sheet_id : int = 1):
        pg.init()
        self.screen = pg.display.set_mode(WINDOWSIZE, pg.NOFRAME)
        Expression.__init__(self, sheet_id)
        self.x = 0
        self.y = 0
        self.width = 200
        self.height = 200
        self.scale = 1.0
        self.alive : bool = True
        self.face = self.get_sprite((2, 1))
        #self.old_time = pg.time.get_ticks()
        #self.animationflag : bool = True

        self.user_actions = pg.event
        

        self.screen_width = GetSystemMetrics(SM_CXSCREEN)
        self.screen_height = GetSystemMetrics(SM_CYSCREEN)

        hwnd = pg.display.get_wm_info()["window"]
        SetWindowLong(hwnd, GWL_EXSTYLE, GetWindowLong(hwnd, GWL_EXSTYLE) | WS_EX_LAYERED | WS_EX_TOPMOST)
        SetLayeredWindowAttributes(hwnd, RGB(*FUCHSICA), 0, LWA_COLORKEY)        
        SetWindowPos(hwnd, HWND_TOPMOST, self.screen_width - WIDTH - MARGIN, self.screen_height - HEIGHT, WIDTH, HEIGHT, 0)

        self.model = pg.image.load(MODEL[model_id]).convert_alpha()

    def set_model(self, x : int, y : int, width : int, height : int, scale : float = 1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale = scale
        self.model_width, self.model_height = self.model.get_size()

        self.model = pg.transform.scale(self.model, (self.model_width * scale , self.model_height * scale))

    def animate(self,expression : str = None , animation_time : int = 200, loop : int = 1):
        if expression:  
            for _ in range(loop):
                for animation in self.animations[expression]:
                    #new_time = pg.time.get_ticks()
                    pg.time.delay(animation_time)
                    self.draw()
                    self.draw(animation,215, 80)
                    pg.display.flip()
                    #self.old_time = new_time 
        else:
            self.draw()
            self.draw(self.face, 215, 90)
        
        pg.display.update()

    def draw(self, image = None, x = 0, y = 0):
        if image == None:
            self.screen.fill(FUCHSICA)  # Transparent background
            self.screen.blit(self.model, (self.x, self.y))

        else:
            self.screen.blit(image,(x, y))

    def update(self):
        pg.display.flip()
    
    def dead(self):
        self.alive = False

    def kill(self):
        pg.quit()
        exit(0)
    


def main():
    model1 = Buddy()
    model1.set_model(0, 90, 200, 400, 0.98)
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