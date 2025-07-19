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

import expyriment

from .. import _internals, control, design, io, misc, stimuli
from ..design import randomise
from ..misc import constants, list_fonts, statistics, unicode2byte
from ..misc._timer import get_time
from . import defaults, end, initialise, start_audiosystem, stop_audiosystem


def _histogram(data):
    """Returns the hist of the data (list of numbers) as dict and
    as string representation

    """

    hist = {}
    for x in data: # make histogram
        x = round(x)
        if x in hist:
            hist[x] += 1
        else:
            hist[x] = 1
    #make string representation
    hist_str = ""
    str1 = None
    for x in range(min(hist.keys()), max(hist.keys())+1):
        if str1 is None:
            str1 = "dRT: "
            str2 = "  n: "
        str1 += f"{x:4d}"
        value = hist.get(x, 0)
        str2 += f"{value:4d}"
        if x % 10 == 0:
            hist_str += f"{str1}\n{str2}\n\n"
            str1 = None

    if str1 is not None:
        hist_str += f"{str1}\n{str2}\n\n"
    return hist, hist_str

def _stimulus_timing(exp):
    """Test the timing of stimulus presentation."""

    def _test1():
        info = """This will test the visual stimulus presentation timing specifics of your system.
During the test, you will see two squares on the screen.
After the test, you will be asked to indicate which (if any) of those two squares were flickering.

[Press RETURN to continue]"""

        text = stimuli.TextScreen("Visual stimulus presentation test", info)
        text.present()
        key, rt_ = exp.keyboard.wait([constants.K_RETURN])
        message = stimuli.TextScreen("Running", "Please wait...")
        message.present()
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

        s1 = stimuli.Canvas(exp.screen.size)  # fullscreen transparent
        s2 = stimuli.Canvas(exp.screen.size)  # fullscreen transparent
        s1.preload()
        s2.preload()
        to_do_time = list(range(0,25)) + list(range(100,125)) + \
                     list(range(200,225)) + list(range(300,325))
        randomise.shuffle_list(to_do_time)
        actual_time = []
        for x in to_do_time:
            s1.present(clear=False)
            start = get_time()
            exp.clock.wait(x)
            s2.present(clear=False)
            actual_time.append((get_time() - start) * 1000)
            exp.clock.wait(randomise.rand_int(30, 60))

        # determine refresh rate
        s = stimuli.Circle(0, colour=exp.background_colour)  # 1 px
        s.preload()
        frame_times = []
        for _x in range(300):
            start = get_time()
            s.present(clear=False)
            frame_times.append(get_time() - start)

        # account for dropped frames and rate limiting
        valid_frame_times = []
        for c, x in enumerate(frame_times[2:]):  # ignore first two frames
            if c > 0 and x / statistics.mean(valid_frame_times) > 1.5:
                pass
            else:
                valid_frame_times.append(x)
        refresh_rate = 1000 / (statistics.mean(valid_frame_times) * 1000)

        def has_peaks(data):
            cv = statistics.std(data) / statistics.mean(data)
            return cv > 1

        def get_local_peak(presentation_time, refresh_rate, spread=25):
            refresh_time = 1000 / refresh_rate
            multiples = presentation_time / refresh_time
            spread = spread / 100
            if abs(multiples) % 1 < spread or abs(multiples) % 1 > 1 - spread:
                return round(multiples) * refresh_time
            else:
                return None

        # show histogram of presentation delays
        def expected_delay(presentation_time, refresh_rate):
            refresh_time = 1000 / refresh_rate
            if refresh_time >= 1:
                return refresh_time - (presentation_time % refresh_time)
            else:
                return 0

        # delay = map(lambda x: x[1]- x[0], zip(to_do_time, actual_time))
        diff = [x[0] - x[1] for x in zip(actual_time, to_do_time)]
        unexplained_delay = [x[1]- x[0] - expected_delay(x[0], refresh_rate) \
                             for x in zip(to_do_time, actual_time)]
        hist, hist_str = _histogram(unexplained_delay)
        inaccuracies = []
        delayed_presentations_accurate = 0
        delayed_presentations_inaccurate = 0
        if os.environ.get("XPY_TESTSUITE_EXPERIMENTAL"):
            peaks = has_peaks(hist.values())
        else:
            peaks = False
        for key in list(hist.keys()):
            peak = get_local_peak(key, refresh_rate)
            if peaks and peak is not None:
                inaccuracies.extend(
                    [abs(round(peak) - key)] * hist[key])
            else:
                inaccuracies.extend(
                    [key % max(1, (1000 / refresh_rate))] * hist[key])
            if key != 0:
                if key % int(misc.py2_round(1000 / refresh_rate)) == 0:
                    delayed_presentations_accurate += hist[key]
                else:
                    delayed_presentations_inaccurate += hist[key]
        inaccuracy = int(misc.py2_round(sum(inaccuracies) / len(inaccuracies)))
        delayed_accurate = int(misc.py2_round(
            100 * delayed_presentations_accurate/len(to_do_time)))
        delayed_inaccurate = int(misc.py2_round(
            100 * delayed_presentations_inaccurate/len(to_do_time)))

        respkeys = {constants.K_F1:0, constants.K_F2:1, constants.K_F3:2,
                    constants.K_0:0, constants.K_1:1, constants.K_2:2,
                    constants.K_KP0:0, constants.K_KP1:1, constants.K_KP2:2}
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
        if int(misc.py2_round(refresh_rate))  < 50 or \
                int(misc.py2_round(refresh_rate)) > 360:
            results1_colour = [255, 0, 0]
        elif int(misc.py2_round(refresh_rate)) not in (60, 75, 120, 144, 240):
            results1_colour = [255, 255, 0]
        else:
            results1_colour = [0, 255, 0]
        r = f"{int(misc.py2_round(refresh_rate))} Hz (~ every {misc.py2_round(1000/refresh_rate, 1)} ms)"
        results1 = stimuli.TextScreen(
            "", f"Estimated Screen Refresh Rate:     {r}\n\n",
            text_font="freemono", text_size=int(16 * scaling), text_bold=True,
            text_justification=0, text_colour=results1_colour,
            position=(0, int(40 * scaling)))
        if response !=1:
            results2_colour = [255, 0, 0]
        else:
            results2_colour = [0, 255, 0]
        results2 = stimuli.TextScreen(
            "",
            f"Detected Framebuffer Pages:        {response+1}\n\n",
            text_font="freemono", text_size=int(16 * scaling), text_bold=True,
            text_justification=0, text_colour=results2_colour,
            position=(0, int(20 * scaling)))
        if inaccuracy > round(refresh_rate / 4):
            results3_colour = [255, 0, 0]
        elif 0 < inaccuracy <= round(refresh_rate / 4):
            results3_colour = [255, 255, 0]
        else:
            results3_colour = [0, 255, 0]
        results3 = stimuli.TextScreen(
            "",
            f"Average Reporting Inaccuracy:      {inaccuracy} ms\n\n",
            text_font="freemono", text_size=int(16 * scaling), text_bold=True,
            text_justification=0, text_colour=results3_colour,
            position=(0, -int(20 * scaling)))
        if delayed_accurate <= 5:
            results5_colour = [0, 255, 0]
        elif delayed_accurate > 5:
            results5_colour = [255, 255, 0]
        if delayed_inaccurate > 10:
            results6_colour = [255, 0, 0]
        elif 10 >= delayed_inaccurate > 1:
            results6_colour = [255, 255, 0]
        else:
            results6_colour = [0, 255, 0]
        if [255, 0, 0] in (results5_colour, results6_colour):
            results4_colour = [255, 0, 0]
        elif [255, 255, 0] in (results5_colour, results6_colour):
            results4_colour = [255, 255, 0]
        else:
            results4_colour = [0, 255, 0]
        results4 = stimuli.TextScreen(
            "",
            f"Unexplained Presentation Delays:   {delayed_accurate + delayed_inaccurate} %\n\n\n",
            text_font="freemono", text_size=int(16 * scaling), text_bold=True,
            text_justification=0, text_colour=results4_colour,
            position=(0, -int(60 * scaling)))
        results5 = stimuli.TextScreen(
            "",
            "........... Accurately Reported:{}{:>3} %\n\n\n".format(
                " " * (len(str(delayed_accurate + delayed_inaccurate))),
                delayed_accurate),
            text_font="freemono", text_size=int(16 * scaling), text_bold=False,
            text_justification=0, text_colour=results5_colour,
            position=(0, -int(80 * scaling)))
        results6 = stimuli.TextScreen(
            "",
            "......... Inaccurately Reported:{}{:>3} %\n\n\n".format(
                " " * (len(str(delayed_accurate + delayed_inaccurate))),
                delayed_inaccurate),
            text_font="freemono", text_size=int(16 * scaling), text_bold=False,
            text_justification=0, text_colour=results6_colour,
            position=(0, -int(100 * scaling)))
        results7 = stimuli.TextScreen(
            "", hist_str, text_font="freemono", text_size=int(16 * scaling),
            text_bold=True, text_justification=0,
            position=(0, -int(160 * scaling)))

        results1.plot(info)
        results2.plot(info)
        results3.plot(info)
        results4.plot(info)
        results5.plot(info)
        results6.plot(info)
        results7.plot(info)
        info2 = stimuli.TextLine("[Press RETURN to continue]",
                                 position=(0, -int(160 * scaling)))
        info2.plot(info)
        while True:
            info.present()
            key, rt_ = exp.keyboard.wait([constants.K_RETURN])
            if key is not None:
                break
        return (to_do_time, actual_time, refresh_rate, inaccuracy,
                delayed_accurate, delayed_inaccurate, response)

    return _test1()


def _audio_playback(exp):
    """Test the audio playback"""

    info = """This will test the auditory stimulus presentation capabilities of your system.
You will be asked to select the audio device, format, and buffer size to test.
Afterwards, a test tone will be played back to you with the chosen settings.

[Press RETURN to continue]
"""
    text = stimuli.TextScreen("Auditory stimulus presentation test", info)
    while True:
        text.present()
        key, rt_ = exp.keyboard.wait([constants.K_RETURN])
        if key is not None:
            break

    # Get audio device
    options = misc.get_audio_devices()
    menu = io.TextMenu("Audio device", menu_items=options)
    audio_device = options[menu.get()]

    # Get sample rate
    sample_rates = (22050, 44100, 48000, 88200, 96000, 192000)
    bit_depths = ((8, "8-bit signed integer (8-bit audio)"),
                 (-8, "8-bit unsigned integer (uncommon)"),
                 (16, "16-bit signed integer (uncommon)"),
                 (-16, "16-bit unsigned integer (16-bit audio)"),
                 (32, "32-bit floating point (23-bit float audio)"))
    channel_counts = (1, 2, 4 ,6)

    buffer_sizes = [32, 64, 128, 256, 512, 1024, 2048, 4096]

    # Scale fonts/logo according to default font size
    scaling = exp.text_size / 20
    if scaling < 1:
        scaling = 1
    if scaling > 2:
        scaling = 2

    # Get samplerate, bitrate for common parameters
    common = [(sample_rates[1], bit_depths[3], channel_counts[1]),
              (sample_rates[2], bit_depths[3], channel_counts[1])]
    default = control.defaults.audiosystem_sample_rate
    if default in [x[0] for x in common]:
        index = [x[0] for x in common].index(default)
    else:
        index = 2
    options = [f"{x[0]} Hz, {abs(x[1][0])}-bit, {x[2]} ch" for x in common]
    options.append("Other")
    menu = io.TextMenu("Audio format", menu_items=options)
    selection = menu.get(index)
    if selection < 2:
        audio_format = common[selection]
    else:
        audio_format = []
        # Get custom samplerate
        default = control.defaults.audiosystem_sample_rate
        if default in sample_rates:
            index = sample_rates.index(default)
        else:
            index = 0
        menu = io.TextMenu("Sample rate",
                           menu_items=[f"{x}" for x in sample_rates])
        audio_format.append(sample_rates[menu.get(index)])
        # Get custom bit depth
        default = control.defaults.audiosystem_bit_depth
        if default in [x[0] for x in bit_depths]:
            index = [x[0] for x in bit_depths].index(default)
        else:
            index = 0
        menu = io.TextMenu("Bit depth",
                           menu_items=[f"{x[0]}" for x in bit_depths])
        audio_format.append(bit_depths[menu.get(index)])
        # Get channels
        default = control.defaults.audiosystem_channels
        if default in channel_counts:
            index = channel_counts.index(default)
        else:
            index = 0
        menu = io.TextMenu("Channels",
                           menu_items=[f"{x}" for x in channel_counts])
        audio_format.append(channel_counts[menu.get(index)])

    ch = "channel"
    if audio_format[2] > 1:
        ch += "s"

    # Test if audio format is supported
    try:
        stop_audiosystem()
        pygame.mixer.pre_init(audio_format[0], audio_format[1][0],
                              audio_format[2], allowedchanges=0)
        start_audiosystem()
    except Exception:
        info = f"""'{audio_device}' does not support '{audio_format[0]} Hz, {audio_format[1][1]}, {audio_format[2]} {ch}'.

[Press RETURN to continue]
        """
        text = stimuli.TextScreen("Audio format not supported", info)
        while True:
            text.present()
            key, rt_ = exp.keyboard.wait([constants.K_RETURN])
            if key is not None:
                break
            return None
        return "", ""

    # Get buffer size
    options = [f"{x}" for x in buffer_sizes]
    default = control.defaults.audiosystem_buffer_size
    if default in buffer_sizes:
        index = buffer_sizes.index(default)
    else:
        index = 0
    menu = io.TextMenu("Buffer size", menu_items=options)
    buffer_size = buffer_sizes[menu.get(index)]

    info = f"""A test tone will now be played on '{audio_device}' with format '{audio_format[0]} Hz, {audio_format[1][1]}, {audio_format[2]} {ch}' and a buffer of {buffer_size} samples.

[Press RETURN to continue]
"""
    text = stimuli.TextScreen("Audio playback test", info)
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
    text = stimuli.TextScreen("Did you hear the tone clearly and undistorted?",
                              "[Press Y or N]")
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

    default_text = """The quick brown fox jumps over the lazy dog.
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
        font_description = f"font '{font_str}', size {size}"
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
                f"{font_description}",
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

    sorted_keys = sorted(results.keys())
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
        exec(f"classes = dir({module})", namesspace)
        for cl in namesspace['classes']:
            if not cl.startswith("_") and cl not in ["False", "None", "True"]:
                exec(f"method = dir({module}.{cl})", namesspace)
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
    from .._internals import get_version
    from ..design import extras as _test1
    from ..io import extras as _test3
    from ..misc import extras as _test4
    from ..misc import get_system_info
    from ..stimuli import extras as _test2

    quit_experiment = False
    if not _internals.active_exp.is_initialised:
        defaults.initialise_delay = 0
        defaults.event_logging = 0
        exp = design.Experiment()
        exp.testsuite = True
        initialise(exp)
        quit_experiment = True
    else:
        exp = _internals.active_exp

    # make menu and code for test functions
    test_functions = ['', '', '']
    menu = ["1) Visual stimulus presentation",
            "2) Auditory stimulus presentation",
            "3) Font Viewer"]
    for mod, cl in _find_self_tests():
        test_functions.append(f"rtn = {mod}.{cl}._self_test(exp)")
        menu.append(f"{len(test_functions)}) {cl} test")

    menu.append(f"{len(test_functions) + 1}) Write protocol")
    menu.append(f"{len(test_functions) + 2}) Quit")
    test_functions.extend(['rtn = _write_protocol(exp, results)',
                            'go_on=False;rtn=[];'])

    # Scale fonts/logo according to default font size
    scaling = exp.text_size / 20

    background = stimuli.Canvas(size=[int(800 * scaling), int(600 * scaling)])
    pict = stimuli.Picture(constants.EXPYRIMENT_LOGO_FILE,
                           position=(0, int(220 * scaling)))
    pict.scale(0.3 * scaling)
    pict.plot(background)

    v = stimuli.TextLine(f"Version {get_version()}",
                         text_size=int(10 * scaling),
                         text_colour=constants.C_EXPYRIMENT_PURPLE)
    v.move((0, int(160 * scaling)))
    v.plot(background)
    results = get_system_info()

    if misc.is_android_running():
        mouse = io.Mouse(show_cursor=False)
    else:
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
            results["testsuite_visual_timing_delayed_accurate"] = \
                str(rtn[4]) + " %"
            results["testsuite_visual_timing_delayed_inaccurate"] = \
                str(rtn[5]) + " %"
            results["testsuite_visual_flipping_user"] = rtn[6]
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
    return results
    return results
