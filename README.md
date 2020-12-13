# **Dealroom Internship Assignment**
*This project was done for Dearlroom.co by Océane Salmeron, December 2020.*

## Table of contents
1. [Installation](#installation)
2. [Part 1 - Classifying entities](#part-1---classifying-entities)
3. [Part 2 - Web scraping](#part-2---web-scraping)
4. [Results](#results)
5. [Logic and code used](#logic-and-code-used)

## Installation
This project run on **Python 3.6**
### Install requirements

To install requirements run in your terminal :
```
pip3 install -r requirements.txt
```
### Chromedriver
You also need to install a chromedriver according to your chrome version. You can download it [here](https://chromedriver.chromium.org/downloads). 

Place your driver at the root folder please, or edit `executable_path` in **scraping.py**.

### NLTK stopwords

Please uncomment line 13 : `#nltk.download('stopwords')` in **classify_entities.py** if it's not downloaded yet.

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
cd Scripts
python3 classify_entities.py
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
cd Scripts
python3 scraping.py
```

## Results

Results for part 1 & 2 are provided in **Results.xlsx** file in the Data folder.

## Logic and code used

Explaination can be found in **LOGIC.md** file. For detailed explaination (line by line), you can check the Notebook folder where you can found **classify_entities.ipynb** and **scraping.ipynb**
