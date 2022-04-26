import mariadb
# Python file with configs used for accessing files and the database

# Path where files are located
tarkovFilesPath = "tarkovdata-master/"

wiki = "https://escapefromtarkov.fandom.com/wiki/"

# object that contains route information for the mariaDB instance
mariaDBConfig = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Password123!',
    'database': 'tarkovdata'
}

# Function that takes a query and returns an error msg if failed and "" if execution works
def ExecuteQuery(query):
    errMsg = ""
    conn = mariadb.connect(**mariaDBConfig)
    cur = conn.cursor()
    try:
        cur.execute(query)
    except Exception as e:
        errMsg = e
    
    cur.close()
    conn.commit()
    conn.close()
    return errMsg