This project contains code in two different files which is specifically created to get new news coming from google news and will update to database in every one hour

# scrapper.py :
> It has several methods to manipulations between webpage content and database but user just have to create instance of Scrapper class and have to call refresh() method to refresh content in database from webpage

# main.py
> It consists calling of refresh method with interval of one hour as well