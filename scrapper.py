from requests import get
from bs4 import BeautifulSoup
from mysql import connector

class Scrapper:

    def __init__(self):
        url = "https://news.google.com/search?q=nri&hl=en-IN&gl=IN&ceid=IN%3Aen"
        # getting html content from url provided
        self.soup = BeautifulSoup(get(url).content, 'html.parser')
        # getting all records having in database for comparision
        self.db_records = self.get_all_records()

    def get_articles(self):
        # blank list to load articles in it from webpage
        list_ = []
        # getting article tag with class specified as it is of class name in page
        articles = self.soup.find_all("article", class_="MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne")

        # iterating through each of article with the class name specified as it contains article
        for article in articles:
            # getting title, link, publisher and time of a specific article
            title = article.find('a', 'DY5T1d RZIKme').text
            title = title.replace("'",r"\'")
            link = "https://news.google.com" + article.find('a', 'DY5T1d RZIKme')['href'][1:]
            publisher = article.find('a','wEwyrc AVN2gc uQIVzc Sksgp').text
            time = article.find('time', 'WW6dff uQIVzc Sksgp').text

            # appending all the articles in a list to check in future
            list_.append({'title':title, 'link':link, 'publisher':publisher, 'time':time})

        return list_

    def refresh(self):
        # getting all the article available in webpage
        articles = self.get_articles()
        for article in articles:
            # inserting all the records which are not in database
            if not self.record_exists(article['title'], article['publisher'], article['time']):
                self.insert(article['title'], article['link'], article['publisher'], article['time'])

    def insert(self, title, link, publisher, time):
        # direct insert to database and also maintained exception if exists
        try:
            sqldb = self.get_connection()
            cursor = sqldb.cursor()
            cursor.execute(f"INSERT INTO articles(`title`,`link`,`publisher`,`time`) VALUES('{title}','{link}','{publisher}','{time}')")
            cursor.close()
            sqldb.commit()
        except:
            return
          
    def get_all_records(self):
        # will return all the articles stored in database
        sqldb = self.get_connection()
        cursor = sqldb.cursor()
        cursor.execute("SELECT * FROM articles")
        return cursor.fetchall()

    def record_exists(self, title, publisher, time):
        # function to check that record is there in database or not
        for record in self.db_records:
            if record[1].replace("'", r"\'") == title and record[3] == publisher and record[4] == time:
                return True
        return False
    
    def get_connection(self):
        # will return connection object to use at multiple place
        return connector.connect(host="localhost", user="root", password="Raka@1211", database="scrapper")

