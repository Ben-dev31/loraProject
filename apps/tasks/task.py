
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem


from kivy.uix.popup import Popup


import datetime

Builder.load_file("templates/task.kv")

class TaskBox(MDCard):
    
    Title = StringProperty("Cours")
    Date = StringProperty("Lund 12/11/24")
    Time = StringProperty("15:30")
    Detail = StringProperty("appel")
    Location = StringProperty("Ecole")
    Frequence = StringProperty("une foie")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def menu_open(self,x):
        menu_items = [
            {
                "text": "Option",
                "on_release": lambda x="option": self.option_callback(x),
            },
            {
                "text": "Supprimé",
                "leading_icon": "delete",
                "leading_icon_color": "red",
                "on_release": lambda x="supprimé": self.delete_callback(x),
            } 
        ]
        self.dropMenu = MDDropdownMenu(
            caller=x, items=menu_items
        )
        self.dropMenu.open()
        
    
    def delete_callback(self, x):
        self.dropMenu.dismiss()
    
    def option_callback(self, x):
        self.dropMenu.dismiss()
        
        
        self.pop = Popup(size_hint = (0.4, .4), title="Parametre")
        self.pop.background_color = [0,0,0,.5]
        
        box = MDRelativeLayout()
        
        item = MDDropDownItem(
            pos_hint = {"center_x": .5, "top": .9},
            on_release = lambda x: self.option_choice(x)
        )
        item.text = "Une foie"
        
        bt = MDRaisedButton(
            text="Valider",
            pos_hint = {"center_x": .5, "center_y": .3},
            on_release = lambda x: self.validate(item)
        )
        
        box.add_widget(item)
        box.add_widget(bt)
        
        self.pop.add_widget(box)
        self.pop.open()
    
    def option_choice(self, x):
        menu_items = [
            {
                "text": "Une foie",
                "on_release": lambda t="Une foie": self.optcallback(x,t)
            },
            {
                "text": "chaque jour",
                "on_release": lambda t="chaque jour": self.optcallback(x,t)
            },
            {
                "text": "chaque semaine",
                "on_release": lambda t="chaque semaine": self.optcallback(x,t)
            },
            {
                "text": "Tous les mois",
                "on_release": lambda t="Tous les mois": self.optcallback(x,t)
            } 
        ]
        
        
        self.dropdown = MDDropdownMenu(caller=x, items=menu_items)
        self.dropdown.open()
    
    def optcallback(self,x,value):
        x.text = value 
        self.dropdown.dismiss()
    
    def validate(self, x):
        self.Frequence = x.text
        self.pop.dismiss()
        

class TaskHome(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.dataStak = [["Donner un nom à cette tâche",''],
                    ["Choisisez une date",''],
                    ["Choisisez une heure",''],
                    ["Ajouter un lieu",''],
                    ["Un détail ",'']
                    ]
        
        self.stat = 0
        
        self.tempStak =  self.dataStak

    def newTask(self):
        self.create_Dialog()
   
    def create_Dialog(self):
        self.pop = Popup(title="New Task", size_hint= (.7, .5))
        self.pop.auto_dismiss = True
        
        self.pop.background_color = [0,0,0,.5]
        
        boxs = MDBoxLayout(orientation = 'vertical')
        
        
        self.box = MDBoxLayout(orientation = 'vertical', spacing=5)
        
        self.box_bt = MDRelativeLayout()
        
        self.label = MDLabel(
            text = self.dataStak[self.stat][0],
            pos_hint={'center_x': 0.5,'center_y': 0.9}
            )
        
        self.label.color = "white"
        
        self.inpBox = MDBoxLayout(orientation = 'horizontal')
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
            on_press = lambda x: self.pop.dismiss()
        )
        self.inpBox.add_widget(self.textinput)
        
        self.box.add_widget(self.label)
        self.box.add_widget(self.inpBox)
        
        self.box_bt.add_widget(previous_bt)
        self.box_bt.add_widget(self.next_bt)
        self.box_bt.add_widget(cancel_bt)
        
        boxs.add_widget(self.box)
        boxs.add_widget(self.box_bt)
        
        self.pop.add_widget(boxs)
        self.pop.open()
    
    def previous(self,x):
        if self.stat > 0:
            self.stat -= 1
            self.label.text = self.dataStak[self.stat][0]
            self.textinput.text = self.dataStak[self.stat][1]
        
        if self.dataStak[self.stat][0].split()[-1].lower() == 'date':
            if len(self.inpBox.children) > 1:
                self.inpBox.clear_widgets([self.inpBox.children[0]])
            self.inpBox.add_widget(
                MDIconButton(
                    icon = 'calendar',
                    on_press = lambda x:self.show_date_picker(x)
                )
            )
        elif self.dataStak[self.stat][0].split()[-1].lower() == 'heure':
            if len(self.inpBox.children) > 1:
                self.inpBox.clear_widgets([self.inpBox.children[0]])
                
            self.inpBox.add_widget(
                MDIconButton(
                    icon = 'clock',
                    on_press = lambda x:self.show_time_picker(x)
                )
            )
           
    
    def next(self,x):
        if self.stat > len(self.dataStak)-1:
            return
        self.dataStak[self.stat][1] = self.textinput.text
        self.stat += 1
        if self.stat < len(self.dataStak):
            self.label.text = self.dataStak[self.stat][0]
            self.textinput.text = self.dataStak[self.stat][1]
            if self.dataStak[self.stat][0].split()[-1].lower() == 'date':
                if len(self.inpBox.children) > 1:
                    self.inpBox.clear_widgets([self.inpBox.children[0]])
                self.inpBox.add_widget(
                    MDIconButton(
                        icon = 'calendar',
                        on_press = lambda x:self.show_date_picker(x)
                    )
                )
            elif self.dataStak[self.stat][0].split()[-1].lower() == 'heure':
                if len(self.inpBox.children) > 1:
                    self.inpBox.clear_widgets([self.inpBox.children[0]])
                self.inpBox.add_widget(
                    MDIconButton(
                        icon = 'clock',
                        on_press = lambda x:self.show_time_picker(x)
                    )
                )
            else:
                if len(self.inpBox.children) > 1:
                    self.inpBox.clear_widgets([self.inpBox.children[0]])

        else:
            
            self.box.clear_widgets()
            
            i = 0
            for cat in self.dataStak:
                self.box.add_widget(
                    MDLabel(
                        text=f"[color=ffffff][b][size= 20sp]{cat[0].split()[-1].capitalize()}[/size] :[/b][/color]  [color=008080]{self.dataStak[i][1]}[/color]",
                        markup = True,
                        halign = "center"
                    )
                )
                i += 1
            
            self.next_bt.text = "Add"
            self.next_bt.unbind(on_press= lambda x : self.next(x))
            self.next_bt.bind(on_press = lambda x : self.create_new(x))
    
    def create_new(self,x):
        task = TaskBox(
            Title = self.dataStak[0][1],
            Date = self.dataStak[1][1],
            Time = self.dataStak[2][1],
            Detail = self.dataStak[4][1],
            Location = self.dataStak[3][1],
        )
        
        self.ids["tasks"].add_widget(task)
        self.pop.clear_widgets()
        self.pop.dismiss()
        self.stat = 0
        self.dataStak = self.tempStak
        
    def on_save_date(self, instance, value, date_range):
        date_value = datetime.datetime.strptime(str(value), "%Y-%m-%d")
        date_value_eu = date_value.strftime("%d/%m/%Y")
        self.textinput.text = str(date_value_eu)
    
    def on_save_time(self, instance, value):
        date_value = datetime.datetime.strptime(str(value), "%H:%M:%S")
        date_value_eu = date_value.strftime("%H:%M")
        self.textinput.text = str(date_value_eu)

    def show_date_picker(self,x):
       
        date_dialog = MDDatePicker()
        # You have to control the position of the date picker dialog yourself.
        date_dialog.bind(on_save=self.on_save_date, on_cancel=date_dialog.dismiss)
        date_dialog.open()
    
    def show_time_picker(self,x):
       
        date_dialog = MDTimePicker()
        # You have to control the position of the date picker dialog yourself.
        date_dialog.bind(on_save=self.on_save_time, on_cancel=date_dialog.dismiss)
        date_dialog.open()
    




class Task(MDApp):

    def build(self):

        return TaskHome()


if __name__=="__main__":
    Task().run()