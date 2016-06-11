#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pygame
import random
import weakref
from GIFImage import GIFImage
from math import ceil, exp

# mouse ids
LEFT_BUTTON = 1
MIDDLE_BUTTON = 2
RIGHT_BUTTON = 3
SCROLL_UP = 4
SCROLL_DOWN = 5

# parameters
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
PADDING = 20
FRAMES_PER_SECOND = 60
NUM_DICE_SIDES = 6 
DICE_WIDTH = 128
DICE_HEIGHT = 128

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (130, 130, 130)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)

DICE_ARRAY = [[0, 0, DICE_WIDTH, DICE_HEIGHT],
              [DICE_WIDTH, 0, DICE_WIDTH, DICE_HEIGHT],
              [2*DICE_WIDTH, 0, DICE_WIDTH, DICE_HEIGHT],
              [0, DICE_HEIGHT, DICE_WIDTH, DICE_HEIGHT],
              [DICE_WIDTH, DICE_HEIGHT, DICE_WIDTH, DICE_HEIGHT],
              [2*DICE_WIDTH, DICE_HEIGHT, DICE_WIDTH, DICE_HEIGHT]]
              
FIBONACCI_ARRAY = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

POSITIONS = [['Anal sex', 'gifs/anal.gif'],
             ['Missionary', 'gifs/missionary.gif'],
             ['69', 'gifs/69.gif'],
             ['Spooning', 'gifs/spooning.gif'],
             ['Doggystyle', 'gifs/doggystyle.gif'],
             ['Cowgirl', 'gifs/cowgirl.gif']]

class Text(pygame.sprite.DirtySprite):

    def __init__(self, text, size, color, background, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.DirtySprite.__init__(self)

        # create a text surface
        antialias = 1
        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, antialias, color)  
        self.W = self.textSurf.get_width()
        self.H = self.textSurf.get_height()

        # create an ordinary surface and add text surf
        self.image = pygame.Surface((self.W, self.H))
        self.image.fill(background)
        self.image.blit(self.textSurf, (0, 0))

        # set pos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.dirty = 1

        
class Image(pygame.sprite.DirtySprite):

    def __init__(self, path, x, y, w, h):
        # Call the parent class (Sprite) constructor
        pygame.sprite.DirtySprite.__init__(self)

        # create an image surface
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(self.image, (w, h))

        # set pos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.dirty = 1
        
class Popup(pygame.sprite.DirtySprite):
    
    def __init__(self, w, h, parent):
        # Call the parent class (Sprite) constructor
        pygame.sprite.DirtySprite.__init__(self)
        
        # store ref to parent object
        self.parent = weakref.ref(parent)    # <= garbage-collector safe!
        
        # create a popup image surface
        self.width = w
        self.height = h
        self.image = pygame.Surface((w, h))
        
        # set popup status
        self.visible = 0
    
    def set_gif(self):
        parent = self.parent()
        sextype = POSITIONS[parent.dice.current_num-1]
        self.text = Text(sextype[0], 36, RED, WHITE, 0, 0)
        self.gif = GIFImage(sextype[1])
        
        # set pos
        x = parent.screen.get_width()/2 - self.width/2
        y = parent.screen.get_height()/2 - self.height/2
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # create a gif image surface
        self.image.fill(WHITE)
        self.gif_surf = pygame.Surface((self.gif.get_width(), 
                                        self.gif.get_height()))
        
    def __update_gif(self):
        self.gif.render(self.gif_surf, (0,0))
        self.image.blit(self.text.image, (0,0))
        PADDING = 10
        scaled_img = pygame.transform.scale(self.gif_surf, (self.width - 2*PADDING, self.height-self.text.H-2*PADDING))
        self.image.blit(scaled_img, (PADDING, self.text.H+PADDING))
    
    def is_showing(self):
        if self.visible == 1:
            return True
        return False
    
    def show(self):
        self.visible = 1
        self.dirty = 1
    
    def close(self):
        self.visible = 0
        self.dirty = 1
    
    def update(self):
        self.dirty = 0
        if self.visible == 1:
            self.__update_gif()
            self.dirty = 1
  
  
class Button(pygame.sprite.DirtySprite):

    def __init__(self, x, y, w, h, parent):
        # Call the parent class (Sprite) constructor
        pygame.sprite.DirtySprite.__init__(self)
        
        # store ref to parent object
        self.parent = weakref.ref(parent)    # <= garbage-collector safe!

        # define button
        # note that buttonRect is not in global coordinates
        # but relative in image
        border_size = 5
        self.buttonRect = pygame.Rect(border_size,
                                      border_size,
                                      w-2*border_size,
                                      h-2*border_size)
        self.buttonColorUp = LIGHT_GRAY
        self.buttonColorDown = DARK_GRAY
        self.borderColor = WHITE
        
        # create an image surface
        self.image = pygame.Surface([w, h])
        
        # set pos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.__draw(self.buttonColorUp)
        
        # state
        self.pressed = False
    
    def __draw(self, color):
        self.image.fill(self.borderColor)
        self.image.fill(color, self.buttonRect)
        
        # add label text
        text = 'Throw dice'
        size = 24
        color = RED
        antialias = 1
        font = pygame.font.SysFont("Arial", size)
        textSurf = font.render(text, antialias, color)
        W = textSurf.get_width()
        H = textSurf.get_height()
        label_pos = (self.buttonRect.w/2 - W/2, self.buttonRect.h/2 - H/2)
        self.image.blit(textSurf, label_pos)
        
    def update(self):
        self.dirty = 1

    def on_press(self, func):
        x, y = pygame.mouse.get_pos()
        rect = self.rect
        if (rect.x <= x) and (x <= (rect.x+rect.w)) \
           and (rect.y <= y) and (y <= rect.y+rect.h) \
           and not self.pressed:
            self.pressed = True
            func()
            self.__draw(self.buttonColorDown)

    def on_release(self):
        self.pressed = False
        self.__draw(self.buttonColorUp)
            
class Dice(pygame.sprite.DirtySprite):
    
    def __init__(self, x, y, size, parent):
        # Call the parent class constructor
        pygame.sprite.DirtySprite.__init__(self)
        
        # store ref to parent object
        self.parent = weakref.ref(parent)    # <= garbage-collector safe!
        
        dice_path = "sides.jpg"
        self.img_orig = pygame.image.load(dice_path).convert()
        
        # set pos
        self.size = size
        self.rect = self.img_orig.get_rect()
        self.rect.topleft = (x, y)
        
        # initialize
        self.current_num = 1
        self.thrown = False
        self.frame_counter = 0
        self.num_counter = 0
        self.__set_random_number()

    def __set_random_number(self):
        self.current_num = self.__generate_outcome()
        rect = DICE_ARRAY[self.current_num-1]
        side_img = self.img_orig.subsurface(rect[0], rect[1], rect[2], rect[3])
        self.image = pygame.transform.scale(side_img, (self.size, self.size))

    def __generate_outcome(self):
        rng_num = random.random()
        outcome = int(ceil(NUM_DICE_SIDES * rng_num))
        return outcome
    
    def __update_dice(self):
        finished = False
        if (FIBONACCI_ARRAY[self.num_counter] == self.frame_counter):
            self.frame_counter = 0
            self.__set_random_number()
            if (self.num_counter == (len(FIBONACCI_ARRAY)-1)):
                self.__reset()
                finished = True
            else:
                self.num_counter += 1
        else:
            self.frame_counter += 1
        
        return finished

    def __reset(self):
        self.thrown = False
        self.num_counter = 0
        self.frame_counter = 0    

    def update(self):
        self.dirty = 1
        if self.thrown:
            finished = self.__update_dice()
            if (finished):
                self.parent().popup.set_gif()
                self.parent().popup.show()

    def throw_dice(self):
        self.thrown = True
        

class GameApp(object):
    
    def __init__(self):
        # initialize game
        pygame.init()
        pygame.font.init()
        logo = pygame.image.load('logo.jpg')
        pygame.display.set_icon(logo)
        pygame.display.set_caption('Sex dice')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH-PADDING,
                                               WINDOW_HEIGHT-PADDING))
        self.running = False

        # crate game label
        font_size = 48
        text = "SEX DICE"
        label_color = RED
        label_background = BLACK
        label_x = 50
        label_y = PADDING
        self.label = Text(text,
                          font_size,
                          label_color,
                          label_background,
                          label_x,
                          label_y)

        # create default image
        sex_path = "sex.jpg"
        sex_w = (WINDOW_WIDTH/2) - 2*PADDING
        sex_h = (WINDOW_HEIGHT/2) - 2*PADDING
        sex_x = WINDOW_WIDTH/2
        sex_y = PADDING
        self.sex_img = Image(sex_path,
                             sex_x,
                             sex_y,
                             sex_w,
                             sex_h)

        # create game button
        rect_w = WINDOW_WIDTH - 3*PADDING
        rect_h = WINDOW_HEIGHT/2 - 2*PADDING
        rect_x = PADDING
        rect_y = WINDOW_HEIGHT/2
        self.button = Button(rect_x,
                             rect_y,
                             rect_w,
                             rect_h,
                             self)

        # create dice
        dice_x = 90
        dice_y = 85
        dize_size = 128
        self.dice = Dice(dice_x,
                         dice_y,
                         dize_size,
                         self)
                    
        # create a gif popup
        popup_w = 400
        popup_h = 300
        self.popup = Popup(popup_w, popup_h, self)

        # define render group
        self.render_group = pygame.sprite.RenderUpdates()
        self.render_group.add(self.button,
                              self.label,
                              self.dice,
                              self.sex_img)
                              
        self.popup_group = pygame.sprite.RenderUpdates()
        self.popup_group.add(self.popup)
        
    def __clean_screen(self):
        self.screen.fill(BLACK)
        pygame.display.update()
                              
    def __processEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if (event.type == pygame.KEYDOWN) and \
            self.popup.is_showing():
            self.popup.close()
            self.__clean_screen()
        if (event.type == pygame.MOUSEBUTTONDOWN) and \
           (event.button == LEFT_BUTTON):
            self.button.on_press(self.dice.throw_dice)
        elif event.type == pygame.MOUSEBUTTONUP and \
            event.button == LEFT_BUTTON:
            self.button.on_release()
        
    def run(self):
        # main loop
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            dt = clock.tick(FRAMES_PER_SECOND)
            #print "Time lapsed: {0}".format(dt)
            for event in pygame.event.get():
                self.__processEvent(event)
                    
            # update view
            if self.popup.is_showing():
                self.popup_group.update()
                pygame.display.update(self.popup_group.draw(self.screen))
            else:
                self.render_group.update()
                pygame.display.update(self.render_group.draw(self.screen))

def main():
    app = GameApp()
    app.run()

if __name__ == "__main__":
    main()
