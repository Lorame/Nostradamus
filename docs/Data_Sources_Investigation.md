# **Data Sources Investigation**

## **Objective**

The main objective of this document is to identify and document all the data required for the project. In this document, you'll be able to find where, how and whether the data was successfully found. If so, I'll put the sources and explain how I collected the data (existing dataset, API, scraping or a combination of these...)

### **Draw regulations for the UEFA Champions League**

Status: ✅ Found on the UEFA's official website.
Date of collection: August 16th 2026. 
Link: <[UEFA Champions League Regulations](https://documents.uefa.com/r/Reglement-de-l-UEFA-Champions-League-2026/27/Article-16-Procedure-pour-le-tirage-au-sort-de-la-phase-de-ligue-Online)>

Relevant sections:
- Article 16: Draw system - league phase
- Article 17: Match system - league phase
- Article 18: Equality of points - league phase

Logically, the rules are not stored in a dataset but in a PDF file. Concerning this data, the next challenge will be to transform these regulations into algorithmic constraints and computational rules that can guide the prediction engine. 

### **The last two UEFA Champions League editions data**

Status: ✅ Found on football-data.org
Date of collection: August 16th 2026.
Link: <[Football-data.org](https://www.football-data.org/)>
How was the data collected : API Token.

All the matches score where available on the UEFA's official website but it was more convenient to use <[Football-data's](https://www.football-data.org/)> API to collect all the data. The data from the editions prior to the 2024-2025 one could be also collected later if needed.

Notable collected information:
- Match dates
- Home and away teams
- Competition stages
- Match scores
