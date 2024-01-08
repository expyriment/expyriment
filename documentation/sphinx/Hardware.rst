Hardware compatibility
=======================

Video cards
-----------
We generally have good experiences with recent NVIDIA or ATI cards.  OpenGL 
mode should work with all drivers that use an OpenGL specification >= 
2.0.  Drivers implementing an older OpenGL specification (>= 1.4) should work 
when the 'GL_ARB_texture_non_power_of_two' extension is present.

**We recommend to always use the Expyriment test suite to check the
performance of your specific configuration!**

*For the OpenGL modes to work correctly, it is important to set the graphic
card's driver settings to support synchronizing to the vertical retrace ("Sync
to VBlank" or "V-sync") and to switch off any power saving schemes on the
graphic card.*

*Vsync and blocking on the vertical retrace are only functioning as intended in
fullscreen mode. Presentation times will not be accurate in window mode!*

*Even with working vsync and blocking, there can be scenarios where visual
stimulus presentations are still physically delayed by one or two frames (i.e.
the display draws them later than it reports). These cases entail the presence
of an additional invisible in-between buffer, either at the level of the
operating system (e.g. a "compositing" window manager) or at the level of the
display driver (e.g. "intelligent" gaming displays). While these delays are
NOT captured by the visual test in the test suite and have to be measured
externally, they should at least be stable across different visual stimulus
presentations and should hence not introduce any differences between
experimental conditions.*

*When using high-DPI displays, Expyriment will attempt to use the full native
resolution for fullscreen mode with OpenGL (if the nativive resolution is not
guessed correctly, it can be manually overwritten by setting 
``control.defaults.display_resolution``. In all other cases (i.e. no OpenGL
and/or window mode) Expyriment might return a screen with a scaled resolution,
according to the operating system's scaling settings. To get a non-scaled
screen in these cases, scaling has to be deactivated on the operating system
level.*

External devices
----------------

Besides standard `serial <expyriment.io.SerialPort>`_ and `parallel <expyriment.io.ParallelPort>`_ port communication,
there is special support for:

* `Event button box`_
* `Streaming button box`_
* `Trigger input`_
* `Marker output`_
* `Cedrus response devices`_

Event button box
~~~~~~~~~~~~~~~~
An event button box is a simple device which sends out values (bytes) whenever 
a button is pressed (or released).

Event button boxes can be used by initializing an 
`<expyriment.io.EventButtonBox>`_
object::

    bb = expyriment.io.EventButtonBox(expyriment.io.SerialPort("COM1"))
    key, rt = bb.wait() # Wait for any value

Streaming button box
~~~~~~~~~~~~~~~~~~~~
A streaming button box constantly sends out a certain baseline value (e.g. 0) 
in predefined intervals (e.g. each 1 ms). Button press (or release) events (if 
present) are added to the baseline.

Streaming button boxes can be used by initializing an  
`<expyriment.io.StreamingButtonBox>`_ object::

    bb = expyriment.io.StreamingButtonBox(expyriment.io.SerialPort("COM1"),
                                baseline=128)
    key, rt = bb.wait() # Wait for any value other than 128

This allows for instance for calculating the response timing without relying on 
the computers internal clock, but by "counting" the incoming bytes from the 
button box::

    bb = expyriment.io.StreamingButtonBox(
                expyriment.io.SerialPort("COM1"), baseline=128)
    bb.clear()
    exp.clock.wait(1000)
    rt = bb.interface.read_input().index(129)   # Get reaction time by counting
                                                # input events since last clear

It is important to notice that operating systems only buffer a certain amount 
of bytes (usually 4096). To prevent an overflow of this buffer, the button box 
has to be checked regularly. Additionally, an ``input_history`` can be used on 
the `<expyriment.io.SerialPort>`_ object which is automatically updated 
whenever the serial port is polled or cleared. By setting the 
``os_buffer_size`` correctly, a warning will be logged whenever the amount of 
bytes in the OS serial port buffer reaches maximum capacity. **The important 
part now is to update the input_history regularly**.  To gain maximal control, 
this should be done manually at Sending to external deviceappropriate places in 
the code.  However, Expyriment provides also the possibility to register a 
callback function which will be called regularly during all waiting methods in 
the library. By registering the ``check()`` method of the streaming button box, 
the ``input_history`` will be updated fairly regular, which should suffice for 
most use cases::

    expyriment.control.register_wait_callback_function(bb.check)
    bb.interface.input_history.check_value(129) # Check if 129 was
                                                # received at any time
    # RT by counting elements in input history
    start = bb.interface.input_history.get_size() - 1
    exp.clock.wait(1000)
    rt = bb.interface.input_nput_history.check_value(129,
                                    search_start_position=start) - start



Trigger input
~~~~~~~~~~~~~
Expyriment can wait for triggers from external devices, like for instance an MR 
scanner.

When updated regularly, Expyriment can also keep track of the amount of 
triggers that have been received. Importantly, this has to be done manually

Trigger inputs can be used by initializing an `<expyriment.io.TriggerInput>`_ 
object.

**Basic usage**

In most of the cases, a researcher knows when a trigger is to be expected and 
he can wait for it explicitly. Code execution will be blocked until the trigger 
is received::

    trigger = exyriment.io.TriggerInput(expyriment.io.SerialPort("COM1"))
    trigger.wait(1) # Wait for code 1

**Advanced usage**

In some cases, code blocking might not be a solution, since a trial has to 
continue while waiting for the trigger. For instance, in an fMRI study, a trial 
might consist of several components and span several TR. One way to solve this 
would be logging constantly all input events in a separate thread.  However, 
this will introduce timing uncertainties, since the operating system is in 
charge of how and when threads communicate. We thus decided against an 
implementation with threads for the same reasons Expyriment does not implement 
a main event loop: Maximal control by the user.  Nevertheless, input events can 
still be buffered without introducing timing uncertainties, given the following 
two conditions:

1. Incoming events are streaming, either by sending some baseline in regular 
   intervals (e.g. a 0 each millisecond), or by a regular incoming signal of 
   interest (e.g. a constant TR from the MR scanner).
2. The input device is polled regularly, such that the serial port OS buffer 
   does not overflow. (Most implementations use an OS buffer of 4096 bytes).

If those two conditions are met, an ``input_history`` can be used on the 
`<expyriment.io.SerialPort>`_ object which is automatically updated whenever 
the serial port is polled or cleared. By setting the ``os_buffer_size`` 
correctly, a warning will be logged whenever the amount of bytes in the OS 
serial port buffer reaches maximum capacity. **The important part now is to 
update the input_history regularly**. To gain maximal control, this should be 
done manually at appropriate places in the code. However, Expyriment provides 
also the possibility to register a callback function which will be called 
regularly during all waiting methods in the library. By registering the 
``get_trigger()``
method of the input trigger, the ``input_history`` will be updated fairly 
regular, which should suffice for most use cases::

    trigger = exyriment.io.TriggerInput(expyriment.io.SerialPort(external"COM1",
                    input_history=True, os_buffer_size=3000))
    expyriment.control.register_wait_callback_function(trigger.get_triggers)
    print trigger.trigger_count


Marker output
~~~~~~~~~~~~~
Expyriment can send markers to external devices, like for instance EEG 
computers.

Marker outputs can be used by creating an `<expyriment.io.MarkerOutput>`_ 
object.

**Basic usage**

Sending out markers is straight forward. Some devices (e.g. EEG systems) expect 
a 0 to be send after the code. We can specify this by telling the output marker 
at what duration this 0 is supposed to be sent::

    marker = expyriment.io.MarkerOutput(expyriment.io.SerialPort("COM1"), duration=20)
    marker.send(1) # Send code 1


Cedrus response devices
~~~~~~~~~~~~~~~~~~~~~~~

Expyriment comes with a high-level wrapper for Cedrus response devices 
`<expyriment.io.extras.CedrusResponseDevice>`_, which allows you to easily 
use all Cedrus response devices.

To use these devices, however, the third-party Python package pyxid_ needs to 
be installed on the system.

**Installing pyxid**

* Download_ pyxid
* Install as described here_.

.. _pyxid: https://github.com/cedrus-opensource/pyxid
.. _Download: https://github.com/cedrus-opensource/pyxid/zipball/master
.. _here: http://docs.python.org/install/index.html#the-new-standard-distutils 
