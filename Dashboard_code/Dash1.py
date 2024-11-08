# Importing libraries
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from dash import html
import numpy as np

# Load the enrollment data
data = pd.read_csv('enrolment_age_2019_20.csv')

# Calculate total enrollment for each row (both genders combined)
data['total_enrollment'] = data.filter(regex='class.*').sum(axis=1)

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Load the dropout rate data
dropout_data = pd.read_csv('C:/Users/abhis/Desktop/no/LLAMAINDEX_COURSE/UDISE_2020_21_Table_5.13.csv')
india_data = dropout_data[dropout_data['India/State /UT'] == 'India']

# Extract dropout rates for boys and girls
boys_dropout = [
    india_data['Dropout Rate - Primary (1 to 5) - Boys'].values[0],
    india_data['Dropout Rate - Upper Primary (6-8) - Boys'].values[0],
    india_data['Dropout Rate - Secondary (9-10) - Boys'].values[0],
]

girls_dropout = [
    india_data['Dropout Rate - Primary (1 to 5) - Girls'].values[0],
    india_data['Dropout Rate - Upper Primary (6-8) - Girls'].values[0],
    india_data['Dropout Rate - Secondary (9-10) - Girls'].values[0],
]

categories = ['Primary (1 to 5)', 'Upper Primary (6 to 8)', 'Secondary (9 to 10)']

# Load the countries data
df = pd.read_csv('C:/Users/abhis/Desktop/no/LLAMAINDEX_COURSE/RS_Session_265_AU_1191_A.csv')
columns_to_fill = ['2019', '2020', '2021', '2022', '2023']
df[columns_to_fill] = df[columns_to_fill].fillna(0)
df[columns_to_fill] = df[columns_to_fill].apply(pd.to_numeric, errors='coerce')

data_new = pd.read_csv('Data_set.csv')
data_new.columns = data_new.columns.str.strip()  # Strip spaces from column names
data_new = data_new.drop(index='India', errors='ignore')
# Define functions for plotting

states = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
    'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
    'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan',
    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
    'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands',
    'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
    'Lakshadweep', 'Delhi', 'Puducherry'
]
def plot_gender_distribution(data):
    class_levels = [col.replace("class_", "").replace("_boys", "") for col in
                    data.filter(regex='class_.*_boys').columns]
    class_columns_boys = data.filter(regex='class_.*_boys').sum().values
    class_columns_girls = data.filter(regex='class_.*_girls').sum().values

    gender_distribution = pd.DataFrame({
        'Class': class_levels,
        'Boys': class_columns_boys,
        'Girls': class_columns_girls
    })

    figure = go.Figure()
    figure.add_trace(
        go.Bar(x=gender_distribution['Class'], y=gender_distribution['Boys'], name='Boys', marker_color='skyblue'))
    figure.add_trace(
        go.Bar(x=gender_distribution['Class'], y=gender_distribution['Girls'], name='Girls', marker_color='salmon'))

    figure.update_layout(barmode='group', title='Gender Distribution by Class Level', xaxis_title='Class Level',
                         yaxis_title='Total Enrollment')
    return figure


import plotly.graph_objects as go

def plot_statewise_enrollment(data):
    state_enrollment = data  # Assuming data has been pre-processed
    return go.Figure(data=go.Bar(
        x=state_enrollment['state_name'],
        y=state_enrollment['total_enrollment'],
        marker_color=['#636EFA', '#EF553B', '#00CC96']  # Replace with desired colors
    ))



# Layout for the Home Page
home_layout = html.Div([
    html.H1("Education Enigma", style={'textAlign': 'center', 'fontSize': '32px'}),

    # Adding the text about the importance of education in India before the images
    html.Div([
        html.H2("", style={'fontSize': '28px', 'marginTop': '20px'}),
        html.P(
            "Education in India is vital as it empowers individuals, improves social standing, and contributes to "
            "the nation's economic and cultural progress. With its potential to bridge societal gaps, education "
            "fosters innovation and prepares youth to meet global challenges. Quality education is essential for "
            "creating a skilled and knowledgeable workforce, driving India's development forward."
        )
    ], style={'padding': '20px'}),

    # Images section
    html.Div(
        [
            dcc.Link(
                html.Div([
                    html.Img(src='/assets/dropoutnew.jpeg', style={'width': '350px', 'height': 'auto'}),
                    html.P("Dropout Rate", style={'fontSize': '18px', 'textDecoration': 'none'})
                ]),
                href='/dropout-analysis'
            ),
            dcc.Link(
                html.Div([
                    html.Img(src='/assets/EDUCATION.png', style={'width': '250px', 'height': 'auto'}),
                    html.P("Countries Preference for Higher Studies",
                           style={'fontSize': '18px', 'textDecoration': 'none'})
                ]),
                href='/countries-dashboard'
            ),
            dcc.Link(
                html.Div([
                    html.Img(src='/assets/higherstudies.jpg', style={'width': '250px', 'height': 'auto'}),
                    html.P("India Universities", style={'fontSize': '18px', 'textDecoration': 'none'})
                ]),
                href='/heatmap'
            ),
            dcc.Link(
                html.Div([
                    html.Img(src='/assets/enrolment.jpeg', style={'width': '250px', 'height': 'auto'}),
                    html.P("Enrollment Age Analysis", style={'fontSize': '18px', 'textDecoration': 'none'})
                ]),
                href='/enrollment-analysis'
            ),
        ],
        style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(3, 1fr)',  # 3 columns with equal width
            'gap': '20px',  # Spacing between grid items
            'padding': '20px'  # Padding around the grid
        }
    )
])

# Layout for the Dropout Rate Analysis Page
# Layout for the Dropout Rate Analysis Page
dropout_layout = html.Div([
    html.H1("Dropout Rates Among Boys and Girls in India", style={'textAlign': 'center'}),
    html.Div([
        dcc.Graph(
            id='primary-dropout',
            figure={
                'data': [
                    go.Bar(
                        x=['Boys', 'Girls'],
                        y=[boys_dropout[0], girls_dropout[0]],
                        marker_color=['skyblue', 'salmon'],
                        name='Primary (1 to 5)'
                    )
                ],
                'layout': go.Layout(
                    title='Dropout Rate - Primary (1 to 5)',
                    xaxis={'title': 'Gender'},
                    yaxis={'title': 'Dropout Rate (%)'},
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
            }
        ),
        dcc.Graph(
            id='upper-primary-dropout',
            figure={
                'data': [
                    go.Bar(
                        x=['Boys', 'Girls'],
                        y=[boys_dropout[1], girls_dropout[1]],
                        marker_color=['skyblue', 'salmon'],
                        name='Upper Primary (6 to 8)'
                    )
                ],
                'layout': go.Layout(
                    title='Dropout Rate - Upper Primary (6 to 8)',
                    xaxis={'title': 'Gender'},
                    yaxis={'title': 'Dropout Rate (%)'},
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
            }
        ),
        dcc.Graph(
            id='secondary-dropout',
            figure={
                'data': [
                    go.Bar(
                        x=['Boys', 'Girls'],
                        y=[boys_dropout[2], girls_dropout[2]],
                        marker_color=['skyblue', 'salmon'],
                        name='Secondary (9 to 10)'
                    )
                ],
                'layout': go.Layout(
                    title='Dropout Rate - Secondary (9 to 10)',
                    xaxis={'title': 'Gender'},
                    yaxis={'title': 'Dropout Rate (%)'},
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
            }
        )
    ], style={
        'display': 'grid',
        'grid-template-columns': 'repeat(3, 1fr)',
        'gap': '20px',
        'padding': '20px'
    }),
    dcc.Link("Back to Home", href='/'),
])

# Layout for the Countries Dashboard Page
countries_layout = html.Div([
    html.H1("Top Countries Dashboard by Year"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in columns_to_fill + ['2024']],
        value='2024',
        clearable=False,
        style={'width': '50%'}
    ),
    dcc.Graph(
        id='bar-graph',
        style={'height': '600px'}
    ),
    dcc.Link("Back to Home", href='/'),
])

# Layout for the Heatmap Page
heatmap_layout = html.Div([
    html.H1("India Universities Heatmap"),
    html.Iframe(
        srcDoc=open('C:/Users/abhis/Desktop/no/LLAMAINDEX_COURSE/india_universities_heatmap_range.html', 'r').read(),
        style={
            'width': '100%',
            'height': '800px',
            'border': 'none'
        }
    ),
    dcc.Link("Back to Home", href='/')
])

# Layout for the Enrollment Age Analysis Page
enrollment_layout = html.Div([
    html.H1("Enrollment Age Analysis for 2019-20"),
    dcc.Graph(
        id='enrollment-bar-chart',
        figure={
            'data': [go.Bar(
                x=data['age'],
                y=data['total_enrollment'],
                marker=dict(color='lightgreen')
            )],
            'layout': go.Layout(
                title='Total Enrollment by Age Group',
                xaxis={'title': 'Age Group'},
                yaxis={'title': 'Total Enrollment'},
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        }
    ),
    dcc.Graph(figure=plot_gender_distribution(data)),  # Ensure this function is defined above
    # dcc.Graph(figure=plot_statewise_enrollment(data)),  # Ensure this function is defined above
    dcc.Link("Back to Home", href='/')
])
new_page_layout = html.Div([
    html.H1("State-wise Education Levels", style={'textAlign': 'center'}),
    dcc.Graph(
        id='state-education-levels',
        figure={  # Example static plot; replace with your dynamic plot logic
            'data': [
                go.Bar(
                    x=states,
                    y=np.random.randint(10, 100, len(states)),  # Example data, replace with actual values
                    marker_color='lightgreen'
                )
            ],
            'layout': go.Layout(
                title='Education Levels by State',
                xaxis={'title': 'State'},
                yaxis={'title': 'Education Level'},
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        }
    ),
    dcc.Link("Back to Home", href='/')
])

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Callback to handle page navigation
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/dropout-analysis':
        return dropout_layout
    elif pathname == '/countries-dashboard':
        return countries_layout
    elif pathname == '/heatmap':
        return heatmap_layout
    elif pathname == '/enrollment-analysis':
        return enrollment_layout
    elif pathname == '/state-education-levels':  # New page URL
        return new_page_layout
    else:
        return home_layout

# Callback for updating the country bar graph
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(selected_year):
    top_10 = df[['Country', selected_year]].sort_values(by=selected_year, ascending=False).head(10)
    max_value = top_10[selected_year].max()
    figure = {
        'data': [go.Bar(
            x=top_10['Country'],
            y=top_10[selected_year],
            marker_color='lightblue'
        )],
        'layout': go.Layout(
            title=f'Top 10 Countries for Higher Studies in {selected_year}',
            xaxis_title='Country',
            yaxis_title='Count',
            plot_bgcolor='white',
            paper_bgcolor='white',
            yaxis=dict(range=[0, max_value * 1.1]),
        )
    }
    return figure


# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
