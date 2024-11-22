

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton

from kivymd.app import MDApp


Builder.load_file("templates/sheet.kv")

class SheetTable(MDBoxLayout):
    Dimension = ListProperty([3,3]) # rows cols nombers
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = True
        self.orientation = "vertical"
        self.spacing = dp(20)
        self.padding = dp(10)
        
        self.data_table = []
        
    def on_parent(self,widget, parent):

        if self.login:
            self.load()
            
        self.login = not self.login

    def load(self, dim = []):
        self.clear_widgets()
        if len(dim) != 0:
            self.Dimension = dim 
            
        self.header_box = MDGridLayout(
            rows = 1,
            spacing = dp(10)
        )
        self.body_box = MDGridLayout(spacing = dp(10))
        
        self.header_box.cols = self.Dimension[1]
        self.body_box.rows = self.Dimension[0]
        self.body_box.cols = self.Dimension[1]
        
        for i in range(self.Dimension[1]):
            hd = MDTextField(
                    mode = "rectangle",
                    hint_text= f"col {i}"
                )
            self.data_table.append([hd])
            self.header_box.add_widget(hd)
            
            
        for k in range(self.Dimension[0]):
            for j in range(self.Dimension[1]):
                hb = MDTextField(
                        mode = "rectangle"
                    )
                self.data_table[j].append(hb)
                self.body_box.add_widget(hb)
                
        self.add_widget(self.header_box)
        self.add_widget(self.body_box)
        self.header_box.adaptive_height = True
        self.body_box.adaptive_height = True
        self.adaptive_height = True
            
    def get_data(self):
        datas = []
        for table in self.data_table:
            col = []
            for el in table:
                col.append(el.text)
            datas.append(col)
        
        return datas
    
    def add_col(self):
        self.Dimension[-1] += 1
        self.header_box.cols = self.Dimension[1]
        self.body_box.cols = self.Dimension[1]
        
        hd = MDTextField(
                mode = "rectangle",
                hint_text= f"col {self.Dimension[-1]-1}"
            )
        self.data_table.append([hd])
        self.header_box.add_widget(hd)
        
        for k in range(self.Dimension[0]):
            hb = MDTextField(
                    mode = "rectangle"
                )
            self.data_table[-1].append(hb)
            self.body_box.add_widget(hb)
        
    def remove_col(self):
        for el in self.data_table[-1][1:]:
            self.body_box.clear_widgets([el])
 
        self.header_box.clear_widgets([self.data_table[-1][0]])
        self.data_table.remove(self.data_table[-1])
        self.Dimension[1] -= 1
        self.header_box.cols = self.Dimension[1]
        self.body_box.cols = self.Dimension[1]
    
    def add_row(self):
        self.Dimension[0] += 1
        self.body_box.rows = self.Dimension[0]
        
        for k in range(self.Dimension[1]):
            hb = MDTextField(
                    mode = "rectangle"
                )
            self.data_table[k].append(hb)
            self.body_box.add_widget(hb)
        
    def remove_row(self):
        for k in range(self.Dimension[1]):
            self.body_box.clear_widgets([self.data_table[k][-1]])
            self.data_table[k].remove(self.data_table[k][-1])
        self.Dimension[0] -= 1
        
class SheetInputDataScreen(MDScreen):
    Dimension = ListProperty([3,4]) # rows cols nombers
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def on_parent(self, widget, parent):
    #     self.ids["sheet_table"].load(dim = self.Dimension)
        
    def back_screen(self):
        pass
    
    def save_content(self):
        sheet = self.ids['sheet_table']
        data = sheet.get_data()
        
        print(data)
    
    def menu(self):
        pass
    
    def add_col(self):
        self.ids["sheet_table"].add_col()
        
    def remove_col(self):
        self.ids["sheet_table"].remove_col()
    
    def add_row(self):
        self.ids["sheet_table"].add_row()
        
    def remove_row(self):
        self.ids["sheet_table"].remove_row()

class SheetApp(MDApp):
    AppName = StringProperty("Sheet")
    
    def build(self):
        return SheetInputDataScreen()


if __name__ == "__main__":
    
    SheetApp().run()