import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mariadb
import config                   # file that contains info about database
import buildDB                  # file containing commands to build database
#from tkHyperlinkManager import HyperlinkManager

# used to show a message to the user in a new window
def Alert(message):
    alertBox = getattr(tk.messagebox, 'show{}'.format('info'))
    alertBox("Alert", message)

def userQuery():
    runQuery(queryVal.get())

# Executes a query brings up alert if it fails
def runQuery(command):
    conn = mariadb.connect(**config.mariaDBConfig)
    cur = conn.cursor()
    try:
        cur.execute(command)
    except Exception as e:
        Alert("Error calling \n\"" + command + "\"\n" + str(e))
        print(e)
        cur.close()
        conn.close()
        return

    rowHeaders = [x[0] for x in cur.description]
    rows = [x for x in cur.fetchall()]

    #print(rowHeaders)
    #print(rows)

    UpdateTable(rowHeaders, rows)

    cur.close()
    conn.close()


# Using the the information collected displays the resulting query 
def UpdateTable(rowHeaders, rows):
    
    # deletes previous values if they exist
    output.column("#0", width=0, stretch=tk.NO)
    for i in output.get_children():
        output.delete(i)

    # generates columns and column headers
    output['columns'] = rowHeaders
    output.column("#0", width=0, stretch=tk.NO)
    output.heading("#0",text="",anchor=tk.CENTER)
    for col in rowHeaders:
        output.column(col, anchor=tk.CENTER, width=100)
        output.heading(col, text=col, anchor=tk.CENTER)
    

    # Generates values
    for row in range(len(rows)):
        output.insert(parent='',index='end',iid=row, text='',
        values=rows[row])



#
if __name__ == "__main__":
    # creating main window
    root = tk.Tk()
    root.geometry('600x400')
    root.title("Tkinter App")



    # Edit Tables widgets
    tablesLF = ttk.LabelFrame(root, text = "")
    tablesLF.grid(row=1, column=0, padx= 10, pady=10, sticky="nsew")

    destroyButton = ttk.Button(tablesLF, text="Destroy",command=buildDB.ClearDB)
    destroyButton.grid(row=0, column=0, pady= (10, 10), padx= (10, 10))

    buildButton = ttk.Button(tablesLF, text="Build",command=buildDB.BuildTables)
    buildButton.grid(row=1, column=0, pady= (10, 10), padx= (10, 10))

    populateButton = ttk.Button(tablesLF, text="Populate",command=buildDB.Populate)
    populateButton.grid(row=2, column=0, pady= (10, 10), padx= (10, 10))



    # Run Query widgets 
    queryLF = ttk.LabelFrame(root, text = "Run Query")
    queryLF.grid(row=0, column=1, pady= (10, 10), padx= (10, 10), sticky="nsew")

    queryVal = tk.StringVar()
    queryVal.set("SELECT * FROM people")
    queryEntry = ttk.Entry(queryLF, textvariable=queryVal, width=30)
    queryEntry.grid(row=0, column= 0, pady= (10, 10), padx= (10, 10))

    queryButton = ttk.Button(queryLF, text="Submit",command=userQuery)
    queryButton.grid(row=0, column=1, pady= (10, 10), padx= (10, 10))



    # Output frame 
    outputFrame = ttk.LabelFrame(root)
    outputFrame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Scrollbars
    outputScroll = ttk.Scrollbar(outputFrame)
    outputScroll.grid(row=0, column=1, sticky="ns")

    outputSideScroll = ttk.Scrollbar(outputFrame, orient=tk.HORIZONTAL)
    outputSideScroll.grid(row=1, column=0, sticky="ew")

    output = ttk.Treeview(outputFrame, yscrollcommand=outputScroll.set, xscrollcommand=outputSideScroll.set)

    outputScroll.config(command=output.yview)
    outputSideScroll.config(command=output.xview)
    output.column("#0", width=400, stretch=tk.NO)
    output.grid(row=0, column=0, sticky="nsew")
    


    root.mainloop()