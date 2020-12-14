# Dealroom Intership Assignment - Logic and Code Explained

This file explains the logic and the code used to realize the assigmnent.

## Table of contents
1. [Part 1 - Classifying entities](#part-1---classifying-entities)
2. [Part 2 - Web scraping](#part-2---web-scraping)


## Part 1 - Classifying entities

### Instructions

The goal of this part was to classify the provided data into those types :

| Type        | Definition           |
| ------------- | ------------- |
| Startups      | Companies founded after 1990, that are innovative and tech-orientated |
| Mature        | Established multinationals and companies, founded before 1990      |
| Universities/School | Universities, primary and secondary education      |
| Government/Non-profit | Governmental organisation and non-profit companies |
| Unclassified |


### Logic

#### 1. Columns choice
First thing was to take a look at the raw data and decide what will be useful and relevant for this task. As we are building a list of keywords revolving around the entity types, I decided to use **'TAGLINE'** and **'TAGS'** columns. **'TAGLINE'** contains a small description about the company and **'TAGS'** has keywords. I also decided to use **'LAUNCH DATE'**, which will be useful to classify Startups and Mature companies.

#### 2. Pre-process
To use these columns we need to clean and pre-process them.
For columns containing text, I first converted them to string. Then I transformed the text to lower caps and remove any numbers. 

For **'TAGS'** I stopped cleaning the text here, and I built a list of keywords from it.

For **'TAGLINE'**, I removed any kind of punctuations and stopwords (from nltk). After this I also built a list from the words.

To perfom the classify algorithm better, I concatenated both lists from **'TAGS'** and **'TAGLINE'** into a single list that I put in a new column called **'ALL'**. From this column I removed duplicates due to the concatenation. For NaN values, due to a bug with .astring() function converting them to 'nan', I replaced them by empty list.

For **'LAUNCH DATE'**, I first renamed the column to **'LAUNCH_DATE'** to avoid making mistake when writing the name. In the raw data, dates were not in the same format. First I converted it to datetime format and the I decided to only keep the year.

#### 3. Classification

To classify the data we needed to build lists of keywords revolving around the entities types. For this I used the .most_common() function that I applied to **'ALL'** after a few operations. That way I could see which words were the most used and put them on my lists. I also put some words that seemed relevant to put.

For the .classify() function, I first created a dictionary using the keys as the entities types and values as length of each intersection set between **'ALL'** and the keywords. I used the .max() function to know the entity type that had the most matches.

If the maximum value was equal to 0, it would mean no lists were matching with the value from **'ALL'**, and therefore it was "Unclassified".

If the maximum was "Startup", I would check if the launch date was after 1990. If it wasn't, it was then classified as a "Mature company". Same logic for "Mature company".


#### 4. Going further

Now that we have a labeled data, we have data available to train a model and use it next time to classify new companies.

Our problem is a text classification with additional meta data (Launch year). We will use a neural network to solve the problem, and build two submodels that we will concatenate later.

The first submodel will have an input shape layer, an embedding layer, and an LSTM layer.

The second submodel will have an input shape layer, and we can add other multiple dense layer if wanted.

Both output of the submodels will be concatenated and used as a layer. We can add other dense layer after this, but for the last one the output will be equal to the number of classes our problem has.



## Part 2 - Web scraping

### Instructions

For this task, the goal is to retrieve information of YC companies from [ycombinator.com](https://www.ycombinator.com/companies/), and export it to the excel assignment sheet.

### Logic

#### 1. Load all contents

[Ycombinator.com/companies](https://www.ycombinator.com/companies/) page is what we called an infinite loading. It will wait for the user to be at the bottom of the page to load more content.

That said, we needed to define a function that would scroll until it reach the end. The previous height of the screen calculated needs to be equal to new height of the screen, for the program to know we loaded all the content.

To be able to execute that we needed a driver. To improve the performance I set the driver capabilities "pageloadstrategy" to eager. This allowed to still retrieve informations without waiting for the full page to load and therefore avoid TimeoutException.

#### 2. Retrieved information for each company

On [Ycombinator.com/companies](https://www.ycombinator.com/companies/) page we have a list of all companies. To get access to their profile page, I retrieved their IDs that i stored in a list.

Then I looped over that list and the driver opened each URLs. It's in this loop that I retrieve all the necessary information : 
- Company name
- Tagline
- Description
- Website
- Launch year
- Team size
- Any socials listed

Those information were stored inside a dictionary so to prepare the export to excel, I created a dataframe from that dictionary.


