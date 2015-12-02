#!/usr/bin/Rscript
# read.expyriment.data(folder, filename_pattern)
#
# Import Exypriment data into R. The function concatinates all data and returns
# a R data frame with all subjects. Between subject factors will be added as
# variables to the data matrix.
#
# Arguments:
#     folder           -- the data folder (string)
#     filename_pattern -- the pattern with which the names of each data file
#                         start (string)
#
# Copyright: 2012-2015 Florian Krause <siebenhundertzehn@googlemail.com>
#            2012-2015 Oliver Lindemann <lindemann09@googlemail.com>
# License: GPL-3.0+
 
read.expyriment.data = function(folder, filename_pattern) 
{
	pattern = paste("^", filename_pattern, ".*\\.xpd", sep="") 

	data = data.frame()
	for (fl_name in list.files(path=folder, pattern )) {
		path = file.path(folder, fl_name)
		message("reading ", path)
		d = read.csv(path, comment.char="#", na.strings=c("NA", "None"))
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
