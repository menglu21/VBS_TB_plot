# VBS_TB_plot
step1: use mergeRoot_step1.py to merge the root files into new files with larger size, to decrease the number of root file and reduce the final condor job
step2: use prepare_condor_step2.py to prepare condor file for plotting
step3: use submit_step3.py to submit condor jobs
step4: use mergeOutput_step4.py to merge the output of condor, i.e., the histograms
step5: use plot.py in PlotCode_step5 to get the final plot
