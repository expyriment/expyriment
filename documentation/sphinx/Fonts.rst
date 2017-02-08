Using fonts
===========
Expyriment has support for system fonts and user provided fonts.

Fonts by name
-------------
When started, Expyriment will scan for available fonts on the system it runs
on and create names for each of them.
To get a list of available names and corresponding fonts, run::

    expyriment.misc.list_fonts()

When setting a font by name in a text-based stimulus (e.g. ``stimuli.TextLine``),
Expyriment will always try to match the given name of the font to a font it has
found on the system that is most similar.
For instance, to set a mono spaced font, one of the following will work::

    stim = expyriment.stimuli.TextLine("Hello", text_font="Monospace")
    stim = expyriment.stimuli.TextLine("Hello", text_font="Mono")
    stim = expyriment.stimuli.TextLine("Hello", text_font="Courier")


**This mechanism will not guarantee that the same name, will lead to the**
**exact same font across different machines!**
**If no filename can be matched, Expyriment will fall back to a default font!**

Fonts by file
--------------
To guarantee that the same font is used across different systems, the full
path to any (TrueType) font file (a system file or a user supplied one)
can also be given as an argument::

    stim = expyriment.stimuli.TextLine("Hello", text_font="/Library/Fonts/Andale Mono.ttf")

**If the font file cannot be found, an error is raised!**

Expyriment fonts
----------------
To have a set of fonts that is guaranteed to be available across platforms,
Expyriments comes with the fonts "freemono", "freesans" and "freeserfif" included.
You can use them directly like this::

    stim = expyriment.stimuli.TextLine("Hello", text_font="freemono")
