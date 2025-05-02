# Setup Instructions

## Clone the repository:
`git clone https://github.com/abeTroop/Health-Inspection-Database.git`
`cd Healt-Inspection-Database`

## Install Python Flask:
`pip install Flask psycopg2`

## Set up database:
Execute `health_inspection_database_dump.sql` with a PostgreSQL tool like PgAdmin

## Fill in database information:
In `app.py` modify this line to include your information:
  `dbname="cse412_project", user="postgres", password="temp", host="localhost", port="5432"`

## Configure Google Maps API:
Go to https://mapsplatform.google.com/ to get an API Key
In `index.html`, replace `YOUR_API_KEY` to include your information:
  `src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap&v=weekly"`

## Run the program:
Run `python app.py`
Navigate to http://127.0.0.1:5000/
