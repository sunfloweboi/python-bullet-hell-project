import tkinter as tk

def startgame():
    # Code to start the game goes here
    import main

class mainmenu:
    def __init__(self, root):
        self.root = root
        self.root.title("bullethell")
        self.root.configure(bg="black")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()


        window_width = 700
        window_height = 800
        x_coordinate = (screen_width/2) - (window_width/2)
        y_coordinate = (screen_height/2) - (window_height/2)
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_coordinate), int(y_coordinate)))


        
        self.start_button = tk.Button(self.root, text="Start Game", font=("Segoe Script", 16), bg="white", command = lambda:[self.root.destroy(), startgame()])
        self.quit_button = tk.Button(self.root, text="Quit", font=("Segoe Script", 16), bg="white", command=self.root.destroy)
        self.label = tk.Label(self.root, text="Bullethell", font=("Segoe Script", 50), bg="black", fg="white")
        
        self.label.place(x=180, y=100, width=350, height=300)
        self.start_button.place(x=200, y=500, width=300, height=35)
        self.quit_button.place(x=200, y=555, width=300, height=35)

   
root = tk.Tk()
app = mainmenu(root)
root.mainloop()

