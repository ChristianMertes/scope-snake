#!/usr/bin/env python3

import time
import curses
import random

import logging

logging.basicConfig(filename='test.log', level=logging.DEBUG)


def print_intro(stdscr):
    y, x = stdscr.getmaxyx()

    window = stdscr.subwin(y - 20, x - 20, 10, 10)
    window.timeout(1000)
    window.addstr(0, 0, 'This is the introduction to the game...')
    continue_text = 'Press <Enter> to continue ...'
    continue_text_empty = ' ' * len(continue_text)
    window.addstr(y - 22, x - 21 - len(continue_text), continue_text)
    window.refresh()

    key = window.getch()
    text = True
    while key != 10:  # wait for enter
        text = not text
        if text:
            window.addstr(y - 22, x - 21 - len(continue_text), continue_text)
        else:
            window.addstr(y - 22, x - 21 - len(continue_text),
                          continue_text_empty)
        window.refresh
        key = window.getch()

    window.clear()
    window.refresh()


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Point(self.x, self.y)


class Drawable():
    def __init__(self):
        self.chars = []
        self.pos = []

    def draw(self, window):
        for i in range(len(self.chars)):
            window.addch(self.pos[i].y, self.pos[i].x, self.chars[i])

    def intersect(self, other):
        for p in self.pos:
            if p in other.pos:
                return True
        return False

    def __str__(self):
        if len(self.chars) == 0:
            return '()'

        text = '(' + self.chars[0] + '=' + str(self.pos[0])
        for i in range(1, len(self.chars)):
            text += ', ' + self.chars[i] + '=' + str(self.pos[i])
        text += ')'
        return text


class Food(Drawable):

    def __init__(self, text, position, horizontal=True):
        super().__init__()

        self.text = text
        self.chars.append(text[0])
        self.pos.append(position)

        for i in range(1, len(text)):
            self.chars.append(text[i])
            new_position = self.pos[i - 1].copy()
            if horizontal:
                new_position.x += 1
            else:
                new_position.y += 1
            self.pos.append(new_position)


class Snake(Drawable):

    def __init__(self):
        super().__init__()

        self.chars.append('/')
        self.pos.append(Point(5, 10))
        self.parts = 1

    def move(self, key):
        # save current head position
        last_pos = self.pos[0].copy()
        # move head according to direction
        if key == curses.KEY_RIGHT:
            self.pos[0].x += 1
        elif key == curses.KEY_LEFT:
            self.pos[0].x -= 1
        elif key == curses.KEY_DOWN:
            self.pos[0].y += 1
        elif key == curses.KEY_UP:
            self.pos[0].y -= 1

        # move all other parts to new locations
        for i in range(1, len(self.chars)):
            if self.pos[i] == last_pos:
                continue
            tmp_pos = self.pos[i]
            self.pos[i] = last_pos.copy()
            last_pos = tmp_pos


    def add_part(self, part):
        for char in part:
            self.chars.append(char)
            self.pos.append(self.pos[-1].copy())
        self.parts += 1


def snake_game(stdscr, scope, loop_on_border=False):
    y, x = stdscr.getmaxyx()
    window = stdscr.subwin(y - 20, x - 20, 10, 10)
    window.keypad(True)
    y, x = window.getmaxyx()

    snake = Snake()

    window.erase()
    window.border()
    snake.draw(window)
    window.refresh()

    valid_keys = [curses.KEY_RIGHT, curses.KEY_LEFT,
                  curses.KEY_UP, curses.KEY_DOWN]

    # components = ['citec', 'csra', 'home', 'living', 'dining', 'colorablelight', 'ceilinglamep1'] 
    components = [c for c in scope.split('/')[1:] if len(c) > 0]
    logging.info('Extracted components: ' + str(components))
    food = []
    for c in components:
        intersects = True
        while intersects:
            horizontal = True
            if random.random() > 0.5:
                horizontal = False

            if horizontal:
                start_x = random.randint(1, x - 2 - len(c))
                start_y = random.randint(1, y - 2)
            else:
                start_x = random.randint(1, x - 2)
                start_y = random.randint(1, y - 2 - len(c))

            f = Food(c, Point(start_x, start_y), horizontal)
            if f.intersect(snake):
                continue
            intersects = False
            for ef in food:
                if f.intersect(ef):
                    intersects = True
                    break
            if not intersects:
                food.append(f)

    timeout = 100
    min_timeout = 30
    window.timeout(timeout)

    key = curses.KEY_RIGHT  # move to the right at the start
    while True:
        prev_key = key
        since = time.time()
        key = window.getch()
        duration = round((time.time() - since) * 1000)
        if key == 27: # quit on esape key press
            logging.info('Stop because escape key got pressed')
            break

        remaining_wait = duration - timeout
        if remaining_wait > 0:
            logging.debug('Sleep remaining ' + str(remaining_wait / 1000) + 's')
            time.sleep(remaining_wait / 1000)

        if key not in valid_keys:
            key = prev_key
        snake.move(key)

        # check self collisions
        if snake.pos[0] in snake.pos[1:]:
            break

        if loop_on_border:
            # loop
            if snake.pos[0].x <= 0:
                snake.pos[0].x = x - 2
            elif snake.pos[0].x >= (x - 1):
                snake.pos[0].x = 1
            if snake.pos[0].y <= 0:
                snake.pos[0].y = y - 2
            elif snake.pos[0].y >= (y - 1):
                snake.pos[0].y = 1
        else:
            # quit on border touch
            if snake.pos[0].x <= 0 or snake.pos[0].x >= (x - 1):
                break
            if snake.pos[0].y <= 0 or snake.pos[0].y >= (y - 1):
                break

        j = -1
        for i in range(len(food)):
            if snake.pos[0] in food[i].pos:
                j = i
                break

        if j != -1:
            f = food.pop(j)
            snake.add_part(f.text[::-1] + '/')

            logging.info('Current scope: ' + ''.join(snake.chars[::-1]))
            if ''.join(snake.chars[::-1]) == scope:
                logging.info('Scope fixed!')
                return True

            timeout = max(timeout - 10, min_timeout)
            logging.info('Change timeout to: ' + str(timeout))
            window.timeout(timeout)
            
        # redraw window
        window.erase()
        window.border()
        snake.draw(window)
        for f in food:
            f.draw(window)
        window.refresh()


def main(stdscr):
    curses.curs_set(0)
    # print_intro(stdscr)
    scope = '/citec/csra/home/living/dining/colorablelight/ceilinglamep1/'
    snake_game(stdscr, scope)


curses.wrapper(main)
