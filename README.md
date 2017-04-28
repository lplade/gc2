# Gutencloud

Select any text from the English-language Project Gutenberg and render it as a wordcloud image.

Requires Python 3, MySQL 5.5.3+

Project Gutenberg etext handling routines based on code from Clemens Wolff's 
[gutenberg](https://github.com/c-w/Gutenberg) module. (We don't actually depend on that module because 
we don't want to generate 3GB of BerkelyDB store.)

## Setup

* Set up a venv for this (optional but recommended)
* Install MySQL. (MariaDB should be fine too.)
* Create a MySQL database: (replace `<user>` and `<password>` with info of your choosing)
    * (sudo)# `mysql -u root -p` and enter your MySQL root password
    * mysql> `CREATE USER '<user>'@'localhost' IDENTIFIED BY '<password>';` (Only 
    if you don't already have this user)
    * mysql> `CREATE DATABASE gutencloud DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;`
    * mysql> `GRANT ALL PRIVILEGES ON gutencloud.* to '<user>'@'localhost';`
* Run `pip install -m requirements.txt` to install required Python modules
* Run `python3 -m utilities.populate_db` to seed the database with metadata from Project Gutenberg. This 
process will:
    * download a 40MB datafile
    * processes that for __a while__ (53,000+ ebooks) and store it in the DB
* Start the app with ...