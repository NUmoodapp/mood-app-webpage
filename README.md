# Getting started with Mood app locally

## Prerequisites

1. Ensure you have [Node.js](https://nodejs.org/en/download/) installed.

## How to run the app

1. Clone this repo, then change directory to the project root and run `npm install` to install dependencies.
2. To run the Express server and React app together, run `npm run dev`.
3. To run the backend, navigate to the /api folder and run `flask run`. You may need to set up your python dependencies first (see below).

## Setting up the back end server 
I followed this guide https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project for the backend. Here's the gist:

1. Navigate to the /api folder and run `python -m venv venv` and then `source venv/bin/activate` (mac) or `venv\Scripts\activate` (windows)
2. Install packages with `pip install flask python-dotenv`
3. Make sure the .flaskenv file is present, then run `flask run`

The back end won't look like much, but when it's running it'll give you a song when you input a statement to the front end. 

Message me with any questions!