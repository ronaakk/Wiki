# Wiki

## Project Aims:
The aim of this project was to build a Wikipedia-like online encyclopedia using the Python Django framework. Users can view available article entries, as well as search for entries on the site. New entries can be created by users, and existing entries can be edited. There is also a 'random page' function that selects and displays a page of the encyclopedia at random.

## Technologies:

Back-end:

* Python
* Django

Front-end:

* HTML (with Django templating)
* CSS (with some Bootstrap Components)

# Functionality

* By clicking an entry, the user will be taken to that entries page where its content will be displayed
* By typing a query in the search bar, the user will be taken to the query if it matches the name of an existing query, or taken to a page listing similar queries if it happens to be a subtring of an actual entry (ex. "py" in "python"), or lastly, taken to an error page where the user is prompted to create a page of their own.
* By clicking "Create New Page" users will be able to create a new page using Github Markdown, where it will be converted into HTML once saved and rendered.
* By clicking "Random Page" the user will be taken to a random entry that is currently within the application.
* On each entry's page, there is an "Edit Page" button which allows users to edit/Update the pages content in Github Markdown.

## Usage:

Requires Python(3) and the Python Pacakage Installe (pip) to run:

* Install requirements (Django): `pip3 install -r requirements.txt`
* Run the app locally: `python3 manage.py runserver`
