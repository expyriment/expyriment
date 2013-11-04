Import Expyriment data into R
=============================
The following function expyriment_data.R_ concatenates all data and returns an R data 
frame with all subjects. Between subject factors will be added as variables to 
the data matrix.::

    #!/usr/bin/Rscript
    # read.expyriment.data(folder, file)
    #
    # Import exypriment data into R. The function concatinates all data and returns
    # a R data frame with all subjects. Between subject factors will be added as
    # variables to the data matrix.
    #
    # Arguments:
    #   folder           -- the data folder (string)
    #   filename_pattern -- the pattern with which the names of each data file
    #                         start (string)
    #
    # Oliver Lindemann, 2012
     
    read.expyriment.data = function(folder, file) 
    {
    	data = data.frame()
    	for (fl_name in list.files(path=folder, file)) {
    		path = file.path(folder, fl_name)
    		message("reading ", path)
    		d = read.csv(path, comment.char="#")
    		fl = file(path, "r")
    		while(TRUE){
    			 line = readLines(fl, n=1)
    			 if (!length(line) || !length(grep("#", line)) )
    			 	break
    			 else {
    				if (length(grep("^#s ", line))>0) {
    					tmp = unlist(strsplit(sub("#s ","", line), ":"))
    					if (length(tmp)<2) {
    						tmp = unlist(strsplit(sub("#s ","", line), "="))
    					}
    					if (grep("^ ", tmp[2]))
    						tmp[2] = substring(tmp[2], 2)
    					if (tmp[1] != "id") {
    						d = cbind(d, new = tmp[2])
    						names(d)[ncol(d)] = tmp[1]
    					}
    				}
    			}
    		}
    		close(fl)
    		if (nrow(data)<1) 
    			data = d
    		else 
    			data = rbind(data, d)
    	}
    	data
    }

.. _expyriment_data.R: https://gist.github.com/lindemann09/497283a29ee69cc7e7a2
