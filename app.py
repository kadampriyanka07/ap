import streamlit as st 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.sidebar.header("Description")
with st.sidebar.expander("About"):
    st.write("This dashboard allows users to explore data from the Gapminder dataset, which contains information about life expectancy, GDP per capita, population, and continent for various countries over several years.")

st.title("Life Insights: Continental Perspectives")

selected_tab = st.sidebar.radio("Navigation", ["Data", "Dashboard"])

data = px.data.gapminder()

if selected_tab == "Data":
    st.subheader("Gapminder Dataset")
    st.write(data)
else:
    selected_year = st.sidebar.slider("Select Year", min_value=1952, max_value=2007, value=2007)
    selected_continent = st.sidebar.selectbox("Select The Continent", data['continent'].unique())
    selected_population = st.sidebar.slider("Select Population", min_value=int(data['pop'].min()), max_value=int(data['pop'].max()), value=(int(data['pop'].min()), int(data['pop'].max())))

    filtered_data = data[(data['year'] == selected_year) & 
                         (data['continent'] == selected_continent) & 
                         (data['pop'] >= selected_population[0]) & 
                         (data['pop'] <= selected_population[1])]

    st.sidebar.table(filtered_data)

    fig1 = px.scatter(filtered_data, x="gdpPercap", y="lifeExp", color="country", size="pop", size_max=60 , log_x=True, title=f"Life Expectancy vs GDP per Capita for {selected_year}")
    fig1.update_layout(xaxis_title="GDP per Capita", yaxis_title="Life Expectancy")
    st.plotly_chart(fig1)

    # Group data by continent and calculate total population
    continent_population = data.groupby('continent')['pop'].sum().reset_index()

    # Calculate average life expectancy by year and continent
    avg_life_expectancy = data.groupby(['year', 'continent'])['lifeExp'].mean().reset_index()

    # Create subplots with 1 row and 2 columns
    fig3 = make_subplots(rows=1, cols=2, subplot_titles=("Total Population by Continent", "Average Life Expectancy by Year and Continent"))

    # Add bar chart
    fig3.add_trace(go.Bar(x=continent_population['continent'], y=continent_population['pop'], name='Population'), row=1, col=1)
    fig3.update_xaxes(title_text="Continent", row=1, col=1)
    fig3.update_yaxes(title_text="Population", row=1, col=1)

    # Add line graph
    for continent in avg_life_expectancy['continent'].unique():
        fig3.add_trace(go.Scatter(x=avg_life_expectancy[avg_life_expectancy['continent'] == continent]['year'],
                                   y=avg_life_expectancy[avg_life_expectancy['continent'] == continent]['lifeExp'],
                                   mode='lines',
                                   name=continent), row=1, col=2)

    # Update layout
    fig3.update_layout(title_text="Population and Life Expectancy by Continent",
                       showlegend=False)
    fig3.update_xaxes(title_text="Year", row=1, col=2)
    fig3.update_yaxes(title_text="Life Expectancy", row=1, col=2)

    # Show the plot
    st.plotly_chart(fig3)

    fig4 = px.scatter(data.query("year == @selected_year"), x="gdpPercap", y="lifeExp", color="continent", log_x=True)
    fig4.update_layout(xaxis_title="GDP per Capita", yaxis_title="Life Expectancy", title=f"Life Expectancy vs GDP per Capita for {selected_year}")
    st.write("Year:", selected_year)
    st.plotly_chart(fig4)
