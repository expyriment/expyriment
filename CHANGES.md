Expyriment Release Notes
========================

Coming up
---------
New Features:
- Expyriment is now based on Pygame 2 (using SDL 2) and depends also on
  numpy & mediadecoder
- It's no longer necessary to install additional features via pip with
  `[feature]`, since all dependencies are installed by default.
- test suite:
    - option to run single tests
    - improvements in reporting visual timing test results
    - improved audio test
    - format changes in saved protocol
- command line interface:
    - option ``-I`` starts an interactive session
    - option ``--display`` defines which display to show the (fullscreen)
      window on
    - option ``--display-resolution`` sets the fullscreen resolution to use
      (overwrites automatically detected maximal display resolution)
    - option ``--text-size`` sets the default experiment text size (as defined
      in ``design.defaults.experiment_text_size``)
    - option ``--window-size`` sets the default size of the window (when using
      window-mode)
-  all wait methods have new parameter ``low_performance`` which allows for
   other threads to be processed while waiting (at the cost of accuracy)
- control.Keyboard.process_control_events:
    - new parameter ``event_detected_function`` to set a function that is
      called as soon as a quit event is detected (but before the end function
      is called)
    - new parameter ``quit_denied_function`` to set a function that is called
      when a user declines the quitting (i.e. presses "n")
- control.Mouse.process_quit_event:
    - new parameter ``event_detected_function`` to set a function that is
      called as soon as a quit event is detected (but before the end function
      is called)
    - new parameter ``quit_confirmed_function`` to set a function that is
      called when a user confirms the quitting (i.e. presses "y")
    - new parameter ``quit_denied_function`` to set a function that is called
      when a user declines the quitting (i.e. presses "n")
- control.pause: added ``text`` and ``key`` parameters
- control.defaults:
    - added ``display`` to set display index for showing screen on
    - added ``display_resolution`` to overwrite detected native resolution
    - added ``audiosystem_device`` to select audio device
- stimuli.Audio:
    - not limited to .wav/.ogg files anymore
    - should support most common formats (i.e. WAV, AIFF, MP3, Ogg, Opus, FLAC)
    - new property ``is_playing`` to check whether the audio stimulus is
      playing
    - new property ``length`` to get the length of the audio stimulus
    - new property ``time`` to get the current playback time
    - new method ``wait_time`` to wait until specified playback time is reached
    - new method ``wait_end`` to wait until the audio stimulus has finished
      playing
    - new method ``pause`` to pause (and unpause) playback of the audio stimulus
    - new method ``seek`` to seek to a specified playback time
    - new method ``forward`` to forward playback by specified duration
    - new method ``rewind`` to rewind playback by specified duration or to the
      start
    - ``seek``, ``rewind``, ``forward``, ``wait_time`` methods all take multiple
      convenient time formats now (e.g. "00:01:30")
- stimuli.Video:
    - general improvements
    - Pygame video backend removed (always relies on mediadecoder)
    - Pygame audio backend is now the default (instead of sounddevice)
    - new parameter ``audio_backend``
    - new stimuli default ``video_audio_backend``
    - Pygame audio backend uses current audiosystem (if started)
    - present method will start playback if not started already
    - frame dropping check is now located in update method (was in present)
    - update method allows for updating without blocking on vertical retrace
      (OpenGL mode only)
    - new property ``n_frames`` to get the total number of frames of the video
    - new property ``fps`` to get the frame rate in frames per second
    - new method ``wait_time`` to wait until a certain time
    - new method ``seek`` to seek to any position in the video
    - ``seek``, ``rewind``, ``forward``, ``wait_time`` methods all take multiple
     convenient time formats now (e.g. "00:01:30")
- io.Screen:
    - new method ``get_display_resolution``
    - new method ``misc.get_display_info``
    - ``update`` method has new ``blocking`` parameter to control blocking on
      vertical retrace (OpenGL mode only) behaviour per call
- io.TextInput: ``get`` method now has parameter ``clear_event_cue``
- misc:
    - new class``MediaTime`` for representing time as used in the context of
      media playback
    - new function ``misc.get_audio_devices`` to get a list of available audio
      devices

Changed:
- Python 2 support has been removed
  Expyriment now only works with Python 3.9 or higher
- deprecated and obsolete classes, methods and parameter were removed
	- parameter `experiment` in control.start
	- permute.balanced_latin_square(), permute.cycled_latin_square()
	- geometry.position2coordinate(), geometry.points_to_vertice()
	- statistics.frequence_table()
	- stimulus.Dot, stimulus. Frame
	- Clock.cpu_time()
	- Visual.replace()
	- Circle.get_polar_coordiantes(), Circle.set_polar_coordinates()
	- FixCross.cross_size
	- Shape.is_point_inside(), Shape.is_shape_overlapping()
- package building with flit and pyproject.toml
- revision number and build data (`__revision__`, `__date__`) removed from
  source files
- Python 2 support has been removed
  Expyriment now only works with Python 3.10 or higher
- Documentation not shipped with Expyriment anymore (i.e. no offline
  documentation available, only online)
- rewrite of permutation module
- pause_key has been removed
- When running in virtual environment, Expyriment settings folder will be local
  to that environment
- Always use maximal display resolution by default for fullscreen mode (unless
  overwritten by control.defaults.display_resolution)
- ``expyriment.control.defaults.openg_gl`` is now called
  ``expyriment.control.defaults.opengl``
- OpenGL mode "3" has been removed: OpenGL mode "2" (default) now does what
  "3" used to do (i.e. "alternative blocking")
- updated command line interface options:
    - ``-0``, ``-g``, ``--no-opengl``, ``-1``, ``-2``, ``-3`` are deprecated
    - OpenGL mode can now be set with new option ``--opengl``
    - all arguments are now also available as alternative long names
- io.TextMenu: `width` is now an optional parameter. If not defined, surface
  width is based on the widest item in the menu
- io.GamePad.wait_press: removed ``time.sleep(0.0005)``
- Deprecated io.Screen.get_monitor_resolution and misc.get_monitor_resolution
- misc.get_system_info:
    - additions and improvements
    - format changes for ``as_text`` output
- renaming: misc.py2py3_sort_array --> misc.string_sort_array
- renaming geometry functions:
    - position2coordinates() to position_to_coordinates()
    - coordinates2position() to coordinates_to_position()
    - cartesian2polar() to cartesian_to_polar()
    - position2visual_angle() to position_to_visual_angle()
    - tuples2points() to tuples_to_points()
    - polar2cartesian() to polar_to_cartesian()
    - visual_angle2position() to visual_angle_to_position()
- components with American spelling are now also available in British spelling,
  enhancing consistency with the overall spelling in the library:
    - method ``control.initialize`` -> ``control.initialise``
    - module ``design.randomize`` -> ``design.randomise``
	- property ``design.Experiment.is_initialized`` ->
      ``design.Experiment.is_initialised``
	- property ``design.Experiment.bws_factor_randomized`` ->
      ``design.Experiment.bws_factor_randomised``
	- constant ``control.defaults.initialize_delay`` ->
      ``control.defaults.initialise_delay``

Fixed:
- bug in colour.is_hex & colour.is_colour
- data_preprocessing: adds suffix ".csv" to filename when writing csv files
- bug when reusing subject id within a minute
- test suite: close serial port after test
- io.Keyboard: 0.5 ms timing inaccuracy in wait methods
- Visual stimuli: don't clear the original canvas when copying
- stimuli.Ellipse: bug when using uneven `line_width` values
- io.Screen: bug in saving screenshots with `save` when using OpenGL
- io.Screen: bug in showing Expyriment logo in task bar
- bug in `misc.get_display_info`
- several bugs in misc.get_system_info


Version 0.10.0 (30 Oct 2019)
----------------------------
New Features:
- Expyriment windows with no frame; set
  ``control.defaults.window_no_frame=True`` before initializing
- download plugins from stash: ``misc.download_from_stash``
- ``stimuli.Shape``: A vertex list can be added when creating a shape object
  using the optional ``vertex_list`` parameter
- all visual stimuli now have ``get_surface_array`` & ``set_surface_array``
  methods for direct pixel manipulations with numpy
- all visual stimuli have a getter and setter for the position in polar
  coordinates: ``polar_coordinate``
- ``cartesian2polar`` & ``polar2cartesian`` in ``misc.geometry``
- ``design``: trials, blocks and experiment objects have the method
  ``has_factor`` to check if a factor is defined
- after installation the command line interface will be available from the
  system command ``expyriment``
- ``io.TextInput`` can now optionally how text right-to-left
- ``io.SerialPort`` has a new method ``send_line``
- geometry module has convenience functions for predefined geometrical
  shapes used for plotting with ``stimuli.Shape``
- ``geometry.lines_intersection_point`` calculates intersection point of two
  lines
- ``stimuli.Line`` is internally based on ``stimuli.Shape`` and has the new
  methods ``get_shape`` and ``get_connected_shape``
- new function ``misc.py2_round``, implementing the old Python 2 rounding behaviour
- ``io.keyboard.check`` now has an argument ``check_for_keyup`` which will
  check for keyup events instead of keydown events
- new class ``misc.Colour``: create colours by names, Hex strings or RGB values;
  the class can also handle HSV, HSL values; the ``misc.HSVColour`` class is
  thus obsolete
- ``misc.data.preprocessing`` can handle glob wildcard pattern

Changed:
- Python's ``time.perf_counter`` function will be used as high-precision timer
  if it exists (that is, for Python 3.3+)
- major rewrite of ``stimuli.Shape`` with several bug fixes; e.g. shapes have no
  ``line_width``, ``contour_colour`` is renamed to ``debug_contour_colour``,
  ``Shape.rect`` is now a ``pygame.Rect``; see improved documentation
- ``extras``
    - extras need to be explicitly imported
    - extras and plugins are not anymore part of expyriment package and can
      be instead downloaded from the Expyriment stash (see
      ``misc.download_from_stash``)
    - all installed extras will be installed in the local settings folder
      (typically ``.expyriment`` in the $HOME directory)
- the option ``ascii_fiter`` in ``io.TextInput`` has been renamed to
  ``character_filter``
- ``frequence_table`` in ``misc.statistics`` has been renamed to
  ``frequency_table``
- ``points_to_vertices`` in ``misc.geometry`` has been renamed to
  ``points2vertices``
- ``position2coordinate`` in ``misc.geometry`` has been renamed to
  ``position2coordinates``
- ``position2coordinates`` & ``coordinates2position`` have a new optional
  argument to calculate positions relative to a surfaces
- ``stimuli.Circle``: ``get_polar_coordinates`` & ``set_polar_coordinates`` are
  obsolete; use ``polar_position``
- ``design``: ``Trial().get_factor``, ``Block().get_factor`` and
  ``Experiment().get_bws_factor`` now raise an exception if the factor is not
  defined; this can be suppressed by using the parameter
  ``return_none_if_not_defined``
- ``misc.geometry.points2vertices`` requires now a list of ``misc.XYPoints`` and
  not a list of tuples; (use ``misc.geometry.tuples2points`` to adapt old code)
- ``stimuli.Video``: attempting to downloaded a missing ffmpeg binary only when
  initializing a Video stimulus with the "mediadecoder" backend
- ``io.Mouse``: quit events will now be controlled via the method
  ``Mouse.set_quit_corner_location``; the class properties
  ``quit_rect_location`` and ``quit_rect_size`` are obsolete
- logging of visual stimuli ``present`` method now after screen update

Fixed:
- Adding field bug in ``io.TouchscreenButtonBox``
- 1-pixel bug when converting Expyriment positions to screen (Pygame)
  positions: ``position2coordinate`` & ``coordinate2position``
- control: ``auto_create_subject_id`` takes now also existing event files into
  account
- ``io.SerialPort`` bug with Python 3
- script path is added to $PYTHONPATH
- representation lists in output CSV files
- bug in ``io.Keyboard.wait``
- bug when drawing textures to screen (OpenGL) leading to 1-pixel inaccuracies
- bug in ``stimuli.Ellipse`` with uneven `line_width` argument
- ``io.TextInput``: argument ``background_stimulus`` now takes all Expyriment
  stimuli
- ``misc.get_system_info()`` uses ``PIL.__version__``
- ``io.TextMenu`` mouse wheel scrolling

Version 0.9.0 (9 Mar 2017)
---------------------------
New Features:
- Python 3 compatibility
- New Video stimulus implementation that supports a large range of formats
- new global boolean constant expyriment.PYTHON3 indicates Python version
- new io device: io.extras.TcpServer
- new method to add full factorial designs:
  Block.add_trials_full_factorial & Experiment.add_blocks_full_factorial
- Network interface to Turbo-Satori: io.extras.TurbosatoriNetworkInterface
  (see www.brainvoyager.com/products/turbosatori.html)
- stimuli.Rectangle: Option to have rounded (anti-aliased) corners
- rotate() method of stimuli applies filtering on the content now
- randomize.coin_flip() with bias parameter ("unfair coins")
- randomize.rand_norm() normally distributed random numbers
- statistics module: std & variance
- Eventfile.log has an optional log_event_tag for the logging of
  inter-event-intervals. If this is defined a summary of the intervals
  will be added to the event file.
- All present methods have an optional log_event_tag that will be passed
  to Eventfile.log (see above)
- New function: misc.has_internet_connection()
- Notify when initializing system fonts takes longer
- io.ParallelPort: new method get_driver()
- New function: misc.which()

Changed:
- all wait methods (io and Clock) now
    (1) have process_control_events attribute to check for quit events from
        keyboard and mouse
    (2) have function attribute (callback_function) to repeatedly run a
        specific function in every loop iteration
    (3) pump the pygame event queue to (hopefully) prevent the OS to think the
        window is "not responding"
- control.set_develop_mode: new skip_wait_methods attribute to omit all wait
  functions in the experiment (for testing)
- rename method: stimulus.replace --> stimulus.reposition
- improvements to io.extras.TcpClient
- move set_skip_wait_functions from misc to io
- move is_idle_running, is_interactive_mode, is_android_running
  from control to misc
- move get_module_hash_dictionary, get_experiment_secure_hash,
  module_hashes_as_string and get_system_info from expyriment to misc
- Testsuite: Visual test will now colour code reported refresh rates

Fixed:
- unicode bug on Windows for font files
- unicode bug on Windows for Audio and Picture
- bug fix in unicode2str
- bug fix Experiment.add_experiment_info
- bug: issue #65, tempfolder at multiuser systems
- minor bug fixes in _secure_hash.py, _files.py
- Cli: -0 option was not recognized
- Correct anti-aliasing for Circle/Ellipse (now works on every background)
- compatibility with pyserial version 3.0
- ParallelPort: inpoutx64 should now work correctly

Version 0.8.0 (30 Jun 2015)
---------------------------
New Features:
- antialiasing option for stimuli.Ellipse() and stimuli.Circle()
- new class: misc.HSVColour. Class to handle HSV colours [hue, saturation, value]
- new function: quitting wait or event loops by callback_function, if this function
  returns an instance of the new class control.CallbackQuitEvent
- new method: all visual stimuli have methods for lowlevel Pygame operations
  get_surface_copy(), set_surface(), get_pixel_array()
- new stimulus: stimuli.extras.ThermometerDisplay
- new io device: io.extras.TbvNetworkClient
- new io device: io.extras.TcpClient
- new stimulus: GaborPatches can be created with stimuli.extras.GaborPatch();
  the stimulus depends on the package "matplotlib".
- new feature: data_preprocessing method sallow now to read in only certain
  variables (see parameter `read_variables`)
- new feature: Expyriment asks in interactive mode if initializing a fullscreen
- new method: stimulus.visual.scale_to_fullscreen
- new class: design.extras.StimulationProtocol
- new method in data_preprocessing: save to R data frame
- new method in data_preprocessing: get_experiment_duration
- new method/property: misc.get_monitor_resolution & Screen.monitor_resolution
- new mouse function: experiments can be quit by mouse events (triple click);
  see documentation of property "mouse_quit_event". This function is only switched
  on per default under Android
- new method visual stimuli.replace
- new method control.is_android_running
- several new options for command line interface
- get_module_hash_dictionary: dictionary secure hashes from all modules
  imported from local folder
- new constant: ALL_KEYPAD_DIGITS
- new helper functions in misc and control
- new feature: control.set_skip_wait_functions
- io.Keyboard has static methods to set and get the quit_key and pause_key
- new feature: too long text lines will be trimmed automatically if the
  max_width parameter has been defined
- new feature: too long words in text boxes will be trimmed automatically,
  this function can be switch off
- new feature: improved functionality of randomize.shuffle_list
- Test suite summarizes delay histograms for visual presentations
- control.defaults.blocking_mode for setting the blocking_mode
- new io.ParallelPort implementation, based on PsychoPy code; it now
  supports reading of 5 status pins (10, 11, 12, 13, 15) and all 8 data pins;
  in addition, the module now works on 64bit Windows system
- Test suite: New ParallelPort test
- stimuli.extra.DotCloud: DotCloud can be multi coloured (see make method)
- lots of documentation improvements

Changed:
- ATTENTION: Open_GL is now also used in window mode and will not be switch
  off automatically, if Expyriment is not running in fullscreen mode.
- ATTENTION: extra modules will not anymore be imported automatically. Please
  call `import.<module_name>.extras`, if you want to use extra features.
- ATTENTION: io.screen.open_gl and control.defaults.open_gl have new parameters::
    0/False - No OpenGL (no vsync / no blocking)
    1       - OpenGL (vsync / no blocking)
    2/True  - OpenGL (vsync / blocking)
    3       - OpenGL (vsync / alternative blocking)
- ATTENTION: stimuli.Ellipse is now defined by radii (Not backwards compatible!)
- ATTENTION: stimuli.Circle is now defined by radius (Not backwards compatible!)
- ATTENTION: two obsolete stimuli stimuli.Frame and stimuli.Dot (see doc)
- ATTENTION: ParallelPort has been changed a lot and is not backwards compatible
  anymore; the old implementation is still available as
  io.extras.SimpleParallelPort
- the property Shape.size has been renamed to shape.shape_size
- stimuli.Rectangle: is_point_inside is now obsolete
- stimuli.Shape: is_point_inside and is_shape_overlapping are now obsolete
- stimuli.Fixcross: fixcross_size parameter and cross_size property are now
  obsolete
- changes to Simon example

Fixed:
- bug in io.TouchScreenButton crash if duration expired
- bug in command line interface: order of argument is now irrelevant
- keypad bug in TextInput
- unicode bug in TextMenu
- bug in anti_aliasing shapes
- some method parameters that require a list and didn't work with tuples
- stimuli with odd dimensions missed a pixel in each dimension in OpenGL mode
- bug in stimuli.Audio.unload() and stimuli.Video.unload()
- bug in io.ParallelPort.poll (now io.extras.SimpleParallelPort)
- bug in Shape: shapes now compensate for the Pygame bug of extended polygons
  along the horizontal axes
- bug in stimuli.extras.DotCloud: colour of dots could not be changed

Version 0.7.0 (2 Mar 2014)
--------------------------
New Features:
- new feature in testsuite: Font viewer
- new extra stimulus: stimuli.extras.RandomDotKinematogram
- new timer and experiment clock to ensure monotonic timing
- Clock: new method (static) monotonic_time (this time should be always used)
- data_preprocessing: new exclusion rule, which allows removing trials
  depending on their deviation (std) from mean (e.g., 'RT > 1.5*std')
- improvements for OS X in get_system_info()
- proper unicode handling: use unicode strings whenever unicode characters
  are needed
- files: the character encoding is now written to files and used when opening
  them
- FreeFonts are now part of the Expyriment distribution to guarantee the same
  fonts across platforms
- new io class: TouchScreenButtonBox
- new options for control.start(): skip_ready_screen and subject_id to start
  with predefined subject id
- experiments now also have a global mouse object: experiment.mouse
- new property for io.Mouse: is_visible
- Secure hashes for experiments help to ensure that the correct version is
  running in the lab. Secure hashes will be displayed at the start and printed
  in all output files as well as in the command line output.

Fixed:
- experiment clock now with monotonic timing
- bug in extras.CedrusResponseDevice
- several bugs in documentation
- incompatibility with multiprocessing.Pool
- bug in Visual.add_noise()
- bug in io.SerialPort.read_line()
- bugfix: stimuli.shapes can now be used as background stimuli for io.TextInput
  & io.TextMenu

Changed:
- several Android related changes (have no impact for normal use of Expyriment)
- overlapping methods of stimuli now work on absolute_position by default

Version 0.6.4 (5 Aug 2013)
--------------------------
New Features:
- log levels can be changed while running experiment via the method
  Experiment.set_logging. Access current  via Experiment.loglevel
- Modification the logging of individual objects while runtime. Most classes
  have now the method set_logging(onoff), to switch on or off the logging.
- design.randomize.rand_element returns a random element from a list
- blocks and trails have the property 'factor_dict', which is a dictionary with
  with all factors
- experimental Android support

Fixed:
- incorrect background colour for TextInput
- Font in TextScreen
- several fixed in documentation
- switching off logging via "expyriment.control.defaults.event_logging = 0" not
  now working
- "numpy version bug" in data.preprocessing
- unicode bug for picture, audio and video filenames
- polling of parallel port
- io.TextMenu font was hardcoded

Version 0.6.3 (14 Apr 2013)
---------------------------
New Features:
- misc.geometry contains function to convert between pixel and degrees of
  visual angle: position2visual_angle & visual_angle2position
- io.TextInput has now a position and can be plotted on a background stimulus
- misc.find_font
- misc.list_fonts

Fixed:
- Initializing experiments in the IDLE shell
- TextInput user_text_font and user_text_bold can now be changed
- bugs in font selection
- API reference tool should now also open when there are whitespaces in Python
  executable path

Changed:
- renamed TextInput.user_colour --> user_text_colour
- FixCross.cross_size has been renamed to FixCross.size. FixCross.size is
  now a tuple (int, int) and defines both dimensions (x, y) separately.
- Expyriment is checking also the version of all required packages and
  dependencies
- all doc string are now in line with the numpy-doc conventions


Version 0.6.2 (12 Dec 2012)
---------------------------
New Features:
- new stimuli.extras.PolygonLine class

Fixed:
- Expyriment could not be imported on Windows 7 64
- misc.geometry.position2coordinate bug
- io.Mouse.self_test bug is fixed

Changed:
- stimuli.Line was rewritten to not depend on PolygonRectangle anymore;
  the old Line stimulus is now stimuli.extras.PolygonLine

Version 0.6.1 (9 Dec 2012)
--------------------------
Fixed:
- Testsuite wouldn't start anymore
- API reference tool would not start on Windows XP in some cases

Version 0.6.0 (4 Dec 2012)
--------------------------
New Features:
- new stimuli.Circle class
- new stimuli.Ellipse class
- new stimuli.extra.PolygonDot class
- new stimuli.extra.PolygonEllipse class
- new stimuli.extra.PolygonRectangle class
- new method: stimuli.Shape.add_vertices to add multiple vertices at once
- an additional suffix for the main data and event files can be set when
  creating an Experiment
- Unfilled Shapes by setting a line_width, when creating a shape
- Shape: new property line_width

Fixed:
- stimuli.Shape: several fixes, related to surface creation and xy point
  calculation
- Logging of unicode text in TextLine stimulus
- stimuli.TextLine and stimuli.TextBox can now also receive a font file as
  text_font argument
- stimuli.TextLine.copy()
- Bug fixes in self tester of stimuli
- Fixed segmentation fault when repeatedly initializing and ending an experiment
- Fixed surface size shapes
- Fixed incorrect line_width plotting for scaled shapes
- Copying preloaded stimuli in OpenGL mode
- Bug fixed in io.InputFile.get_line()

Changed:
- io.DataFile: variable "Subject" is now called "subject_id"
- io.Screen.update() should be even more accurate now (about 0.5 milliseconds)
- misc.data_preprocessing: argument and property "experiment_name" in all
  objects is now called "file_name"
- misc.data_preprocessing.Aggregator can handle files with different suffixes:
  see __inti__ and reset
- stimuli.Dot: is_center_inside, is_overlapping and is_inside are deprecated now
- stimuli.Dot is deprecated now, use stimuli.Circle instead
- stimuli.Shape: is_point_inside and is_shape_overlapping are deprecated now
- stimuli.Shape.native_scaling does now optionally scale also the line_width
- stimuli.Frame: property line_width is now renamed to frame_line_width. Since
  line_width is a property the underlying shape and always 0 (filled shapes)
- stimuli.Frame is deprecated now, use stimuli.Rectangle with line_width > 0
- stimuli.Rectangle was rewritten and is not inherited from Shape anymore;
  the old Rectangle stimulus is now known as stimuli.extras.PolygonRectangle

Version 0.5.2 (13 Jun 2012)
---------------------------
New Features:
- data_preprocessing.print_n_trials(variables)
- data_preprocessing.get_variable_data: get data as numpy arrays.
- data_preprocessing.add_variable: add data from numpy.
- read trials from csv file into a block design.block.add_trials_from_csv_file
- block.read_design (counterpart to save_design)
- the main event_file logs now also the standard output and Python errors
- statistic functions are now robust against type violations (like nan_mean)
- design will be automatically saved to event file when experiment starts
- functions to check if IDLE of IPython are running (in control)
- several further new minor features

Fixed:
- Serial Port test can now be quit without quitting the test suite
- FixCross, width vertical line
- Serial Port will be closed when script crashes in IDLE
- Fix for stimuli.extras.VisualMask
- Fix for io.TextInput
- Fixes and adjustments for default logging
- API browser now works on OS X
- API browser fonts on Windows
- several bug fixes in data_preprocessing

Version 0.5.1 (07 Mar 2012)
---------------------------
Fixed:
- Bug in Serial Port test when no input is received
- Bug for get_version() under Python 2.6 under OS X

Changed:
- Text colour for API HTML reference

Version 0.5.0 (06 Mar 2012)
---------------------------
New Features:
- new io class: TextMenu
- new function: expyriment.get_system_info()
- new function in control: get_defaults()
- new method in ButtonBox: check()
- new methods in io.Mouse: wait_event, wait_motion
- new misc modules: geometry and statistics
- new Cedrus Response Devices support in io.extras
- new test suite:
  - new method in control: run_testsuite()
  - the testsuite can write a protocol with all results and information about
    the system
- folder for settings and extra plugins:
  $HOME/.expyriment/ or $HOME/~expyriment/
  - if the file post_import.py exist in this folder it will be executed
    automatically after the import of expyriment
  - extra plugins can be now also included in the folder
    $HOME/.expyriment/<module_name>/  (or ~expyriment)
- command line interface:
  - see "python -m expyriment.cli -h" for help
- better on- and offline documentation:
  - new function: expyriment.show_documentation()
  - new Api Reference Tool (API browse and search GUI)
- new function in misc.data_preprocessing: write_concatenated_data
- ButtonBox and TriggerInput work now optional with bitwise comparisons
- SerialPort and ParallelPort have a get_available_ports() method
- wait callback functions can now also be registered via the experiment
- some new constants
Changed:
- ButtonBox has been replaced by StreamingButtonBox and EventButtonBox
- the experiment is now THE central structure in the framework. Importantly,
  start does not require an experiment anymore and starts instead the
  currently initialized experiment.
- textinput.filter is rename to textinput.ascii_filter
- stimuli.TextBox: Size is now a mandatory parameter
- ending expyriment will now only optionally call sys.exti()
- stimuli.Audio.is_playing() and Audio.wait_end() are replaced by
  control.get_audiosystem_is_playing() and control.wait_end_audiosystem()
- stimuli.Audio.play() now returns a pygame.mixer.Channel object
- control.run_in_develop_mode() is renamed to control.set_develop_mode()
- no config files will be supported anymore
Fixed:
- the Windows installer will now remove all files from an old installation
  before installing
- IDLE will not freeze anymore, when a script crashes
- several attributes/properties were did not appear in the API reference
- major bug in keyboard.check()
- (possibly) fixed is_playing() method in Audio
- ordering of serial ports in SerialPort.get_available_ports()
- visual problems when graphics card is set to do flipping with triple buffer

Version 0.4.0 (22 Nov 2011)
---------------------------
New Features:
- saving and loading designs, new functions in experiment class (save_design
  and load_design)
- new module: expyriment.misc.data_preprocessing with functions for data
  handling and a new tool to preprocess and aggregate expyriment data
  (class Aggregator). Note: Preliminary version. Use with caution.
- new extra stimulus class: visual mask  (depends on PIL)
- new extra io class: Webcam (depends in PIL and OpenCV)
- new extra io class: MidiIn
- new extra io class: MidiOut
- the repository and the expyriment source code zip file contain examples
- 'setup.py install' removes old installation
- new function: block.save_trials
Changed:
- Extra modules are now hidden
- skipped function experiment.save_trial_list (please use the new
  experiment.save_design instead)
- rename property block.all_factors_as_text --> block.factors_as_text
- rename property experiment.trials_as_text --> experiment.design_as_text
- rename experiment.bws_factor_permutation_randomize -->
  experiment.bws_factor_randomized
- Factor conditions/levels have to be a number (int, float) or a string. No
  other data types are allowed.
Fixed:
- Bug in testing function of visual extra stimuli
- Bug fix, unbalanced between subject factor permutation for hierarchical
  designs by subject_ID
- Bug fix, playing short tones (duration<1 sec.)


Version 0.3.3 (19 Oct 2011)
---------------------------
New Features:
- stimuli.Video.wait_frame() stops playback and screen updating
  after the given frame
Fixed:
- Printing experiments with no block factors defined will work now


Version 0.3.2 (12 Oct 2011)
---------------------------
New Features:
- stimuli.Audio: wait_end(), is_playing
Changed:
- stimuli.Video: present() will now block until the first frame is presented.
- stimuli.Video: play() will not render anything anymore
- stimuli.Tone and stimuli.extras.NoiseTone: duration is now set in ms
- design.Block.get_a_random_trial() is now called get_random_trial()
Fixed:
- Visual stimuli: picture() method works now
- Visual stimuli: copy() method was erroneous
- design.Block.get_summary(): Ordering of trial factors
- design.Block and design.Trial: Factor values can now be dictionaries as well
- stimuli.Tone and stimuli.extras.NoiseTone: Works correctly on Windows now
- design.Block.get_random_trial(): Could crash in some occasions
- Fix underscore at the end of filenames


Version 0.3.1 (8 Sep 2011)
---------------------------
Changed:
- SerialPort: byte_buffer is now input_history
- ParallelPort: byte_buffer removed (just did not make any sense)
- ButtonBox: buffer and has_buffer attributes are gone
- Buttons of Mouse and GamePad now start from 0
- register_wait_function renamed to register_wait_callback_function
Fixed:
- Critical bug on Windows about parsing of expyriment installation folder
- Critical bug in Block.copy() which would destroy Pygame surface
- Mouse.check_button_pressed(): Mismatch in button numbering
- Dot: Fixed calculation for setting polar coordinates
- ParallelPort: Sending data
- MarkerOutput: Duration computation


Version 0.3.0 (31 Aug 2011)
---------------------------
New Features:
- expyriment.control.register_wait_function(): A function registered here
  will be called in each wait method in the framework at least once
- expyriment.control.run_in_develop_mode(): Automatically sets some defaults
  (window_mode=True, open_gl=False, fast_quit=True)
- SerialPort: read_line() will wait for and return full lines
- SerialPort: os_buffer_size attribute will affect the warning behaviour of the
  byte buffer
- ByteBuffer: add_events() can be used to add multiple events at once
Changed:
- defaults, constants as well as initialize(), start(), pause() and end() will
  no longer be available via expyriment but only via expyriment.control
- SerialPort: Updating the byte_buffer is now faster and warnings are more precise
Fixed:
- GamePad.wait_press(): Can now also check for first button (button 0)


Version 0.2.1 (19 Aug 2011)
---------------------------
New Features:
- MarkerOutput can now send with a specified duration (needed for EEG systems
  connected via parallel port)
- Advanced trial shuffling
Fixed:
- Critical bug in Trial.copy() which leads to broken surfaces
- Blocking mode for serial port
- Unicode in TextBox? and TextScreen?
- wait_press() in GamePad does now check for more than one button


Version 0.2.0 (26 May 2011)
---------------------------
New Features:
- Overall structure has changed quite a bit. There are now only 5 submodules
  (control, design, io, stimuli, misc). Things like initialize() and start()
  are now in control. Constants are now in misc. Each module has its own
  defaults now.
Changed:
- Adding blocks and trexpyrimentials will always add a copy. There is no option
  for adding a reference anymore.
- Block and Trial IDs are now relative to where they are added. For instance,
  two blocks can contain 10 unique trials each, but for both blocks the trial
  IDs will go from 0 to 9.
- Adding stimuli will always add a reference!
- Stimuli have still an absolute unique ID
Fixed:
- A variety of small bugs have been fixed

Version 0.1.4 (22 May 2011)
---------------------------
Fixed:
- Getting a picture from a stimulus was broken

Version 0.1.3 (12 May 2011)
---------------------------
Fixed:
- Tempfiles of surfaces are now closed after creation (critical on Windows!)

Version 0.1.2 (11 May 2011)
---------------------------
Changed:
- expyriment version now printed on import, not on Experiment creation anymore
Fixed:
- Setup script will not try to check mercurial information by default anymore

Version 0.1.1 (11 May 2011)
---------------------------
New Features:
- Throws a useful exception on old or integrated Intel graphics cards that
  do not support OpenGL properly
Fixed:
- Experiment.permute_blocks() will not destroy the surfaces of the
  stimuli anymore

Version 0.1.0 (10 May 2011)
---------------------------
First public release
