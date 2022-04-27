# Python script that accesses an existing mariadb instance
import config
import json

ID = "id CHAR(24) NOT NULL"
NAME = "name VARCHAR(100)"
LINK = "link VARCHAR(200)"
CURRENCY = "currency CHAR(3)"
NUMBER = "number int"
QUEST_ITEM = "is_quest_item int"
WARNING = "warning VARCHAR(100)"
TYPE = "type VARCHAR(10)"

traders = {
    "name" : "traders", 
    "keys" : ["trader_" + ID, "locale_" + NAME, NAME, CURRENCY, LINK], 
    "pk" : "trader_id", "fk" : []
}
maps = {
    "name" : "maps", 
    "keys" : ["map_" + ID, NAME, LINK], 
    "pk" : "map_id", "fk" : []
}
items = {
    "name" : "items", 
    "keys" : ["item_" + ID, NAME, "short_" + NAME, QUEST_ITEM, LINK], 
    "pk" : "item_id", "fk" : []
}
quests = {
    "name" : "quests", 
    "keys" : ["quest_" + ID, "trader_" + ID, NAME, "prev_quest_" + ID, LINK], 
    "pk" : "quest_id", "fk" : [["trader_id", "traders(trader_id)"], ["prev_quest_id", "quests(quest_id)"]]
}
objective_warnings = {
    "name" : "objective_warnings", 
    "keys" : ["objective_warning_" + ID, "quest_" + ID, WARNING], 
    "pk" : "objective_warning_id", "fk" : [["quest_id", "quests(quest_id)"]]
}
objective_skills = {
    "name" : "objective_skills", 
    "keys" : ["objective_skill_" + ID, "quest_" + ID, "skill_" + NAME, NUMBER], 
    "pk" : "objective_skill_id", "fk" : [["quest_id", "quests(quest_id)"]]
}
objective_locates = {
    "name" : "objective_locates", 
    "keys" : ["objective_locate_" + ID, "quest_" + ID, "target_" + NAME, NUMBER, "map_" + ID], 
    "pk" : "objective_locate_id", "fk" : [["quest_id", "quests(quest_id)"], ["map_id", "maps(map_id)"]]
}
objective_kills = {
    "name" : "objective_kills", 
    "keys" : ["objective_kill_" + ID, "quest_" + ID, "target_" + NAME, NUMBER, "map_" + ID], 
    "pk" : "objective_kill_id", "fk" : [["quest_id", "quests(quest_id)"], ["map_id", "maps(map_id)"]]
}
objective_use_items = {
    "name" : "objective_use_items", 
    "keys" : ["objective_use_item_" + ID, "quest_" + ID, "item_" + ID, NUMBER, "map_" + ID, TYPE], 
    "pk" : "objective_use_item_id", "fk" : [["quest_id", "quests(quest_id)"], ["map_id", "maps(map_id)"], ["item_id", "items(item_id)"]]
}
objective_gets = {
    "name" : "objective_gets", 
    "keys" : ["objective_get_" + ID, "quest_" + ID, "item_" + ID, NUMBER, TYPE],
    "pk" : "objective_get_id", "fk" : [["quest_id", "quests(quest_id)"], ["item_id", "items(item_id)"]]
}
objective_reps = {
    "name" : "objective_reps",
    "keys" : ["objective_rep_" + ID, "quest_" + ID, "trader_" + ID, NUMBER],
    "pk" : "objective_rep_id", "fk" : [["quest_id", "quests(quest_id)"], ["trader_id", "traders(trader_id)"]]
}


DB_TABLES = [
    traders, maps, items, quests,
    objective_warnings, objective_skills, objective_locates, objective_kills,
    objective_use_items, objective_gets, objective_reps
]



# clear existing tables
def ClearDB():
    for table in reversed(DB_TABLES):
        err = config.ExecuteQuery("DROP TABLE " + table["name"])
        if err:
            print(table["name"], "does not exist")
            print(err)



# Set up tables and attributes 
def BuildTables():
    for table in DB_TABLES:
        createQuery = "CREATE TABLE IF NOT EXISTS " + table["name"] + " ( "
        
        # keys
        for key in table["keys"]:
            createQuery += key + ", "

        # primary key
        createQuery += "PRIMARY KEY (" + table["pk"] + "), "

        # foreign key
        for fk in table["fk"]:
            createQuery += "FOREIGN KEY (" + fk[0] + ") REFERENCES " + fk[1] + ", "
        
        createQuery = createQuery[:-2] + ")" # drops the trailing ", " and closes the query
        
        err = config.ExecuteQuery(createQuery)
        if err:
            print(err)
        else:
            print(table["name"], "Created")



# Read and populate tables
def Populate(tables = "all"):

    # populates traders table
    if tables == "all" or "traders" in tables:
        file = open(config.tarkovFilesPath + "traders.json", 'r', encoding='utf8' )
        data = json.load(file)
        file.close()
        # id for the trader is 24 characters and starts with 1 for the sake of simplicity
        for trader in data:
            curr = data[trader]
            query = "INSERT INTO " + traders["name"] + " VALUES (\"" + str(pow(10, 23) + curr["id"])
            query += "\", \""  + curr["locale"]["en"] + "\", \"" + curr["name"] + "\", \""
            query += curr["salesCurrency"] + "\", \"" + curr["wiki"] + "\");"

            err = config.ExecuteQuery(query)
            if err:
                print(err)
                return -1
    
        print(len(data), "rows added to traders table")

    # populates maps table
    if tables == "all" or "maps" in tables:
        file = open(config.tarkovFilesPath + "maps.json", 'r', encoding='utf8')
        data = json.load(file)
        file.close()
        # id for the trader is 24 characters and starts with 1 for the sake of simplicity
        for map in data:
            curr = data[map]
            query = "INSERT INTO " + maps["name"] + " VALUES (\"" + str(2 * pow(10, 23) + curr["id"])
            query += "\", \""  + curr["locale"]["en"] + "\", \"" + curr["wiki"] + "\");"

            err = config.ExecuteQuery(query)
            if err:
                print(err)
                return -1
    
        print(len(data), "rows added to maps table")

    # populates items table
    if tables == "all" or "items" in tables:
        file = open(config.tarkovFilesPath + "items.en.json", 'r', encoding='utf8')
        data = json.load(file)
        file.close()
        # id for the trader is 24 characters and starts with 1 for the sake of simplicity
        for item in data:
            curr = data[item]
            name = curr["name"].replace("\'", "\'\'").replace("\"", "\"\"")
            shortname = curr["shortName"].replace("\'", "\'\'").replace("\"", "\"\"")
            query = "INSERT INTO " + items["name"] + " VALUES (\"" + curr["id"]
            query += "\", \"" + name + "\", \"" + shortname + "\", "
            query += "0, \"" + config.wiki + name.replace(" ", "_") + "\");"

            if query.isascii() :
                err = config.ExecuteQuery(query)
            else:
                print("Query:\n" + query + "\ncontains illigal characters")

            if err:
                print(err)
                print(query)
                return -1
    
        print(len(data), "rows added to items table")
    


    return 1

    



ClearDB()
BuildTables()
Populate()