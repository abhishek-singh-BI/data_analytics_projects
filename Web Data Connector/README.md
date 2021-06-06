Web Data Connector for Tableau.

- PROBLEM STATEMENT:

1. Create a custom Web Data Connector (WDC) when you want to connect to a web data source from Tableau.

2. This will open up a wide range of data available over http to be used in your organisation.

- Questions:

1. What are the areas having earthquakes of more than 4.5 magnitude in the last 7 days?
2. Is there any cluster/specific area where this seems to be more prevalent?

- Challenges:

1. Getting a clean data from web into tableau.
2. Expertise in javascript is required to create connectors with temporary tokens.
3. Specific API parameters and their understanding is necessary to correctly code them into javascript.
4. Tableau cannot parse a non flat JSON structure (hierarchy). Need to flatten the same in javascript.
5. HTML and JS code needs to be deployed on a server.

- Solution:


1. WDC with an HTML page containing JavaScript code that connects to web data (for example, by means of a REST API), converts the data to a JSON format, and passes the data to Tableau.

2. The link for the same is used in tableau to connect to the specific web data connector.

3. Map chart to represent exactly the places with severe earthquakes in last 7 days.

4. Size attribute along with color helps user to visually detect deadlier earthquakes at a glance.

Link to solution : https://public.tableau.com/app/profile/abhishek6922/viz/EarthQuakeDataUsingWDC/Summary