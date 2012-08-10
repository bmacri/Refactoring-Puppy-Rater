class DogObject():
    pass

class RatingsObject():
    pass
    
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
    
def truncate():
    conn = MySQLdb.connect(host= "localhost",
                                user="root",
                                passwd = settings.db_password,
                                db="spcadogs")
    cursor = conn.cursor()
    cursor.execute ("TRUNCATE dogdetails;")
    conn.commit()


