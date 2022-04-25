This project uses a docker mariadb that can be accessed with the python scripts

docker run -p 3306:3306 -d --name mariadb -eMARIADB_ROOT_PASSWORD=Password123! mariadb/server:10.4

mariadb --host 127.0.0.1 -P 3306 --user root -pPassword123! 


pip freeze > requirements.txt

pip install -r requirements.txt