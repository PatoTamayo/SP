# Basic Dash application that displays a heading, a table, and a plotly graph.

# Basic imports
from dash import Dash, html, dash_table, dcc
import plotly.express as px
import pandas as pd
import mysql.connector

def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(user=user_name, database=database_name,
    password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)


# Create some data
def select_data():
    """Selects all the data from the database"""
    try:
        # Create a connection to the database
        cnx, cursor = createConnection('root', 'IoT_situacion_problema', 'tecdemonterrey', 'localhost', '3306')

        # Query the database
        query = ("SELECT * FROM new_table")

        # Execute the query
        cursor.execute(query)

        # Get the data
        data = cursor.fetchall()

        # Return the data
        return data
    
    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        """Close the connection"""
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or
        'cursor' in globals()):
            cnx.close()
            cursor.close()


# Create a plotly line graph
# Data must be in a pandas dataframe, so we convert it to a dataframe first
# The columns parameter is used to name the columns of the dataframe
data = pd.DataFrame(select_data(), columns=["id_data","humidity", "temperature","date_time"])

# Dash is a framework for building web applications. It is built on top of Flask, Plotly.js, and React.js.

# Create a Dash application instance
app = Dash(__name__)

# Dash apps are composed of HTML components. Some basic knowledge of HTML is ideal, but not necesarilly required. 
# The app layout represents the app components that will be displayed in the web browser, normally contained within a html.Div.

# Define the layout of the web application
app.layout = html.Div([
    # A div is a container for other HTML elements. These are usually stored in the children property.
    html.Div(
        # The children property is used to define the elements that will be displayed inside the div.
        children=[
            # The html.H1 component is used to display a heading. The style property is used to give the heading styling properties.
            # In this case, the style is used to center the heading.
            html.H1("Temperature and Humidity", style={'text-align': 'center'}),
            dcc.Graph(figure=px.line(data, x='id_data', y=["humidity", "temperature"], title="Temperature and humidity are closely related in outdoor applications")),

            # The dataTable component is used to display data in a table format.
           

            # The dcc.Graph component is used to display a plotly graph.
           
        ])
])

app.run_server(debug=True)