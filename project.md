Project Phase 1 for Presentation

We have used the global security threats between 2015 and 2024 to generate the dashboard by using Streamlit and Plotly. We have added various filters to manipulate the data and KPI cards to show key metrics at a glance.

**What each chart describes:**

The **Attacks by Type** chart compares how often each attack type (Phishing, Ransomware, DDoS, Man-in-the-Middle, SQL Injection) occurs, helping you see which threats are most common.

The **Target Industries** chart shows which sectors (Education, Retail, IT, Healthcare, Banking, Government, Telecommunications) are hit most often, so you can identify the most at-risk industries.

The **Incidents Over Time** line chart tracks incident counts year by year, revealing trends and whether cyber threats are increasing or decreasing over time.

The **Attack Source Distribution** pie chart shows who is behind the attacks (Hacker Groups, Nation-states, Insiders, or Unknown), giving a breakdown of threat actors.

The **Top 10 Countries by Financial Loss** chart ranks the countries with the highest total financial impact, highlighting where losses are concentrated.

The **Security Vulnerability Types** chart shows which weaknesses (Unpatched Software, Social Engineering, Weak Passwords, Zero-day) are most often exploited, guiding prioritization of security fixes.

The **Defense Mechanisms Used** chart shows which defenses (VPN, Firewall, Antivirus, AI-based Detection) are most commonly applied in response to incidents.

The **Incident Resolution Time** histogram shows how long it typically takes to resolve incidents, revealing the distribution of resolution times in hours.

Project Phase 2

At first, our dataset lacked latitude and longitude information, which meant we couldn't visualize geospatial data on the dashboard. To address this, we enriched the dataset by adding the appropriate lat/lon coordinates for each location, as documented in app.ipynb. With these enhancements, we were able to implement an interactive geospatial choropleth map in the dashboard, allowing users to explore cybersecurity incidents geographically based on their filter selections.