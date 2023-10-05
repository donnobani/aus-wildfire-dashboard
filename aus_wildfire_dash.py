import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

# Create app
app = dash.Dash(__name__)

# clear layout
# do not display exception until callback gets executed
app.config.suppress_callback_exceptions = True

# reading data into dataframe
df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
)
# extracting year and month from date column
df["Month"] = pd.to_datetime(
    df["Date"]
).dt.month_name()  # convert month number to month name
df["Year"] = pd.to_datetime(df["Date"]).dt.year

# defining layout
app.layout = html.Div(
    children=[
        # title
        html.H1(
            "Australia Wildfire Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 26},
        ),
        # radio select - region
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Select Region:", style={"margin-right": "2em"}),
                        dcc.RadioItems(
                            ["NSW", "QL", "SA", "TA", "VI", "WA"],
                            "NSW",
                            id="region",
                            inline=True,
                        ),
                    ]
                ),
            ]
        ),
        # dropdown select - year
        html.Div(
            [
                html.H2("Select Year:", style={"margin-right": "2em"}),
                dcc.Dropdown(df.Year.unique(), value=2005, id="year"),
            ]
        ),
        # plot1 - pie
        # plot2 - bar
        html.Div(
            [html.Div([], id="plot1"), html.Div([], id="plot2")],
            style={"display": "flex"},
        ),
    ]
)


# callback func decorator
@app.callback(
    [
        Output(component_id="plot1", component_property="children"),
        Output(component_id="plot2", component_property="children"),
    ],
    [
        Input(component_id="region", component_property="value"),
        Input(component_id="year", component_property="value"),
    ],
)

# defining callback func
def reg_year_display(input_region, input_year):
    # retrieving region data
    region_data = df[df["Region"] == input_region]

    # retrieving year data from region
    y_r_data = region_data[region_data["Year"] == input_year]

    # retrieving plot1 data
    est_data = y_r_data.groupby("Month")["Estimated_fire_area"].mean().reset_index()
    # plot1 - pie chart
    fig1 = px.pie(
        est_data,
        values="Estimated_fire_area",
        names="Month",
        title="{} : Monthly Average Estimated Fire Area in year {}".format(
            input_region, input_year
        ),
    )
    # retrieving plot2 data
    veg_data = y_r_data.groupby("Month")["Count"].mean().reset_index()
    # plot2 - bar chart
    fig2 = px.bar(
        veg_data,
        x="Month",
        y="Count",
        title="{} : Average Count of Pixels for Presumed Vegetation Fires in year {}".format(
            input_region, input_year
        ),
    )
    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


# run app
if __name__ == "__main__":
    app.run_server()
