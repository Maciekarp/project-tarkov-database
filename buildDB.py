# Python script that accesses an existing mariadb instance
from lib2to3.pgen2.token import NEWLINE
import config
import json

ID = "id CHAR(24)"
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
    

    # populates quests table, all objective tables and adds to items table items that only exist
    # within quests
    if tables == "all" or "quests" in tables:
        file = open(config.tarkovFilesPath + "quests.json", 'r', encoding='utf8')
        data = json.load(file)
        file.close()
        
        # id for the trader is 24 characters and starts with 1 for the sake of simplicity
        numQuests = 0
        numObjectives = 0
        questConnections = {}   # Dictionary where key is the current quest and value is next quest
        for quest in data:
            
            # Populates quests table
            name = quest["title"].replace("\'", "\'\'").replace("\"", "\"\"")
            #shortname = quest["locales"]["en"].replace("\'", "\'\'").replace("\"", "\"\"")

            query = "INSERT INTO " + quests["name"] + " VALUES (\"" + str(4 * pow(10, 23) + quest["id"])
            query += "\", \"" + str(pow(10, 23) + quest["giver"])
            query += "\", \"" + name + "\", NULL, \""
            query += quest["wiki"] + "\");"

            if query.isascii() :
                err = config.ExecuteQuery(query)
                if err and not "Duplicate entry" in str(err):
                    print(err)
                    print(query)
                    return -1
                else:
                    numQuests += 1
            else:
                print("Query:\n" + query + "\ncontains illigal characters")
                continue
            
            # adds unlocks to quest connections to be updated after all quests are added
            if quest["require"]["quests"]:
                currQuest = quest["require"]["quests"][-1]
                if type(currQuest) is list:
                    currQuest = currQuest[-1]
                questConnections[str(4 * pow(10, 23) + quest["id"])] = str(4 * pow(10, 23) + currQuest)
            
            # populates the objectives tables with objectves in the quest
            for objective in quest["objectives"]:
                tabletype = "INSERT INTO "
                values = " VALUES (\"" + str(3 * pow(10, 23) + objective["id"]) + "\", \"" + str(4 * pow(10, 23) + quest["id"]) + "\""
                if objective["type"] == "warning":
                    tabletype += objective_warnings["name"]
                    values += ", \"" + objective["target"].replace("\'", "\'\'").replace("\"", "\"\"") + "\""
                elif objective["type"] == "reputation":
                    tabletype += objective_reps["name"]
                    values += ", \"" + str(pow(10, 23) + objective["target"]) + "\", " + str(objective["number"])
                elif objective["type"] == "skill":
                    tabletype += objective_skills["name"]
                    values += ", \"" + objective["target"] + "\", " + str(objective["number"])
                elif objective["type"] == "locate":
                    tabletype += objective_locates["name"]
                    location = "\"" + str(2 * pow(10, 23) + objective["location"]) + "\""
                    if objective["location"] == -1:
                        location = "NULL"
                    values += ", \"" + objective["target"] + "\", " + str(objective["number"]) 
                    values += ", " + location
                elif objective["type"] == "kill":
                    tabletype += objective_kills["name"]
                    location = "\"" + str(2 * pow(10, 23) + objective["location"]) + "\""
                    if objective["location"] == -1:
                        location = "NULL"
                    values += ", \"" + objective["target"] + "\", " + str(objective["number"]) 
                    values += ", " + location
                elif objective["type"] == "mark" or objective["type"] == "pickup" or objective["type"] == "place":
                    tabletype += objective_use_items["name"]
                    # if an object needs to be pucked up and the target is a quest specific item it needs to be added to the items table
                    tool = ""
                    if objective["type"] == "mark":
                        tool = objective["tool"]
                    else:
                        tool = objective["target"]
                        if len(tool) != 24:
                            tool = tool.replace(" ", "")
                            if len(tool) > 24:
                                tool = tool[len(tool) - 24:]
                            elif len(tool) < 24:
                                tool = ("q" * (24 - len(tool))) + tool
                        query = "INSERT INTO items VALUES(\"" + tool + "\", \"" + objective["target"] + "\", NULL, 1, NULL)"
                        err = config.ExecuteQuery(query)
                        if err and not "Duplicate entry" in str(err):
                            print(err)
                            print(query)
                    values += ", \"" + tool + "\", " + str(objective["number"])
                    values += ", \"" + str(2 * pow(10, 23) + objective["location"]) + "\", \"" + objective["type"] + "\""
                elif objective["type"] == "find" or objective["type"] == "collect" or objective["type"] == "key":
                    tabletype += objective_gets["name"]
                    target = objective["target"]
                    if type(target) is list:
                        target = target[0]
                    values += ", \"" + target + "\", " + str(objective["number"]) + ", \"" + objective["type"] + "\""
                elif objective["type"] == "build":
                    continue
                else:
                    print("Objective type \"" + objective["type"] + "\" does not exist in database")
                    continue
                
                numObjectives += 1
                query = tabletype + values + ");"
                err = config.ExecuteQuery(query)
                if err and not "Duplicate entry" in str(err):
                    print(err)
                    print(query)
                    return -1
        
        print(len(questConnections))
        # goes through each connection updating foreign keys of previoulsy inserted quests
        for connection in questConnections:
            query = "UPDATE " + quests["name"] + " SET prev_quest_id = \"" + questConnections[connection] + "\" WHERE " + quests["pk"] + " = \"" + connection + "\";"
            print(query)
            err = config.ExecuteQuery(query)
            if err and not "Duplicate entry" in str(err):
                print(err)
                print(query)
                return -1

        print(numQuests, "rows added to quests table")

    return 1

    


# used for debugging if buildDB is called on its own clears table and builds it
if __name__ == "__main__":
    ClearDB()
    BuildTables()
    Populate()
    #Populate("quests")