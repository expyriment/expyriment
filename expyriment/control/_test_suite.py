# -*- coding: utf-8 -*-
"""The expyriment testsuite.

This module contains several functions to test the machine expyriment is
running on.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os

import pygame
try:
    import OpenGL.GL as ogl
except Exception:
    ogl = None

from . import defaults, initialize, end
from .. import stimuli, io, _internals, design, control
import expyriment

from .. import misc
from ..misc import constants, statistics, list_fonts, unicode2byte
from ..misc._timer import get_time
from ..design import randomize

def _make_graph(x, y, colour):
    """Make the graph."""

    graph = stimuli.Canvas(size=(max(x) * 3 + 10, max(y) * 3 + 10))
    for counter in range(len(x)):
        dot = stimuli.Dot(radius=1, colour=colour)
        dot.position = (x[counter] * 3 - graph.size[0] // 2 + 5,
                        y[counter] * 3 - graph.size[1] // 2 + 5)
        dot.plot(graph)
    return graph

def _histogram(data):
    """Returns the hist of the data (list of numbers) as dict and
    as string representation

    """

    hist = {}
    for x in data: # make histogram
        x = int(round(x))
        if x in hist:
            hist[x] += 1
        else:
            hist[x] = 1
    #make string representation
    hist_str = ""
    cnt = 0
    str1 = None
    for x in range(min(hist.keys()), max(hist.keys())+1):
        if str1 is None:
            str1 = "dRT: "
            str2 = "  n: "
        str1 += "%4d" % x
        if x in hist:
            value = hist[x]
        else:
            value = 0
        str2 += "%4d" % value
        if x % 10 == 0:
            hist_str += str1 + "\n" + str2 + "\n\n"
            str1 = None

    if str1 is not None:
        hist_str += str1 + "\n" + str2 + "\n\n"
    return hist, hist_str

def _stimulus_timing(exp):
    """Test the timing of stimulus presentation."""

    def _test1():
        info = """This will test the visual stimulus presentation timing specifics of your system.
During the test, you will see two squares on the screen.
After the test, you will be asked to indicate which (if any) of those two squares were flickering.

[Press RETURN to continue]"""

        text = stimuli.TextScreen("Visual stimulus presentation test", info)
        #y = []
        #for x in [16, 32, 48, 64]:
        #    y.extend([x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, ])
        #graph1 = _make_graph(range(60), y, [0, 255, 0])
        #y = range(80)
        #graph2 = _make_graph(range(60), y, [255, 0, 0])
        #graph1.position = (-200, -100)
        #graph2.position = (200, -100)
        while True:
            text.present()
        #graph1.present(clear=False, update=False)
        #graph2.present(clear=False)
            key, rt_ = exp.keyboard.wait([constants.K_RETURN])
            if key is not None:
                break
        message = stimuli.TextScreen("Running", "Please wait...")
        message.present()
        message.present()
        message.present()
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
        c1.present(clear=False)
        c2.present(clear=False)
        c3.present(clear=False)

        s1 = stimuli.Circle(1, colour=exp.background_colour)
        s2 = stimuli.Circle(1, colour=exp.background_colour)
        s1.preload()
        s2.preload()
        to_do_time = list(range(0, 60)) * 3
        randomize.shuffle_list(to_do_time)
        actual_time = []
        for x in to_do_time:
            s1.present(clear=False)
            start = get_time()
            exp.clock.wait(x)
            s2.present(clear=False)
            actual_time.append((get_time() - start) * 1000)
            exp.clock.wait(randomize.rand_int(30, 60))

        # determine refresh_rate
        tmp = []
        for _x in range(100):
            start = get_time()
            s1.present(clear=False)
            tmp.append(get_time() - start)
            start = get_time()
            s2.present(clear=False)
            tmp.append(get_time() - start)
        refresh_rate = 1000 / (statistics.mean(tmp) * 1000)

        #text = stimuli.TextScreen("Results", "[Press RETURN to continue]")
        #graph = _make_graph(to_do_time, actual_time, [150, 150, 150])
        #graph.position = (0, -100)
        #text.present(update=False)
        #graph.present(clear=False)
        #exp.keyboard.wait([constants.K_RETURN])
        #text = stimuli.TextScreen(
        #    "Which picture looks most similar to the results?",
        #    "[Press LEFT or RIGHT arrow key]")
        #y = []
        #for x in [16, 32, 48, 64]:
        #    y.extend([x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, ])
        #graph1 = _make_graph(range(60), y, [0, 255, 0])
        #y = range(80)
        #graph2 = _make_graph(range(60), y, [255, 0, 0])
        #graph1.position = (-200, -100)
        #graph2.position = (200, -100)
        #text.present(update=False)
        #graph1.present(clear=False, update=False)
        #graph2.present(clear=False)
        #key, _rt = exp.keyboard.wait([constants.K_LEFT,
        #                             constants.K_RIGHT])
        #if key == constants.K_LEFT:
        #    response1 = "Steps"
        #elif key == constants.K_RIGHT:
        #    response1 = "Line"
        #else:
        #    response1 = None


        # show histogram of presentation delays
        def expected_delay(presentation_time, refresh_rate):
            refresh_time = 1000 / refresh_rate
            if refresh_time >= 1:
                return refresh_time - (presentation_time % refresh_time)
            else:
                return 0
        # delay = map(lambda x: x[1]- x[0], zip(to_do_time, actual_time))
        unexplained_delay = [x[1]- x[0] - expected_delay(x[0], refresh_rate) for x in zip(to_do_time, actual_time)]
        hist, hist_str = _histogram(unexplained_delay)
        inaccuracies = []
        delayed_presentations = 0
        for key in list(hist.keys()):
            inaccuracies.extend([key % max(1, (1000 // refresh_rate))] * hist[key])
            if key != 0:
                delayed_presentations += hist[key]
        inaccuracy = int(misc.round( sum(inaccuracies)/ len(inaccuracies)))
        delayed = misc.round(100 * delayed_presentations/180.0, 2)

        respkeys = {constants.K_F1:0, constants.K_F2:1, constants.K_F3:2,
                    constants.K_0:0, constants.K_1:1, constants.K_2:2}
        text = stimuli.TextScreen(
            "How many of the two squares were flickering?",
            "[Press 0 (or F1), 1 (or F2), 2 (or F3)]")
        while True:
            text.present()
            key, _rt = exp.keyboard.wait(respkeys)
            if key is not None:
                break
        response = respkeys[key]

        # Scale fonts/logo according to default font size
        scaling = exp.text_size / 20
        if scaling < 1:
            scaling = 1
        if scaling > 2:
            scaling = 2

        info = stimuli.TextScreen("Results", "")
        if int(misc.round(refresh_rate))  < 50 or int(misc.round(refresh_rate)) > 360:
            results1_colour = [255, 0, 0]
        elif int(misc.round(refresh_rate)) not in (60, 75, 120, 144, 240):
            results1_colour = [255, 255, 0]
        else:
            results1_colour = [0, 255, 0]
        results1 = stimuli.TextScreen("",
                    "Estimated Screen Refresh Rate:     {0} Hz (~ every {1} ms)\n\n".format(
                        int(misc.round(refresh_rate)), misc.round(1000/refresh_rate, 2)),
                    text_font="freemono", text_size=int(16 * scaling), text_bold=True,
                    text_justification=0, text_colour=results1_colour, position=(0, int(40 * scaling)))
        results2 = stimuli.TextScreen("",
                    "Detected Framebuffer Pages:        {0}\n\n".format(response+1),
                    text_font="freemono", text_size=int(16 * scaling), text_bold=True,
                    text_justification=0, position=(0, int(20 * scaling)))
        if inaccuracy > 2:
            results3_colour = [255, 0, 0]
        elif inaccuracy in (1, 2):
            results3_colour = [255, 255, 0]
        else:
            results3_colour = [0, 255, 0]
        results3 = stimuli.TextScreen("",
                    "Average Reporting Inaccuracy:      {0} ms\n\n".format(inaccuracy),
                    text_font="freemono", text_size=int(16 * scaling), text_bold=True,
                    text_justification=0, text_colour=results3_colour, position=(0, -int(20 * scaling)))
        if delayed > 10:
            results4_colour = [255, 0, 0]
        elif 10 > delayed > 1:
            results4_colour = [255, 255, 0]
        else:
            results4_colour = [0, 255, 0]
        results4 = stimuli.TextScreen("",
                    "Unexplained Presentation Delays:   {0} %\n\n\n".format(delayed),
                    text_font="freemono", text_size=int(16 * scaling), text_bold=True,
                    text_justification=0, text_colour=results4_colour, position=(0, -int(40 * scaling)))
        results5 = stimuli.TextScreen("",
                    hist_str,
                    text_font="freemono", text_size=int(16 * scaling), text_bold=True,
                    text_justification=0, position=(0, -int(100 * scaling)))
        results1.plot(info)
        results2.plot(info)
        results3.plot(info)
        results4.plot(info)
        results5.plot(info)
        info2 = stimuli.TextLine("[Press RETURN to continue]", position=(0, -int(160 * scaling)))
        info2.plot(info)
        while True:
            info.present()
            key, rt_ = exp.keyboard.wait([constants.K_RETURN])
            if key is not None:
                break
        return to_do_time, actual_time, refresh_rate, inaccuracy, delayed, response



#     def _test2():
#         info = """This will test if stimulus presentation can be synchronized to the refreshrate of the screen.
# A good result is a fast, constant and smooth flickering without any distortions (e.g. horizontal stripes, tearing).
# The estimated refreshrate should resemble your actual screen refreshrate (common refreshrates are between 40 and 240 Hz).
#
# [Press RETURN to continue]"""
#
#         text = stimuli.TextScreen("Stimulus presentation test (2)", info)
#         text.present()
#         exp.keyboard.wait([constants.K_RETURN])
#         black = stimuli.BlankScreen(colour=constants.C_BLACK)
#         black.preload()
#         white = stimuli.BlankScreen(colour=constants.C_WHITE)
#         white.preload()
#         times = []
#         black.present()
#         for _x in range(100):
#             start = get_time()
#             black.present()
#             times.append(get_time() - start)
#             start = get_time()
#             white.present()
#             times.append(get_time() - start)
#         refresh_rate = 1000 / (statistics.mean(times) * 1000)
#         info = """Your estimated refresh rate is {0} Hz.
#
# [Press RETURN to continue]
# """.format(refresh_rate)
#         text = stimuli.TextScreen("Results", info)
#         text.present()
#         exp.keyboard.wait([constants.K_RETURN])
#         text = stimuli.TextScreen(
#             "Was the flickering fast, constant and smooth, without any distortions?",
#             "[Press Y or N]")
#         text.present()
#         key, _rt = exp.keyboard.wait([constants.K_y,
#                                       constants.K_n])
#         if key == constants.K_y:
#             response2 = "Yes"
#         elif key == constants.K_n:
#             response2 = "No"
#
#         return refresh_rate, response2

#     def _test2():
#         info = """This will test the video card's settings for multiple buffers and page flipping.
# If none of the following squares are constantly blinking, page flipping is not activated and buffer contents are copied.
# If only the left square is constantly blinking, page flipping is activated and a double buffer is used.
# If additionally the right square is constantly blinking, page flipping is activated and a triple buffer is used.
#
# [Press RETURN to continue]"""
#
#         text = stimuli.TextScreen("Visual stimulus presentation test (2)", info)
#         text.present()
#         exp.keyboard.wait([constants.K_RETURN])
#         c1 = stimuli.Canvas((400, 400))
#         c2 = stimuli.Canvas((400, 400))
#         c3 = stimuli.Canvas((400, 400))
#         frame1 = stimuli.Rectangle((100, 100), position=(-100, 0))
#         frame2 = stimuli.Rectangle((100, 100), position=(100, 0))
#         bg = stimuli.Rectangle((90, 90), colour=exp.background_colour)
#         bg.plot(frame1)
#         bg.plot(frame2)
#         frame1.plot(c1)
#         frame2.plot(c2)
#         frame1.plot(c3)
#         frame2.plot(c3)
#         c1.preload()
#         c2.preload()
#         c3.preload()
#         c1.present()
#         c2.present()
#         c3.present()
#         for _x in range(50):
#             d = stimuli.Dot(1, colour=(1, 1, 1))
#             d.present(clear=False)
#             exp.clock.wait(100)
#         text = stimuli.TextScreen(
#             "How many squares were constantly blinking?",
#             "[Press 0, 1 or 2]")
#         text.present()
#         key, _rt = exp.keyboard.wait([constants.K_0,
#                                       constants.K_1,
#                                       constants.K_2])
#         if key == constants.K_0:
#             response3 = 0
#         elif key == constants.K_1:
#             response3 = 1
#         elif key == constants.K_2:
#             response3 = 2
#
#         return (response3,)

    return _test1()


def _audio_playback(exp):
    """Test the audio playback"""

    audio_formats = []
    hz = (44100, 48000, 96000)
    bits = (-16, -24, -32)
    for x in bits:
        for y in hz:
            try:
                pygame.mixer.quit()
                pygame.mixer.pre_init(y, x, 2, 512, allowedchanges=pygame.AUDIO_ALLOW_FREQUENCY_CHANGE)
                pygame.mixer.init()
                audio_formats.append((y, x))
            except:
                break
    buffer_sizes = [32, 64, 128, 256, 512, 1024, 2048, 4096]

    # Scale fonts/logo according to default font size
    scaling = exp.text_size / 20
    if scaling < 1:
        scaling = 1
    if scaling > 2:
        scaling = 2

    # Get samplerate, bitrate
    options = [f"{x[0]} Hz, {x[1] * -1} bit" for x in audio_formats]
    default = (control.defaults.audiosystem_sample_rate,
               control.defaults.audiosystem_bit_depth)
    if default in audio_formats:
        index = audio_formats.index(default)
    else:
        index = 0
    menu = io.TextMenu("Audio format", menu_items=options)
    audio_format = audio_formats[menu.get(index)]

    # Get buffer size
    options = [f"{x} samples" for x in buffer_sizes]
    default = control.defaults.audiosystem_buffer_size
    if default in buffer_sizes:
        index = buffer_sizes.index(default)
    else:
        index = 0
    menu = io.TextMenu("Buffer size", menu_items=options)
    buffer_size = buffer_sizes[menu.get(index)]

    settings = \
        f"{audio_formats[0]} Hz, {audio_format[1]} bit, {buffer_size} samples"
    pygame.mixer.quit()
    pygame.mixer.pre_init(audio_format[0], audio_format[1], 2, buffer_size)
    pygame.mixer.init()
    pygame.mixer.init()

    info = f"""This will test the audio playback. A test tone will be played.

[Press RETURN to continue]
"""
    text = stimuli.TextScreen(f"Audio playback test [settings]", info)
    while True:
        text.present()
        key, rt_ = exp.keyboard.wait([constants.K_RETURN])
        if key is not None:
            break
    exp.screen.clear()
    exp.screen.update()
    a = stimuli.Tone(duration=1000)
    a.present()
    exp.clock.wait(1000)
    text = stimuli.TextScreen("Did you hear the tone?", "[Press Y or N]")
    while True:
        text.present()
        key, _rt = exp.keyboard.wait([constants.K_y,
                                      constants.K_n])
        if key is not None:
            break
    if key == constants.K_y:
        response = "Yes"
    elif key == constants.K_n:
        response = "No"

    return response, buffer_size

def _font_viewer(exp):
    all_fonts = list(list_fonts().keys())

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

    # Scale fonts/logo according to default font size
    scaling = exp.text_size / 20
    if scaling < 1:
        scaling = 1
    if scaling > 2:
        scaling = 2

    default_text = u"""The quick brown fox jumps over the lazy dog.
ABCDEFGHIJKLMNOPQRSTUVWXYZ ÄÖÜ
abcdefghijklmnopqrstuvwxyz äöü
1234567890.:,;ßéèê(*!?')"""
    text = default_text
    size = int(14 * scaling)
    font_id = 0
    italic = False
    bold = False
    quest = io.TextInput(message="Please enter text: (Keep empty for default text)", length=35)
    mouse = io.Mouse(show_cursor=True)

    bs = (exp.screen.size[0] // 3.5, exp.screen.size[1] // 3.5)

    # rects center, left, right, top, button]
    cl = (20, 20, 20)
    rects = [stimuli.Rectangle(size=bs, position=[0, 0], colour=cl),
             stimuli.Rectangle(size=bs,
                    position=[int((bs[0] - exp.screen.size[0])/ 2.2), 0],
                    colour=cl),
             stimuli.Rectangle(size=bs,
                    position=[int((exp.screen.size[0] - bs[0])/ 2.2), 0],
                    colour=cl),
             stimuli.Rectangle(size=bs,
                    position=[0, int((bs[1] - exp.screen.size[1])/2.2)],
                    colour=cl),
             stimuli.Rectangle(size=bs,
                    position=[0, int((exp.screen.size[1] - bs [1])/2.2)],
                    colour=cl)]
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
        except Exception:
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

    longest = 0
    for key in results.keys():
        longest = max(len(key), longest)

    sorted_keys = list(results.keys())
    sorted_keys.sort()
    rtn = ""
    for key in sorted_keys:
        tabs = " " * (longest - len(key)) + "\t"
        rtn += key + ":" + tabs + repr(results[key]) + "\n"

    filename = os.path.join(os.getcwd(), "test_suite_protocol.xpp")
    with open(filename, 'wb') as f:
        f.write(unicode2byte(rtn))
    while True:
        text = stimuli.TextScreen(
            "Saved as",
            '"' + filename + '"' + "\n\n[Press RETURN to continue]")
        text.present()
        key, rt_ = exp.keyboard.wait(constants.K_RETURN)
        if key is not None:
            break
    return []  # required for event loop

def _find_self_tests():
    classes = []
    method = []
    rtn = []
    namesspace = {}
    namesspace["expyriment"] = expyriment
    for module in ["expyriment.io", "expyriment.io.extras"]:
        exec("classes = dir({0})".format(module), namesspace)
        for cl in namesspace['classes']:
            if not cl.startswith("_") and not cl in ["False", "None", "True"]:
                exec("method = dir({0}.{1})".format(module, cl), namesspace)
                if "_self_test" in namesspace['method']:
                    rtn.append([module, cl])
    return rtn

def run_test_suite(item=None):
    """Run the Expyriment test suite.

    Parameters
    ----------
    item : int, optional
        the item to run; runs all tests if None (default=None)

    """

    # test imports
    from ..design import extras as _test1
    from ..stimuli import extras as _test2
    from ..io import extras as _test3
    from ..misc import extras as _test4
    from ..misc import get_system_info
    from .._internals import get_version

    quit_experiment = False
    if not _internals.active_exp.is_initialized:
        defaults.initialize_delay = 0
        defaults.event_logging = 0
        exp = design.Experiment()
        exp.testsuite = True
        initialize(exp)
        quit_experiment = True
    else:
        exp = _internals.active_exp

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

    # Scale fonts/logo according to default font size
    scaling = exp.text_size / 20
    if scaling < 1:
        scaling = 1
    if scaling > 2:
        scaling = 2

    background = stimuli.Canvas(size=[800, int(600 * scaling)])
    pict = stimuli.Picture(constants.EXPYRIMENT_LOGO_FILE,
                           position=(0, int(220 * scaling)))
    pict.scale(0.3 * scaling)
    pict.plot(background)

    v = stimuli.TextLine("Version {0}".format(get_version()),
                         text_size=int(10 * scaling),
                         text_colour=constants.C_EXPYRIMENT_PURPLE)
    v.move((0, int(160 * scaling)))
    v.plot(background)
    results = get_system_info()

    try:
        import android
        mouse = io.Mouse(show_cursor=False)
    except ImportError:
        android = None
        mouse = None

    preselected_item = 0
    go_on = True
    while go_on:
        if item is not None:
            go_on = False
            select = item
        else:
            select = io.TextMenu("Test suite", menu, justification=0,
                                 background_stimulus=background,
                                 mouse=mouse).get(preselected_item)

        if select == 0:
            rtn = _stimulus_timing(exp)
            results["testsuite_visual_timing_to_do"] = rtn[0]
            results["testsuite_visual_timing_actual"] = rtn[1]
            results["testsuite_visual_sync_refresh_rate"] = str(rtn[2]) + " Hz"
            results["testsuite_visual_timing_inaccuracy"] = str(rtn[3]) + " ms"
            results["testsuite_visual_timing_delayed"] = str(rtn[4]) + " %"
            results["testsuite_visual_flipping_user"] = rtn[5]
            delay = [x[1]-x[0] for x in zip(
                results["testsuite_visual_timing_to_do"],
                results["testsuite_visual_timing_actual"])]
            results["testsuite_visual_timing_delay_histogram"], _ = _histogram(
                delay)
            results["testsuite_visual_opengl"] = exp.screen.opengl
            if ogl is not None and exp.screen.opengl:
                results["testsuite_visual_opengl_vendor"] = ogl.glGetString(
                    ogl.GL_VENDOR).decode()
                results["testsuite_visual_opengl_renderer"] = ogl.glGetString(
                    ogl.GL_RENDERER).decode()
                results["testsuite_visual_opengl_version"] = ogl.glGetString(
                    ogl.GL_VERSION).decode()
                extensions = ogl.glGetString(
                    ogl.GL_EXTENSIONS).decode().split(" ")
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
            audio_results = _audio_playback(exp)
            results["testsuite_audio_user"] = audio_results[0]
            try:
                results["testsuite_audio_frequency"] = str(pygame.mixer.get_init()[0]) + " Hz"
                results["testsuite_audio_bitdepth"] = str(abs(pygame.mixer.get_init()[1])) + " bit"
                results["testsuite_audio_channels"] = pygame.mixer.get_init()[2]
                results["testsuite_audio_buffersize"] = audio_results[1]
            except Exception:
                results["testsuite_audio_frequency"] = ""
                results["testsuite_audio_bitdepth"] = ""
                results["testsuite_audio_channels"] = ""
                results["testsuite_audio_buffersize"] = ""
            preselected_item = select + 1
        elif select == 2:
            _font_viewer(exp)
            preselected_item = select + 1
        else:
            namesspace = {}
            namesspace.update(globals())
            namesspace.update(locals())
            exec(test_functions[select], namesspace)
            rtn = namesspace['rtn']
            results.update(rtn)
            if 'go_on' in namesspace:
                go_on = namesspace['go_on']
            preselected_item = select + 1
            namesspace = None

    if quit_experiment:
        end(goodbye_delay=0, goodbye_text="Quitting test suite")
    else:
        exp.screen.clear()
        exp.screen.update()

    return results
