import dash
from dash_html_components import Div
from dash_table import DataTable

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


data=[
    dict(a=''' ```javascript
return 20;
    ```
'''), # need to dedent the ``` for actual usage
    dict(a='''An image\n
![Plotly](https://aws1.discourse-cdn.com/business7/uploads/plot/original/2X/7/7957b51729ad7fd9472879cd620b9b068d7105bb.png)'''),
    dict(a='''
_italics_\n
**bold**\n
~~strikethrough~~
'''),
    dict(a='''Nested table
Statement | Is it true?
--- | ---
This page has two tables | yes
This table has two rows | no
This is an example of tableception | yes
'''),
    dict(a='[Dash documentation](https://dash.plot.ly)')
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 

app.layout = Div([
    DataTable(
        columns=[
            dict(name='a', id='a', type='text', presentation='markdown'),
        ],
        css=[
            dict(selector='img[alt=Plotly]', rule='height: 200px;')
        ],
        data=data
    ),
])

app.run_server(debug=True)