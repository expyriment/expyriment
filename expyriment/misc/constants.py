""" The constants module.

This module contains expyriment constants.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os as _os

import pygame as _pygame

from ..misc import byte2unicode as _str2unicode
from ..misc._colour import Colour as _Colour

# Keys
K_BACKSPACE = _pygame.K_BACKSPACE
K_TAB = _pygame.K_TAB
K_CLEAR = _pygame.K_CLEAR
K_RETURN = _pygame.K_RETURN
K_PAUSE = _pygame.K_PAUSE
K_ESCAPE = _pygame.K_ESCAPE
K_SPACE = _pygame.K_SPACE
K_EXCLAIM = _pygame.K_EXCLAIM
K_QUOTEDBL = _pygame.K_QUOTEDBL
K_HASH = _pygame.K_HASH
K_DOLLAR = _pygame.K_DOLLAR
K_AMPERSAND = _pygame.K_AMPERSAND
K_QUOTE = _pygame.K_QUOTE
K_LEFTPAREN = _pygame.K_LEFTPAREN
K_RIGHTPAREN = _pygame.K_RIGHTPAREN
K_ASTERISK = _pygame.K_ASTERISK
K_PLUS = _pygame.K_PLUS
K_COMMA = _pygame.K_COMMA
K_MINUS = _pygame.K_MINUS
K_PERIOD = _pygame.K_PERIOD
K_SLASH = _pygame.K_SLASH
K_0 = _pygame.K_0
K_1 = _pygame.K_1
K_2 = _pygame.K_2
K_3 = _pygame.K_3
K_4 = _pygame.K_4
K_5 = _pygame.K_5
K_6 = _pygame.K_6
K_7 = _pygame.K_7
K_8 = _pygame.K_8
K_9 = _pygame.K_9
K_COLON = _pygame.K_COLON
K_SEMICOLON = _pygame.K_SEMICOLON
K_LESS = _pygame.K_LESS
K_EQUALS = _pygame.K_EQUALS
K_GREATER = _pygame.K_GREATER
K_QUESTION = _pygame.K_QUESTION
K_AT = _pygame.K_AT
K_LEFTBRACKET = _pygame.K_LEFTBRACKET
K_BACKSLASH = _pygame.K_BACKSLASH
K_RIGHTBRACKET = _pygame.K_RIGHTBRACKET
K_CARET = _pygame.K_CARET
K_UNDERSCORE = _pygame.K_UNDERSCORE
K_BACKQUOTE = _pygame.K_BACKQUOTE
K_a = _pygame.K_a
K_b = _pygame.K_b
K_c = _pygame.K_c
K_d = _pygame.K_d
K_e = _pygame.K_e
K_f = _pygame.K_f
K_g = _pygame.K_g
K_h = _pygame.K_h
K_i = _pygame.K_i
K_j = _pygame.K_j
K_k = _pygame.K_k
K_l = _pygame.K_l
K_m = _pygame.K_m
K_n = _pygame.K_n
K_o = _pygame.K_o
K_p = _pygame.K_p
K_q = _pygame.K_q
K_r = _pygame.K_r
K_s = _pygame.K_s
K_t = _pygame.K_t
K_u = _pygame.K_u
K_v = _pygame.K_v
K_w = _pygame.K_w
K_x = _pygame.K_x
K_y = _pygame.K_y
K_z = _pygame.K_z
K_DELETE = _pygame.K_DELETE
K_KP0 = _pygame.K_KP0
K_KP1 = _pygame.K_KP1
K_KP2 = _pygame.K_KP2
K_KP3 = _pygame.K_KP3
K_KP4 = _pygame.K_KP4
K_KP5 = _pygame.K_KP5
K_KP6 = _pygame.K_KP6
K_KP7 = _pygame.K_KP7
K_KP8 = _pygame.K_KP8
K_KP9 = _pygame.K_KP9
K_KP_PERIOD = _pygame.K_KP_PERIOD
K_KP_DIVIDE = _pygame.K_KP_DIVIDE
K_KP_MULTIPLY = _pygame.K_KP_MULTIPLY
K_KP_MINUS = _pygame.K_KP_MINUS
K_KP_PLUS = _pygame.K_KP_PLUS
K_KP_ENTER = _pygame.K_KP_ENTER
K_KP_EQUALS = _pygame.K_KP_EQUALS
K_UP = _pygame.K_UP
K_DOWN = _pygame.K_DOWN
K_RIGHT = _pygame.K_RIGHT
K_LEFT = _pygame.K_LEFT
K_INSERT = _pygame.K_INSERT
K_HOME = _pygame.K_HOME
K_END = _pygame.K_END
K_PAGEUP = _pygame.K_PAGEUP
K_PAGEDOWN = _pygame.K_PAGEDOWN
K_F1 = _pygame.K_F1
K_F2 = _pygame.K_F2
K_F3 = _pygame.K_F3
K_F4 = _pygame.K_F4
K_F5 = _pygame.K_F5
K_F6 = _pygame.K_F6
K_F7 = _pygame.K_F7
K_F8 = _pygame.K_F8
K_F9 = _pygame.K_F9
K_F10 = _pygame.K_F10
K_F11 = _pygame.K_F11
K_F12 = _pygame.K_F12
K_F13 = _pygame.K_F13
K_F14 = _pygame.K_F14
K_F15 = _pygame.K_F15
K_NUMLOCK = _pygame.K_NUMLOCK
K_CAPSLOCK = _pygame.K_CAPSLOCK
K_SCROLLOCK = _pygame.K_SCROLLOCK
K_RSHIFT = _pygame.K_RSHIFT
K_LSHIFT = _pygame.K_LSHIFT
K_RCTRL = _pygame.K_RCTRL
K_LCTRL = _pygame.K_LCTRL
K_RALT = _pygame.K_RALT
K_LALT = _pygame.K_LALT
K_RMETA = _pygame.K_RMETA
K_LMETA = _pygame.K_LMETA
K_LSUPER = _pygame.K_LSUPER
K_RSUPER = _pygame.K_RSUPER
K_MODE = _pygame.K_MODE
K_HELP = _pygame.K_HELP
K_PRINT = _pygame.K_PRINT
K_SYSREQ = _pygame.K_SYSREQ
K_BREAK = _pygame.K_BREAK
K_MENU = _pygame.K_MENU
K_POWER = _pygame.K_POWER
K_EURO = _pygame.K_EURO
K_ALL_LETTERS = list(range(K_a, K_z + 1))
K_ALL_DIGITS = list(range(K_0, K_9 + 1))
K_ALL_KEYPAD_DIGITS = list(range(K_KP0, K_KP9 + 1))

# Colours
C_BLACK = _Colour((0, 0, 0))
C_WHITE = _Colour((255, 255, 255))
C_RED = _Colour((255, 0, 0))
C_GREEN = _Colour((0, 255, 0))
C_BLUE = _Colour((0, 0, 255))
C_YELLOW = _Colour((255, 255, 0))
C_GREY = _Colour((200, 200, 200))
C_DARKGREY = _Colour((150, 150, 150))
C_EXPYRIMENT_ORANGE = _Colour((255, 150, 50))
C_EXPYRIMENT_PURPLE = _Colour((160, 70, 250))

# Permutation types
P_BALANCED_LATIN_SQUARE = 'balanced'
P_CYCLED_LATIN_SQUARE = 'cycled'
P_RANDOM = 'random'

# Misc
_tmp = _os.path.abspath(
    _os.path.join(_os.path.dirname(__file__),
                  "..", "expyriment_logo.png"))
EXPYRIMENT_LOGO_FILE = _str2unicode(_tmp)
