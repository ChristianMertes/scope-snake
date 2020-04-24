#!/usr/bin/env python3

import time
import curses
import random

# import logging

# logging.basicConfig(filename='test.log', level=logging.DEBUG)

def write_line(window, text, line):
    col = 0
    for char in text:
        window.addch(line, col, char)
        col += 1
        window.refresh()
        time.sleep(0.1)
    time.sleep(0.5)


def print_outro(stdscr):
    y, x = stdscr.getmaxyx()

    height = 30
    width = 100
    y, x = stdscr.getmaxyx()
    if x < width or y < height:
        # logging.error('Terminal window is to small (' + str(x) + 'x' + str(y) + ') need at least (100x50)')
        return
   
    start_x = int((x - width) / 2)
    start_y = int((y - height) / 2)
    window = stdscr.subwin(height, width, start_y, start_x)
    window.timeout(1000)

    write_line(window, 'Du hast es geschafft.', 0)
    write_line(window, 'Die Scopes sind repariert und alle Komponenten laufen wieder.', 1)
    write_line(window, 'Der Demo steht nichts mehr im Wege!', 2)
    write_line(window, '    ', 3)
    write_line(window, 'Vielen Dank fürs Spielen!', 4)


def print_intro(stdscr):
    y, x = stdscr.getmaxyx()

    height = 30
    width = 100
    y, x = stdscr.getmaxyx()
    if x < width or y < height:
        # logging.error('Terminal window is to small (' + str(x) + 'x' + str(y) + ') need at least (100x50)')
        return
   
    start_x = int((x - width) / 2)
    start_y = int((y - height) / 2)
    window = stdscr.subwin(height, width, start_y, start_x)
    window.timeout(1000)

    write_line(window, 'Es ist wieder einmal soweit.', 0)
    write_line(window, 'Eine Demo im CSRA muss von dir gegeben werden.', 1)
    write_line(window, 'Deshalb testests du das Apartment nochmal auf Herz und Nieren.', 2)
    write_line(window, '    ', 3)
    write_line(window, 'Es läuft NICHTS!!!', 4)
    write_line(window, '    ', 5)
    write_line(window, 'Da fällt dir ein, dass sich die Scopes der Homeautomation mal wieder geändert haben...', 6)
    write_line(window, 'Einige Entwickler scheinen ihre Komponenten noch nicht angepasst zu haben.', 7)
    write_line(window, 'Hilf ihnen, indem du die einzelnen Scope Komponenten in der richtigen Reihenfolge einsammelst.', 8)

    continue_text = 'Drücke <Enter> zum starten ...'
    continue_text_empty = ' ' * len(continue_text)
    window.addstr(height - 1, width - 1 - len(continue_text), continue_text)
    window.refresh()

    key = window.getch()
    text = True
    while key != 10:  # wait for enter
        text = not text
        if text:
            window.addstr(height - 1, width - 1 - len(continue_text), continue_text)
        else:
            window.addstr(height - 1, width - 1 - len(continue_text),
                          continue_text_empty)
        window.refresh
        key = window.getch()

    window.clear()
    window.refresh()


def print_result(stdscr, result_message, continue_text):
    height = 30
    width = 100
    y, x = stdscr.getmaxyx()
    if x < width or y < height:
        # logging.error('Terminal window is to small (' + str(x) + 'x' + str(y) + ') need at least (100x50)')
        return
   
    start_x = int((x - width) / 2)
    start_y = int((y - height) / 2)
    window = stdscr.subwin(height, width, start_y, start_x)
    window.timeout(1000)

    line = 0
    for s in result_message:
        window.addstr(line, 0, s)
        line += 1

    continue_text_empty = ' ' * len(continue_text)
    window.addstr(height - 1, width - 1 - len(continue_text), continue_text)
    window.refresh()

    key = window.getch()
    text = True
    while key != 10:  # wait for enter
        text = not text
        if text:
            window.addstr(height - 1, width - 1 - len(continue_text), continue_text)
        else:
            window.addstr(height - 1, width - 1 - len(continue_text),
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

    def add_part_at(self, part, at):
        part_pos = self.pos[at - 1].copy()
        for i in range(len(part)):
            self.chars.insert(at + i, part[i])
            self.pos.append(part_pos)
        self.parts += 1


def add_food(c, food_list, snake, width, height):
    intersects = True
    while intersects:
        horizontal = True
        if random.random() > 0.5:
            horizontal = False

        if horizontal:
            start_x = random.randint(1, width - 2 - len(c))
            start_y = random.randint(1, height - 2)
        else:
            start_x = random.randint(1, width - 2)
            start_y = random.randint(1, height - 2 - len(c))

        f = Food(c, Point(start_x, start_y), horizontal)
        if f.intersect(snake):
            continue
        intersects = False
        for ef in food_list:
            if f.intersect(ef):
                intersects = True
                break
        if not intersects:
            food_list.append(f)

def snake_game(stdscr, scope, loop_on_border=False, scope_reverse=False, fast_food=False, start_timeout=100, min_timeout=30, timeout_step=10):
    height = 30
    width = 80
    y, x = stdscr.getmaxyx()
    if x < width or y < height:
        # logging.error('Terminal window is to small (' + str(x) + 'x' + str(y) + ') need at least (100x50)')
        return ''
   
    start_x = int((x - width) / 2)
    start_y = int((y - height) / 2)
    # logging.info(str((start_x, start_y, width, height)))
    window = stdscr.subwin(height, width, start_y, start_x)
    window.keypad(True)

    timeout = start_timeout
    window.timeout(timeout)

    snake = Snake()
    current_scope = ''.join(snake.chars[::-1])

    valid_keys = [curses.KEY_RIGHT, curses.KEY_LEFT,
                  curses.KEY_UP, curses.KEY_DOWN]

    components = [c for c in scope.split('/')[1:] if len(c) > 0]
    # logging.info('Extracted components: ' + str(components))
    food = []
    for c in components:
        add_food(c, food, snake, width, height)
    if fast_food:
        food_directions = []
        for f in food:
            food_directions.append(valid_keys[random.randint(0, 3)])

    window.erase()
    window.border()
    snake.draw(window)
    for f in food:
        f.draw(window)
    stdscr.addstr(start_y + height + 3, start_x, 'Current scope: ' + current_scope)
    stdscr.refresh()

    if fast_food:
        food_moved = True

    key = curses.KEY_RIGHT  # move to the right at the start
    while True:
        vertical_movement = (key == curses.KEY_UP or key == curses.KEY_DOWN)
        if vertical_movement:
            scaled_timeout = int((width * timeout) / (height * 2))
            # logging.info('Adapt timeout on vertical movement to ' + str(scaled_timeout))
            window.timeout(scaled_timeout)
        else:
            window.timeout(timeout)

        prev_key = key
        since = time.time()
        key = window.getch()
        duration = round((time.time() - since) * 1000)
        if key == 27: # quit on esape key press
            # logging.info('Stop because escape key got pressed')
            return ''

        remaining_wait = duration - timeout
        if remaining_wait > 0:
            # logging.debug('Sleep remaining ' + str(remaining_wait / 1000) + 's')
            time.sleep(remaining_wait / 1000)

        if key not in valid_keys:
            key = prev_key

        # keep movement direction if the opposite key is pressed so that
        # it is not possible to kill oneself accidentally
        if prev_key == curses.KEY_LEFT and key == curses.KEY_RIGHT:
            key = prev_key
        elif prev_key == curses.KEY_RIGHT and key == curses.KEY_LEFT:
            key = prev_key
        elif prev_key == curses.KEY_DOWN and key == curses.KEY_UP:
            key = prev_key
        elif prev_key == curses.KEY_UP and key == curses.KEY_DOWN:
            key = prev_key

        snake.move(key)

        # check self collisions
        if snake.pos[0] in snake.pos[1:]:
            return current_scope

        if loop_on_border:
            # loop
            if snake.pos[0].x <= 0:
                snake.pos[0].x = width - 2
            elif snake.pos[0].x >= (width - 1):
                snake.pos[0].x = 1
            if snake.pos[0].y <= 0:
                snake.pos[0].y = height - 2
            elif snake.pos[0].y >= (height - 1):
                snake.pos[0].y = 1
        else:
            # quit on border touch
            if snake.pos[0].x <= 0 or snake.pos[0].x >= (width - 1):
                return current_scope
            if snake.pos[0].y <= 0 or snake.pos[0].y >= (height - 1):
                return current_scope

        if fast_food:
            food_moved = not food_moved
            if not food_moved:
                for i in range(len(food)):
                    f = food[i]
                    f.move(food_directions[i])
                    # loop
                    if f.pos[0].x <= 0:
                        f.pos[0].x = width - 2
                    elif f.pos[0].x >= (width - 1):
                        f.pos[0].x = 1
                    if f.pos[0].y <= 0:
                        f.pos[0].y = height - 2
                    elif f.pos[0].y >= (height - 1):
                        f.pos[0].y = 1

                    if random.random() < 0.15:
                        food_directions[i] = valid_keys[random.randint(0, 3)]



        #for i in range(len(food)):
        for f in food:
            if not snake.intersect(f):
                continue

            food.remove(f)
            # f = food.pop(i)
            # i -= 1
            if scope_reverse:
                snake.add_part_at(f.text[::-1] + '/', 1)
            else:
                snake.add_part(f.text[::-1] + '/')

            current_scope = ''.join(snake.chars[::-1])
            # logging.info('Current scope: ' + ''.join(snake.chars[::-1]))
            if ''.join(snake.chars[::-1]) == scope:
                # logging.info('Scope fixed!')
                return current_scope

            if len(food) == 0:
                return current_scope

            timeout = max(timeout - timeout_step, min_timeout)
            # logging.info('Change timeout to: ' + str(timeout))
            # window.timeout(timeout)
            
        # redraw window
        window.erase()
        window.border()
        snake.draw(window)
        for f in food:
            f.draw(window)
        stdscr.addstr(start_y + height + 3, start_x, 'Current scope: ' + current_scope)
        stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    print_intro(stdscr)
    scopes = ['/citec/csra/home/living/dining/colorablelight/ceilinglamep1/',
              '/citec/csra/home/hallway/entrance/motiondetector/motionsensorentrancehallway/',
              '/citec/csra/control/center/colorablelight/recordstatelamp/']
    for i in range(len(scopes)):
        scope = scopes[i]
        reverse = i == 0 or i == 2
        start_timeout = 150
        min_timeout = 75
        timeout_step = 15
        fast_food = False
        if i == 2:
            fast_food = True
            start_timeout = 200
            min_timeout = 100
            timeout_step = 15

        result = snake_game(stdscr, scope, False, reverse, fast_food, start_timeout, min_timeout, timeout_step)
        stdscr.clear()
        stdscr.refresh()
        while result != scope:
            # logging.info('Result is: ' + result)
            if result == '':
                # logging.info('Return because empty result...')
                return
            stdscr.clear()
            stdscr.refresh()
            msg = ['Das ist nicht der richtige Scope!', '', 'Dein Scope ist:    ' + result, '', 'Richtig wäre aber: ' + scope]
            print_result(stdscr, msg, 'Drücke <Enter> um es nochmal zu versuchen...')
            result = snake_game(stdscr, scope, False, reverse, fast_food, start_timeout, min_timeout, timeout_step)
            stdscr.clear()
            stdscr.refresh()

        if i < 2:
            msg = ['Du hast es geschafft!']
            print_result(stdscr, msg, 'Auf zum nächste Scope <Enter>...')

    print_outro(stdscr)


curses.wrapper(main)
