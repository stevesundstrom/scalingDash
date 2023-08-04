from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_daq as daq

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    html.H3('Dash Arithmetic'),
    html.Div(daq.NumericInput(
        id='n1',
        min=-100,
        max=100,
        value=1
    ), style={'display': 'inline-block', 'padding': 5}),
    html.Div(dcc.Dropdown(
        id='pmtd',
        options=['+', '-', '*', '÷'],
        value='+',
        clearable=False,
        searchable=False
    ), style={'display': 'inline-block', 'padding': 5, 'vertical-align': 'middle'}),
    html.Div(daq.NumericInput(
        id='n2',
        min=-100,
        max=100,
        value=2
    ), style={'display': 'inline-block', 'padding': 5}),
    html.Div('=', style={'display': 'inline-block', 'padding': 5}),
    html.Div(id='numeric-input-output', style={'display': 'inline-block'})
])


@callback(
    Output('numeric-input-output', 'children'),
    [Input('n1', 'value'),
     Input('pmtd', 'value'),
     Input('n2', 'value')]
)
def update_output(n1, pmtd, n2):
    if pmtd == '+':
        return n1 + n2
    elif pmtd == '-':
        return n1 - n2
    if pmtd == '*':
        return n1 * n2
    elif n2 == 0:
        return 'Err'
    else:
        return n1 / n2


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)
