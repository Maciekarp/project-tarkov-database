from tkinter import *
from tkinter import ttk

## custom widget for a table of data
#class TableWidget(tk.Frame):
#    def __init__(self, parent, rows=1, columns=1):
#        tk.Frame.__init__(self, parent)
#
#        # loop that constructs the table
#        for row in range(rows):
#            for col in range(columns):
#                pass
#


# 
def runQuery():
    print("Query submited")


#
def UpdateTable():

    pass


#
if __name__ == "__main__":
    # creating main window
    root = Tk()
    root.geometry('500x400')
    root.title("Tkinter App")

    queryLF = ttk.LabelFrame(root, text = "Run Query")

    queryVal = StringVar()
    queryEntry = ttk.Entry(queryLF, textvariable=queryVal, width=20)
    queryEntry.grid(row=0, column= 0, pady= (10, 10), padx= (10, 10))

    queryButton = ttk.Button(queryLF, text="Submit",command=runQuery)
    queryButton.grid(row=0, column=1, pady= (10, 10), padx= (10, 10))

    queryLF.pack(pady= (10, 10), padx= (10, 10))



    # Output frame 
    outputFrame = Frame(root)
    outputFrame.pack()

    # Scrollbars
    outputScroll = Scrollbar(outputFrame)
    outputScroll.pack(side=RIGHT, fill=Y)

    output = ttk.Treeview(outputFrame, yscrollcommand=outputScroll.set)
    output.pack()

    outputScroll.config(command=output.yview)

    root.mainloop()