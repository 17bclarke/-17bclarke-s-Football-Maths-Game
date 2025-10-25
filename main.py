import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.config import Config
import random
import math
import time
import sqlite3

conn = sqlite3.connect("NEA_db.db")
c = conn.cursor()
username = None
content = None

class Forgot_Password(App):
    def build(self):
        Window.clearcolor = (0,0.8,0,0.8)
        return FP()

class Home_page(App):
    def build(self):
        Window.clearcolor = (0,0.8,0,0.8)
        return First()
    
class Rules(App):
    def build(self):
        Window.clearcolor = (0,0.8,0,0.8)
        return Second()

class Login(App):
    def build(self):
        Window.clearcolor = (0,0.8,0,0.8)
        return Login_page()

class Sign_Up(App):
    def build(self):
        Window.clearcolor = (0,0.8,0,0.8)
        return Sign_up()
    
class Game(App):
    def build(self):
        Window.clearcolor = (0,0.8,0,0.8)
        return Main_Window()

class FP(GridLayout):
    def __init__(self,**kwargs):
        super(FP, self).__init__(**kwargs)
        self.fullscreen = True
        self.closeable = False
        self.cols = 2
        self.add_widget(Label(text="",size_hint_y=None, height=150))
        self.add_widget(Label(text="",size_hint_y=None, height=150))
        self.add_widget(Label(text="Username:",font_size=72,color= (0.8,0,0,1),bold=True, size_hint_y=None, height=100))
        self.username = TextInput(multiline=False,font_size=64,background_color=(0,0,0.8,1), foreground_color=(1,1,1,1),size_hint_y=None, height=100, halign="center")
        self.add_widget(self.username)
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="New password:",font_size=72,color= (0.8,0,0,1),bold=True, size_hint_y=None, height=100))
        self.password = TextInput(multiline=False,font_size=64,background_color=(0,0,0.8,1),foreground_color=(1,1,1,1) ,size_hint_y=None, height=100, halign="center",password=True)
        self.add_widget(self.password)
        self.add_widget(Label(text="",size_hint_y=None, height=300))
        self.add_widget(Label(text="",size_hint_y=None, height=300))
        self.Button1 = Button(text="Submit",font_size=72,background_color=(0,0.8,0,1),height=100)
        self.Button1.bind(on_press=self.check)
        self.add_widget(self.Button1)
        self.Button2 = Button(text="Return to login",font_size=72,background_color=(0,0.8,0,1),height=100)
        self.Button2.bind(on_press=self.return_user)
        self.add_widget(self.Button2)
    
    def return_user(self,instance):
        self.clear_widgets()
        Login().run()

    def check(self,instance):
        c.execute("SELECT Usernames FROM U_P")
        Usernames = c.fetchall()
        conn.commit()
        value = 0
        self.username.text = self.username.text.lower()
        for usernames in Usernames:
            if self.username.text == usernames[0]:
                value += 1
                c.execute("SELECT Passwords FROM U_P WHERE Usernames = ?",(self.username.text, ))
                password = c.fetchall()
                conn.commit()
                character = 0
                for letters in self.password.text:
                    SCS = '[@_!#$%^&*()<>?/\|}{~:]'
                    if letters.isnumeric() or letters in SCS:
                        character += 1
                    if 12 >= len(self.password.text) >= 4 and character > 0:
                        if self.password.text != password[0]:
                            c.execute("UPDATE U_P SET Passwords = "+self.password.text+" WHERE Usernames = ?",(self.username.text, ))
                            conn.commit()
                            self.clear_widgets()
                            Login().run()
                if character == 0 or len(self.password.text) < 4 or len(self.password.text) > 12:
                    content = BoxLayout(orientation='vertical', padding=20)
                    name_label = Label(text="Invalid password")
                    content.add_widget(name_label)
                    self.popup = Popup(title="Password", content=content, size_hint=(None, None), size=(800, 400))
                    self.popup.open()    
        if value == 0:
            content = BoxLayout(orientation='vertical', padding=20)
            name_label = Label(text="Username doesn't exist")
            content.add_widget(name_label)
            self.popup = Popup(title="Username", content=content, size_hint=(None, None), size=(800, 400))
            self.popup.open()

class First(GridLayout):
    def __init__(self,**kwargs):
        super(First, self).__init__(**kwargs)
        self.fullscreen = True
        self.closeable = False
        self.cols = 1
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        # creating leaderboard
        c.execute("SELECT Wins FROM U_P")
        names = c.fetchall()
        conn.commit()
        base = 0
        for name in names:
            if name[0] > base:
                base = name[0]

        name_DB = []
        while len(name_DB) < 3:
            c.execute("SELECT Usernames FROM U_P WHERE Wins = ?",(base, ))
            values = c.fetchall()
            conn.commit()
            for value in values:
                if value not in name_DB and value != []:
                    name_DB.append(value)
            base = base - 1

        self.add_widget(Label(text="Welcome "+username,size_hint_y=None, height=300,font_size=100))
        self.add_widget(Label(text="Leaderboard: ",size_hint_y=None, height=100,font_size=90,halign="left"))
        c.execute("SELECT Wins FROM U_P WHERE Usernames = ?",(name_DB[0][0], ))
        value = c.fetchall()
        conn.commit()
        self.add_widget(Label(text="1. "+str(name_DB[0][0])+" with "+str(value[0][0])+" wins",size_hint_y=None, height=100,font_size=90))
        c.execute("SELECT Wins FROM U_P WHERE Usernames = ?",(name_DB[1][0], ))
        value = c.fetchall()
        conn.commit()
        self.add_widget(Label(text="2. "+str(name_DB[1][0])+" with "+str(value[0][0])+" wins",size_hint_y=None, height=100,font_size=90))
        c.execute("SELECT Wins FROM U_P WHERE Usernames = ?",(name_DB[2][0], ))
        value = c.fetchall()
        conn.commit()
        self.add_widget(Label(text="3. "+str(name_DB[2][0])+" with "+str(value[0][0])+" wins",size_hint_y=None, height=100,font_size=100))
        self.add_widget(Label(text="",size_hint_y=None, height=100,font_size=100))
        self.buttons = Button(text="Play",font_size=72,background_color=(0,1,0,1),height=100)
        self.buttons.bind(on_press=self.play)
        self.add_widget(self.buttons)
        self.button = Button(text="Rules",font_size=72,background_color=(0,1,0,1),height=100)
        self.button.bind(on_press=self.rules)
        self.add_widget(self.button)

    def play(self, instance):
        self.clear_widgets()
        Game().run()

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self,keyboard,keycode,text,modifiers):
        if text == "q":
            # returns you to login screen
            self.canvas.clear()
            Login().run()

    def rules(self, instance):
        self.clear_widgets()
        Rules().run()

class Second(GridLayout):
    def __init__(self, **kwargs):
        super(Second, self).__init__(**kwargs)
        self.fullscreen = True
        self.closeable = False
        self.cols = 1
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self.add_widget(Label(text="Here are the rules:",size_hint_y=None, height=300,font_size=100, halign="left"))
        self.add_widget(Label(text="You are playing as the red team",size_hint_y=None, height=100,font_size=50))
        self.add_widget(Label(text="The first team with 3 goals wins",size_hint_y=None, height=100,font_size=50))
        self.add_widget(Label(text="Use WASD or the arrow keys to move and C to pass in the direction you last moved",size_hint_y=None, height=100,font_size=50))
        self.add_widget(Label(text="Use F to swap player",size_hint_y=None, height=100,font_size=50))
        self.add_widget(Label(text="Use R to see the score",size_hint_y=None, height=100,font_size=50))
        self.add_widget(Label(text="Pressing Q at any time will return you to the login screen",size_hint_y=None, height=100,font_size=50))
        self.add_widget(Label(text="",size_hint_y=None, height=50,font_size=100))
        self.returns = Button(text="Play",font_size=72,background_color=(0,1,0,1),height=100)
        self.returns.bind(on_press=self.plays)
        self.add_widget(self.returns)
        self.lead = Button(text="Leaderboard",font_size=72,background_color=(0,1,0,1),height=100)
        self.lead.bind(on_press=self.Leader)
        self.add_widget(self.lead)

    def plays(self, instance):
        self.clear_widgets()
        Game().run()

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self,keyboard,keycode,text,modifiers):
        if text == "q":
            # returns you to login screen
            self.canvas.clear()
            Login().run()

    def Leader(self, instance):
        self.clear_widgets()
        Home_page().run()

class Main_Window(GridLayout):
    def __init__(self, **kwargs):
        super(Main_Window, self).__init__(**kwargs)
        self.fullscreen = True
        self.closeable = False
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self.question_maker()
        self.rgoals = 0
        self.bgoals = 0
        self.control = 0
        self.possession = 0
        self.move = 3
        # creating pitch, players and ball
        with self.canvas:
            self.bg = Rectangle(source="pitch.png", pos=self.pos, size=self.size)
            self.score = Rectangle(source=str(self.bgoals)+str(self.rgoals)+".png", pos=(650,1000), size=(300,300))
            self.pass_button = Rectangle(source="pass.png", pos=(0,1000), size=(250,250))

            self.team1 = [Rectangle(source="shirt_red.png",pos=(800,600), size=(self.size[0]/8,self.size[1]/6)),
                         Rectangle(source="shirt_red.png",pos=(10,600), size=(self.size[0]/8,self.size[1]/6)),
                         Rectangle(source="shirt_red.png",pos=(250,300), size=(self.size[0]/8,self.size[1]/6)),
                         Rectangle(source="shirt_red.png",pos=(250,800), size=(self.size[0]/8,self.size[1]/6)),
                         Rectangle(source="shirt_red.png",pos=(400,600), size=(self.size[0]/8,self.size[1]/6))]
        
            self.team2 = [Rectangle(source="shirt_blue.png",pos=(1000,600), size=(self.size[0]/8,self.size[1]/6)),
                         Rectangle(source="shirt_blue.png",pos=(1500,600), size=(self.size[0]/8,self.size[1]/6)),
                         Rectangle(source="shirt_blue.png",pos=(1250,300), size=(self.size[0]/8,self.size[1]/6)),
                         Rectangle(source="shirt_blue.png",pos=(1250,800), size=(self.size[0]/8,self.size[1]/6)),
                         Rectangle(source="shirt_blue.png",pos=(1100,600), size=(self.size[0]/8,self.size[1]/6))]
            
            self.ball = Rectangle(source="ball.png", pos=(775,600), size=(self.size[0]/24,self.size[1]/18))
            self.team1[self.control].source = "shirt_green.png"

        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def update_bg(self, *args):
        # makes sure the pitch covers the full screen
        self.bg.size = self.size

    def _on_key_down(self,keyboard,keycode,text,modifiers):
        # moves the players on key press
        self.distance = math.sqrt((self.ball.pos[0]-self.team1[self.control].pos[0])**2 + (self.ball.pos[1]-self.team1[self.control].pos[1])**2)
        if self.distance < 200:
            self.pass_button.source = "pass.png"
            self.pass_button.pos = (0,1000)
            self.pass_button.size = (250,250)
        else:
            self.pass_button.source = "corner.png"
            self.pass_button.pos = (10,950)
            self.pass_button.size = (250,250)
        
        self._keyboard.bind(on_key_down=self._on_key_down)
        if text == "w" or keycode[1] == "up":
            self.team1[self.control].pos = (self.team1[self.control].pos[0],self.team1[self.control].pos[1]+20)
            self.move = 1
            Clock.unschedule(self.choice)
            Clock.unschedule(self.team_move)
            Clock.schedule_interval(self.choice, 0.5)
            Clock.schedule_interval(self.team_move, 0.5)
        if text == "s" or keycode[1] == "down":
            self.team1[self.control].pos = (self.team1[self.control].pos[0],self.team1[self.control].pos[1]-20)
            self.move = 2
            Clock.unschedule(self.choice)
            Clock.unschedule(self.team_move)
            Clock.schedule_interval(self.choice, 0.5)
            Clock.schedule_interval(self.team_move, 0.5)
        if text == "a" or keycode[1] == "left":
            self.team1[self.control].pos = (self.team1[self.control].pos[0]-20,self.team1[self.control].pos[1])
            self.move = 3
            Clock.unschedule(self.choice)
            Clock.unschedule(self.team_move)
            Clock.schedule_interval(self.choice, 0.5)
            Clock.schedule_interval(self.team_move, 0.5)
        if text == "d" or keycode[1] == "right":
            self.team1[self.control].pos = (self.team1[self.control].pos[0]+20,self.team1[self.control].pos[1])
            self.move = 4
            Clock.unschedule(self.choice)
            Clock.unschedule(self.team_move)
            Clock.schedule_interval(self.choice, 0.5)
            Clock.schedule_interval(self.team_move, 0.5)
        if text == "c":
            if self.distance < 200:
                self.ask_question()
        if text == "f":
            # changes what player you control
            self.team1[self.control].source = "shirt_red.png"
            if self.control == 0:
                self.control = 4
                self.team1[self.control].source = "shirt_green.png"
            else:
                self.control -= 1
                self.team1[self.control].source = "shirt_green.png"
        if text == "r":
            Clock.unschedule(self.choice)
            Clock.unschedule(self.team_move)
            self._keyboard.unbind(on_key_down=self._on_key_down)
            content = BoxLayout(orientation='vertical', padding=20)
            string_value = str(self.rgoals) + " " + str(self.bgoals)
            name_label = Label(text="Red "+string_value+" Blue",font_size=72)
            content.add_widget(name_label)
            self.popup = Popup(title="Score", content=content, size_hint=(None, None), size=(800, 400))
            self.popup.bind(on_dismiss=self.reschedule_function)
            self.popup.open()

        if text == "q":
            # returns you to login screen
            self.canvas.clear()
            Login().run()

        self.collision()
        self.check_goal()
        self.boundaries()

    def choice(self, instance):
        if self.possession == 0:
            Clock.schedule_once(self.move_bt)
        else:
            Clock.schedule_once(self.bt_in_possession)

    def bt_in_possession(self, instance):
        num = 0
        for player in self.team2:
            if player != self.team2[1]:
                if player.pos[1] < self.ball.pos[1]:
                    player.pos = (player.pos[0],player.pos[1]+20)
                    num += 1
                elif player.pos[1] > self.ball.pos[1]:
                    player.pos = (player.pos[0],player.pos[1]-20)
                    num += 1
                elif player.pos[0] > self.ball.pos[0]:
                    player.pos = (player.pos[0]-20,player.pos[1])
                    num += 1
                else:
                    player.pos = (player.pos[0]+20,player.pos[1])
                    num += 1
                if player == self.team2[1] and player.pos[0] > 10:
                    player.pos = (player.pos[0]-10,player.pos[1])
        
        for player in self.team2:
            if player.pos[0] > 1555:
                player.pos = (1525,player.pos[1])
            elif player.pos[0] < 5:
                player.pos = (50,player.pos[1])
            elif player.pos[1] > 1150:
                player.pos = (player.pos[0],1125)
            elif self.ball.pos[1] < 5:
                player.pos = (player.pos[0],50)  

            self.collision()
            self.check_goal()
            self.boundaries()
        if num == 0:
            self.possession = 0
    
    def move_bt(self, instance):
        num = 0
        for player in self.team2:
            num +=1
            if player == self.team2[1]:
                if player.pos[1] < self.ball.pos[1]:
                    player.pos = (player.pos[0],player.pos[1]+20) 
                elif player.pos[1] > self.ball.pos[1]:
                    player.pos = (player.pos[0],player.pos[1]-20)
            elif player == self.team2[self.control]:
                if player.pos[0] < self.ball.pos[0]:
                    player.pos = (player.pos[0]+20,player.pos[1]) 
                elif player.pos[0] > self.ball.pos[0]:
                    player.pos = (player.pos[0]-20,player.pos[1])
                if player.pos[1] < self.ball.pos[1]:
                    player.pos = (player.pos[0],player.pos[1]+20) 
                elif player.pos[1] > self.ball.pos[1]:
                    player.pos = (player.pos[0],player.pos[1]-20)
            else:
                if player.pos[0] < self.team1[num-1].pos[0]:
                    player.pos = (player.pos[0]+20,player.pos[1])
                elif player.pos[0] > self.team1[num-1].pos[0]:
                    player.pos = (player.pos[0]-20,player.pos[1])
                if player.pos[1] < self.team1[num-1].pos[1]:
                    player.pos = (player.pos[0],player.pos[1]+20) 
                elif player.pos[1] > self.team1[num-1].pos[1]:
                    player.pos = (player.pos[0],player.pos[1]-20)
        for player in self.team2:
            if player.pos[0] > 1555:
                player.pos = (1525,player.pos[1])
            elif player.pos[0] < 5:
                player.pos = (50,player.pos[1])
            elif player.pos[1] > 1150:
                player.pos = (player.pos[0],1125)
            elif self.ball.pos[1] < 5:
                player.pos = (player.pos[0],50)  
            self.collision()
            self.check_goal()
            self.boundaries()
        
    def ask_question(self):
        self.question_maker()
        self._keyboard.unbind(on_key_down=self._on_key_down)
        Clock.unschedule(self.choice)
        Clock.unschedule(self.team_move)
        self.distance = math.sqrt((self.ball.pos[0]-self.team1[self.control].pos[0])**2 + (self.ball.pos[1]-self.team1[self.control].pos[1])**2)
        self.values = time.time()
        self.question = random.choice(self.database)
        self.answer = self.question.split("*")
        self.answer = int(self.answer[0])*int(self.answer[1])
        content = BoxLayout(orientation='vertical', padding=20)
        name_label = Label(text=self.question)
        content.add_widget(name_label)
        self.name = TextInput(multiline=True)
        content.add_widget(self.name)
        self.submit = Button(text="Submit", on_press=self.check_answer)
        self.submit.bind(on_press=self.check_answer)
        content.add_widget(self.submit)

        self.popup = Popup(title="Question", content=content, size_hint=(None, None), size=(800, 400))
        self.popup.bind(on_dismiss=self.reschedule_function)
        self.popup.open()

    def reschedule_function(self, instance):
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        Clock.schedule_interval(self.choice, 0.5)
        Clock.schedule_interval(self.team_move, 0.5)
    
    def check_answer(self, instance):
        test_num = 0
        words = str(self.name.text).split()
        for word in words:
            if not word.isdigit():
                test_num += 1
        if test_num == 0 and not self.name.text == "":
            self.answer = self.question.split("*")
            field = "Field" + str(self.answer[1])
            c.execute("SELECT "+field+" FROM "+username+" WHERE Indexes = ?",(self.answer[0], ))
            value = c.fetchall()
            conn.commit()
            value = value[0][0]
            mean_distance = 0
            for players in self.team1:
                mean_distance += math.sqrt((self.ball.pos[0]-players.pos[0])**2 + (self.ball.pos[1]-players.pos[1])**2)
            mean_distance = mean_distance / 5
            if mean_distance < 0:
                mean_distance = mean_distance * -1

            mean_distances = 0
            for players in self.team2:
                mean_distances += math.sqrt((self.ball.pos[0]-players.pos[0])**2 + (self.ball.pos[1]-players.pos[1])**2)
            mean_distances = mean_distances / 5

            if mean_distances < 0:
                mean_distances = mean_distances * -1
            mean_distance -= mean_distances

            if mean_distance < 0:
                mean_distance = mean_distance * -1
            self.compare_answer = int(self.answer[0]) * int(self.answer[1])
            if int(self.name.text) == self.compare_answer:
                value += mean_distance / (time.time() - self.values)
                value = str(value)
                c.execute("UPDATE "+username+" SET "+field+" = "+value+" WHERE Indexes = ?",(self.answer[0], ))
                conn.commit()
                self.popup.dismiss()
                if self.move == 1:
                    self.ball.pos = (self.ball.pos[0],self.ball.pos[1]+200)
                if self.move == 4:
                    self.ball.pos = (self.ball.pos[0]+200,self.ball.pos[1])
                if self.move == 2:
                    self.ball.pos = (self.ball.pos[0],self.ball.pos[1]-200)
                if self.move == 3:
                    self.ball.pos = (self.ball.pos[0]-200,self.ball.pos[1])
            else:
                value -= (time.time() - self.values) / (mean_distance)
                value = str(value)
                c.execute("UPDATE "+username+" SET "+field+" = "+value+" WHERE Indexes = ?",(self.answer[0], ))
                self.database = []
                self.question_maker()
                conn.commit()
                self.move_bt(instance)

        c.execute("SELECT * FROM "+username)
        t = c.fetchall()
        conn.commit()
        total = 0
        for value in t[0]:
            total += value
        print(total)

        self.reschedule_function(instance)
        self.popup.dismiss()
        self.database.remove(self.question)
        self.check_goal()
        self.boundaries()

    def team_move(self, instance):
        num = 0
        if self.possession == 1:
            for player in self.team1:
                num +=1
                if player == self.team1[1]:
                    if player.pos[1] < self.ball.pos[1]:
                        player.pos = (player.pos[0],player.pos[1]+20) 
                    elif player.pos[1] > self.ball.pos[1]:
                        player.pos = (player.pos[0],player.pos[1]-20)
                elif player != self.team1[self.control]:
                    if player.pos[0] < self.team2[num-1].pos[0]:
                        player.pos = (player.pos[0]+20,player.pos[1])
                    elif player.pos[0] > self.team2[num-1].pos[0]:
                        player.pos = (player.pos[0]-20,player.pos[1])
                    if player.pos[1] < self.team2[num-1].pos[1]:
                        player.pos = (player.pos[0],player.pos[1]+20) 
                    elif player.pos[1] > self.team2[num-1].pos[1]:
                        player.pos = (player.pos[0],player.pos[1]-20)
        else:
            for player in self.team1:
                if player != self.team1[self.control] and player != self.team1[1]:
                    self.distance = math.sqrt((self.team1[self.control].pos[0]-player.pos[0])**2 + (self.team1[self.control].pos[1]-player.pos[1])**2)
                    if self.distance > 300:
                        if self.ball.pos[1] > player.pos[1] and player.pos[1] < 1300:
                            player.pos = (player.pos[0],player.pos[1]+20)
                        elif self.ball.pos[1] < player.pos[1]  and player.pos[1] > 300:
                            player.pos = (player.pos[0],player.pos[1]-20)
                        elif self.ball.pos[0] < player.pos[0]  and player.pos[0] > 300:
                            player.pos = (player.pos[0]-20,player.pos[1])
                        elif self.ball.pos[0] > player.pos[0] and player.pos[0] < 1300:
                            player.pos = (player.pos[0]+20,player.pos[1])
                elif player != self.team1[self.control]:
                    if self.team1[1].pos[1] < self.ball.pos[1]:
                        self.team1[1].pos = (self.team1[1].pos[0],self.team1[1].pos[1]+20)
                    elif self.team1[1].pos[1] > self.ball.pos[1]:
                        self.team1[1].pos = (self.team1[1].pos[0],self.team1[1].pos[1]-20)
        if self.team1[1].pos[0] > 10 and self.team1[1] != self.team1[self.control]:
            self.team1[1].pos = (self.team1[1].pos[0]-10,self.team1[1].pos[1])

        for player in self.team1:
            if player.pos[0] > 1555:
                player.pos = (1525,player.pos[1])
            elif player.pos[0] < 5:
                player.pos = (50,player.pos[1])
            elif player.pos[1] > 1150:
                player.pos = (player.pos[0],1125)
            elif self.ball.pos[1] < 5:
                player.pos = (player.pos[0],50)        
                    
    def check_goal(self):
        if self.ball.pos[0] < 5 and self.ball.pos[1] > 400 and self.ball.pos[1] < 700:
            self.bgoals += 1
            self.ball.pos = (775,600)
            self.team1[self.control].source = "shirt_red.png"
            self.control = 0
            self.possession = 0
            self.team1[self.control].source = "shirt_green.png"
            self.formation()
            self.score.source = str(self.bgoals)+str(self.rgoals)+".png"

        elif self.ball.pos[0] > 1555 and self.ball.pos[1] > 400 and self.ball.pos[1] < 700:
            self.rgoals += 1
            self.ball.pos = (775,600)
            self.possession = 1
            self.formation()
            self.score.source = str(self.bgoals)+str(self.rgoals)+".png"
        if self.rgoals == 3 or self.bgoals == 3:
            Clock.unschedule(self.choice)
            Clock.unschedule(self.team_move)
            self._keyboard.unbind(on_key_down=self._on_key_down)
            if self.rgoals == 3:
                # increases your win tally if you score a goal
                c.execute("SELECT Wins FROM U_P WHERE Usernames = ?",(username, ))
                win = c.fetchall()
                win = win[0][0] + 1
                c.execute("UPDATE U_P SET wins = "+str(win)+" WHERE Usernames = ?",(username, ))
                conn.commit()
                name_label = Label(text="Congratulations!")
            else:
                name_label = Label(text="Unlucky, Better luck next time!")
            content = BoxLayout(orientation='vertical', padding=20)
            content.add_widget(name_label)
            self.popup = Popup(title="",content=content, size_hint=(None, None), size=(800, 400))
            self.popup.open()
            self.canvas.clear()
            Home_page().run()

    def formation(self):
        self.team1[0].pos = (800,550)
        self.team1[1].pos = (10,550)
        self.team1[2].pos = (250,300)
        self.team1[3].pos = (250,800)
        self.team1[4].pos = (400,550)

        self.team2[0].pos = (1100,550)
        self.team2[1].pos = (1500,550)
        self.team2[2].pos = (1250,300)
        self.team2[3].pos = (1250,800)
        self.team2[4].pos = (1100,550)

    def boundaries(self):
        if self.ball.pos[0] > 1555:
            self.ball.pos = (1525,self.ball.pos[1])
            self.formation()
            self.team2[self.control].pos = (1550,self.ball.pos[1])
            self.possession = 1
        elif self.ball.pos[0] < 5:
            self.ball.pos = (75,700)
            self.formation()
            self.team1[self.control].source = "shirt_red.png"
            self.control = 1
            self.move = 4
            self.possession = 0
            self.team1[1].pos = (50,self.ball.pos[1])
            self.team1[self.control].source = "shirt_green.png"
        elif self.ball.pos[1] > 1150:
            self.ball.pos = (self.ball.pos[0],1125)
            self.formation()
            if self.possession == 0:
                self.move = 2
                self.possession = 1
                self.team2[self.control].pos = (self.ball.pos[0],1150)
            else:
                self.possession = 0
                self.team1[self.control].pos = (self.ball.pos[0],1150)
        elif self.ball.pos[1] < 5:
            self.ball.pos = (self.ball.pos[0],50)
            self.formation()
            if self.possession == 0:
                self.move = 1
                self.team1[self.control].pos = (self.ball.pos[0],25)
            else:
                self.team2[self.control].pos = (self.ball.pos[0],25)
    
    def collision(self):
        self.distance = math.sqrt((self.ball.pos[0]-self.team1[self.control].pos[0])**2 + (self.ball.pos[1]-self.team1[self.control].pos[1])**2)
        if self.distance < 100:
            if (self.ball.pos[1]-self.team1[self.control].pos[1]) > 50:
                self.ball.pos = (self.ball.pos[0],self.ball.pos[1]+100)
            elif (self.ball.pos[0]-self.team1[self.control].pos[0]) > 0:
                self.ball.pos = (self.ball.pos[0]+100,self.ball.pos[1])
            elif (self.ball.pos[1]-self.team1[self.control].pos[1]) < -50:
                self.ball.pos = (self.ball.pos[0],self.ball.pos[1]-100)
            elif (self.ball.pos[0]-self.team1[self.control].pos[0]) < 0:
                self.ball.pos = (self.ball.pos[0]-100,self.ball.pos[1])
            self.possession = 0

        self.distance = math.sqrt((self.ball.pos[0]-self.team1[1].pos[0])**2 + (self.ball.pos[1]-self.team1[1].pos[1])**2)
        if self.distance < 100:
            if (self.ball.pos[1]-self.team1[1].pos[1]) > 50:
                self.ball.pos = (self.ball.pos[0],self.ball.pos[1]+100)
            elif (self.ball.pos[0]-self.team1[1].pos[0]) > 0:
                self.ball.pos = (self.ball.pos[0]+100,self.ball.pos[1])
            elif (self.ball.pos[1]-self.team1[1].pos[1]) < -50:
                self.ball.pos = (self.ball.pos[0],self.ball.pos[1]-100)
            elif (self.ball.pos[0]-self.team1[1].pos[0]) < 0:
                self.ball.pos = (self.ball.pos[0]-100,self.ball.pos[1])
            self.possession = 0

        self.distance = math.sqrt((self.ball.pos[0]-self.team2[self.control].pos[0])**2 + (self.ball.pos[1]-self.team2[self.control].pos[1])**2)
        if self.distance < 100:
            if (self.ball.pos[1]-self.team2[self.control].pos[1]) > 0:
                self.ball.pos = (self.ball.pos[0],self.ball.pos[1]+100)
            elif (self.ball.pos[0]-self.team2[self.control].pos[0]) > 0:
                self.ball.pos = (self.ball.pos[0]+100,self.ball.pos[1])
            elif (self.ball.pos[1]-self.team2[self.control].pos[1]) < 0:
                self.ball.pos = (self.ball.pos[0],self.ball.pos[1]-100)
            elif (self.ball.pos[0]-self.team2[self.control].pos[0]) < 0:
                self.ball.pos = (self.ball.pos[0]-100,self.ball.pos[1])
            self.possession = 1

        self.distance = math.sqrt((self.ball.pos[0]-self.team2[1].pos[0])**2 + (self.ball.pos[1]-self.team2[1].pos[1])**2)
        if self.distance < 100:
            if (self.ball.pos[1]-self.team2[1].pos[1]) > 0:
                self.ball.pos = (self.ball.pos[0],self.ball.pos[1]+100)
            elif (self.ball.pos[0]-self.team2[1].pos[0]) > 0:
                self.ball.pos = (self.ball.pos[0]+100,self.ball.pos[1])
            elif (self.ball.pos[1]-self.team2[1].pos[1]) < 0:
                self.ball.pos = (self.ball.pos[0],self.ball.pos[1]-100)
            elif (self.ball.pos[0]-self.team2[1].pos[0]) < 0:
                self.ball.pos = (self.ball.pos[0]-100,self.ball.pos[1])
            self.possession = 1             

    def question_maker(self):
        c.execute("SELECT * FROM "+username)
        self.data = c.fetchall()
        conn.commit()   
        self.counter = 0
        self.counter2 = 0
        self.base = self.data[1][1]
        self.database = []
        self.counter = 0
        for parts in self.data:
            self.counter2 = 0
            self.counter += 1
            for part in parts:
                if part != self.data[self.counter-1][0]:
                    self.counter2 += 1
                    if part < self.base:
                        self.base = part
                        self.question = str(self.counter)+"*"+str(self.counter2)
                        self.database = []
                        self.database.append(self.question)
                    elif part == self.base:
                        self.base = part
                        self.question = str(self.counter)+"*"+str(self.counter2)
                        self.database.append(self.question)

class Login_page(GridLayout):
    def __init__(self, **kwargs):
        self.cols = 2
        self.fullscreen = True
        self.closeable = False

        super(Login_page, self).__init__(**kwargs)
        self.add_widget(Label(text="",size_hint_y=None, height=150))
        self.add_widget(Label(text="",size_hint_y=None, height=150))
        self.add_widget(Label(text="Username:",font_size=72,color= (0.8,0,0,1),bold=True, size_hint_y=None, height=100))
        self.username = TextInput(multiline=False,font_size=64,background_color=(0,0,0.8,1), foreground_color=(1,1,1,1),size_hint_y=None, height=100, halign="center")
        self.add_widget(self.username)
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="Password:",font_size=72,color= (0.8,0,0,1),bold=True, size_hint_y=None, height=100))
        self.password = TextInput(multiline=False,font_size=64,background_color=(0,0,0.8,1),foreground_color=(1,1,1,1) ,size_hint_y=None, height=100, halign="center",password=True)
        self.add_widget(self.password)
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.Button3 = Button(text="forgot password",font_size=36,background_color=(0,0.8,0,0),height=50,on_press=self.pressed,halign="left",valign="center",underline=True, size_hint_y=None)
        self.add_widget(self.Button3)
        self.add_widget(Label(text="",size_hint_y=None, height=50))
        self.add_widget(Label(text="",size_hint_y=None, height=225))
        self.add_widget(Label(text="",size_hint_y=None, height=225))
        self.Button1 = Button(text="Submit",font_size=72,background_color=(0,0.8,0,1),height=50)
        self.Button1.bind(on_press=self.press)
        self.add_widget(self.Button1)
        self.Button2 = Button(text="Sign Up",font_size=72,background_color=(0,0.8,0,1),height=50,on_press=self.presses)
        self.Button2.bind(on_press=self.presses)
        self.add_widget(self.Button2)

    def pressed(self,instance):
        self.clear_widgets()
        Forgot_Password().run()

    def press(self, instance):
        global username
        c.execute("SELECT Usernames FROM U_P")
        u = False
        p = False
        Usernames = c.fetchall()
        conn.commit()
        counter = 0
        while counter < len(Usernames):
            if self.username.text.lower() == Usernames[counter][0]:
                username = self.username.text.lower()
                c.execute("SELECT Passwords FROM U_P WHERE Usernames = ?",(username, ))
                Passwords = c.fetchall()
                u = True
                if Passwords[0][0] == self.password.text:
                    p = True
                    self.clear_widgets()
                    Home_page().run()
                counter = len(Usernames)
            else: 
                counter += 1
        if u == False:
            self.username.text = ""
            self.password.text = ""
        elif p == False:
            self.password.text = ""

    def presses(self, instance):
        self.clear_widgets()
        Sign_Up().run()

class Sign_up(GridLayout):
    def __init__(self, **kwargs):
        self.cols = 2
        super(Sign_up, self).__init__(**kwargs)
        self.fullscreen = True
        self.closeable = False
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="Username:",font_size=72,color= (0.8,0,0,1),bold=True, size_hint_y=None, height=100))
        self.username = TextInput(multiline=False,font_size=64,background_color=(0,0,0.8,1), foreground_color=(1,1,1,1),size_hint_y=None, height=100, halign="center")
        self.add_widget(self.username)
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="Password:",font_size=72,color= (0.8,0,0,1),bold=True, size_hint_y=None, height=100))
        self.password = TextInput(multiline=False,font_size=64,background_color=(0,0,0.8,1),foreground_color=(1,1,1,1) ,size_hint_y=None, height=100, halign="center",password=True)
        self.add_widget(self.password)
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="",size_hint_y=None, height=100))
        self.add_widget(Label(text="Confirm Password:",font_size=72,color= (0.8,0,0,1),bold=True, size_hint_y=None, height=100))
        self.cpassword = TextInput(multiline=False,font_size=64,background_color=(0,0,0.8,1),foreground_color=(1,1,1,1) ,size_hint_y=None, height=100, halign="center",password=True)
        self.add_widget(self.cpassword)
        self.words = Label(text="Usernames must start with a letter and need to be:\nminimum 4 letters or numbers (no special characters)\nand a maxium of 12 characters",size_hint_y=None, height=200,color=(0.8,0,0,1))
        self.add_widget(self.words)
        self.add_widget(Label(text="Passwords need to be minimum 4 characters\nand a maxium of 12 characters\nwith at least one number or special character",size_hint_y=None, height=200,color=(.8,0,0,1)))
        self.Button1 = Button(text="Sign Up",font_size=72,background_color=(0,0.8,0,1),height=100)
        self.Button1.bind(on_press=self.SP)
        self.add_widget(self.Button1)
        self.Button2 = Button(text="Back to Login",font_size=72,background_color=(0,0.8,0,1),height=100,on_press=self.presses)
        self.Button2.bind(on_press=self.BTL)
        self.add_widget(self.Button2)

    def presses(self, instance):
        Sign_Up().run()

    def SP(self, instance):
        characters = 0
        c.execute("SELECT Usernames FROM U_P")
        Usernames = c.fetchall()
        conn.commit()
        counter1 = 0
        for letters in self.password.text:
            SCS = '[@_!#$%^&*()<>?/\|}{~:]'
            if letters.isnumeric() or letters in SCS:
                characters += 1
        if 12 >= len(self.username.text) >= 4 and self.username.text.isalnum() and self.username.text[0].isalpha():
            if 12 >= len(self.password.text) >= 4 and characters > 0:
                for users in Usernames:
                    if self.username.text == users[0]:
                        counter1 += 1
                if counter1 == 0:
                    if self.password.text == self.cpassword.text:
                        c.execute("INSERT INTO U_P (Usernames, Passwords, Wins)  VALUES (?, ?, ?)",(self.username.text.lower(), self.password.text, 0, ))
                        conn.commit()
                        c.execute("CREATE TABLE `" + self.username.text.lower() + "`(indexes INT,Field1 INT,Field2 INT,Field3 INT,Field4 INT,Field5 INT,Field6 INT,Field7 INT,Field8 INT,Field9 INT,Field10 INT); ")
                        conn.commit()
                        for count in range(1,11):
                            c.execute("INSERT INTO `"+self.username.text.lower()+"` (indexes, Field1, Field2, Field3, Field4, Field5,Field6, Field7 , Field8, Field9 , Field10)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(count, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ))
                            conn.commit()
                        content = BoxLayout(orientation='vertical', padding=20)
                        name_label = Label(text="Login successful")
                        content.add_widget(name_label)
                        self.popup = Popup(title="Login", content=content, size_hint=(None, None), size=(800, 400))
                        self.popup.open()
                        self.clear_widgets()
                        Login().run()

                    else:
                        self.password.text = ""
                        self.cpassword.text = ""
                else:
                    self.words.text = "Username already exists"
                    self.username.text = ""
                    self.password.text = ""
                    self.cpassword.text = ""
            else:
                content = BoxLayout(orientation='vertical', padding=20)
                name_label = Label(text="Invalid password")
                content.add_widget(name_label)
                self.popup = Popup(title="Login", content=content, size_hint=(None, None), size=(800, 400))
                self.popup.open()
                self.password.text = ""
                self.cpassword.text = ""             
        else:
            self.words.text = "Usernames must start with a letter and need to be:\nminimum 4 letters or numbers (no special characters)"
            content = BoxLayout(orientation='vertical', padding=20)
            name_label = Label(text="Invalid username")
            content.add_widget(name_label)
            self.popup = Popup(title="Sign up", content=content, size_hint=(None, None), size=(800, 400))
            self.popup.open()
            self.username.text = ""
            self.password.text = ""
            self.cpassword.text = ""

    def BTL(self, instance):
        self.clear_widgets()
        Login().run()

if __name__ == '__main__':
    #Forgot_Password().run()
    #Home_page().run()
    #Rules().run()
    #Game().run()
    #Sign_Up.run()
    Login().run()