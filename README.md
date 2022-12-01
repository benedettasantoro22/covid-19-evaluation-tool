# Covid-19 evaluation tool
The goal of this project was to create a software tool
for the evaluation of the infection probability for Covid-19 in closed settings.
This tool is meant to be used by people who are not familiar with mathematical modelling then the aim
was to create a user-friendly software.


In this repository you will find a folder with the following codes in python:
1. [interface.py obtained with Qt designer with the description of the graphical user interface](code/interface.py)
2. programme.py the code to make the GUI work correctly for the evaluation
3. dialog.py for the dialog window embedded in the main window


You will find also a folder with the images used in the GUI and the dialog window (the resource_rc.py code is mandatory to import correctly images).

## Using the code
You just need to import the repository in your local computer:

` git clone https://github.com/benedettasantoro22/covid-19-evaluation-tool.git `

and run the code:

` python .\programme.py `

If you have a Windows computer and want to obtain a standalone file, you can compile the "programme.spec":

`pyinstaller programme.spec  `                                   

## Output files

The tool will give a series of output files:
+ logbook to track all the evaluation performed and automatically updated
* a text file with the evaluation
- a folder with the plots of the infection probability profiles

If you have any questions or suggestions please contact me by email.




