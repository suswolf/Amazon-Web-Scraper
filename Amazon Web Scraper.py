#Importing the libraries needed for the task

from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd

#Let's define each of the functions we will use in the algoritm

def get_title(soup):
    try:
        title = soup.find("span", {"id":'productTitle'}).text.strip()
    except AttributeError:
        title = ''
    return title

def get_price(soup):
    try:
        price = float(soup.find("span", {"class":'a-price-whole'}).text.strip().replace(',', '')) + (float(soup.find("span", {"class":'a-price-fraction'}).text.strip())/100)
    except AttributeError:
        price = ''
    return price

def get_rating(soup):
    try:
        rating = soup.find("span", {"class":'a-icon-alt'}).text.strip()
    except AttributeError:
        try:
            rating = soup.find("span", {"class":'a-size-base a-color-base'}).text.strip()
        except:
            rating = ''
    return rating

def get_reviews(soup):
    try:
        reviews = soup.find("span", {"id":'acrCustomerReviewText'}).text.strip()
    except AttributeError:
        reviews = ''
    return reviews

def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").text.strip()

    except AttributeError:
        available = "Not Available"	

    return available

#The next is the main fuction to extract and access the data

def amazon_scrapper(product_name):

    #We use the product name provided by the user to complete and get the right URL from Amazon
    searchterm = product_name.replace(' ', '+')
    URL = f'https://www.amazon.com/s?k={searchterm}&__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1G0HPO5K3XQPW&sprefix={searchterm}%2Caps%2C151&ref=nb_sb_noss_1'
    
    #We need to use the headers data from our computer to access the webpage. You can find this on internet
    headers = {"User-Agent": "", 
                     "Accept-Encoding": "gzip, deflate, br, zstd", 
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
                     "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    #We use requests and BeautifulSoup to access and parse the webpage
    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, 'html.parser')

    #Create a kind of list of each product link with BeautifulSoup
    links = soup1.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    #Now we get the actual links of the previous 'list' and put them in an actual list of links
    link_list = []
    for link in links:
        link_list.append('https://www.amazon.com' + link.get('href'))

    #Create an empty dictionary to save the data we are going to extract
    product_dic = {'Title': [], 'Price': [], 'Rating': [], 'Reviews': [], 'Availability': [], 'Date': [], 'link': []} 
    
    #A loop to extract the data of each product and save it in the dictionary
    for link in link_list:
        #With this other loop we try to avoid being refused by the server
        product_page = ''
        while product_page == '':
            try:
                product_page = requests.get(link, headers=headers)
                break
            #In case of being refused we put the scraper to sleep a certain time, you can change it if it not works in your case
            except:
                print("Connection refused by the server...")
                print("Let me sleep for 120 seconds")
                print("Zzzzzz...")
                time.sleep(120)
                print("Was a nice sleep, now let me continue...")
                continue

        #We parse and extract the data of each product webpage
        product_soup = BeautifulSoup(product_page.content, "html.parser")
        
        product_dic['Title'].append(get_title(product_soup))
        product_dic['Price'].append(get_price(product_soup))
        product_dic['Rating'].append(get_rating(product_soup))
        product_dic['Reviews'].append(get_reviews(product_soup))
        product_dic['Availability'].append(get_availability(product_soup))
        #We add the date and link of each product too
        product_dic['Date'].append(datetime.date.today())
        product_dic['link'].append(link)
        #We use time and sleep library to avoid refusing
        time.sleep(1)
    
    #Finaly we convert the dictionary into a dataframe using Pandas, and later into a csv and excel files to save it
    amazon_df = pd.DataFrame.from_dict(product_dic)
    amazon_df.to_csv(f'{searchterm}.csv', index = False, header = True)
    amazon_df.to_excel(f'{searchterm}.xlsx', index = False, header = True)

    return amazon_df

#With this we execute the code and visualize the dataframe

product_name = input('Enter the product name: ')

amazon_df = amazon_scrapper(product_name)

amazon_df