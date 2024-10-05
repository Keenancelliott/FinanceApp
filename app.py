from Functions import process_uploaded_data
from dash import Dash, html, dash_table, dcc, Input, Output, State
import plotly.express as px
import os
from flask import Flask, send_from_directory
import base64
#import io
import pandas as pd  # For processing uploaded data

current_directory = os.getcwd()

UPLOAD_DIRECTORY = current_directory + "/app_uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

server = Flask(__name__)
app = Dash(server=server)

# Route to serve files for download (optional)
@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

app.layout = html.Div([
    html.Div(children='VanSinE Finance', style={'textAlign': 'center', 'color': 'black', 'fontSize': 40}),
    html.Br(),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Br(),
    
    # Placeholder graphs and tables before data is uploaded
    html.Div(id='graphs-and-tables')
])

# Function to generate empty figures
def generate_empty_graphs_and_tables():
    return html.Div([
        html.Div(children='Card Balance Over Time', style={'textAlign': 'left', 'color': 'black', 'fontSize': 30}),
        dcc.Graph(figure=px.line(pd.DataFrame(), x=None, y=None)),
        html.Div(children='Credit Card Transactions', style={'textAlign': 'left', 'color': 'black', 'fontSize': 30}),
        dash_table.DataTable(data=[], page_size=10),
        html.Div(children='Recurring Monthly Transactions', style={'textAlign': 'left', 'color': 'black', 'fontSize': 30}),
        dash_table.DataTable(data=[]),
        html.Br(),
        html.Br(),
        html.Div(children='Number of Transactions by Weekday', style={'textAlign': 'left', 'color': 'black', 'fontSize': 30}),
        dcc.Graph(figure=px.bar(pd.DataFrame(), x=None, y=None))
    ])

# Initial rendering (empty state)
@app.callback(
    Output('graphs-and-tables', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_graphs(list_of_contents, list_of_names):
    if list_of_contents is None:
        # Display empty graphs if no files are uploaded
        return generate_empty_graphs_and_tables()

    # Process the uploaded files
    for content, name in zip(list_of_contents, list_of_names):
        content_string = content.split(',')[1]
        decoded = base64.b64decode(content_string)
        filepath = os.path.join(UPLOAD_DIRECTORY, name)
        with open(filepath, 'wb') as f:
            f.write(decoded)
    
    # Assume process_uploaded_data returns processed DataFrames (ccDat, ReTrans, DailyCounts)
    ccDat, ReTrans, DailyCounts = process_uploaded_data()

    # Return populated graphs and tables
    return html.Div([
        html.Div(children='Card Balance Over Time', style={'textAlign': 'left', 'color': 'black', 'fontSize': 30}),
        dcc.Graph(figure=px.line(ccDat, x='Date', y='TotalBal', labels={"TotalBal": "Balance"})),
        html.Div(children='Credit Card Transactions', style={'textAlign': 'left', 'color': 'black', 'fontSize': 30}),
        dash_table.DataTable(data=ccDat.to_dict('records'), page_size=10),
        html.Div(children='Recurring Monthly Transactions', style={'textAlign': 'left', 'color': 'black', 'fontSize': 30}),
        dash_table.DataTable(data=ReTrans.to_dict('records')),
        html.Br(),
        html.Br(),
        html.Div(children='Number of Transactions by Weekday', style={'textAlign': 'left', 'color': 'black', 'fontSize': 30}),
        dcc.Graph(figure=px.bar(DailyCounts, x=DailyCounts.index, y=DailyCounts, labels={"y": "Number of Transactions"}))
    ])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
