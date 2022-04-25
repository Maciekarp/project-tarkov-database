# Python script that accesses an existing mariadb instance
# 
from msilib.schema import tables
import config
import mariadb
import json

quests = {"name" : "quests", }
traders = {"name" : "traders", }
maps = {"name" : "maps", }
items = {"name" : "items", }
objective_warning = {"name" : "objective_warning", }
objective_skill = {"name" : "objective_skill", }
objective_locate = {"name" : "objective_locate", }
objective_use_item = {"name" : "objective_use_item", }
objective_get = {"name" : "objective_get", }
objective_rep = {"name" : "objective_rep", }


tables = [
    quests, traders, maps, items, 
    objective_warning, objective_skill, objective_locate, 
    objective_use_item, objective_get, objective_rep
]

# clear existing tables
def ClearDB():
    conn = mariadb.connect(**config.mariaDBConfig)
    cur = conn.cursor()
    for table in tables:
        try:
            cur.execute("DROP TABLE", table.name)
        except:
            print(table.name, "does not exist")
    cur.close()
    conn.close()

# Set up tables and attributes 
def BuildTables():
    pass

# Read and populate tables

def Populate():
    pass