Example Experiments
===================

Here you can find some code examples to see Expyriment in action. All examples 
are fully working experiments.

Simon task
-----------
An experiment to asses a spatial stimulus-response compatibility effect (see 
`wikipedia <http://en.wikipedia.org/wiki/Simon_effect>`_).

.. literalinclude:: ../../examples/simon_task.py

Word fragment completion task
-----------------------------
Task as used for instance in `Weldon, 1991 <http://www.ncbi.nlm.nih.gov/pubmed/1829476>`_.
The script read in a stimulus list file (:download:`demo stimulus list 
<../../examples/word_fragment_completion_stimuluslist.csv>`).

.. literalinclude:: ../../examples/word_fragment_completion_task.py

Number classification task
--------------------------
A full experiment to access SNARC and SNARC-like effects in a number and a 
letter classification task (e.g., `Gevers, Reynvoer, & Fias (2003) 
<http://dx.doi.org/10.1016/S0010-0277(02)00234-2>`_) with two response 
mappings, error feedback and between-subject factors.

.. literalinclude:: ../../examples/snarc_experiment.py



Line bisection task
-------------------
Example of a line bisection task that is optimized for the use of touchscreens 
and the `Expyriment Android Runtime`_.

.. literalinclude:: ../../examples/line-bisection.py

.. _`Expyriment Android Runtime`: https://github.com/expyriment/expyriment-android-runtime/

Really short example
--------------------
Expyriment is efficient!. See here a very short example of an functioning 
experiment in less than 20 lines of pure code.

.. literalinclude:: ../../examples/really_short_exp.py

Data preprocessing
------------------
Preprocessing the data of the SNARC experiment for further statistical analysis.

.. literalinclude:: ../../examples/snarc_data_preprocessing.py 
