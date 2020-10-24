# Import the functions we need from flask
from flask import Flask
from flask import render_template 
from flask import jsonify

# Import the functions we need from SQL Alchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import sqlite3
import os

# Define the database connection parameters
# username = 'postgres'  # Ideally this would come from config.py (or similar)
# password = '1234'  # Ideally this would come from config.py (or similar)
# database_name = 'GlobalFirePower' # Created in Week 9, Night 1, Exercise 08-Stu_CRUD 
# connection_string = f'postgresql://{username}:{password}@localhost:5432/{database_name}'

# Connect to the database
# engine = create_engine(connection_string)
database_path = "Project2.db"
engine = create_engine(f"sqlite:///{database_path}?check_same_thread=False")
base = automap_base()
base.prepare(engine, reflect=True)

connection = sqlite3.connect("Project2.db")

# Choose the table we wish to use
table = base.classes.EVData

# Instantiate the Flask application. (Chocolate cake recipe.)
# This statement is required for Flask to do its job. 
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Effectively disables page caching

# Here's where we define the various application routes ...
@app.route("/")
def IndexRoute():
    ''' This function runs when the browser loads the index route. 
        Note that the html file must be located in a folder called templates. '''

    webpage = render_template("index.html")
    return webpage

@app.route("/other")
def OtherRoute():
    ''' This function runs when the user clicks the link for the other page.
        Note that the html file must be located in a folder called templates. '''

    # Note that this call to render template passes in the title parameter. 
    # That title parameter is a 'Shirley' variable that could be called anything 
    # we want. But, since we're using it to specify the page title, we call it 
    # what we do. The name has to match the parameter used in other.html. 
    webpage = render_template("other.html", title_we_want="EVData")
    return webpage

@app.route("/map")
def MapRoute():
    ''' This function runs when the user clicks the link for the other page.
        Note that the html file must be located in a folder called templates. '''

    # Note that this call to render template passes in the title parameter. 
    # That title parameter is a 'Shirley' variable that could be called anything 
    # we want. But, since we're using it to specify the page title, we call it 
    # what we do. The name has to match the parameter used in other.html. 
    webpage = render_template("map.html", title_we_want="EVData")
    return webpage

@app.route("/facility_type")
def FacilityRoute():
    ''' This function runs when the user clicks the link for the other page.
        Note that the html file must be located in a folder called templates. '''

    # Note that this call to render template passes in the title parameter. 
    # That title parameter is a 'Shirley' variable that could be called anything 
    # we want. But, since we're using it to specify the page title, we call it 
    # what we do. The name has to match the parameter used in other.html. 
    webpage = render_template("facility_type.html", title_we_want="Facility Type")
    return webpage

@app.route("/chargernetwork")
def ChargerRoute():
    webpage = render_template("chargernetwork.html", title_we_want="Charger Networks")
    return webpage    




@app.route("/chargersperstate")
def QueryChargersperstate():
    ''' Query the database for chargers per state and return the results as a JSON. '''

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.State).all()
    session.close()

    # Create a list of dictionaries, with each dictionary containing one row from the query. 
    # all_charger = []
    # for State in results:
    #     dict = {}
    #     dict["State"] = State
    #     all_charger.append(dict)

    chargercount = {}
    for State in results:
        if (State[0] in chargercount):
            chargercount[State[0]]+=1
        else:
            chargercount[State[0]] = 1

    # Return the jsonified result. 
    return jsonify(chargercount)

@app.route("/facilitytype")
def QueryFacilityType():
    ''' Query the database for facility types and return the results as a JSON. '''

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.Facility_Type).all()
    session.close() 

    # Create a list of dictionaries, with each dictionary containing one row from the query. 
    # all_facilitytype = []
    # for facilitytype in results:
    #     dict = {}
    #     dict["facilitytype"] = type
    #     all_facilitytype.append(dict)

    facilitycount = {}
    for Facility_Type in results:
        if Facility_Type[0] != "Unknown":
            if (Facility_Type[0] in facilitycount):
                facilitycount[Facility_Type[0]]+=1
            else:
                facilitycount[Facility_Type[0]] = 1
        else:
            continue


    # Return the jsonified result. 
    return jsonify(facilitycount)

@app.route("/locations")
def QueryLocations():
    ''' Query the database for locations and return the results as a JSON. '''
    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.Latitude, table.Longitude).all()
    session.close

    return jsonify(results)

@app.route("/newlocations")
def QuerynewLocations():
    ''' Query the database for fighter aircraft and return the results as a JSON. '''

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.Latitude, table.Longitude, table.State, table.Street_Address, table.EV_Connector_Types, table.EV_Network,
                            table.City, table.ZIP).all()
    session.close()

    # Create a list of dictionaries, with each dictionary containing one row from the query. 
    all_cord = []
    for result in results:
        dict = {}
        dict["lat"] = result[0]
        dict["lon"] = result[1]
        dict["state"] = result[2]
        dict["address"] = result[3]
        dict["ctype"] = result[4]
        dict["network"] = result [5]
        dict["city"] = result [6]
        dict["zip"] = result [7]
        all_cord.append(dict)

    # Return the jsonified result. 
    return jsonify(all_cord)

@app.route("/networks")
def QueryNetwork():
    ''' Query the database for facility types and return the results as a JSON. '''
    
    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.EV_Connector_Types).all()
    session.close()
    
    connectortype = {}
    for EV_Connector_Type in results:
        if (EV_Connector_Type[0] in connectortype):
            connectortype[EV_Connector_Type[0]]+=1
        else:
            connectortype[EV_Connector_Type[0]] = 1
    

    # # Return the jsonified result. 
    return jsonify(connectortype)



if __name__ == '__main__':
    app.run(debug=True)

# @app.route("/test")
# def TestRoute():
#     ''' This function returns a simple message, just to guarantee that
#         the Flask server is working. '''

#     return "This is the test route!"

# @app.route("/dictionary")
# def DictionaryRoute():
#     ''' This function returns a jsonified dictionary. Ideally we'd create 
#         that dictionary from a database query. '''

#     dict = { "Fine Sipping Tequila": 10,
#              "Beer": 2,
#              "Red Wine": 8,
#              "White Wine": 0.25}
    
#     return jsonify(dict) # Return the jsonified version of the dictionary

# @app.route("/dict")
# def DictRoute():
#     ''' This seems to work in the latest versions of Chrome. But it's WRONG to
#         return a dictionary (or any Python-specific datatype) without jsonifying
#         it first! '''        

#     dict = { "one": 1,
#              "two": 2,
#              "three": 3}
    
#     return dict # WRONG! Don't return a dictionary! Return a JSON instead. 


# # This statement is required for Flask to do its job. 
# # Think of it as chocolate cake recipe. 