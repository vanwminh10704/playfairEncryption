import tkinter

app = tkinter.Tk()
app.title("PlayFair Cipher")
Message = tkinter.Label(app,text = "Message").grid(row = 0, column = 0,padx = 5, pady = 5, sticky = "w")
MessageContent = tkinter.Entry(app).grid(row = 0, column = 1,padx = 5, pady = 5, sticky = "w")
app.geometry("450x450")
app.mainloop()


