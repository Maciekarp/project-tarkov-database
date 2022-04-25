import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mariadb
import config
from functools import partial



# used to show a message to the user in a new window
def Alert(message):
    alertBox = getattr(tk.messagebox, 'show{}'.format('info'))
    alertBox("Alert", message)

# Runs a 
def runQuery(command):
    conn = mariadb.connect(**config.mariaDBConfig)
    cur = conn.cursor()
    try:
        cur.execute(command)
    except:
        Alert("Error calling \n\"" + command + "\"")
        cur.close()
        conn.close()
        return

    rowHeaders = [x[0] for x in cur.description]
    rows = [x for x in cur.fetchall()]

    print(rowHeaders)
    print(rows)

    UpdateTable(rowHeaders, rows)

    cur.close()
    conn.close()


# Using the the information collected displays the resulting query 
def UpdateTable(rowHeaders, rows):
    
    # deletes previous values if they exist
    for i in output.get_children():
        output.delete(i)

    # generates columns and column headers
    output['columns'] = rowHeaders
    output.column("#0", width=0, stretch=tk.NO)
    output.heading("#0",text="",anchor=tk.CENTER)
    for col in rowHeaders:
        output.column(col, anchor=tk.CENTER, width=80)
        output.heading(col, text=col, anchor=tk.CENTER)


    # Generates values
    for row in range(len(rows)):
        output.insert(parent='',index='end',iid=row, text='',
        values=rows[row])


#
if __name__ == "__main__":
    # creating main window
    root = tk.Tk()
    root.geometry('500x400')
    root.title("Tkinter App")


    # Run Query widgets 
    queryLF = ttk.LabelFrame(root, text = "Run Query")

    queryVal = tk.StringVar()
    queryVal.set("SELECT * FROM people")
    queryEntry = ttk.Entry(queryLF, textvariable=queryVal, width=40)
    queryEntry.grid(row=0, column= 0, pady= (10, 10), padx= (10, 10))

    queryButton = ttk.Button(queryLF, text="Submit",command=partial(runQuery, queryVal.get()))
    queryButton.grid(row=0, column=1, pady= (10, 10), padx= (10, 10))

    queryLF.pack(pady= (10, 10), padx= (10, 10))



    # Output frame 
    outputFrame = tk.Frame(root)
    outputFrame.pack()

    # Scrollbars
    outputScroll = tk.Scrollbar(outputFrame)
    outputScroll.pack(side=tk.RIGHT, fill=tk.Y)

    output = ttk.Treeview(outputFrame, yscrollcommand=outputScroll.set)
    output.pack()

    outputScroll.config(command=output.yview)

    root.mainloop()