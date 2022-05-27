import socket
from tkinter import *
from threading import Thread

from click import option

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# nickname = input("Choose your Nickname:\t")

ip_address = "127.0.0.1"
port = 8000


client.connect((ip_address, port))

print("Connected with the Server...")

answered = False


class GUI:

    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry("500x600")
        self.login.configure(bg="lightgreen")
        self.login.resizable(height=FALSE, width=False)

        self.title = Label(self.login, width=10, height=1, text="Login",
                           bg="lightgreen", font="Calibri 35 bold italic")
        self.title.place(x=140, y=10)

        self.line = Label(self.login, width=400, bg="green")
        self.line.place(y=70, relheight=0.01)

        nameEntry = Entry(self.login, width=25, justify="center",
                          font=("Chalkboard SE", 22), bd=1, bg="white")
        nameEntry.place(x=50, y=120)

        button = Button(self.login, text="Save", font=("Chalkboard SE", 15), command=lambda: saveName(
            self, nameEntry.get()), width=12, height=1, bg="blue", bd=3)
        button.place(x=50, y=220)

        self.Window.mainloop()

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("Quiz Room")
        self.Window.resizable(height=FALSE, width=False)
        self.Window.configure(width=500, height=600, bg="#17202A")

        self.textCons = Text(self.Window, width=20, height=2,
                             bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        self.textCons.place(relheight=0.5, relwidth=1, rely=0.08,)
        self.textCons.config(cursor="arrow")

        option_a = Button(self.Window, text="Answer A", font=(
            "Chalkboard SE", 15), state=NORMAL, command=lambda: send(self, option="A"))
        option_a.place(rely=0.6, x=100)

        option_b = Button(self.Window, text="Answer B", font=(
            "Chalkboard SE", 15), state=NORMAL, command=lambda: send(self, option="B"))
        option_b.place(rely=0.6, x=270)

        option_c = Button(self.Window, text="Answer C", font=(
            "Chalkboard SE", 15), state=NORMAL, command=lambda: send(self, option="C"))
        option_c.place(rely=0.7, x=100)

        option_d = Button(self.Window, text="Answer D", font=(
            "Chalkboard SE", 15), state=NORMAL, command=lambda: send(self, option="D"))
        option_d.place(rely=0.7, x=270)


    def receive(self):
        while True:
            try:
                msg = client.recv(2048).decode('utf-8')
                if msg == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                    print('nickname send...')
                else:
                    global answered

                    answered = False
                    self.show_msg(msg)

            except:
                print("An error occured")
                client.close()
                break

    def show_msg(self, msg):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg+"\n\n")
        self.textCons.config(state=NORMAL)
        self.textCons.see(END)


def send(self, option):
    msg = f"{self.name}:{option}"
    client.send(msg.encode("utf-8"))
    self.textCons.delete('1.0', END)


def saveName(self, name):
    self.login.destroy()
    # self.name = name
    self.layout(name)
    rcv = Thread(target=self.receive)
    rcv.start()


g = GUI()


"""
def receive():
    while True:
        try:
            msg = client.recv(2048).decode("utf-8")
            if msg == "NICKNAME":
                client.send(nickname.encode("utf-8"))

            else:
                print(msg)

        except:
            print("An error occurred")
            client.close()
            break


def write():
    while True:
        msg = f"{nickname}:{input('')}"
        client.send(msg.encode("utf-8"))


receive_thread = Thread(target=receive)
receive_thread.start()

write_thread = Thread(target=write)
write_thread.start()
"""
