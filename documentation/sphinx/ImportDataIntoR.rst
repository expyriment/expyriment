Import Expyriment data into R
=============================
The method *misc.data_preprocessing.write_concatenated_data()* in
:doc:`Data Preprocessing <expyriment.misc.data_preprocessing>`)
allows to write R data frames, which can then be imported into R.

Alternatively, the R function expyriment_data.R_ concatenates all data and returns an R data
frame with all subjects. Between subject factors will be added as variables to 
the data matrix.

.. _expyriment_data.R: https://raw2.github.com/expyriment/expyriment-tools/master/expyriment_data.R
