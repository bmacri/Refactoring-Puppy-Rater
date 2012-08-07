import codecs
import pdb
import re
import time 

import MySQLdb
import requests

import settings


path = settings.project_path + 'pupfiles/'

class DogObject():
    pass

class RatingsObject():
    pass

class DogDetails():

    def __init__(self):
        pass

    def requests_url_contents(self, url):
        r = requests.get(url)
        return r
        

    def create_filename(self, url):
        url_sections = url.split('/')
        filename = path + url_sections[-1] + '.html'
        return filename
        
        
    def save_contents(self, url):
        r = self.requests_url_contents(url)
        contents = r.text
        filename = self.create_filename(url)
        f = codecs.open(filename, 'w', encoding='utf-8')
        f.write(contents)
        f.close
        return filename
        

    def file_contents(self,filename):
        f = codecs.open(filename, 'r', encoding='utf-8')
        contents = f.read()
        f.close()
        return contents
        

    def return_webpage_contents(self,url):
        filename = self.save_contents(url)
        contents = self.file_contents(filename)
        return contents
        

    def dog_details(self, contents):
        detail_dict = {}
        detail_dict['name'] = self.dog_name(contents)
        detail_dict['spca_id'] = self.dog_id(contents)
        detail_dict['gender'] = self.dog_gender(contents)
        detail_dict['breed'] = self.dog_breed(contents)
        detail_dict['color'] = self.dog_color(contents)
        detail_dict['age'] = self.dog_age(contents)
        detail_dict['description'] = self.dog_description(contents)
        detail_dict['image'] = self.dog_image(contents)
        return detail_dict
    
    def mysql_get_cursor(self):
        conn = MySQLdb.connect(host= "localhost",
                                user="root",
                                passwd = settings.db_password,
                                db="spcadogs")
        cursor = conn.cursor()
        return conn, cursor
        

    def dog_details_to_db(self, detail_dict):
        conn, cursor = self.mysql_get_cursor()
        cursor.execute ("INSERT INTO dogdetails (name, spca_id, gender, breed, color, age, description, image) VALUES (%(name)s, %(spca_id)s, %(gender)s, %(breed)s, %(color)s, %(age)s, %(description)s, %(image)s);", detail_dict)
        conn.commit()

     
    def details_from_db(self):
        conn, cursor = self.mysql_get_cursor()
        cursor.execute ("SELECT * FROM dogdetails;")
        all_db_data = cursor.fetchall()     
        conn.commit()
        dog_info_list = []
        for each_dog in all_db_data:
            db_dog = DogObject()
            db_dog.name = each_dog[0]
            db_dog.spca_id = each_dog[1]
            db_dog.gender = each_dog[2]
            db_dog.breed = each_dog[3]
            db_dog.color = each_dog[4]
            db_dog.age = each_dog[5]
            db_dog.description = each_dog[6]
            db_dog.image = each_dog[7]
            db_dog.ratings_list = self.select_ratings(db_dog.spca_id)  
            dog_info_list.append(db_dog)
        return dog_info_list
        
        
    def insert_ratings_dict(self, ratings_dict):
        conn, cursor = self.mysql_get_cursor()
        cursor.execute("INSERT INTO ratings (spca_id, cuteness, personality, comment) VALUES (%(spca_id)s, %(cuteness)s, %(personality)s, %(comment)s);", ratings_dict)
        conn.commit()
                
        
    def select_ratings(self, spca_id):
        conn, cursor = self.mysql_get_cursor()
        cursor.execute ("SELECT * FROM ratings WHERE spca_id = "+str(spca_id)+";")
        comments = cursor.fetchall()    
        conn.commit()
        ratings_list = []
        for rating in comments: #for row in ratings table where spca_id == parameter
            ratings_object = RatingsObject()
            ratings_object.cuteness = rating[2]
            ratings_object.personality = rating[3]
            ratings_object.comment = rating[4]
            ratings_list.append(ratings_object)
        return ratings_list

    
        
        
    def trim_contents_singledog(self, contents):
        begin_index = contents.find('<h1 class="title"')
        end_index = contents.find('<div id="animal_profile_logos">', begin_index + 1)
        trimmed_contents = contents[begin_index:end_index] 
        return trimmed_contents
        

    def individual_dog_urls(self, contents, dog_url_list=[]):
        domain = "http://www.sfspca.org"
        animal_name_class = contents.find('"views-field-field-animal-name-value"')
        if animal_name_class == -1:
            return dog_url_list
        link_tag = contents.find('<a href=', animal_name_class + 1)
        start_quote = contents.find('"', link_tag + 1)
        end_quote = contents.find('"', start_quote + 1)
        next_url = domain + contents[start_quote + 1:end_quote]
        dog_url_list.append(next_url)
        #print dog_url_list
        rest_of_urls = self.individual_dog_urls(contents[end_quote + 1:], dog_url_list)
        return dog_url_list
        
    
    def goto_next_page(self, contents):
        domain = 'http://www.sfspca.org'
        next_page_index = contents.find('"pager-next"')
        if next_page_index == -1:
            return False
        url_begin_index = contents.find('<a href="', next_page_index)
        url_end_index = contents.find('"', url_begin_index + 10)
        url = domain + contents[url_begin_index + 9:url_end_index]
        return url
            
        
    def dog_image(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        begin_image_section = trimmed_contents.find('<h1 class')
        end_image_section = trimmed_contents.find('NAME:', begin_image_section + 1)
        image_section = trimmed_contents[begin_image_section:end_image_section]
        begin_image_index = image_section.find('src=')
        end_image_index = image_section.find('"', begin_image_index + 6)
        image = image_section[begin_image_index + 5:end_image_index]
        return image
        
            
    def dog_name(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_name_index = trimmed_contents.find('NAME:')
        trimmed_contents = trimmed_contents[find_name_index:]
        name = re.search("([A-Z]+[a-z]+ *)+", trimmed_contents)
        if name:
            name = name.group()
            return name
        return None
        

    def dog_id(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_id_index = trimmed_contents.find('ID:')
        trimmed_contents = trimmed_contents[find_id_index:]
        spca_id = re.search("[0-9]+", trimmed_contents)
        if spca_id:
            spca_id = spca_id.group()
            #print spca_id
            return spca_id
        return None
        

    def dog_gender(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_gender_index = trimmed_contents.find('GENDER:')
        trimmed_contents = trimmed_contents[find_gender_index:]
        gender = re.search("[A-Z]+[a-z]+", trimmed_contents)
        if gender:
            gender = gender.group()
            return gender
        return None


    def dog_breed(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_breed_index = trimmed_contents.find('BREED:')
        trimmed_contents = trimmed_contents[find_breed_index:]
        breed = re.search('<p class="ap_attr">([^<>]+?)<', trimmed_contents)
        if breed:
            breed = breed.group(1)
            #breed = breed.replace(',','\,')
            return breed
        return None
        
    
    def dog_color(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_color_index = trimmed_contents.find('COLOR:')
        trimmed_contents = trimmed_contents[find_color_index:]
        color = re.search("[A-Z]+[a-z]+", trimmed_contents)
        if color:
            color = color.group()
            return color
        return None
            
    
    def dog_age(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        find_age_index = trimmed_contents.find('AGE:')
        trimmed_contents = trimmed_contents[find_age_index:]
        age = re.search("([0-9]+y) ([0-9]+m)", trimmed_contents)
        if age:
            age = age.group()
            
        else:
            age = "Age not listed"
        return age


    def dog_description(self, contents):
        trimmed_contents = self.trim_contents_singledog(contents)
        begin_description = trimmed_contents.find('"pet-detail">')
        if begin_description == -1:
            description = 'No description available'
            return description
        end_description = trimmed_contents.find('</div>', begin_description + 1)
        description = trimmed_contents[begin_description + 13:end_description]
        description = description.replace('&#39;',"\'")
        return description

    


#-------------------------------------------------------------------------------------------------------------------------------------------
dog = DogDetails()

'''contents = dog.file_contents(settings.project_path + 'alldogs.html')

dog_url_list = dog.individual_dog_urls(contents)
assert dog_url_list[0] == 'http://www.sfspca.org/adoptions/pet-details/10424952-1', dog_url_list[0]
assert dog_url_list[1] == 'http://www.sfspca.org/adoptions/pet-details/15425048-3', dog_url_list[1]
assert dog_url_list[-1] == 'http://www.sfspca.org/adoptions/pet-details/16447161-2', dog_url_list[-1]
assert len(dog_url_list) == 21; len(dog_url_list)

assert dog.goto_next_page(contents) == 'http://www.sfspca.org/adoptions/dogs?page=1', dog.goto_next_page(contents)

contents = dog.file_contents(settings.project_path + 'singledog.html')
single_dog_dict = dog.dog_details(contents)

assert single_dog_dict['image'] == 'http://www.sfspca.org/sites/default/files/imagecache/animal_profile_default/photos/55513a35-c8c4-4b35-acd8-e90a05746766.jpg', single_dog_dict['image']
assert single_dog_dict['name'] == 'Lychee', single_dog_dict['name']
assert single_dog_dict['spca_id'] == '10424952', single_dog_dict['spca_id']
assert single_dog_dict['gender'] == 'Female', single_dog_dict['gender']
assert single_dog_dict['breed'] == 'Chihuahua\, Short Coat', single_dog_dict['breed']
assert single_dog_dict['color'] == 'Tan', single_dog_dict['color']
assert single_dog_dict['age'] == '3y 8m', single_dog_dict['age']
assert single_dog_dict['description'] == "Lychee is a friendly\, curious\, somewhat shy at first lady who\'s heart\'s desire is to be someone\'s constant friend. She can get a bit overwhelmed at too much noise so would prefer someone who is more book-worm than rock-star.  She is a volunteer favorite for her affectionate personality and stellar leash manners.  She would love to be the only dog in her household.", single_dog_dict['description']
'''
#-------------------------------------------------------------------------------------------------------------------------------------------
def truncate():
    conn = MySQLdb.connect(host= "localhost",
                                user="root",
                                passwd = settings.db_password,
                                db="spcadogs")
    cursor = conn.cursor()
    cursor.execute ("TRUNCATE dogdetails;")
    conn.commit()
        
def populate_db(all_contents):
    truncate()
    next_page = dog.goto_next_page(all_contents)
    while next_page:
        dog_url_list = dog.individual_dog_urls(all_contents, [])
        for url in dog_url_list:
            contents = dog.return_webpage_contents(url)
            dog_detail_dict = dog.dog_details(contents)
            dog.dog_details_to_db(dog_detail_dict)
        all_contents = dog.return_webpage_contents(next_page)
        next_page = dog.goto_next_page(all_contents)
    dog_url_list = dog.individual_dog_urls(all_contents, [])
    for url in dog_url_list:
        contents = dog.return_webpage_contents(url)
        dog_detail_dict = dog.dog_details(contents)
        dog.dog_details_to_db(dog_detail_dict)
    return
    
       
        
if __name__ == '__main__':
    all_contents = dog.return_webpage_contents('http://www.sfspca.org/adoptions/dogs')
    populate_db(all_contents)
    data = dog.details_from_db()
    print data
    filename = 'crontest.txt'
    f = open(filename, 'a')
    f.write('get_details.py ran at ' + str(time.time())+ '\n')
    f.close()
    
    
    


