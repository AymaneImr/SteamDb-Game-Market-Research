from seleniumbase import  SB
import pandas as pd
import time
import sqlite3

conn = sqlite3.connect('myDB.db')

steam_games_developers  = 'https://steamdb.info/developers/'
steam_games_tags       = 'https://steamdb.info/tags/'
steam_games_publishers = 'https://steamdb.info/publishers/'
steam_games_franchises = 'https://steamdb.info/franchises/'

#Done * 3
with SB(uc=True, test=True, headed=True) as sb:
#     -> NOTE both developers and franchises tables share the same table structure as publishers table
#            ->> the only difference between them is the number of rows each table has, and to set a range to it depending on how many rows(down below in the for loop).
    sb.driver.open(steam_games_publishers, 3)
    conti = input('to continue')
    time.sleep(20)
    def test_scrape():
        all_names     = []
        all_products  = []
        all_positives = []
        all_negatives = []
        all_ratings   = []

        # -> change the range according to the explaination above 
        for j in range(9):
    
            try:
                names_element    = sb.driver.find_elements('#table-apps > tbody > tr > td:nth-of-type(3)')
                for name in names_element:
                    all_names.append(name.text)
                products_element = sb.driver.find_elements('#table-apps > tbody > tr > td:nth-of-type(4)')
                for product in products_element:
                    all_products.append(product.text)
                positive_element = sb.driver.find_elements('#table-apps > tbody > tr > td:nth-of-type(5)')
                for positive in positive_element:
                    all_positives.append(positive.text)
                negative_element = sb.driver.find_elements('#table-apps > tbody > tr > td:nth-of-type(6)')
                for negative in negative_element:
                    all_negatives.append(negative.text)
                ratings_element  = sb.driver.find_elements('#table-apps > tbody > tr > td:nth-of-type(7)')
                for rating in ratings_element:
                    all_ratings.append(rating.text)
        
            except Exception:
                pass
        
            sb.driver.click('button.next')
            time.sleep(6)
    
        data = {
            'names': all_names,
            'products': all_products,
            'positive_reviews': all_positives,
            'negative_reviews': all_negatives,
            'ratings': all_ratings
        }
    
        try:
            df = pd.DataFrame(data)
        except ValueError:
            df = pd.DataFrame.from_dict(data, orient='index')

        # storing the data in an excel file because those tables doesn't hold a large amount of rows
        file_name = 'steam_games_publishers.xlsx'
        df_excel = df.to_excel(file_name)

    if conti == 'yes':
        test_scrape()


# -> scrape available tag's games 
with SB(uc=True, test=True, headed=True) as sb:
    sb.driver.uc_open_with_tab(steam_games_tags)
    to_start = input('start? ')
    time.sleep(6)
    
    def scrape():
        
        links = []
        hrefs = sb.driver.find_elements('div.taglist .label a.btn[href]')
        for href in hrefs:
            links.append(href.get_attribute("href"))
        
        
        unique_links = []
        for unique_link in links:
            if unique_link not in unique_links:
                unique_links.append(unique_link)
        # -> remove min_reviews parameter from the urls
        
        unique_links_without_min_reviews = []
        for href in unique_links:
            if href.endswith("?min_reviews=500"):
                href = href.split('?min_reviews=500')
                href = href[0]
            unique_links_without_min_reviews.append(href)
        
        # -> create links file
        for i in unique_links_without_min_reviews:
            # -> on windows replace .odt by .txt
            with open('tags_links.odt', mode='a+') as file:
                file.write("'"+i+"'"+ ','+'\n')
        
        # read links file and store links in a list
        with open('scraping-data/test/links.odt', 'r') as f:
            links = [link.strip().replace("'", "") for link in f.read().split(',')]
            links_to_scrape = list(links)
        
        all_names    = []
        all_types    = []
        all_prices   = []
        all_ratings  = []
        all_releases = []
        all_follows  = []
        all_onlines  = []
        all_peaks    = []
        
        #loop through each tag link to scrape all tags
        for link in links_to_scrape:
            sb.driver.open(link)
            time.sleep(7)
            
            #scrape the current tag name -> specify just the tag name using the split function as shown below
            tag = sb.driver.find_element('h1.header-title')
            tag = tag.text.split()[3:]
            tag = ' '.join(tag)
            time.sleep(2)
            
            #extract the number of available rows in each tag table to know exactly how many loops in each tag table
            count = sb.driver.find_element('span#js-sales-count')
            count = count.text
            
            # -> calculate how many loops in each tag 
            # NOTE you may notice that there are some tags that have over 10k games but steamdb.info can't display all thet amount of data so it only display 10k  
            if count == '10,000':
                range_time = 10
            elif ',' in count:
                count = count.split(',')[0]
                range_time = int(count) + 1 

            elif int(count) < 999:
                range_time = 1
            
            time.sleep(3)
            
            #select the 1k option in how many rows per table 
            sb.select_option_by_text('select.dt-input', '1K')
            time.sleep(5)
            for i in range(range_time):
                
                try:
                    names = sb.driver.find_elements('tbody > tr > td:nth-of-type(3) > a')
                    for name in names:
                        all_names.append(name.text)
                    
                    types = sb.driver.find_elements('span.cat')
                    for _type in types:
                        all_types.append(_type.text)

                    prices = sb.driver.find_elements('tbody > tr > td:nth-of-type(5)')
                    for price in prices:
                        all_prices.append(price.text)

                    ratings = sb.driver.find_elements('tbody > tr > td:nth-of-type(6)')
                    for rating in ratings:
                        all_ratings.append(rating.text)

                    releases = sb.driver.find_elements('tbody > tr > td:nth-of-type(7)')
                    for release in releases:
                        all_releases.append(release.text)

                    follows = sb.driver.find_elements('tbody > tr > td:nth-of-type(8)')
                    for follow in follows:
                        all_follows.append(follow.text)

                    onlines = sb.driver.find_elements('tbody > tr > td:nth-of-type(9)')
                    for online in onlines:
                        all_onlines.append(online.text)

                    peaks = sb.driver.find_elements('tbody > tr > td:nth-of-type(10)')
                    for peak in peaks:
                        all_peaks.append(peak.text)

                except Exception:
                    pass
                
                #click next foe the next table
                sb.driver.click('button.next')
                time.sleep(2)
                print(link)
            
            #store our lists data in dic to create a DataFrame
            data = {
                'tag'    : tag,
                'name'   : all_names,
                'type'   : all_types,
                'price'  : all_prices,
                'rating' : all_ratings,
                'release': all_releases,
                'follows': all_follows,
                'online' : all_onlines,
                'peak'   : all_peaks
            }
            
            try:
                df = pd.DataFrame(data)
            except ValueError:
                df = pd.DataFrame.from_dict(data, orient='index')
            
            # -> store our data in a database (sqlite3) due to the large amount of rows -> rows < +1m 
            df.to_sql('games', con=conn, if_exists='append', index=False)
            
            #clear all the lists after each link so we won't have any duplicates rows 
            all_names.clear()   
            all_types.clear()
            all_prices.clear()   
            all_ratings.clear()  
            all_releases.clear() 
            all_follows.clear()  
            all_onlines.clear()  
            all_peaks.clear()  
        
    
    if to_start == 'yes':
        scrape()
    else:
        print('ops')

