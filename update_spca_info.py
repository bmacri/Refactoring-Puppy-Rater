import MySQLdb

import database 
import scraping

        
def populate_db(all_contents):
    database.truncate()
    next_page = database
    scraping.goto_next_page(all_contents)
    while next_page:
        dog_url_list = scraping.individual_dog_urls(all_contents, [])
        for url in dog_url_list:
            contents = scraping.return_webpage_contents(url)
            dog_detail_dict = scraping.dog_details(contents)
            database.dog_details_to_db(dog_detail_dict)
        all_contents = scraping.return_webpage_contents(next_page)
        next_page = scraping.goto_next_page(all_contents)
    dog_url_list = scraping.individual_dog_urls(all_contents, [])
    for url in dog_url_list:
        contents = scraping.return_webpage_contents(url)
        dog_detail_dict = scraping.dog_details(contents)
        database.dog_details_to_db(dog_detail_dict)
    return
    
       
        
if __name__ == '__main__':
    all_contents = scraping.return_webpage_contents('http://www.sfspca.org/adoptions/dogs')
    populate_db(all_contents)
    data = database.details_from_db()
    print data
    filename = 'crontest.txt'
    f = open(filename, 'a')
    f.write('update_spca_info.py ran at ' + str(time.time())+ '\n')
    f.close()
    
    
    


