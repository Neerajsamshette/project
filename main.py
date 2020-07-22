from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from hoverable import HoverBehavior
from kivy.core.window import Window
import json
from datetime import datetime
import glob
from pathlib import Path
import random

Builder.load_file('design.kv')

# Window.clearcolor = (255,255,255,255)

class LoginScreen(Screen):
    def Login_page(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
            if uname in users and users[uname]["password"] == pword:
                self.manager.current = "Login_success"
            else:
                self.ids.Error.text = 'Invalid username or password'
    def SignUp(self):
        self.manager.current = "Sign_up_screen"

class SignUpScreen(Screen):
    def Add_user(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
            users[uname] = {"username":uname,"password":pword,
            "created": datetime.now().strftime("%Y-%m-%D-%H-%M-%S")}
            
            with open("users.json") as file:
                json.dump(users,file)
        self.manager.current = "Sign_in_success"
    def Logout(self):
        self.manager.current = 'Login_screen'

class SignInSuccess(Screen):
    def successfull(self):
        self.manager.current = "Login_screen"

class LoginSuccess(Screen):
    def Logout(self):
        self.manager.current = "Login_screen"

    def get_feelings(self,feel):
        feel = feel.lower()

        available_feelings = glob.glob("quotes/*txt")
        
        available_feelings = [Path(filename).stem for filename in available_feelings]
        
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                file = file.readlines()
                # quotes = files.readlines()
                self.ids.quote.text = random.choice(file)
        # print(available_feelings)

class ImageButton(ButtonBehavior,Image,HoverBehavior):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()