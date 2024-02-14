import streamlit as st 
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns

st.sidebar.header("Description")
st.sidebar.subheader("Step into the dynamic world of global health with our interactive dashboard, where you'll uncover fascinating insights into life expectancy across continents. Explore the diverse landscapes of each region, from the vibrant communities of Africa to the innovative cities of Europe. Delve into rich, interactive visualizations that reveal the factors shaping life expectancy trends, from healthcare access to socio-economic development. Join us on this engaging journey as we unravel the complexities of global health and inspire meaningful action for a brighter, healthier world.")

st.title("Life Insights: Continental Perspectives")

data = px.data.gapminder()
st.dataframe(data)

selected_year = st.sidebar.slider("Select Year" , min_value=1952, max_value=2007, value=2007)
selected_continent = st.sidebar.selectbox("Select The Continent", data['continent'].unique())
selected_population = st.sidebar.slider("Select Population", min_value=int(data['pop'].min()), max_value=(data['pop'].max()), value = (int(data['pop'].min()),int(data['pop'].max())))
st.write('selected_population', selected_population)

filtered_data = data[(data['year'] == selected_year) & 
                      (data['continent'] == selected_continent) & 
                      (data['pop'] >= selected_population[0]) & 
                      (data['pop'] <= selected_population[1])]


st.sidebar.table(filtered_data)
fig1 = px.scatter(filtered_data,x="gdpPercap",y="lifeExp",color = "country",size = "pop",size_max=60 , log_x=True, title = "Life Expectancy v/s GDP per Capital for {selected_year}")
st.plotly_chart(fig1)

# Count the number of countries in each continent
continent_counts = data['continent'].value_counts().reset_index()
continent_counts.columns = ['continent', 'count']

# Group data by continent and calculate total population
continent_population = data.groupby('continent')['pop'].sum().reset_index()

# Create subplots with 1 row and 2 columns, specifying subplot type as 'pie'
fig2 = make_subplots(rows=1, cols=2, specs=[[{'type':'pie'}, {'type':'pie'}]], subplot_titles=("Number of Countries by Continent", "Population by Continent"))

# Add first pie chart
fig2.add_trace(go.Pie(labels=continent_counts['continent'], values=continent_counts['count']), row=1, col=1)

# Add second pie chart
fig2.add_trace(go.Pie(labels=continent_population['continent'], values=continent_population['pop']), row=1, col=2)

# Update layout
fig2.update_layout(title_text="Comparison of Countries and Population by Continent", showlegend=False)
st.plotly_chart(fig2)

# Group data by continent and calculate total population
continent_population = data.groupby('continent')['pop'].sum().reset_index()

# Calculate average life expectancy by year and continent
avg_life_expectancy = data.groupby(['year', 'continent'])['lifeExp'].mean().reset_index()

# Create subplots with 1 row and 2 columns
fig3 = make_subplots(rows=1, cols=2, subplot_titles=("Total Population by Continent", "Average Life Expectancy by Year and Continent"))

# Add bar chart
fig3.add_trace(go.Bar(x=continent_population['continent'], y=continent_population['pop'], name='Population'), row=1, col=1)

# Add line graph
for continent in avg_life_expectancy['continent'].unique():
    fig3.add_trace(go.Scatter(x=avg_life_expectancy[avg_life_expectancy['continent'] == continent]['year'],
                             y=avg_life_expectancy[avg_life_expectancy['continent'] == continent]['lifeExp'],
                             mode='lines',
                             name=continent), row=1, col=2)

# Update layout
fig3.update_layout(title_text="Population and Life Expectancy by Continent",
                  showlegend=False)
# Show the plot
st.plotly_chart(fig3)

fig4 = px.scatter(data.query("year == @selected_year"),x="gdpPercap",y="lifeExp",color = "continent",log_x=True)

st.write("Year : " , selected_year)
st.plotly_chart(fig4)
