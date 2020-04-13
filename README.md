# Project 1

Web Programming with Python and JavaScript

The aims of the project is to build a website for searching informations and review books.

Main file in this repository:
 - books.csv: csv file contain information about books
 - models.py: contain the definitions of each table in database
 - import.py: create data base and add information in books.csv to the database
 - application.py: flask application file
 - requirements.txt: use to install some programs which is necessary for running the website

Main folder in this repository:
 - templates folder: contain all .html files
 - static folder: contain all stylesheet files and images files used in the website
 - flask session: contain attributes files
 - __pycache__: contain attributes files

 To run the project:
 - First computer need to be install python version 3.6 or higher and pip3
 - Run command 'pip3 install -r requirements.txt' in your terminal window to make sure that
 all of the necessary Python packages are installed.
 - Run command 'export FLASK_APP=application.py', 'export FLASK_DEBUG=1'
 - Run command 'export DATABASE_URL="postgres://qomyhclyatesll:82c7ad019c13196ab8b87da38866f8839ed4f8246d52a8248724ed97612cccea@ec2-52-71-85-210.compute-1.amazonaws.com:5432/d2gsskts8mt67g"'
  - Run flask run
  - Use browser to navigate http://127.0.0.1:5000