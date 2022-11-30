# covid-19-evaluation-tool
This project is a fundamental part of my PhD activity; the goal was to create a software tool
for the evaluation of the evaluation of the infection probability for Covid-19 in closed settings.
This tool is meant to be used by people who are not familiar with mathematical modelling then the goal
was to create a user-friendly software.


In this repository you will find a folder with the following codes in python:
1) interface.py obtained with Qt designer with the description of the graphical user interface
2) programme.py the code to make the GUI work correctly for the evaluation
3) dialog.py for the dialog window


You will find also a folder with the images embedded in the GUI and the dialog window (the resource_rc.py code is mandatory to import correctly images).
If you would like to have a standalone file in your windows computer you can compile the "programme.spec" file.


The tool will give a series of output files:
a) logbook to track all the evaluation performed and automatically updated
b) a file with the evaluation
c) a folder with the plots of the infection probability profiles

If you have any questions or suggestions please contact me.




