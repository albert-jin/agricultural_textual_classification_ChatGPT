1 Background
Big data created from social media like Twitter has made a prominent position in almost all industries and sectors right from individuals to government stakeholders, nongovernment institutions, private businesses, volunteering organizations. In the recent decade, there has been a spurt of interest in the role of social media data in disaster response, since several natural disasters strike across the globe every year, causing large-scale suffering and economic losses to the public. Although there are many studies about social media and disaster response, respectively, social media data is rarely used for disaster response; thus, experts understand less about information spread via social media in the context of natural hazards and disaster response. We create a natural disaster dataset with sentimental labels, which contains 49,816 Twitter data about natural disasters in the United States. Based on the motivation of taking full advantage of the potential of social media data and saving capital expenditures, this dataset provides decision-makers like relief agencies, emergency managers, and government officers with an opportunity for future research.

Twitter is chosen as the primary sentiment analysis object, as Twitter is a popular microblog that has 140 million active users posting more than 400 million tweets every day. During the period of disaster response, a large number of users posted information like disaster damage reports and disaster preparedness situations, making Twitter an essential social media for updating and accessing data. Mining sentimental data efficiently will better understand the disaster response timely and easily. Twitter has provided an application programming interface (API) that can be used by developers to access and read Twitter data. A streaming API is also offered that can access real-time Twitter data. However, Twitter's search API only allows users to collect 180 requests every 15 minutes in the past seven days, with a maximum number of 100 tweets per claim in the free version. Therefore, this research utilizes TwitterScraper in Python of data collection to retrieve the content and Beautifullsoup4 to parse the retrieved content.

2 Installation
2.1 To install TwitterScraper package
(sudo) pip install twitterscraper

3 Usage
3.1 Example of data collection using TwitterScraper

#Import libraries
from twitterscraper import query_tweets
import datetime as dt
import pandas as pd

#Set time frames_YY,MM,DD (Attention: the earliest begin_date is 2006,3,1)
begin_date = dt.date(2017,8,10)
end_date = dt.date(2017,9,9)

#Input keywords, time frames, and language
tweets = query_tweets("Hurricane Harvey AND Food", begindate = begin_date, enddate = end_date, lang = 'en')

#Output dataset into a csv file
df = pd.DataFrame(t.__dict__ for t in tweets )df.to_csv("Dataset_Hurricane Harvey.csv") 


