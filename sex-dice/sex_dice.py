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

def map_sex_choice(num):
    if num == 1:
       print 'Suga kuk'
    elif num == 2: 
       print 'Slicka fitta'
    elif num == 3:
       print 'Doggystyle'
    elif num == 4:
       print 'Knulla hårt'
    elif num == 5:
       print '69'
    elif num == 6:
       print 'Snopp i rumpen!'

def generate_outcome(delay):
    rng_num = random.random()
    num_dice_sides = 6    
    outcome = int(ceil(num_dice_sides * rng_num))
    time.sleep(delay)
    #map_sex_choice(outcome)
    return outcome

def throw_dice():
    a = 0.33/2500;
    for i in range(0, 50):
        delay = a *(i*i)
        outcome = generate_outcome(delay)
        print outcome

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

    def __init__(self, x, y, w, h,):
        # Call the parent class (Sprite) constructor
        pygame.sprite.DirtySprite.__init__(self)

        # create an image surface
        self.image = pygame.image.load("sex.jpg").convert()
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
        buttonRect = pygame.Rect(border_size,
                                 border_size,
                                 w-2*border_size,
                                 h-2*border_size)
        buttonColor = pygame.Color("grey")
        borderColor = pygame.Color("white")

        # create an image surface
        self.image = pygame.Surface([w, h])    
        self.image.fill(borderColor)
        self.image.fill(buttonColor, buttonRect)

        # set pos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # add label text
        text = 'Throw dice'
        antialias = 1
        color = (255, 0, 0)
        font = pygame.font.SysFont("Arial", 22)
        textSurf = font.render(text, antialias, color)
        W = textSurf.get_width()
        H = textSurf.get_height()
        label_pos = (buttonRect.w/2 - W/2, buttonRect.h/2 - H/2)
        self.image.blit(textSurf, label_pos)

        # state
        self.pressed = False

    def update(self):
        pass #do something here

    def on_press(self, pos):
        x, y = pos
        rect = self.rect
        if (rect.x <= x) and (x <= (rect.x+rect.w)) \
           and (rect.y <= y) and (y <= rect.y+rect.h):
            self.pressed = True

    def on_release(self):
        if self.pressed:
            throw_dice()
            self.pressed = False
    
def main():
    # initialize game
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    #logo = pygame.image.load('')
    #pygame.display.set_icon(logo)
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
    sex_w = (WINDOW_WIDTH/2) - 2*PADDING
    sex_h = (WINDOW_HEIGHT/2) - 2*PADDING
    sex_x = WINDOW_WIDTH/2
    sex_y = PADDING
    sex_img = Image(sex_x,
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

    # define render group
    render_group = pygame.sprite.RenderUpdates()
    render_group.add(button, sex_img, label)
    #for object in clickableObjectsList:
    #   object.clickCheck(event.pos)

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
                button.on_press(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP and \
                 event.button == LEFT_BUTTON:
                button.on_release()
                    
                
            # update view
            render_group.update()
            pygame.display.update(render_group.draw(screen))
            
    

if __name__ == "__main__":
    main()
