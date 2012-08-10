from bs4 import BeautifulSoup
import codecs
import MySQLdb
import requests

import settings

path = settings.project_path + 'pupfiles/'

domain = "http://www.sfspca.org"

def requests_url_contents(url):
    r = requests.get(url)
    return r
    

def create_filename(url):
    url_sections = url.split('/')
    filename = path + url_sections[-1] + '.html'
    return filename
    
    
def save_contents(url):
    r = requests_url_contents(url)
    contents = r.text
    filename = create_filename(url)
    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write(contents)
    f.close
    return filename
    

def file_contents(filename):
    soup = BeautifulSoup(open(filename))
    return soup
    

def return_webpage_contents(url):
    filename = save_contents(url)
    soup = file_contents(filename)
    return soup
    

def dog_details(soup):
    detail_dict = {}
    detail_dict['name'] = dog_name(soup)
    detail_dict['spca_id'] = dog_id(soup)
    detail_dict['gender'] = dog_gender(soup)
    detail_dict['breed'] = dog_breed(soup)
    detail_dict['color'] = dog_color(soup)
    detail_dict['age'] = dog_age(soup)
    detail_dict['description'] = dog_description(soup)
    detail_dict['image'] = dog_image(soup)
    return detail_dict

     
def individual_dog_urls(soup, dog_url_list=[]):
    for url in soup.find_all('a'):
        if 'pet-details' in url.get('href', ''):
            dog_url_list.append(domain + url.get('href')) 
    return dog_url_list
    
#----------------------------------------------------------------------------

def goto_next_page(self, contents):
    next_page_index = contents.find('"pager-next"')
    url_begin_index = contents.find('<a href="', next_page_index)
    url_end_index = contents.find('"', url_begin_index + 10)
    url = domain + contents[url_begin_index + 9:url_end_index]
    return url

    
def get_dog_image(soup):
    image = soup.find(id="animal_pic_")['src']
    return image


'''def dog_name(soup):
    names = soup.find_all('NAME')
    print names
    return names
    
soup = return_webpage_contents('http://www.sfspca.org/adoptions/pet-details/16213392-0')
dog_name(soup)    

    

def dog_id(soup):
    
    return spca_id
    

def dog_gender(soup):
   
    return gender


def dog_breed(soup):
    
    return dog_breed
    

def dog_color(soup):
    
    return color
        

def dog_age(soup):
   
    return age


def dog_description(soup):
    
    return description'''




#-------------------------------------------------------------------------------------------------------------------------------------------

soup = return_webpage_contents('http://www.sfspca.org/adoptions/dogs')
dog_url_list = individual_dog_urls(soup)
assert dog_url_list[0] == ('http://www.sfspca.org/adoptions/pet-details/10424952-1'), dog_url_list[0]

soup = return_webpage_contents('http://www.sfspca.org/adoptions/pet-details/16213392-0')
assert get_dog_image(soup) == 'http://www.sfspca.org/sites/default/files/imagecache/animal_profile_default/photos/6bfb81a3-a8fd-4a88-b686-608cf8bd13b3_TN1.jpg'















