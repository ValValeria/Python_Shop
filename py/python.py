
from tkinter import *
 
clicks = 0
 
 
def click_button():
    global clicks
    clicks += 1
    buttonText.set("Clicks {}".format(clicks))
 
root = Tk()
root.title("GUI на Python")
root.geometry("300x250")
 
buttonText = StringVar()
buttonText.set("Clicks {}".format(clicks))
for y in range(1) :

  for x in range(1):

    btn=Button(
     text=str('Check your name'),
     background="#feca57",
     foreground="white",
     font="Arial 10",
     command=click_button
    )
    label=Label(text='Find out if you have special name',font="Arial 10")


    label.grid(row=y+2,column=x)
    btn.grid(row=y+3,column=x,ipadx=10, ipady=6, padx=10, pady=10)

    
    message_entry=Entry(width=200)
    message_entry.grid(row=y+4,column=x)

    
 
root.mainloop()
