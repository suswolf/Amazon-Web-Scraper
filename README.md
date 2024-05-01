# Amazon Web Scraper

In this project, I create a web scraper to extract prices, ratings and other data from Amazon products. It works for the first searching page of the introduced product, but in the future I plan to make it work for several pages of the searched item.

The algoritm returns a dataframe of the main search webpage of a product with its price, ratings, number of reviews, date of extraction of the data and a link. And to make it done we use several libraries such as Pandas, BeautifulSoup, Requests and time. Also, the dataframe is converted into documents csv and xlsx for later use.

In the practice of this task we face several obstacles that Amazon put in the way to avoid scraping. We need to use the User-Agent of our PC and we need to wait a certain time between each calling to the web to avoid being refused by the server. This parameters might change depending on the location of the user and on the item searched.
