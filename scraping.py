from bs4 import BeautifulSoup
import re
import urllib2

domain = "http://www.sfspca.org" 

def url_contents(url):
    soup = BeautifulSoup(urllib2.urlopen(url)) 
    return soup

     
def individual_dog_urls(soup, dog_url_list=[]):
    for url in soup.find_all('a'):
        if 'pet-details' in url.get('href', ''):
            dog_url_list.append(domain + url.get('href')) 
    return dog_url_list
    
   
def get_dog_image(soup):
    image = soup.find(id="animal_pic_")['src']
    return image
    

def dog_description(soup):
    desc = soup.find(id="animal_description").findChildren()[0].get_text()
    return desc

#------------------------------------------------------------------------    
    
'''def goto_next_page(soup):
    l = soup.find_all("li")
    liitem = [x for x in l if "pager-next" in x['class']]
    soup = BeautifulSoup('liitem')
    print soup, type(soup)
    return liitem

soup = url_contents('http://www.sfspca.org/adoptions/dogs')
goto_next_page(soup)'''



def dog_name(soup):
    names = soup.find_all("p", "class")
    print 'names is %s' % names
    return 
    
    
soup = url_contents('http://www.sfspca.org/adoptions/pet-details/16213392-0')
dog_name(soup)    

    

'''def dog_id(soup):
    
    return spca_id
    

def dog_gender(soup):
   
    return gender


def dog_breed(soup):
    
    return dog_breed
    

def dog_color(soup):
    
    return color
        

def dog_age(soup):
   
    return age
    
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


#------------------------------------------------------------------------------------------------------------------------------
soup = url_contents('http://www.sfspca.org/adoptions/dogs')
dog_url_list = individual_dog_urls(soup)
assert dog_url_list[0] == ('http://www.sfspca.org/adoptions/pet-details/10424952-1'), dog_url_list[0]

soup = url_contents('http://www.sfspca.org/adoptions/pet-details/16213392-0')

assert get_dog_image(soup) == 'http://www.sfspca.org/sites/default/files/imagecache/animal_profile_default/photos/6bfb81a3-a8fd-4a88-b686-608cf8bd13b3_TN1.jpg'
assert dog_description(soup) == "Tika was a great mom to 2 beautiful puppies that have all found wonderful new homes.  Now it's her turn to find a family. Tika is a bright and active young dog, hoping to find a home with adopters who'll be able provide her with plenty of opportunities for both mental and physical exercise on a daily basis. Attending training classes will be a great way for her to learn the skills needed to become a well mannered companion!  Her favorite activity is to play with other dogs and to get snuggles and belly rubs from her special people.  This girl is going to make some lucky family a great pet!", dog_description(soup)'''















