from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import mysql.connector

# Función para crear una conexión a la base de datos
def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

# Función para seleccionar datos de la base de datos
def select_data():
    try:
        # Crear una conexión a la base de datos
        cnx, cursor = createConnection('sql10652849', 'sql10652849', 'eCzcDvEeph', 'sql10.freemysqlhosting.net', '3306')

        # Consulta SQL para obtener datos (ajusta la consulta según tu esquema de base de datos)
        query = "SELECT * FROM new_table"

        cursor.execute(query)

        # Obtener los datos
        data = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        cnx.close()

        return data

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu nombre de usuario o contraseña")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)

data = pd.DataFrame(select_data(), columns=["id_data", "humidity", "temperature", "date_time", "mq135Value", "proximity"])

# Crear una instancia de la aplicación Dash
app = Dash(__name__)

# Definir el diseño de la aplicación web
app.layout = html.Div([
    html.H1("Temperature and Humidity", style={'text-align': 'center'}),
    dcc.Graph(id='temperature-humidity-plot', figure=px.line(data, x='date_time', y=["humidity", "temperature", "mq135Value"], title="Temperature and humidity are closely related in outdoor applications")),
    dcc.Graph(id='proximity-plot', figure=px.line(data, x='date_time', y=["proximity"], title="Things are far away")),
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # Intervalo de actualización en milisegundos (5 segundos)
        n_intervals=0  # Inicialización del contador de intervalos
    )
])

@app.callback(
    [Output('temperature-humidity-plot', 'figure'),
     Output('proximity-plot', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    data = pd.DataFrame(select_data(), columns=["id_data", "humidity", "temperature", "date_time", "mq135Value", "proximity"])

    fig1 = px.line(data, x='date_time', y=["humidity", "temperature", "mq135Value"], title="Temperature and humidity")
    fig2 = px.line(data, x='date_time', y=["proximity"], title="Proximity")

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
