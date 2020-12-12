# **Dealroom Internship Assignment**
*This project was done for Dearlroom.co by Océane Salmeron, December 2020.*

## Part 1 - Classifying entities
The goal of this part was to classify the provided data into those types :

| Type        | Definition           |
| ------------- | ------------- |
| Startups      | Companies founded after 1990, that are innovative and tech-orientated |
| Mature        | Established multinationals and companies, founded before 1990      |
| Universities/School | Universities, primary and secondary education      |
| Government/Non-profit | Governmental organisation and non-profit companies |
| Unclassified |

The data provided is an export of startups from the Dealroom database.

To execute the script run :
```
python3 Scripts/classify_entities.py
```

## Part 2 - Web scraping

For this task, the goal is to retrieve information of YC companies from [ycombinator.com](https://www.ycombinator.com/companies/), and export it to the excel assignment sheet.

The information I retrieved are :
- Company name
- Tagline
- Description
- Website
- Launch year
- Team size
- Socials

To execute the script run :
```
python3 Scripts/scraping.py
```
