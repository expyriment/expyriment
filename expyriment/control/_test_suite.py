"""The expyriment testsuite.

This module contains several functions to test the machine expyriment is
running on.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os

import pygame
try:
    import OpenGL.GL as ogl
except:
    ogl = None

import defaults

import expyriment
from expyriment import stimuli, io
from expyriment.misc import constants, statistics
from expyriment.misc._timer import get_time


def _make_graph(x, y, colour):
    """Make the graph."""

    graph = stimuli.Canvas(size=(max(x) * 3 + 10, max(y) * 3 + 10))
    for counter in range(len(x)):
        dot = stimuli.Dot(radius=1, colour=colour)
        dot.position = (x[counter] * 3 - graph.size[0] / 2 + 5,
                        y[counter] * 3 - graph.size[1] / 2 + 5)
        dot.plot(graph)
    return graph


def _stimulus_timing(exp):
    """Test the timing of stimulus presentation."""

    def _test1():
        info = """This will test if stimuli can be presented timing accurately.
The left picture shows a good result, the right picture shows a bad result.

[Press RETURN to continue]"""
        text = stimuli.TextScreen("Stimulus presentation test (1)", info)
        y = []
        for x in [16, 32, 48, 64]:
            y.extend([x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, ])
        graph1 = _make_graph(range(60), y, [0, 255, 0])
        y = range(80)
        graph2 = _make_graph(range(60), y, [255, 0, 0])
        graph1.position = (-200, -100)
        graph2.position = (200, -100)
        text.present(update=False)
        graph1.present(clear=False, update=False)
        graph2.present(clear=False)
        exp.keyboard.wait([constants.K_RETURN])
        exp.screen.clear()
        exp.screen.update()
        cnvs = stimuli.FixCross(cross_size=200, line_width=3)
        picture = stimuli.Rectangle((100, 100))
        cnvs.preload()
        picture.preload()
        todo_time = []
        actual_time = []
        for x in range(200):
            todo_time.append(expyriment.design.randomize.rand_int(0, 60))
            picture.present()
            start = exp.clock.time
            exp.clock.wait(todo_time[-1])
            cnvs.present()
            actual_time.append(exp.clock.time - start)
            exp.clock.wait(expyriment.design.randomize.rand_int(30, 100))
        text = stimuli.TextScreen("Results", "[Press RETURN to continue]")
        graph = _make_graph(todo_time, actual_time, [150, 150, 150])
        graph.position = (0, -100)
        text.present(update=False)
        graph.present(clear=False)
        exp.keyboard.wait([constants.K_RETURN])
        text = stimuli.TextScreen(
            "Which picture looks most similar to the results?",
            "[Press LEFT or RIGHT arrow key]")
        y = []
        for x in [16, 32, 48, 64]:
            y.extend([x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, ])
        graph1 = _make_graph(range(60), y, [0, 255, 0])
        y = range(80)
        graph2 = _make_graph(range(60), y, [255, 0, 0])
        graph1.position = (-200, -100)
        graph2.position = (200, -100)
        text.present(update=False)
        graph1.present(clear=False, update=False)
        graph2.present(clear=False)
        key, _rt = exp.keyboard.wait([constants.K_LEFT,
                                     constants.K_RIGHT])
        if key == constants.K_LEFT:
            response1 = "Steps"
        elif key == constants.K_RIGHT:
            response1 = "Line"

        return todo_time, actual_time, response1


    def _test2():
        info = """This will test if stimulus presentation can be synchronized to the refreshrate of the screen.
A good result is a fast, constant and smooth flickering without any distortions (e.g. horizontal stripes, tearing).
The estimated refreshrate should resemble your actual screen refreshrate (common refreshrates are between 40 and 240 Hz).

[Press RETURN to continue]"""

        text = stimuli.TextScreen("Stimulus presentation test (2)", info)
        text.present()
        exp.keyboard.wait([constants.K_RETURN])
        black = stimuli.BlankScreen(colour=constants.C_BLACK)
        black.preload()
        white = stimuli.BlankScreen(colour=constants.C_WHITE)
        white.preload()
        times = []
        black.present()
        for _x in range(100):
            start = get_time()
            black.present()
            times.append(get_time() - start)
            start = get_time()
            white.present()
            times.append(get_time() - start)
        refresh_rate = 1000 / (statistics.mean(times) * 1000)
        info = """Your estimated refresh rate is {0} Hz.

[Press RETURN to continue]
""".format(refresh_rate)
        text = stimuli.TextScreen("Results", info)
        text.present()
        exp.keyboard.wait([constants.K_RETURN])
        text = stimuli.TextScreen(
            "Was the flickering fast, constant and smooth, without any distortions?",
            "[Press Y or N]")
        text.present()
        key, _rt = exp.keyboard.wait([constants.K_y,
                                      constants.K_n])
        if key == constants.K_y:
            response2 = "Yes"
        elif key == constants.K_n:
            response2 = "No"

        return refresh_rate, response2

    def _test3():
        info = """This will test the video card's settings for multiple buffers and page flipping.
If none of the following squares are constantly blinking, page flipping is not activated and buffer contents are copied.
If only the left square is constantly blinking, page flipping is activated and a double buffer is used.
If additionally the right square is constantly blinking, page flipping is activated and a tripple buffer is used.

[Press RETURN to continue]"""

        text = stimuli.TextScreen("Stimulus presentation test (3)", info)
        text.present()
        exp.keyboard.wait([constants.K_RETURN])
        c1 = stimuli.Canvas((400, 400))
        c2 = stimuli.Canvas((400, 400))
        c3 = stimuli.Canvas((400, 400))
        frame1 = stimuli.Rectangle((100, 100), position=(-100, 0))
        frame2 = stimuli.Rectangle((100, 100), position=(100, 0))
        bg = stimuli.Rectangle((90, 90), colour=exp.background_colour)
        bg.plot(frame1)
        bg.plot(frame2)
        frame1.plot(c1)
        frame2.plot(c2)
        frame1.plot(c3)
        frame2.plot(c3)
        c1.preload()
        c2.preload()
        c3.preload()
        c1.present()
        c2.present()
        c3.present()
        for _x in range(50):
            d = stimuli.Dot(1, colour=(1, 1, 1))
            d.present(clear=False)
            exp.clock.wait(100)
        text = stimuli.TextScreen(
            "How many squares were constantly blinking?",
            "[Press 0, 1 or 2]")
        text.present()
        key, _rt = exp.keyboard.wait([constants.K_0,
                                      constants.K_1,
                                      constants.K_2])
        if key == constants.K_0:
            response3 = 0
        elif key == constants.K_1:
            response3 = 1
        elif key == constants.K_2:
            response3 = 2

        return (response3,)

    return _test1() + _test2() + _test3()


def _audio_playback(exp):
    """Test the audio playback"""

    info = """This will test the audio playback. A test tone will be played.

[Press RETURN to continue]
"""
    text = stimuli.TextScreen("Audio playback test", info)
    text.present()
    exp.keyboard.wait([constants.K_RETURN])
    exp.screen.clear()
    exp.screen.update()
    a = stimuli.Tone(duration=1000)
    a.present()
    exp.clock.wait(1000)
    text = stimuli.TextScreen("Did you hear the tone?", "[Press Y or N]")
    text.present()
    key, _rt = exp.keyboard.wait([constants.K_y,
                                 constants.K_n])
    if key == constants.K_y:
        response = "Yes"
    elif key == constants.K_n:
        response = "No"

    return response

def _font_viewer(exp):
    all_fonts = expyriment.misc.list_fonts().keys()

    def info_screen():
        stimuli.TextScreen(heading="Expyriment Font Viewer",
            text="""
arrow keys left/right -- Switch font type
arrow keys up/down    -- Switch font size
                  i   -- Switch italic
                  b   -- Switch bold
                  c   -- Change text
                  h   -- Help
               return -- Quit


                 [Touch screen]
click left/right side --  Switch font type
click up/down side    --  Switch font size
click center          --  Quit
               """,
            text_font="freemono", text_bold=True,
            text_justification=0).present()
        exp.keyboard.wait()


    default_text = """The quick brown fox jumps over the lazy dog.
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
1234567890.:,;(*!?')"""
    text = default_text
    size = 14
    font_id = 0
    italic = False
    bold = False
    quest = io.TextInput(message="Please enter text: (Keep empty for default text)", length=35)
    mouse = io.Mouse(show_cursor=True)

    bs = (exp.screen.size[0] / 3.5, exp.screen.size[1] / 3.5)

    # rects center, left, right, top, button]
    cl = (20, 20, 20)
    rects = [stimuli.Rectangle(size=bs, position=[0, 0], colour=cl),
             stimuli.Rectangle(size=bs, position=[(bs[0] - exp.screen.size[0]) / 2.2, 0], colour=cl),
             stimuli.Rectangle(size=bs, position=[(exp.screen.size[0] - bs[0]) / 2.2, 0], colour=cl),
             stimuli.Rectangle(size=bs, position=[0, (bs[1] - exp.screen.size[1]) / 2.2], colour=cl),
             stimuli.Rectangle(size=bs, position=[0, (exp.screen.size[1] - bs [1]) / 2.2], colour=cl)]
    rect_key_mapping = [constants.K_RETURN, constants.K_LEFT, constants.K_RIGHT,
                        constants.K_UP, constants.K_DOWN]

    info_screen()
    while True:
        font_str = all_fonts[font_id]
        font_description = "font '{0}', size {1}".format(font_str, size)
        if italic:
            font_description += ", italic"
        if bold:
            font_description += ", bold"

        canvas = stimuli.BlankScreen()
        for r in rects:
            r.plot(canvas)
        try:
            stimuli.TextScreen(
                heading=font_description,
                text=text,
                text_font=font_str, text_size=size,
                text_justification=0,
                text_italic=italic,
                text_bold=bold,
                text_colour=(255, 255, 255)).plot(canvas)
        except:
            stimuli.TextLine(text="Sorry, I can't display the text with " +
                "{0}".format(font_description),
                text_colour=constants.C_EXPYRIMENT_ORANGE).plot(canvas)
        canvas.present()
        mouse.clear()
        exp.keyboard.clear()
        while True:
            key = exp.keyboard.check()
            if mouse.get_last_button_down_event() is not None:
                for cnt, r in enumerate(rects):
                    if r.overlapping_with_position(mouse.position):
                        print cnt
                        key = rect_key_mapping[cnt]
                        break
            if key is not None:
                break

        if (key == constants.K_RETURN):
            break
        elif key == constants.K_UP:
            size += 2
        elif key == constants.K_DOWN:
            size -= 2
        elif key == constants.K_LEFT:
            font_id -= 1
            if font_id < 0:
                font_id = len(all_fonts) - 1
        elif key == constants.K_RIGHT:
            font_id += 1
            if font_id >= len(all_fonts):
                font_id = 0
        elif key == constants.K_i:
            italic = not(italic)
        elif key == constants.K_b:
            bold = not(bold)
        elif key == constants.K_c:
            text = quest.get()
            if len(text) <= 0:
                text = default_text
        else:
            info_screen()
    mouse.hide_cursor()


def _write_protocol(exp, results):
    """Write a protocol with all test results."""

    sorted_keys = results.keys()
    sorted_keys.sort()
    rtn = ""
    for key in sorted_keys:
        tabs = "\t" * (4 - int((len(key) + 1) / 8)) + "\t"
        try:
            rtn += key + ":" + tabs + results[key] + "\n"
        except TypeError:
            rtn += key + ":" + tabs + repr(results[key]) + "\n"

    filename = os.path.join(os.getcwd(), "test_suite_protocol.xpp")
    with open(filename, 'w') as f:
        f.write(rtn)
    text = stimuli.TextScreen(
        "Saved as",
        '"' + filename + '"' + "\n\n[Press RETURN to continue]")
    text.present()
    exp.keyboard.wait(constants.K_RETURN)
    return []  # required for event loop

def _find_self_tests():
    classes = []
    method = []
    rtn = []
    for module in ["expyriment.io", "expyriment.io.extras"]:
        exec("classes = dir({0})".format(module))
        for cl in classes:
            if not cl.startswith("_"):
                exec("method = dir({0}.{1})".format(module, cl))
                if "_self_test" in method:
                    rtn.append([module, cl])
    return rtn

def run_test_suite():
    """Run the Expyriment test suite."""

    quit_experiment = False
    if not expyriment._active_exp.is_initialized:
        defaults.initialize_delay = 0
        defaults.event_logging = 0
        exp = expyriment.control.initialize()
        quit_experiment = True
    else:
        exp = expyriment._active_exp

    # make menu and code for test functions
    test_functions = ['', '', '']
    menu = ["1) Visual stimulus presentation",
            "2) Auditory stimulus presentation",
            "3) Font Viewer"]
    for mod, cl in _find_self_tests():
        test_functions.append("rtn = {0}.{1}._self_test(exp)".format(mod, cl))
        menu.append("{0}) {1} test".format(len(test_functions), cl))

    menu.append("{0}) Write protocol".format(len(test_functions) + 1))
    menu.append("{0}) Quit".format(len(test_functions) + 2))
    test_functions.extend(['rtn = _write_protocol(exp, results)',
                            'go_on=False;rtn=[];'])

    background = stimuli.Canvas(size=[400, 600])
    pict = stimuli.Picture(constants.EXPYRIMENT_LOGO_FILE, position=(0, 200))
    pict.scale(0.5)
    pict.plot(background)

    results = expyriment.get_system_info()

    try:
        import android
        mouse = expyriment.io.Mouse(show_cursor=False)
    except ImportError:
        android = None
        mouse = None

    preselected_item = 0
    go_on = True
    while go_on:
        select = expyriment.io.TextMenu(
            "Test suite", menu, width=350, justification=0,
            background_stimulus=background, mouse=mouse).get(preselected_item)

        if select == 0:
            rtn = _stimulus_timing(exp)
            results["testsuite_visual_timing_todo"] = rtn[0]
            results["testsuite_visual_timing_actual"] = rtn[1]
            results["testsuite_visual_timing_user"] = rtn[2]
            results["testsuite_visual_sync_refresh_rate"] = str(rtn[3]) + " Hz"
            results["testsuite_visual_sync_user"] = rtn[4]
            results["testsuite_visual_flipping_user"] = rtn[5]
            if ogl is not None:
                results["testsuite_visual_opengl_vendor"] = ogl.glGetString(ogl.GL_VENDOR)
                results["testsuite_visual_opengl_renderer"] = ogl.glGetString(ogl.GL_RENDERER)
                results["testsuite_visual_opengl_version"] = ogl.glGetString(ogl.GL_VERSION)
                results["testsuite_visual_pygame_driver"] = pygame.display.get_driver()
                extensions = ogl.glGetString(ogl.GL_EXTENSIONS).split(" ")
                if extensions[-1] == "":
                    extensions = extensions[:-1]
                results["testsuite_visual_opengl_extensions"] = extensions
            else:
                results["testsuite_visual_opengl_vendor"] = ""
                results["testsuite_visual_opengl_renderer"] = ""
                results["testsuite_visual_opengl_version"] = ""
                results["testsuite_visual_pygame_driver"] = ""
                results["testsuite_visual_opengl_extensions"] = ""
            results["testsuite_visual_pygame_driver"] = pygame.display.get_driver()
            results["testsuite_visual_pygame_screensize"] = exp.screen.size
            preselected_item = select + 1
        elif select == 1:
            results["testsuite_audio_user"] = _audio_playback(exp)
            try:
                results["testsuite_audio_frequency"] = str(pygame.mixer.get_init()[0]) + " Hz"
                results["testsuite_audio_bitdepth"] = str(abs(pygame.mixer.get_init()[1])) + " bit"
                results["testsuite_audio_channels"] = pygame.mixer.get_init()[2]
            except:
                presults["testsuite_audio_frequency"] = ""
                results["testsuite_audio_bitdepth"] = ""
                results["testsuite_audio_channels"] = ""
            preselected_item = select + 1
        elif select == 2:
            _font_viewer(exp)
            preselected_item = select + 1
        else:
            exec(test_functions[select])
            results.update(rtn)
            preselected_item = select + 1

    if quit_experiment:
        expyriment.control.end(goodbye_delay=0, goodbye_text="Quitting test suite")
