Data preprocessing and exporting
================================

Data preprocessing
------------------
In most cases, data acquired by Expyriment needs to be further processed before 
a statistical analysis can be performed. This processing entails an aggregation 
of the dependent variables over all factor-level combinations of the 
experimental design. Expyriment provides an easy, but flexible way to
automate this process with the included data preprocessing module of the misc 
package (:doc:`expyriment.misc.data_preprocessing`).

Exporting data
--------------
In some cases, one might export the recorded data to preprocess it in other programmes.
Expyriment allows for this, too.

CSV format
~~~~~~~~~~
The method ``misc.data_preprocessing.write_concatenated_data()`` in
:doc:`Data Preprocessing <expyriment.misc.data_preprocessing>`
allows to export the concatenated data as a CSV (comman separated values) file.

R data frame
~~~~~~~~~~~~
The method ``misc.data_preprocessing.write_concatenated_data()`` in
:doc:`Data Preprocessing <expyriment.misc.data_preprocessing>`
also allows to export the concatenated data as an R data frames,
which can then be imported into R.
Please be aware that this functionality needs the rpy2_ package installed.

Alternatively, you may use the R module expyriment_data.R_ to handle xpd files without
data preprocessing in Python. The R function ``read.expyriment.data`` concatinates all
raw data and returns an R data frame with all subjects. Between subject factors will 
be added as variables to the data matrix.

.. _expyriment_data.R: https://github.com/expyriment/expyriment-stash/blob/master/tools/expyriment_data.R
.. _rpy2: http://rpy.sourceforge.net
