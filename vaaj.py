import tkinter as tk


root = tk.Tk()
root.geometry("800x400")



def showWin():
    new_win = tk.Tk()
    new_win.geometry("300x300")
    photo = tk.PhotoImage(file="./unnamed.png")  # or example.png

    label = tk.Label(new_win, image=photo)
    label.pack()


btn1 = tk.Button(text="click me", command=showWin)
btn1.pack()

root.mainloop()