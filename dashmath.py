from dash import Dash, dcc, html, Input, Output, callback
import dash_daq as daq

app = Dash(__name__)

app.layout = html.Div([
    html.H2('Dash Math', style={'display': 'inline-block'}),
    html.Div(daq.NumericInput(
        id='n1',
        min=-100,
        max=100,
        value=1
    ), style={'display': 'inline-block', 'padding': 5}),
    html.Div(dcc.Dropdown(
        id='pmmd',
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
     Input('pmmd', 'value'),
     Input('n2', 'value')]
)
def update_output(n1, pmmd, n2):
    if pmmd == '+':
        return n1 + n2
    elif pmmd == '-':
        return n1 - n2
    if pmmd == '*':
        return n1 * n2
    elif n2 == 0:
        return 'Err'
    else:
        return n1 / n2


if __name__ == '__main__':
    app.run()
