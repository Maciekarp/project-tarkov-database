# Takov DB

## Project Description
This is a simple python app that provides an interface to populate and query a
database containing data from the game Escape from Tarkov

This project uses a docker mariadb image that can be accessed with the python scripts

## How to setup
To run this you must have [Python](https://www.python.org/downloads/), 
[Docker](https://www.docker.com/products/docker-desktop/), 
[MariaDB](https://mariadb.com/downloads/community/),
and [MariaDB Python Connector](https://mariadb.com/downloads/connectors/connectors-data-access/python-connector) installed on your system

First a MariaDB database must be started to do so in the command prompt run:
`docker run -p 3306:3306 -d --name mariadb -eMARIADB_ROOT_PASSWORD=Password123! mariadb/server:10.4`


`mariadb --host 127.0.0.1 -P 3306 --user root -pPassword123!`


`pip freeze > requirements.txt`

`pip install -r requirements.txt`
