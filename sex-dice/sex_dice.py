#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import time
import random
import pygame
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

DICE_ARRAY = [[0, 0, DICE_WIDTH, DICE_HEIGHT],
              [DICE_WIDTH, 0, DICE_WIDTH, DICE_HEIGHT],
              [2*DICE_WIDTH, 0, DICE_WIDTH, DICE_HEIGHT],
              [0, DICE_HEIGHT, DICE_WIDTH, DICE_HEIGHT],
              [DICE_WIDTH, DICE_HEIGHT, DICE_WIDTH, DICE_HEIGHT],
              [2*DICE_WIDTH, DICE_HEIGHT, DICE_WIDTH, DICE_HEIGHT]]
              
FIBONACCI_ARRAY = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


class Text(pygame.sprite.DirtySprite):

    def __init__(self, text, size, color, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.DirtySprite.__init__(self)

        # create a text surface
        antialias = 1
        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, antialias, color)  
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()

        # create an ordinary surface and add text surf
        self.image = pygame.Surface((W, H))
        self.image.blit(self.textSurf, (0, 0))

        # set pos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass #do something here

        
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
        pass #do something here
  
  
class Button(pygame.sprite.DirtySprite):

    def __init__(self, x, y, w, h):
        # Call the parent class (Sprite) constructor
        pygame.sprite.DirtySprite.__init__(self)

        # define button
        # note that buttonRect is not in global coordinates
        # but relative in image
        border_size = 5
        self.buttonRect = pygame.Rect(border_size,
                                      border_size,
                                      w-2*border_size,
                                      h-2*border_size)
        self.buttonColorUp = pygame.Color(130, 130, 130)
        self.buttonColorDown = pygame.Color(100, 100, 100)
        self.borderColor = pygame.Color("white")

        # create an image surface
        self.image = pygame.Surface([w, h])
        
        # set pos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.draw(self.buttonColorUp)
        
        # state
        self.pressed = False
    
    def draw(self, color):
        self.image.fill(self.borderColor)
        self.image.fill(color, self.buttonRect)
        
        # add label text
        text = 'Throw dice'
        size = 24
        color = pygame.Color("red")
        antialias = 1
        font = pygame.font.SysFont("Arial", size)
        textSurf = font.render(text, antialias, color)
        W = textSurf.get_width()
        H = textSurf.get_height()
        label_pos = (self.buttonRect.w/2 - W/2, self.buttonRect.h/2 - H/2)
        self.image.blit(textSurf, label_pos)
        # label = Text(text, size, color, self.rect.x, self.rect.y)        

    def on_press(self, dice, pos):
        x, y = pos
        rect = self.rect
        if (rect.x <= x) and (x <= (rect.x+rect.w)) \
           and (rect.y <= y) and (y <= rect.y+rect.h) \
           and not self.pressed:
            self.pressed = True
            dice.throw_dice()
            self.draw(self.buttonColorDown)

    def on_release(self):
        self.pressed = False
        self.draw(self.buttonColorUp)
            
class Dice(Image):
    
    def __init__(self, x, y, size):
        # Call the parent class (Image) constructor
        pygame.sprite.DirtySprite.__init__(self)
        
        dice_path = "sides.jpg"
        self.img_orig = pygame.image.load(dice_path).convert()
        
        # set pos
        self.size = size
        self.rect = self.img_orig.get_rect()
        self.rect.topleft = (x, y)
        
        # initialize
        self.thrown = False
        self.frame_counter = 0
        self.num_counter = 0
        self.set_random_number()

    def set_random_number(self):
        num = self.generate_outcome()
        rect = DICE_ARRAY[num-1]
        side_img = self.img_orig.subsurface(rect[0], rect[1], rect[2], rect[3])
        self.image = pygame.transform.scale(side_img, (self.size, self.size))

    def generate_outcome(self):
        rng_num = random.random()
        outcome = int(ceil(NUM_DICE_SIDES * rng_num))
        return outcome

    def reset(self):
        self.thrown = False
        self.num_counter = 0
        self.frame_counter = 0    

    def update(self):
        if self.thrown:
            if (FIBONACCI_ARRAY[self.num_counter] == self.frame_counter):
                self.frame_counter = 0
                self.set_random_number()
                if (self.num_counter == (len(FIBONACCI_ARRAY)-1)):
                    self.reset()
                else:
                    self.num_counter += 1
            else:
                self.frame_counter += 1

    def throw_dice(self):
        self.thrown = True


def main():
    # initialize game
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    logo = pygame.image.load('logo.jpg')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Sex dice')
    screen = pygame.display.set_mode((WINDOW_WIDTH-PADDING,
                                      WINDOW_HEIGHT-PADDING))

    # crate game label
    font_size = 48
    text = "SEX DICE"
    label_color = pygame.Color("red")
    label_x = 50
    label_y = PADDING
    label = Text(text,
                 font_size,
                 label_color,
                 label_x,
                 label_y)

    # create default image
    sex_path = "sex.jpg"
    sex_w = (WINDOW_WIDTH/2) - 2*PADDING
    sex_h = (WINDOW_HEIGHT/2) - 2*PADDING
    sex_x = WINDOW_WIDTH/2
    sex_y = PADDING
    sex_img = Image(sex_path,
                    sex_x,
                    sex_y,
                    sex_w,
                    sex_h)

    # create game button
    rect_w = WINDOW_WIDTH - 3*PADDING
    rect_h = WINDOW_HEIGHT/2 - 2*PADDING
    rect_x = PADDING
    rect_y = WINDOW_HEIGHT/2
    button = Button(rect_x,
                    rect_y,
                    rect_w,
                    rect_h)

    # create dice
    dice_x = 90
    dice_y = 85
    dize_size = 128
    dice = Dice(dice_x,
                dice_y,
                dize_size)
                
    # define render group
    render_group = pygame.sprite.RenderUpdates()
    render_group.add(button, sex_img, label, dice)

    # main loop
    running = True
    while running:
        dt = clock.tick(FRAMES_PER_SECOND)
        #print "Time lapsed: {0}".format(dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and \
               event.button == LEFT_BUTTON:
                mouse_pos = pygame.mouse.get_pos()
                button.on_press(dice, mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP and \
                 event.button == LEFT_BUTTON:
                button.on_release()
                    
                
        # update view
        render_group.update()
        pygame.display.update(render_group.draw(screen))
            
    

if __name__ == "__main__":
    main()
