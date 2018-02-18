Beginner's tutorial to get started with Expyriment
====================================================

Since Expyriment is a library for the programming language Python,
basic Python knowledge will be needed. Python is relatively easy to
learn, and there are many excellent `Python tutorials`_ online.

To programme an experiment, any text editor is suitable.
We, however, suggest a good programming editor or IDE that offers syntax
highlighting and code completion. If you do not have a favourite editor yet,
give `Pycharm`_ a try, which is also offered as a free version (community edition)
that runs on Windows, Linux and OS X.

.. _`Python tutorials`: http://docs.python-guide.org/en/latest/intro/learning/
.. _`Pycharm`: https://www.jetbrains.com/pycharm/

How to get started with Expyriment?
-----------------------------------

Let's start right away with a very basic example!

Write the following code into an empty text file and save the file as 
first_experiment.py::

    import expyriment

    exp = expyriment.design.Experiment(name="First Experiment")
    expyriment.control.initialize(exp)

    expyriment.control.start()

    expyriment.control.end()

Now run the file by either double clicking on it (if you are on Windows) or by 
typing the following into a command line::
    
    python first_experiment.py

The following should happen:

* Expyriment will start up, showing the startup screen and a countdown of 10 
  seconds
* "Preparing experiment..." will be presented on the screen (very briefly)
* You will be asked to enter the subject number
* "Ready" will be presented on the screen
* After pressing ENTER "Quitting experiment..." will be presented on the screen

Let's see what we just did in more detail:
    
    ::
    
        import expyriment 
    
    We imported the Expyriment package into Python, such that we can use it 
    there.

    ::
    
        exp = expyriment.design.Experiment(name="First Experiment")
        expyriment.control.initialize(exp)
    
    We created a new Experiment object by calling the Experiment class in the 
    submodule design and named it "First Experiment". Immediately after we 
    initialized this experiment to be the active one. This does the following:
    
    * Present the startup screen with the countdown (which is there to ensure 
      that the Python interpreter has enough time to start up properly and will 
      be time accurate afterwards)
    * Start an experimental clock (which thereafter will be available as 
      ``exp.clock``)
    * Create the screen (which thereafter will be available as ``exp.screen``)
    * Create an event file (which thereafter will be available as 
      ``exp.events``)
    * Present the "Preparing experiment..." screen

    ::
    
        expyriment.control.start()

    We started running the currently active (initiated) experiment.
    This does the following:

    * Present a screen to ask for the subject number (which thereafter will be 
      available as ``exp.subject``) and wait for the RETURN key to be pressed
    * Create a data file (which thereafter will be available as ``exp.data``)
    * Present the "Ready" screen
    
    ::
    
        expyriment.control.end()

    We finished our experiment, so we quit Expyriment.
    This will automatically save the data as well as the event file and show 
    the "Ending experiment..." screen.


Okay great, now let's actually do something in this experiment. Let's say we 
want to present a stimulus. Change the code to look like this::

    import expyriment

    exp = expyriment.design.Experiment(name="First Experiment")
    expyriment.control.initialize(exp)

    stim = expyriment.stimuli.TextLine(text="Hello World")
    stim.preload()

    expyriment.control.start()

    stim.present()
    exp.clock.wait(1000)

    expyriment.control.end()


If you run the programme now the following should happen:

* Expyriment will start up, showing the startup screen and a countdown of 10 
  seconds
* "Preparing experiment..." will be presented on the screen (very briefly)
* You will be asked to enter the subject number
* "Ready" will be presented on the screen
* After pressing ENTER, "Hello World" will be presented on the screen for 1000 
  ms
* "Ending experiment..." will be presented on the screen


Again, let's look into the new things we added in more detail:

    ::
    
        stim = expyriment.stimuli.TextLine(text="Hello World")

    We created a text stimulus with the text "Hello World".

    ::
    
        stim.preload()
    
    We preloaded the stimulus into memory (to ensure that this does not happen 
    when presenting it later, since this may take some time).

    ::
    
        stim.present()

    We presented the stimulus on the screen.

    ::
    
        exp.clock.wait(1000)

    We waited for 1000 ms, while the stimulus is still on the screen (since we 
    did not present something else afterwards).


Let's add some common experimental design structures to get a bit more 
organized.
Modify the code to look like this::

    import expyriment

    exp = expyriment.design.Experiment(name="First Experiment")
    expyriment.control.initialize(exp)

    block = expyriment.design.Block(name="A name for the block")
    trial = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="Hello World")
    stim.preload()
    trial.add_stimulus(stim)
    block.add_trial(trial)
    exp.add_block(block)

    expyriment.control.start()

    stim.present()
    exp.clock.wait(1000)

    expyriment.control.end()

Running this will show you the same as before. This is, because we only made 
changes in the experimental design, but not in the experiment conduction!

Here is what we added in detail:

    ::
    
        block = expyriment.design.Block("A name for the block")
    
    We created an experimental block by calling the Block class in the design 
    submodule and gave the block then name "Block One"

    ::
    
        trial = expyriment.design.Trial()

    We created an experimental trial by calling the Trial class in the design 
    submodule.

    ::
    
        trial.add_stimulus(stim)

    We added our stimulus to the trial.

    ::
    
        block.add_trial(trial)
    
    We added our trial to the block.

    ::
    
        exp.add_block(block)
    
    We added our block to the experiment.


We now have a nice hierarchical structure:

* The experiment with one block
* The block has one trial
* The trial includes one stimulus


Of course this is only makes sense when more blocks and trials are used.
Let's now create two blocks with 2 Trials each. Each of those trials will have 
exactly one stimulus. Change the code to look like this::

    import expyriment

    exp = expyriment.design.Experiment(name="First Experiment")
    expyriment.control.initialize(exp)

    block_one = expyriment.design.Block(name="A name for the first block")
    trial_one = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 1, Trial 1")
    stim.preload()
    trial_one.add_stimulus(stim)
    trial_two = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 1, Trial 2")
    stim.preload()
    trial_two.add_stimulus(stim)
    block_one.add_trial(trial_one)
    block_one.add_trial(trial_two)
    exp.add_block(block_one)

    block_two = expyriment.design.Block(name="A name for the second block")
    trial_one = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 2, Trial 1")
    stim.preload()
    trial_one.add_stimulus(stim)
    trial_two = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 2, Trial 2")
    stim.preload()
    trial_two.add_stimulus(stim)
    block_two.add_trial(trial_one)
    block_two.add_trial(trial_two)
    exp.add_block(block_two)


    expyriment.control.start()

    for block in exp.blocks:
        for trial in block.trials:
            trial.stimuli[0].present()
            exp.clock.wait(1000)

    expyriment.control.end()

When running this the following happens:

* Expyriment will start up, showing the startup screen and a countdown of 10 
  seconds
* "Preparing experiment..." will be presented on the screen
* You will be asked to enter the subject number
* "Ready" will be presented on the screen
* After pressing ENTER, the stimuli are presented in the order: stimuli in 
  trial_one and trial_two of block_one followed by the stimuli in trial_one and 
  trial_two of block_two. All four are presented for 1000 ms
* "Ending experiment..." will be presented on the screen

Let's see what we did exactly:

    ::
    
        block_one = expyriment.design.Block(name="A name for the first block")
        trial_one = expyriment.design.Trial()
        sim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 1, Trial 1")
        stim.preload()
        rial_one.add_stimulus(stim)
        trial_two = expyriment.design.Trial()
        stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 1, Trial 2)
        trial_two.add_stimulus(stim)
        block_one.add_trial(trial_one)
        block_one.add_trial(trial_two)
        exp.add_block(block_one)
    
    We created a block, two trials and two stimuli. We put one of the stimuli 
    in each of the trials, the trials into the block and the block into the 
    experiment.

    ::
    
        block_two = expyriment.design.Block(name="A name for the second block")
        trial_one = expyriment.design.Trial()
        stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 2, Trial 1
        stim.preload()
        trial_one.add_stimulus(stim)
        trial_two = expyriment.design.Trial()    
        stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 2, Trial 2")
        trial_two.add_stimulus(stim)
        block_two.add_trial(trial_one)
        block_two.add_trial(trial_two)
        exp.add_block(block_two)

    We created another block with again two trials and two stimuli and 
    connected them like the first one.

    ::
    
        for block in exp.blocks:
            for trial in block.trials:
                trial.stimuli[0].present()
                exp.clock.wait(1000)
    
    We loop over all blocks in the experiment (two in our case). For each of 
    the blocks, we loop again over all trials in that block (again two in our 
    case).  For each trial we present the first stimulus (because we only added 
    one to each trial). After each stimulus presentation we wait for 1000 ms.

We now want to measure some reaction times after each stimulus presentation.
Modify the code to look like this::

    import expyriment

    exp = expyriment.design.Experiment(name="Text Experiment")
    expyriment.control.initialize(exp)

    block_one = expyriment.design.Block(name="A name for the first block")
    trial_one = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 1, Trial 1")
    stim.preload()
    trial_one.add_stimulus(stim)
    trial_two = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 1, Trial 2")
    trial_two.add_stimulus(stim)
    block_one.add_trial(trial_one)
    block_one.add_trial(trial_two)
    exp.add_block(block_one)

    block_two = expyriment.design.Block(name="A name for the second block")
    trial_one = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 2, Trial 1")
    stim.preload()
    trial_one.add_stimulus(stim)
    trial_two = expyriment.design.Trial()
    stim = expyriment.stimuli.TextLine(text="I am a stimulus in Block 2, Trial 2")
    trial_two.add_stimulus(stim)
    block_two.add_trial(trial_one)
    block_two.add_trial(trial_two)
    exp.add_block(block_two)

    expyriment.control.start()

    for block in exp.blocks:
        for trial in block.trials:
            trial.stimuli[0].present()
            key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                         expyriment.misc.constants.K_RIGHT])
            exp.data.add([block.name, trial.id, key, rt])

    expyriment.control.end()

When you run this code, the following happens:

* Expyriment will start up, showing the startup screen and a countdown of 10 
  seconds
* "Preparing experiment..." will be presented on the screen
* You will be asked to enter the subject numtrial_one.add_stimulusber
* "Ready" will be presented on the screen
* After pressing ENTER the stimuli are presented in the order: stimuli in 
  trial_one and trial_two of block_one followed by the stimuli in trial_one and 
  trial_two of block_two. After each presentation the programme waits for the 
  LEFT or RIGHT arrow key to be pressed until it proceeds.
* "Ending experiment..." will be presented on the screen

Let's see why this is:

    ::
    
        key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
                            
    We waited for a keyboards response which is either the LEFT or the RIGHT 
    arrow key (as defined by a list with those two keys as elements).  This 
    function returns the key that was pressed as well as the reaction time.

    ::
    
        exp.data.add([block.name, trial.id, key, rt])
    
    We added the name of the block, the id of the trial, the pressed key and 
    the reaction time to the data file (by adding a list with those two as 
    elements).  The id of a trial is automatically set when the trial is added 
    to a block.

    Now have a look at the "data" and "events" directories (in the same 
    directory where your first_example.py is located). The "data" directory 
    contains data log files, named according to the experiment name, the 
    subject number and a timestamp. The file ending is .xpd. (Note: To 
    disable time stamps in output filenames, you have change the defauls of
    the io module before you initialize your experiment: 
    ``expyriment.io.defaults.outputfile_time_stamp = False``).  The event 
    directory contains event log files with the ending .xpe.
    Open the latest data file to see the data we just logged. Notice that the 
    first rows are a header with some information about the file. However, it 
    would be nice to also have the variable names of what is logged in there. 
    To do this, add the following lines above where you start the experiment::

        exp.data_variable_names = ["Block", "Trial", "Key", "RT"]

    What this does is to add the given names into the data file header, 
    separated by commas.

The last thing to mention in this brief tutorial are the default settings.  
Each module (control, design, io, stimuli, misc) has its own defaults.  
Changing these defaults will only have an effect before the corresponding 
object is created. Thus, a safe place is right at the beginning of your file, 
just above creating an experiment. Note also that it is handy to overwrite 
other default settings in the beginning as well, to have one central place for 
important settings. It might also shorten calls to the classes later on. For 
instance, the ``experiment_name`` can also be set as 
``expyriemtn.design.defaults.experiment_name = "Test Experiment`` and the
``name="Test Experiment"`` parameter when creating the Experiment is  not
needed anymore. However, using explicit parameters in the call to classes
will overwrite any previous default settings!

One of the most common things to do, while developing is to change
to develop mode, which changes several default settings in one go (such as
setting the default presentation mode from fullscreen to a window, and skipping
the start screen and subject ID query)::

    expyriment.control.set_develop_mode(True)

That's it so far. We are at the end of the getting started tutorial. As a 
summary, have a look at the following code, which again shows the overall 
structure of an Expyriment file with the 3 main parts::

    import expyriment

    # Any global settings go here

    exp = expyriment.control.initialize()

    # Create design (blocks and trials)
    # Create stimuli (and put them into trials)
    # Create input/output devices (like button boxes etc.)

    expyriment.control.start()

    # Experiment conduction
    # Loop over blocks and trials, present stimuli and get user input

    expyriment.control.end()
