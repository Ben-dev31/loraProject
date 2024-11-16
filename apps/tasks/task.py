
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout
    
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

from kivy.uix.popup import Popup


Builder.load_file("templates/task.kv")

class TaskBox(MDCard):
    
    Title = StringProperty("Cours")
    Date = StringProperty("Lund 12/11/24")
    Location = StringProperty("15:30")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

class Dialog:
    def __init__(self) -> None:
        
        self.dataStak = [["Donner un nom à cette tâche",''],
                    ["Choisisez une date ",''],
                    ["Choisisez une heure",''],
                    ["Ajouter un lieu",''],
                    ["Un détail ?",'']
                    ]
        
        self.stat = 0
        
    
    def create_Dialog(self):
        pop = Popup(title="New Task", size_hint= (.7, .5))
        pop.auto_dismiss = True
        
        self.box = MDRelativeLayout()
        self.label = MDLabel(
            text = self.dataStak[self.stat][0],
            color="white",
            pos_hint={'center_x': 0.5,'center_y': 0.9}
            )
        self.textinput = MDTextField(
            multiline=False,
            mode = "rectangle",
            text_color_normal= "green",
            text= self.dataStak[self.stat][1],
            pos_hint={'center_x': 0.5,'center_y': 0.5}
            )
        
        previous_bt = MDRaisedButton(
            text="Back",
            pos_hint={'center_x': 0.2,'center_y': 0.2},
            on_press = lambda x:self.previous(x)
        )
        self.next_bt = MDRaisedButton(
            text="Next",
            pos_hint={'center_x': 0.5,'center_y': 0.2},
            on_press = lambda x:self.next(x)
        )
        cancel_bt = MDRaisedButton(
            text="Cancel",
            pos_hint={'center_x': 0.8,'center_y': 0.2},
            on_press = lambda x: pop.dismiss()
        )
        
        self.box.add_widget(self.label)
        self.box.add_widget(self.textinput)
        self.box.add_widget(previous_bt)
        self.box.add_widget(self.next_bt)
        self.box.add_widget(cancel_bt)
        
        pop.add_widget(self.box)
        pop.open()
    
    def previous(self,x):
        if self.stat > 0:
            self.stat -= 1
            self.label.text = self.dataStak[self.stat][0]
            self.textinput.text = self.dataStak[self.stat][1]
    
    def next(self,x):
        self.dataStak[self.stat][1] = self.textinput.text
        self.stat += 1
        if self.stat < len(self.dataStak)-1:
            self.label.text = self.dataStak[self.stat][0]
            self.textinput.text = self.dataStak[self.stat][1]

        else:
            self.next_bt.text = "Ok"
            
            
    

class TaskHome(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def newTask(self):
        dialog = Dialog()
        dialog.create_Dialog()

class Task(MDApp):

    def build(self):

        return TaskHome()


if __name__=="__main__":
    Task().run()