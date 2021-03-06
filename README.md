# Gutencloud

Select any text from the English-language Project Gutenberg and render it as a wordcloud image.

![wordcloud for Moby Dick](screenshots/screenshot-1.png)

Requires Python 3, MySQL 5.5.3+

There seems to be a bug in Flask-SQLAlchemy 2.2, use 2.1 for now.

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
* Copy `gutencloud/secrets_template.py` to `gutencloud/secrets.py`. 
Change the values in `secrets.py` to database credentials (above).
* Run `pip install -m requirements.txt` to install required Python modules
* Run `python3 -m utilities.populate_db` to seed the database with metadata from Project Gutenberg. This 
process will:
    * download a 40MB datafile
    * processes that for __a while__ (53,000+ ebooks) and store it in the DB
* Start the app with `python3 -m gutencloud.server`

## To Do
* Fix bugs
* Write tests
* Better UX
    * Options for different wordcloud styles
    * Wordcloud in image map
* Better packaging
* Host on web so normal people who don't admin SQL servers can use

## Lessons learned
* Why all that hoopla about "semantic web" mysteriously died off around 2009. (XML-RDF is complicated!)
* MySQL's default version of UTF-8 is limited to 3 bytes, unlike Python (and most other implementations) 
which support a full 4 bytes. Have to override default to get "real" UTF-8 in MySQL.
* For a site that serves the public domain, Project Gutenberg is weirdly unfriendly to programmers.
