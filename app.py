from MainDataAnalysis import ccDat, ReTrans, DailyCounts
from dash import Dash, html, dash_table, dcc, Input, Output, State
import plotly.express as px
import os
from flask import Flask, send_from_directory
import base64
import io

current_directory = os.getcwd()

UPLOAD_DIRECTORY = current_directory + "/app_uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

server = Flask(__name__)
app = Dash(server=server)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

app.layout = html.Div([
    html.Div(children='VanSinE Finance', style={'textAlign': 'center', 'color':'black', 'fontSize':40}),
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
    html.Div(children='Card Balance Over Time', style={'textAlign': 'left', 'color':'black', 'fontSize':30}),
    dcc.Graph(figure=px.line(ccDat, x='Date', y='TotalBal', labels={"TotalBal": "Balance"})),
    html.Div(children='Credit Card Transactions', style={'textAlign': 'left', 'color':'black', 'fontSize':30}),
    dash_table.DataTable(data=ccDat.to_dict('records'), page_size=10),
    html.Div(children='Recurring Monthly Transactions', style={'textAlign': 'left', 'color':'black', 'fontSize':30}),
    dash_table.DataTable(data=ReTrans.to_dict('records')),
    html.Br(),
    html.Br(),
    html.Div(children='Number of Transactions by Weekday', style={'textAlign': 'left', 'color':'black', 'fontSize':30}),
    dcc.Graph(figure=px.bar(DailyCounts, x=DailyCounts.index, y=DailyCounts, labels={"y": "Number of Transactions"}))
])

# Callback to process and save uploaded files
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def save_uploaded_file(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        for content, name in zip(list_of_contents, list_of_names):
            print("LIST OF NAMES", name)
            # Separate the base64 encoded content from the header
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)
            # Save the file to the upload directory
            filepath = os.path.join(UPLOAD_DIRECTORY, name)
            print("OPENING" + filepath)
            with open(filepath, 'wb') as f:
                 f.write(decoded)
        return html.Div([html.H5(f"Uploaded {', '.join(list_of_names)} successfully!")])
    return html.Div(['No files uploaded yet.'])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

#from MainDataAnalysis import ccDat, ReTrans, DailyCounts
# from dash import Dash, html, dash_table, dcc, Input, Output, State
# import plotly.express as px
# import os
# from flask import Flask, send_from_directory
# import base64
# from Functions import GetData, CleanTDdata, RecurringTransactions

# os.chdir('/Users/keenansmacbook/Desktop/AccountingProject')

# UPLOAD_DIRECTORY = "/Users/keenansmacbook/Desktop/AccountingProject/app_uploaded_files"
# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

# server = Flask(__name__)
# app = Dash(server=server)

# # Callback to process and save uploaded files
# @app.callback(
#     [Output('output-data-upload', 'children'), 
#      Output('graph-output1', 'figure'),
#      Output('graph-output2', 'figure')],
#     [Input('upload-data', 'contents')],
#     [State('upload-data', 'filename')])


# # @server.route("/download/<path:path>")
# # def download(path):
# #     """Serve a file from the upload directory."""
# #     return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

# def save_process_file(list_of_contents, list_of_names):
#     if list_of_contents is not None:
#         for content, name in zip(list_of_contents, list_of_names):
#             # Separate the base64 encoded content from the header
#             content_type, content_string = content.split(',')
#             decoded = base64.b64decode(content_string)
#             # Save the file to the upload directory
#             filepath = os.path.join(UPLOAD_DIRECTORY, name)
#             with open(filepath, 'wb') as f:
#                 f.write(decoded)
#             ccDatRaw = GetData('/Users/keenansmacbook/Desktop/AccountingProject/app_uploaded_files')
#             ccDat = CleanTDdata(ccDatRaw)
#             ReTrans = RecurringTransactions(ccDat)
#             DailyCounts = ccDat['weekday'].value_counts()
#             ccBalanceFig = px.line(ccDat, x='Date', y='TotalBal', labels={"TotalBal": "Balance"})
#             DailyCountsFig = px.bar(DailyCounts, x=DailyCounts.index, y=DailyCounts, labels={"y": "Number of Transactions"})


#         return html.Div([html.H5(f"Uploaded {', '.join(list_of_names)} successfully!")]), ccDat, ReTrans, DailyCounts, ccBalanceFig, DailycountsFig
#     return html.Div(['No files uploaded yet.'])

# app.layout = html.Div([
#     html.Div(children='VanSinE Finance', style={'textAlign': 'center', 'color':'black', 'fontSize':40}),
#     html.Br(),
#     dcc.Upload(
#         id='upload-data',
#         children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
#         style={
#             'width': '100%',
#             'height': '60px',
#             'lineHeight': '60px',
#             'borderWidth': '1px',
#             'borderStyle': 'dashed',
#             'borderRadius': '5px',
#             'textAlign': 'center',
#             'margin': '10px'
#         },
#         multiple=True
#     ),
#     html.Div(id='output-data-upload'),
#     html.Br(),
#     html.Div(children='Card Balance Over Time', style={'textAlign': 'left', 'color':'black', 'fontSize':30}),
#     dcc.Graph(id='graph-output1'),
#     html.Div(children='Credit Card Transactions', style={'textAlign': 'left', 'color':'black', 'fontSize':30}),
#     #dash_table.DataTable(data=ccDat.to_dict('records'), page_size=10),
#     #html.Div(children='Recurring Monthly Transactions', style={'textAlign': 'left', 'color':'black', 'fontSize':30}),
#     #dash_table.DataTable(data=ReTrans.to_dict('records')),
#     html.Br(),
#     html.Br(),
#     html.Div(children='Number of Transactions by Weekday', style={'textAlign': 'left', 'color':'black', 'fontSize':30}),
#     dcc.Graph(id='graph-output2')
# ])

# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True)