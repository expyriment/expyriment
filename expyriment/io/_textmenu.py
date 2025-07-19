"""
A TextMenu.

This module contains a class implementing a TextMenu.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from .. import _internals, misc, stimuli
from . import defaults
from ._input_output import Input
from ._keyboard import Keyboard
from ._mouse import Mouse


class TextMenu(Input):
    """A class implementing a text menu."""

    def __init__(self, heading, menu_items, width=None, position=None,
                 text_size=None, gap=None, heading_font=None,
                 text_font=None, background_colour=None,
                 text_colour=None, heading_text_colour=None,
                 select_background_colour=None, select_text_colour=None,
                 select_frame_colour=None, select_frame_line_width=None,
                 justification=None, scroll_menu=None,
                 background_stimulus=None, mouse=None):
        """Create a text menu.

        This creates a menu with items to be selected.

        Parameters
        ----------
        heading : str
            menu heading
        menu_items : str or list
            list with menu items
        width : int, optional
            width of the menu. If not defined, the width depends on the widest
            item in the menu
        position : (int, int), optional
        text_size : int, optional
        background_colour : (int, int, int), optional
            background colour of the menu
        gap : int, optional
            size of gap (pixel) between heading and item list
        heading_font : str, optional
            font to be used for the heading
        text_font : str, optional
            font to be used for the text
        text_colour : (int, int, int), optional
            text colour of the items
        heading_text_colour : (int, int, int), optional
            text colour of the heading
        select_background_colour : (int, int, int), optional
            background colour of the currently selected item
        select_text_colour : (int, int, int), optional
            text colour of the currently selected item
        select_frame_colour : (int, int, int), optional
            colour of the frame around the selected item
        select_frame_line_width : int, optional
            line width of the frame around the selected item
        justification : int, optional
            text justification: 0 (left), 1 (center), 2 (right)
        scroll_menu : int, optional
            maximum length of an item list before a scroll menu will
            be display. If the parameter is 0 of False scroll menu
            will not be displayed
        background_stimulus : visual expyriment stimulus, optional
            The background stimulus is a second stimulus that will be presented
            together with the TextMenu. For both stimuli overlap TextMenu
            will appear on top of the background_stimulus
        mouse : expyriment.io.Mouse object or True, optional
            If True or a mouse object is given, the menu will be controlled
            by the mouse

        """

        if position is None:
            position = defaults.textmenu_position
        if gap is None:
            gap = defaults.textmenu_gap
        if heading_font is None:
            heading_font = defaults.textmenu_text_font
        if text_font is None:
            text_font = defaults.textmenu_text_font
        if text_size is None:
            text_size = defaults.textmenu_text_size
        if text_size is None:
            text_size = _internals.active_exp.text_size
        if background_colour is None:
            background_colour = defaults.textmenu_background_colour
        if text_colour is None:
            text_colour = defaults.textmenu_text_colour
        if heading_text_colour is None:
            heading_text_colour = defaults.textmenu_heading_text_colour
        if select_background_colour is None:
            select_background_colour = \
                defaults.textmenu_select_background_colour
        if select_text_colour is None:
            select_text_colour = defaults.textmenu_select_text_colour
        if select_frame_colour is None:
            select_frame_colour = defaults.textmenu_select_frame_colour
        if select_frame_line_width is None:
            select_frame_line_width = defaults.textmenu_select_frame_line_width
        if justification is None:
            justification = defaults.textmenu_justification
        if scroll_menu is None:
            scroll_menu = defaults.textmenu_scroll_menu

        self._scroll_menu = abs(int(scroll_menu))
        if self._scroll_menu > 0 and self._scroll_menu < 5:
            self._scroll_menu = 5
        self._gap = gap
        self._position = position
        self._bkg_colours = [background_colour, select_background_colour]
        self._text_colours = [text_colour, select_text_colour]

        # determine line size
        item_surface_size = stimuli.TextLine(menu_items[0], text_font=text_font,
                                             text_size=text_size).surface_size
        if width is None:
            # get larges width
            for mi in menu_items[1:]:
                s = stimuli.TextLine(mi,text_font=text_font,
                                     text_size=text_size).surface_size
                if s[0] > item_surface_size[0]:
                    item_surface_size = s
            width = item_surface_size[0] + 2

        self._line_size = (width, item_surface_size[1] + 2)
        stimuli._stimulus.Stimulus._id_counter -= 1
        self._frame = stimuli.Rectangle(
            line_width=select_frame_line_width,
            size=(self._line_size[0] + 2 * select_frame_line_width,
                  self._line_size[1] + 2 * select_frame_line_width),
            colour=select_frame_colour)
        stimuli._stimulus.Stimulus._id_counter -= 1
        if background_stimulus is not None:
            if background_stimulus.__class__.__base__ in \
                    [stimuli._visual.Visual, stimuli.Shape]:
                self._background_stimulus = background_stimulus
            else:
                raise TypeError(f"{type(background_stimulus)} " +
                                "is not a valid background stimulus. " +
                                "Use an expyriment visual stimulus.")
        else:
            self._background_stimulus = None

        if mouse is True:
            self._mouse = _internals.active_exp.mouse
        elif isinstance(mouse, Mouse):
            self._mouse = mouse
        else:
            self._mouse = None

        self._canvas = stimuli.BlankScreen()
        stimuli._stimulus.Stimulus._id_counter -= 1
        self._original_items = menu_items
        self._menu_items = []
        for item in menu_items:
            self._menu_items.append(stimuli.TextBox(item,
                text_size=text_size, text_font=text_font,
                text_justification=justification,
                size=self._line_size))
            stimuli._stimulus.Stimulus._id_counter -= 1
        self._heading = stimuli.TextLine(
            heading,
            text_size=text_size,
            text_font=heading_font,
            text_colour=heading_text_colour,
            text_bold=True,
            background_colour=self._bkg_colours[0]) ## changes Florian TODO
        stimuli._stimulus.Stimulus._id_counter -= 1

    @property
    def heading(self):
        """Getter for heading"""
        return self._heading

    @property
    def menu_items(self):
        """Getter for menu_items"""
        return self._menu_items

    @property
    def position(self):
        """Getter for position"""
        return self._position

    @property
    def text_size(self):
        """Getter for text_size"""
        return self._heading.text_size

    @property
    def background_colour(self):
        """Getter for background_colour"""
        return self._bkg_colours[0]

    @property
    def select_background_colour(self):
        """Getter for select_background_colour"""
        return self._bkg_colours[1]

    @property
    def gap(self):
        """Getter for gap"""
        return self._gap

    @property
    def text_colour(self):
        """Getter for text_colour"""
        return self._text_colours[0]

    @property
    def select_text_colour(self):
        """Getter for select_text_colour"""
        return self._text_colours[1]

    @property
    def heading_text_colour(self):
        """Getter for heading_text_colour"""
        return self._heading.text_colour

    @property
    def select_frame_colour(self):
        """Getter for select_frame_colour"""
        return self._frame.colour

    @property
    def select_frame_line_width(self):
        """Getter for select_frame_line_width"""
        return self._frame.line_width

    @property
    def justification(self):
        """Getter for justification"""
        return self._heading.text_justification

    @property
    def scroll_menu(self):
        """Getter for scroll_menu"""
        return self._scroll_menu

    @property
    def background_stimulus(self):
        """Getter for background_stimulus"""
        return self._background_stimulus

    def _append_item(self, item, is_selected, y_position):
        """helper function"""
        item.clear_surface()
        item.position = (self._position[0], y_position + self._position[1])
        if is_selected:
            item.background_colour = self._bkg_colours[1]
            item.text_colour = self._text_colours[1]
        else:
            item.background_colour = self._bkg_colours[0]
            item.text_colour = self._text_colours[0]
        item.plot(self._canvas)

    def _redraw(self, selected_item):
        """helper function"""
        if self._scroll_menu > 0:
            n = self._scroll_menu
        else:
            n = len(self._menu_items)
        self._canvas.clear_surface()
        if self._background_stimulus is not None:
            self._background_stimulus.plot(self._canvas)
        y_pos = int(((1.5 + n) * self._line_size[1]) + (n * self._gap)) // 2
        self._heading.position = (self._position[0], y_pos + self._position[1])
        self._heading.plot(self._canvas)
        y_pos = y_pos - int(0.5 * self._line_size[1])

        if self._scroll_menu == 0:
            for cnt, item in enumerate(self._menu_items):
                y_pos -= (self._line_size[1] + self._gap)
                self._append_item(item, cnt == selected_item, y_pos)
                if cnt == selected_item:
                    self._frame.position = (0, y_pos)
        else:  # scroll menu
            for cnt in range(selected_item - self._scroll_menu // 2,
                             selected_item + 1 + self._scroll_menu // 2):
                y_pos -= (self._line_size[1] + self._gap)
                if cnt >= 0 and cnt < len(self._menu_items):
                    self._append_item(self._menu_items[cnt],
                                      cnt == selected_item,
                                      y_pos)
                    if cnt == selected_item:
                        self._frame.position = (0, y_pos)

        if self._frame.line_width > 0:
            self._frame.plot(self._canvas)
        self._canvas.present()

    def get(self, preselected_item=0):
        """Present the menu and return the selected item.

        Parameters
        ----------
        preselected_item : int, optional
            item that is preselected when showing menu

        Returns
        -------
        selected : int
            integer representing the selected item in the list

        """

        selected = preselected_item
        # Keyboard
        if self._mouse is None:
            while True:
                self._redraw(selected)
                key = Keyboard().wait()[0]
                if key == misc.constants.K_UP:
                    selected -= 1
                elif key == misc.constants.K_DOWN:
                    selected += 1
                elif key in misc.constants.K_ALL_DIGITS and\
                        key > misc.constants.K_0:
                    selected = key - misc.constants.K_1
                elif key == misc.constants.K_RETURN:
                    break
                if selected < 0:
                    selected = 0
                elif selected >= len(self._menu_items):
                    selected = len(self._menu_items) - 1
            return selected
        # Mouse
        else:
            while True:
                pressed = None
                self._redraw(selected)
                event, pos, rt = self._mouse.wait_press()
                if self._scroll_menu == 0:
                    for cnt in range(len(self._menu_items)):
                        if 0 <= cnt < len(self._menu_items):
                            if self._menu_items[cnt].overlapping_with_position(pos):
                                pressed = cnt
                else:
                    for cnt in range(selected-self._scroll_menu // 2,
                                     selected+1+self._scroll_menu // 2):
                        if 0 <= cnt < len(self._menu_items):
                            if self._menu_items[cnt].overlapping_with_position(pos):
                                pressed = cnt
                if pressed is not None:
                    if pressed == selected and event <=2:
                        # selected and not mouse wheel
                        break
                    else:
                        selected = pressed
            return self._original_items[pressed]


    @staticmethod
    def _demo(exp=None):
        if exp is None:
            from .. import control
            control.set_develop_mode(True)
            control.defaults.event_logging = 0
            _exp = control.initialise()
        menu = TextMenu(heading="Expyriment TextMenu",
                        menu_items=["Items 1", "Items 1", "Items 3",
                                    "Items 4", "Items 5"],
                        width=250, select_frame_line_width = 5)
        print(menu.get())
