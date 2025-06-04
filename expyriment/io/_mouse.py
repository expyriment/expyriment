"""
Mouse input.

This module contains a class implementing pygame mouse input.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import time
from types import FunctionType

import pygame

from . import defaults
from ..misc._timer import get_time
from ..misc import is_android_running
from ._input_output  import Input
from .. import _internals, misc

class Mouse(Input):
    """A class implementing a mouse input.

    Calling ``expyriment.control.initialize(exp)`` will automatically create a
    mouse instance and will reference it in exp.mouse for easy access.

    """

    #static class properties for quit_events
    _quit_corner_location = None
    _corner_rect_size = (30, 30)
    _quit_action_events = []


    def __init__(self, show_cursor=True, track_button_events=None,
                 track_motion_events=None):
        """Initialize a mouse input.

        Parameters
        ----------
        show_cursor : bool, optional
            shows mouse cursor (default = True)
        track_button_events : bool, optional
            track button events via Pygame queue (default = True)
        track_motion_events : bool, optional
            track motion events via Pygame queue (default = False)

        Notes
        -----
        (a) It is strongly suggest to avoid tracking of motions events,
        (track_motion_events=True), because it quickly causes an overflow in
        the Pygame event queue and you might consequently loose important
        events.

        (b) Turning the mouse wheel causes button_down_events. Thus,
        turning the mouse wheel rather extensively causes an overflow of
        the Pygame event queue. You might consider turn off the default
        tracking of mouse button event by calling
        `experiment.mouse.track_button_events = False`.

        (c) See ``process_quit_event`` for the forced quitting of experiments
        via mouse events.

        """

        Input.__init__(self)
        if is_android_running():
            Mouse._quit_corner_location = 1
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

    @staticmethod
    def set_quit_corner_location(corner, corner_rect_size=(None, None)):
        """Activate the possibility to quit experiment using a mouse event.

        Defines the corner on which the user has to click to elicit a
        quit dialog.

        If quit corner location has been defined, clicking quickly three
        times (i.e., within 1 second) in the specified corner forces
        experiment to quit.

        To switch off the detection of mouse quit events, please call
        ``Mouse.set_quit_corner_location(corner=None)``.

        Changing the corner and rect_size always affects all mouse
        instances.

        Parameters
        ----------
        corner: int or None
            location code (0,1, 2 or 3) of the quit corner; the default value
            under Android is 1, otherwise None; see also the notes
            below.

       corner_rect_size = tuple (int, int), optional
            size of the field (rect) that detects the quit action in one
            corner of the screen; default = (30, 30)

        Notes
        -----
        Mouse quit events are especially useful for experiments on devices
        without hardware keyboard, such as tablet PCs or smartphones.

        Corner location codes::

                0 = upper left corner,  1 = upper right corner   (0) (1)
                2 = lower right corner, 3 = lower left corner    (3) (2)
                otherwise the detection of mouse quit events is deactivated

        The detection of mouse quit events is activated by default under
        Android.

        """

        if corner is not None:
            if not isinstance(corner, int) or corner<0 or corner >3:
                corner = None
                print("Warning: {} is an unknown corner location. Mouse quit "
                                     "event is deactivated.".format(corner))
        Mouse._quit_corner_location = corner

        try:
            Mouse._corner_rect_size = (int(corner_rect_size[0]),
                                       int(corner_rect_size[1]))
        except Exception:
            pass

    @staticmethod
    def process_quit_event(click_position=None, event_detected_function=None,
                           quit_confirmed_function=None,
                           quit_denied_function=None):
        """Check if mouse exit action has been performed.

        If quit corner location is has been defined via
        ``Mouse.set_quit_corner_location()``  (i.e. 0, 1, 2 or 3), clicking
        quickly three times (i.e., within 1 second) in one of the corners of
        the screen forces the experiment to quit.

        The function is called automatically by all mouse get event and wait
        methods (similar to ``Keyboard.process_control_keys``).  If no mouse
        functions are called by your program, this function can be polled to
        ensure quitting experiment by mouse.

        Parameters
        ----------
        click_position : tuple of int (x,y), optional
            clicked location to be processed. If not defined, the Pygame event
            queue will be checked for mouse down events and the current
            position is taken
        event_detected_function : function, optional
            function to be called when key event is detected.
        quit_confirmed_function : function, optional
            function to be called if quitting has been confirmed.
        quit_denied_function : function, optional
            function to be called if quitting has been denied.


        Returns
        -------
        out : bool, optional
            True if exit action has been performed
            False otherwise

        See Also
        --------
        set_quit_corner_location

        """

        if Mouse._quit_corner_location not in (0, 1, 2, 3):
            return False

        if click_position is None:
            # check Pygame queue
            pos = None
            # pygame.event.pump() # not sure if it is required!
            for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                if event.button > 0:
                    screen_size = _internals.active_exp.screen.surface.get_size()
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0] - screen_size[0] // 2,
                          -pos[1] + screen_size[1] // 2)
                    break
            if pos is None:
                return False
            else:
                return Mouse.process_quit_event(click_position=pos)

        # determine threshold x & y
        if Mouse._quit_corner_location == 0 or Mouse._quit_corner_location == 3: # left
            threshold_x = -_internals.active_exp.screen.center_x + \
                    Mouse._corner_rect_size[0]
        else:# right
            threshold_x = _internals.active_exp.screen.center_x - \
                    Mouse._corner_rect_size[0]
        if Mouse._quit_corner_location == 0 or Mouse._quit_corner_location == 1: # upper
            threshold_y = _internals.active_exp.screen.center_y - \
                    Mouse._corner_rect_size[1]
        else:# lower
            threshold_y = -_internals.active_exp.screen.center_y + \
                    Mouse._corner_rect_size[1]
        # check
        if (Mouse._quit_corner_location == 0 and \
            click_position[0] < threshold_x and \
            click_position[1] > threshold_y) \
           or (Mouse._quit_corner_location == 1 and \
               click_position[0] > threshold_x and \
               click_position[1] > threshold_y) \
           or (Mouse._quit_corner_location == 2 and \
               click_position[0] > threshold_x and \
               click_position[1] < threshold_y) \
           or (Mouse._quit_corner_location == 3 and \
               click_position[0] < threshold_x and \
               click_position[1] < threshold_y):

            Mouse._quit_action_events.append(get_time())
            if len(Mouse._quit_action_events)>=3:
                diff = get_time()-Mouse._quit_action_events.pop(0)
                if (diff < 1):
                    # simulate quit key
                    simulated_key = pygame.event.Event(
                        pygame.KEYDOWN,
                        {'key': _internals.active_exp.keyboard.get_quit_key()})
                    return _internals.active_exp.keyboard.process_control_keys(
                        key_event=simulated_key,
                        event_detected_function=event_detected_function,
                        quit_confirmed_function=quit_confirmed_function,
                        quit_detected_function=quit_denied_function)
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
    def pressed_buttons(self):
        """Getter for pressed_buttons."""

        pygame.event.pump()
        return pygame.mouse.get_pressed()

    @property
    def is_cursor_visible(self):
        """Getter for is_cursor_visible"""

        visible = pygame.mouse.set_visible(False)
        pygame.mouse.set_visible(visible)
        return visible

    def get_last_button_down_event(self, process_quit_event=True):
        """Get the last button down event.
        All earlier button down events will be removed from the queue.

        Parameters
        ----------
        process_quit_event : boolean, optional
            if False, the current location will not be processed for mouse
            quitting events in the case that a button down event has been
            found (default = True).

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
        if rtn==0:
            if process_quit_event and Mouse.process_quit_event(self.position):
                return -1
        return rtn

    def get_last_button_up_event(self):
        """Get the last button up event.
        All earlier button up events will be removed from the queue.

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
        return rtn

    def check_button_pressed(self, button_number):
        """Return False or button id if a specific button is currently pressed.

        Parameters
        ----------
        button_number : int
            the button number (0,1,2) to be checked

        Returns
        -------
        is_pressed: boolean

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
        """Getter for position."""

        pygame.event.pump()
        screen_size = _internals.active_exp.screen.surface.get_size()
        pos = pygame.mouse.get_pos()
        return (pos[0] - screen_size[0] // 2, -pos[1] + screen_size[1] // 2)

    @position.setter
    def position(self, position):
        """Setter for position."""

        screen_size = _internals.active_exp.screen.surface.get_size()
        pos = (position[0] + screen_size[0] // 2,
               - position[1] + screen_size[1] // 2)
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
            _internals.active_exp._event_file_log("Mouse,cleared", 2)


    def wait_event(self, wait_button=True, wait_motion=True, buttons=None,
                   duration=None, wait_for_buttonup=False,
                   callback_function=None, process_control_events=True,
                   low_performance=False):
        """Wait for a mouse event (i.e., motion, button press or wheel event).

        Button id coding:

        - None    for no mouse button event or
        - 0,1,2   for left. middle and right button or
        - 3       for wheel up or
        - 4       for wheel down (wheel works only for keydown events).

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
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.keyboard.process_control_keys()`` and
            ``io.mouse.process_quit_event()`` (default = True)
        low_performance : bool, optional
            reduce CPU performance (and allow potential threads to run) while
            waiting at the cost of less timing accuracy (default = False)

        Returns
        -------
        event_id : int
            id of the event that quited waiting
        move : bool
            True if a motion occurred
        pos : (int, int)
            mouse position (tuple)
        rt : int
            reaction time

        Notes
        ------
        This will also by default process control events (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a ``Keyboard().check()`` anymore!

        See Also
        --------
        expyriment.design.Experiment.register_wait_callback_function

        """

        if _internals.skip_wait_methods:
            return None, None, None, None
        start = get_time()
        self.clear()
        old_pos = pygame.mouse.get_pos()
        btn_id = None
        rt = None
        motion_occured = False
        if buttons is None:
            buttons = [0, 1, 2, 3, 4]
        else:
            try:
                buttons = list(buttons)
            except Exception:
                buttons = [buttons]
        while True:
            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    btn_id = rtn_callback
                    rt = int((get_time() - start) * 1000)
                    break
            if _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    btn_id = rtn_callback
                    rt = int((get_time() - start) * 1000)
                    break
                if process_control_events:
                    if _internals.active_exp.keyboard.process_control_keys():
                        break
            if wait_motion:
                motion_occured = old_pos != pygame.mouse.get_pos()
            if wait_button:
                if wait_for_buttonup:
                    btn_id = self.get_last_button_up_event()
                else:
                    btn_id = self.get_last_button_down_event(
                        process_quit_event=process_control_events)
            if btn_id ==-1:
                btn_id = None
                break
            elif btn_id in buttons or motion_occured:
                rt = int((get_time() - start) * 1000)
                break
            elif (duration is not None and \
                    int((get_time() - start) * 1000) >= duration):
                break
            if low_performance:
                time.sleep(0.0001)

        position_in_expy_coordinates = self.position

        if self._logging:
            _internals.active_exp._event_file_log(
            "Mouse,received,{0}-{1},wait_event".format(btn_id, motion_occured))
        return btn_id, motion_occured, position_in_expy_coordinates, rt


    def wait_press(self, buttons=None, duration=None, wait_for_buttonup=False,
                   callback_function=None, process_control_events=True,
                   low_performance=False):
        """Wait for a mouse button press or mouse wheel event.

        Parameters
        ----------
        buttons : int or list, optional
            a specific button or list of buttons to wait for
        duration : int, optional
            maximal time to wait in ms
        wait_for_buttonup : bool, optional
            if True it waits for button-up
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.keyboard.process_control_keys()`` and
            ``io.mouse.process_quit_event()`` (default = false)
        low_performance : bool, optional
            reduce CPU performance (and allow potential threads to run) while
            waiting at the cost of less timing accuracy (default = False)

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
                              wait_for_buttonup=wait_for_buttonup,
                              callback_function=callback_function,
                              process_control_events=process_control_events,
                              low_performance=low_performance)
        return rtn[0], rtn[2], rtn[3]

    def wait_motion(self, duration=None, callback_function=None,
                    process_control_events=True, low_performance=False):
        """Wait for a mouse motion.

        Parameters
        ----------
        duration : int, optional
            maximal time to wait in ms
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.keyboard.process_control_keys()`` and
            ``io.mouse.process_quit_event()`` (default = false)
        low_performance : bool, optional
            reduce CPU performance (and allow potential threads to run) while
            waiting at the cost of less timing accuracy (default = False)

        Returns
        -------
        pos : (int, int)
            mouse position (tuple)
        rt : int
            reaction time

        """

        rtn = self.wait_event(wait_button=False, wait_motion=True, buttons=[],
                              duration=duration, wait_for_buttonup=False,
                              callback_function=callback_function,
                              process_control_events=process_control_events,
                              low_performance=low_performance)

        if isinstance(rtn[0], _internals.CallbackQuitEvent):
            return rtn[0], rtn[3]
        else:
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
            tracking button events (default = False)
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

        from .. import stimuli
        # measure mouse polling time
        info = """This will test how timing accurate your mouse is.

[Press RETURN to continue]"""

        stimuli.TextScreen("Mouse test (1)", info).present()
        exp.keyboard.wait(misc.constants.K_RETURN)
        mouse = Mouse()
        go = stimuli.TextLine("Keep on moving...")
        go.preload()
        stimuli.TextLine("Please move the mouse").present()
        mouse.wait_motion()
        go.present()
        exp.clock.reset_stopwatch()
        motion = []
        while exp.clock.stopwatch_time < 200:
            _pos, rt = mouse.wait_motion()
            motion.append(rt)
        stimuli.TextLine("Thanks").present()
        polling_time = misc.statistics.mode(motion)

        info = """Your mouse polling time is {0} ms.

[Press RETURN to continue] """.format(polling_time)
        text = stimuli.TextScreen("Results", info)
        text.present()
        exp.keyboard.wait([misc.constants.K_RETURN])

        info = """This will test if you mouse buttons work.
Please press all buttons one after the other to see if the corresponding buttons on the screen light up.
When done, click inside one of the buttons on the screen to end the test.
If your mouse buttons do not work, you can quit by pressing q.

[Press RETURN to continue]"""

        stimuli.TextScreen("Mouse test (2)", info).present()
        exp.keyboard.wait(misc.constants.K_RETURN)

        # test mouse clicking
        rects = [stimuli.Rectangle(size=[30, 30], position=[-50, 0]),
                 stimuli.Rectangle(size=[30, 30], position=[0, 0]),
                 stimuli.Rectangle(size=[30, 30], position=[50, 0])]
        canvas = stimuli.Canvas(size=[350, 500])
        btn = None
        go_on = True
        while go_on:
            canvas.clear_surface()
            for cnt, r in enumerate(rects):
                r.unload()
                if cnt == btn:
                    r.colour = misc.constants.C_YELLOW
                else:
                    r.colour = misc.constants.C_RED
                r.plot(canvas)

            if btn == 3:
                text = "Mouse wheel UP"
            elif btn == 4:
                text = "Mouse wheel DOWN"
            else:
                text = ""
            stimuli.TextLine(text, position=[0, 50]).plot(canvas)
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
                elif exp.keyboard.check(keys=misc.constants.K_q):
                    buttons_work = 0
                    mouse.hide_cursor()
                    go_on = False
                    break

        result = {}
        result["testsuite_mouse_polling_time"] = str(polling_time) + " ms"
        result["testsuite_mouse_buttons_work"] = buttons_work
        return result

