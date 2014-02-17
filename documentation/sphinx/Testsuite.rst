Expyriment test suite
=====================

The Expyriment test suite is a guided tool for testing your computer's 
abilities/performance. This includes timing accuracy of visual stimulus 
presentation, audio playback functionality, mouse functionality and serial port 
functionality/usage.

Eventually, all test results can be saved as a protocol, together with some 
information about the system.

**Starting the test suite**

The test suite can either be started from within an experiment, or from an 
interactive Python session (for instance with IPython).

To start the test suite, just call::

    expyriment.control.run_test_suite()

**Menu overview**

Here is a brief explanation of the available options:

1. *Visual stimulus presentation*

 * Tests if stimuli can be presented timing accurately
 * Tests if stimulus presentation is synchronized to the refresh rate of the 
   screen
 * Tests the video card's settings for buffering

2. *Auditory stimulus presentation*

  * Tests functionality of audio playback

3. *Font viewer*

 * Test installed fonts

4. *Mouse test*

 * Tests mouse accuracy (polling time)
 * Tests functionality of mouse buttons

5. *Serial port test*

 * Tests functionality of devices connected via the serial port

6. *Write protocol*

 * Saves all test results, as well as information about the system, as a text 
   file.

7. *Quit*

 * Quits the test suite


