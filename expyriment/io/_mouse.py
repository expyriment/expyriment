"""
Mouse input.

This module contains a class implementing pygame mouse input.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import pygame

import defaults
import expyriment
from expyriment.misc._timer import get_time
from _keyboard import Keyboard
from _input_output  import Input

_detect_quit_event = None

class Mouse(Input):
    """A class implementing a mouse input.

    Calling `expyriment.control.intialize(exp)` will automatically create a
    mouse instance and will reference it in exp.mouse for easy access.

    """

    def __init__(self, show_cursor=True, track_button_events=None,
                 track_motion_events=None, quit_click_rect_size=None,
                 quit_rect_location=None):
        """Initialize a mouse input.

        Notes
        -----

        Parameters
        ----------
        show_cursor : bool, optional
            shows mouse cursor (default = True)
        track_button_events : bool, optional
            track button events via Pygame queue (default = True)
        track_motion_events : bool, optional
            track motion events via Pygame queue (default = False)
        quit_click_rect_size : tuple (int, int), optional
            the size of the field (rect) that detects the quit action by
            triple clicking in one corner of the screen.
            Only relevant, if "mouse quit event" is used. (default = (30, 30))
        quit_rect_location = int, optional
            the location of the quit click action field.  Only relevant, if
            "mouse quit event" is used. (default = 1)
            0 = upper left corner,  1 = upper right corner   (0) (1)
            2 = lower right corner, 3 = lower left corner    (3) (2)

        Notes
        -----
        (a) It is strongly suggest to avoid tracking of motions events,
        (track_motion_events=True), because it quickly causes an overflow in
        the Pygame event queue and you might consequently loose important
        events.

        (b) If "mouse quit events" is switched on, clicking quickly three times
        (i.e., within 1 second) in one of the corners of the screen forces
        the experiment to quit (default left corner, see `quit_rect_location`
        parameter). This function is especially useful for experiments on
        devices without hardware keyboard, such as tablet PCs or smartphones.

        The "mouse quit event" function is switch on per default, only under
        Android. To switch on/off in the function manually set the property
        `detect_quit_event`.

        """

        Input.__init__(self)
        self._quit_action_events = []
        self.detect_quit_event = expyriment.control.is_android_running()
        if show_cursor is None:
            show_cursor = defaults.mouse_show_cursor
        if track_button_events is None:
            track_button_events = defaults.mouse_track_button_events
        if track_motion_events is None:
            track_motion_events = defaults.mouse_track_motion_events
        if show_cursor:
            self.show_cursor(track_button_events, track_motion_events)
        else:
            self.track_button_events = track_button_events
            self.track_motion_events = track_motion_events
        if quit_click_rect_size is None:
            quit_click_rect_size = defaults.mouse_quit_click_rect_size
        if quit_rect_location is None:
            quit_rect_location = defaults.mouse_quit_rect_location
        self.quit_click_rect_size = quit_click_rect_size
        self.quit_rect_location = quit_rect_location

    def _process_mouse_quit_event(self, click_position=None):
        """Check if mouse exit action has been performed

        Parameters
        ----------
        click_position : tuple of int (x,y), optional
            the position to be processed. If no position is defined, the
            function checks if a button up event is in the pygame event
            queue. So if, the current mouse position will be use to estimate
            the click location.

        Returns
        -------
        out : bool, optional
            True if exit action has been performed
            False otherwise

        Notes
        -----
        For more information see documentation of property "detect_quit_event"

        """

        if _detect_quit_event==False:
            return False
        if click_position is None:
            # check event queue for button event
            pygame.event.pump()
            btn_recently_pressed = False
            for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                if event.button==1:
                    btn_recently_pressed = True
            if btn_recently_pressed:
                return self._process_mouse_quit_event(self.position)
        else:
            # determine threshold x & y
            if self.quit_rect_location == 0 or self.quit_rect_location == 3: # left
                threshold_x = -expyriment._active_exp.screen.center_x + \
                        self.quit_click_rect_size[0]
            else:# right
                threshold_x = expyriment._active_exp.screen.center_x - \
                        self.quit_click_rect_size[0]
            if self.quit_rect_location == 0 or self.quit_rect_location == 1: # upper
                threshold_y = expyriment._active_exp.screen.center_y - \
                        self.quit_click_rect_size[1]
            else:# lower
                threshold_y = -expyriment._active_exp.screen.center_y + \
                        self.quit_click_rect_size[1]
            # check
            if (self.quit_rect_location == 0 and \
                    click_position[0] < threshold_x and\
                    click_position[1] > threshold_y) \
               or (self.quit_rect_location == 1 and \
                    click_position[0] > threshold_x and \
                    click_position[1] > threshold_y) \
               or (self.quit_rect_location == 2 and \
                    click_position[0] > threshold_x and \
                    click_position[1] < threshold_y) \
               or (self.quit_rect_location == 3 and \
                    click_position[0] < threshold_x and \
                    click_position[1] < threshold_y):

                self._quit_action_events.append(get_time())
                if len(self._quit_action_events)>=3:
                    diff = get_time()-self._quit_action_events.pop(0)
                    if (diff<1):
                        # simulate quit key
                        simulated_key = pygame.event.Event(pygame.KEYDOWN,\
                                    {'key': Keyboard.get_quit_key()})
                        return Keyboard.process_control_keys(
                            key_event=simulated_key)
        return False


    @property
    def track_button_events(self):
        """Getter for track_button_events."""

        return self._track_button_events

    @track_button_events.setter
    def track_button_events(self, value):
        """Setter for track_button_events.

        Switch on/off the processing of button and wheel events.

        """

        self._track_button_events = value
        if value:
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        else:
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            pygame.event.set_blocked(pygame.MOUSEBUTTONUP)

    @property
    def track_motion_events(self):
        """Getter for track_motion_events.

        Switch on/off the buffering of motion events in the Pygame event queue.

        Notes
        -----
        It is strongly suggest to avoid tracking of motions events,
        (track_motion_events=True), because it quickly causes an overflow in
        the Pygame event queue and you might consequently loose important
        events.

        """

        return self._track_motion_events

    @track_motion_events.setter
    def track_motion_events(self, value):
        """Setter for track_motion_events.

        Switch on/off the processing of motion events.

        """

        self._track_motion_events = value
        if value:
            pygame.event.set_allowed(pygame.MOUSEMOTION)
        else:
            pygame.event.set_blocked(pygame.MOUSEMOTION)

    @property
    def detect_quit_event(self):
        """Getter for detect_quit_event.

        Switch on/off the detection of mouse quit events.
        This property is global property and affects all mouse instances.

        Notes
        -----
        Under Android, the "mouse quit event" function is switch on per
        default. Further information, see the init function in the class
        documentation of Mouse.


        """

        return _detect_quit_event

    @detect_quit_event.setter
    def detect_quit_event(self, value):
        """Setter for detect_quit_event.

        Switch on/off detection of mouse quit events
        This property is global property.

        """

        global _detect_quit_event
        _detect_quit_event = value

    @property
    def pressed_buttons(self):
        """Getter for pressed buttons."""

        pygame.event.pump()
        return pygame.mouse.get_pressed()

    @property
    def is_cursor_visible(self):
        """returns if cursor is visible"""

        visible = pygame.mouse.set_visible(False)
        pygame.mouse.set_visible(visible)
        return visible

    def get_last_button_down_event(self):
        """Get the last button down event.
        All earlier button down events will be removed from the queue.

        Returns
        -------
        btn_id : int
            button number (0,1,2) or 3 for wheel up or 4 for wheel down,
            if quit screen mouse action has been performed, the method
            returns -1

        """

        rtn = None
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if event.button > 0:
                rtn = event.button - 1
        if rtn==0 and _detect_quit_event:
            if self._process_mouse_quit_event(self.position):
                return -1
        return rtn

    def get_last_button_up_event(self):
        """Get the last button up event.
        All earlier button up and down events will be removed from the
        queue.


        Returns
        -------
        btn_id : int
            button number (0,1,2)
            if quit screen mouse action has been performed, the method
            returns -1

        """

        rtn = None
        for event in pygame.event.get(pygame.MOUSEBUTTONUP):
            if event.button > 0:
                rtn = event.button - 1
        if self._process_mouse_quit_event():
            return -1
        return rtn

    def check_button_pressed(self, button_number):
        """Return (True/False) if a specific button is currently pressed.

        Returns
        -------
        btn_id : int
            button number (0,1,2)

        """

        btns = self.pressed_buttons
        if len(btns) >= 1 and button_number >= 0:
            return btns[button_number]
        else:
            return False

    def check_wheel(self):
        """Check the mouse wheel.

        Returns
        -------
        direction : str
            "up" or "down" if mouse wheel has been recently rotated
            upwards or downwards otherwise it returns None.

        """

        evt = self.get_last_button_down_event()
        if evt == 3:
            return "up"
        elif evt == 4:
            return "down"
        else:
            return None

    @property
    def position(self):
        """Getter of mouse position."""

        pygame.event.pump()
        screen_size = expyriment._active_exp.screen.surface.get_size()
        pos = pygame.mouse.get_pos()
        return (pos[0] - screen_size[0] / 2, -pos[1] + screen_size[1] / 2)

    @position.setter
    def position(self, position):
        """Setter for mouse position."""

        screen_size = expyriment._active_exp.screen.surface.get_size()
        pos = (position[0] + screen_size[0] / 2,
               - position[1] + screen_size[1] / 2)
        pygame.mouse.set_pos(pos)

    def set_cursor(self, size, hotspot, xormasks, andmasks):
        """Set the cursor.

        Parameters
        ----------
        size : (int, int)
            size of the cursor
        hotspot : (int, int)
            position of the hotspot (0,0 is top left)
        xormask : list
            sequence of bytes with cursor xor data masks
        andmask : list
            sequence of bytes with cursor bitmask data

        """

        return pygame.mouse.set_cursor(size, hotspot, xormasks, andmasks)

    def get_cursor(self):
        """Get the cursor."""

        return pygame.mouse.get_cursor()

    def clear(self):
        """Clear the event cue from mouse events."""

        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        pygame.event.clear(pygame.MOUSEBUTTONUP)
        pygame.event.clear(pygame.MOUSEMOTION)
        if self._logging:
            expyriment._active_exp._event_file_log("Mouse,cleared", 2)


    def wait_event(self, wait_button=True, wait_motion=True, buttons=None,
                   duration=None, wait_for_buttonup=False):
        """Wait for a mouse event (i.e., motion, button press or wheel event)

        Parameters
        ----------
        wait_button : bool, optional
            set 'False' to ignore for a button presses (default=True)
        wait_motion : bool, optional
            set 'False' to ignore for a mouse motions (default=True)
        buttons : int or list, optional
            a specific button or list of buttons to wait for
        duration : int, optional
            the maximal time to wait in ms
        wait_for_buttonup : bool, optional
            if True it waits for button-up default=False)

        Returns
        -------
        event_id : int
            id of the event that quited waiting
        move : bool
            True if a motion occured
        pos : (int, int)
            mouse position (tuple)
        rt : int
            reaction time

        Notes
        ------
        button id coding

        - None    for no mouse button event or
        - 0,1,2   for left. middle and right button or
        - 3       for wheel up or
        - 4       for wheel down (wheel works only for keydown events).

        """

        if expyriment.control.defaults._skip_wait_functions:
            return None, None, None, None
        start = get_time()
        self.clear()
        old_pos = pygame.mouse.get_pos()
        btn_id = None
        rt = None
        motion_occured = False
        if buttons is None:
            buttons = [0, 1, 2, 3, 4]
        if type(buttons) is not list:
            buttons = [buttons]
        while True:
            expyriment._active_exp._execute_wait_callback()
            if wait_motion:
                motion_occured = old_pos != pygame.mouse.get_pos()
            if wait_button:
                if wait_for_buttonup:
                    btn_id = self.get_last_button_up_event()
                else:
                    btn_id = self.get_last_button_down_event()
            if btn_id ==-1:
                btn_id = None
                break
            elif btn_id in buttons or motion_occured:
                rt = int((get_time() - start) * 1000)
                break
            elif Keyboard.process_control_keys() or (duration is not None and \
                    int((get_time() - start) * 1000) >= duration):
                break

        position_in_expy_coordinates = self.position

        if self._logging:
            expyriment._active_exp._event_file_log(
            "Mouse,received,{0}-{1},wait_event".format(btn_id, motion_occured))
        return btn_id, motion_occured, position_in_expy_coordinates, rt


    def wait_press(self, buttons=None, duration=None, wait_for_buttonup=False):
        """Wait for a mouse button press or mouse wheel event.

        Parameters
        ----------
        buttons : int or list, optional
            a specific button or list of buttons to wait for
        duration : int, optional
            maximal time to wait in ms
        wait_for_buttonup : bool, optional
            if True it waits for button-up

        Returns
        -------
        event_id : int
            id of the event that quited waiting
        pos : (int, int)
            mouse position (tuple)
        rt : int
            reaction time

        Notes
        ------
        button id coding

        - None    for no mouse button event or
        - 0,1,2   for left. middle and right button or
        - 3       for wheel up or
        - 4       for wheel down (wheel works only for keydown events).

        """

        rtn = self.wait_event(wait_button=True, wait_motion=False,
                              buttons=buttons, duration=duration,
                              wait_for_buttonup=wait_for_buttonup)
        return rtn[0], rtn[2], rtn[3]

    def wait_motion(self, duration=None):
        """Wait for a mouse motion.

        Parameters
        ----------
        duration : int, optional
            maximal time to wait in ms

        Returns
        -------
        pos : (int, int)
            mouse position (tuple)
        rt : int
            reaction time


        """

        rtn = self.wait_event(wait_button=False, wait_motion=True, buttons=[],
                        duration=duration, wait_for_buttonup=False)
        return rtn[2], rtn[3]


    def show_cursor(self, track_button_events=True, track_motion_events=False):
        """Show the cursor.

        Parameters
        ----------
        track_button_events : bool, optional
            tracking button events (default = True)
        track_motion_events : bool, optional
            tracking motion events (default = False)

        """

        pygame.mouse.set_visible(True)
        self.track_button_events = track_button_events
        self.track_motion_events = track_motion_events

    def hide_cursor(self, track_button_events=False, track_motion_events=False):
        """Hide the cursor.

        Parameters
        ----------
        track_button_events : bool, optional
            tracking button events (default = True)
        track_motion_events : bool, optional
            tracking motion events (default = False)

        """

        pygame.mouse.set_visible(False)
        self.track_button_events = track_button_events
        self.track_motion_events = track_motion_events


    @staticmethod
    def _self_test(exp):
        """Test the mouse.

        Returns
        -------
        polling_time : int
            polling time
        buttons_work : int
            1 -- if mouse test was ended with mouse button,
            0 -- if testing has been quit with q

        """

        # measure mouse polling time
        info = """This will test how timing accurate your mouse is.

[Press RETURN to continue]"""

        expyriment.stimuli.TextScreen("Mouse test (1)", info).present()
        exp.keyboard.wait(expyriment.misc.constants.K_RETURN)
        mouse = expyriment.io.Mouse()
        go = expyriment.stimuli.TextLine("Keep on moving...")
        go.preload()
        expyriment.stimuli.TextLine("Please move the mouse").present()
        mouse.wait_motion()
        go.present()
        exp.clock.reset_stopwatch()
        motion = []
        while exp.clock.stopwatch_time < 200:
            _pos, rt = mouse.wait_motion()
            motion.append(rt)
        expyriment.stimuli.TextLine("Thanks").present()
        polling_time = expyriment.misc.statistics.mode(motion)

        info = """Your mouse polling time is {0} ms.

[Press RETURN to continue] """.format(polling_time)
        text = expyriment.stimuli.TextScreen("Results", info)
        text.present()
        exp.keyboard.wait([expyriment.misc.constants.K_RETURN])

        info = """This will test if you mouse buttons work.
Please press all buttons one after the other to see if the corresponding buttons on the screen light up.
When done, click inside one of the buttons on the screen to end the test.
If your mouse buttons do not work, you can quit by pressing q.

[Press RETURN to continue]"""

        expyriment.stimuli.TextScreen("Mouse test (2)", info).present()
        exp.keyboard.wait(expyriment.misc.constants.K_RETURN)

        # test mouse clicking
        rects = [expyriment.stimuli.Rectangle(size=[30, 30], position=[-50, 0]),
                 expyriment.stimuli.Rectangle(size=[30, 30], position=[0, 0]),
                 expyriment.stimuli.Rectangle(size=[30, 30], position=[50, 0])]
        canvas = expyriment.stimuli.Canvas(size=[350, 500])
        btn = None
        go_on = True
        while go_on:
            canvas.clear_surface()
            for cnt, r in enumerate(rects):
                r.unload()
                if cnt == btn:
                    r.colour = expyriment.misc.constants.C_YELLOW
                else:
                    r.colour = expyriment.misc.constants.C_RED
                r.plot(canvas)

            if btn == 3:
                text = "Mouse wheel UP"
            elif btn == 4:
                text = "Mouse wheel DOWN"
            else:
                text = ""
            expyriment.stimuli.TextLine(text, position=[0, 50]).plot(canvas)
            canvas.present()
            btn = None
            while btn is None:
                btn = mouse.get_last_button_down_event()
                if btn is not None:
                    position = mouse.position
                    for r in rects:
                        if r.overlapping_with_position(position):
                            buttons_work = 1
                            mouse.hide_cursor()
                            go_on = False
                            break
                elif exp.keyboard.check(keys=expyriment.misc.constants.K_q):
                    buttons_work = 0
                    mouse.hide_cursor()
                    go_on = False
                    break

        result = {}
        result["testsuite_mouse_polling_time"] = str(polling_time) + " ms"
        result["testsuite_mouse_buttons_work"] = buttons_work
        return result

