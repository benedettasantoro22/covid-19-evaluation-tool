
# Tool for the evaluation of infection probability from Covid-19 indoor

<img
  src="/code/IMMAGINI-GUI/corona-virus.jpg"
  alt="Alt text"
  title=""
  style="float right;width:200px;height:200px">


The goal of this project was to create a software tool
for the evaluation of the infection probability for Covid-19 in closed settings.
This tool is meant to be used by people who are not familiar with mathematical modelling then the aim
was to create a user-friendly software.

The code is totally written in Python and for the graphical part I used the PyQT5 library.
In this repository you will find the [code](code) folder with the following files:
1. [interface.py](code/interface.py) the code for the implementation of the graphical user interface;
2. [programme.py](code/programme.py) the code to make the GUI work correctly for the evaluation;
3. [dialog.py](code/dialog.py) for the dialog window embedded in the main window.

You will find also a [folder](code/IMMAGINI-GUI) with the images used in the GUI and the dialog window (the resource_rc.py code is mandatory to import correctly images).

## Using the code
You just need to import the repository in your local computer:

` git clone https://github.com/benedettasantoro22/covid-19-evaluation-tool.git `

go to the folder:

`  cd covid-19-evaluation-tool.git `

and run the code:

` python .\programme.py `

You'll probably need to install some additional libraries to run the code, like PyQT5; if so type:

` pip install library_name `

If you prefer a standalone file, you can compile the "programme.spec" [^1] file:

`pyinstaller programme.spec  `                                   

For all instructions on how touse the GUI see the [README.md](code/README.md) file.

If you have any questions or suggestions please contact me by email. 

[^1]: You need to install pyinstaller for this operation.


