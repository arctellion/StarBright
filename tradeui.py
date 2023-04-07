import kivy
import re
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty
import travtools.commerce as cm


# class UwpInput(TextInput):
#     #[a-zA-Z](?:[a-zA-Z0-9]){6}-[a-zA-Z0-9]
#     #pat = re.compile('[a-zA-Z](?:[a-zA-Z0-9]){6}-[a-zA-Z0-9]')
#   #pat = [ABCDEXFGHY][0-9A-F][0-9A-F][0-9A][0-9A-F][0-9A-F][0-9A-J]-[0-9A-J]

#class MyUI(Widget):
class MyUI(TabbedPanel):
    uwp = ObjectProperty(None)
    steward = ObjectProperty(None)
    admin = ObjectProperty(None)
    street = ObjectProperty(None)
    liaison = ObjectProperty(None)
    days = ObjectProperty(None)
    status = ObjectProperty(None)
    cargostatus = ObjectProperty(None)
    cargo = ObjectProperty(None)
    broker = ObjectProperty(None)
    uwpsell = ObjectProperty(None)
    trade = ObjectProperty(None)
    uwp_pat = re.compile('[ABCDEXFGHY][0-9A-F][0-9A-F][0-9A][0-9A-F][0-9A-F][0-9A-J]-[0-9A-J]')
    skills = {}
    trade = ""
    value = 0

    # Goes inside MyGrid Class
    def buy(self):
        self.status.text = ""
        if self.uwp.text == "":
            self.status.text = "No UWP Provided."
        elif len(self.uwp.text) != 9: 
            self.status.text = "Incorrect length UWP, should be 9 characters long."
        elif not self.uwp_pat.match(self.uwp.text):
            self.status.text = "Incorrect UWP pattern."
        else:
            try: 
                self.skills = {'Steward':int(self.steward.text), 'Admin':int(self.admin.text), 'Streetwise':int(self.street.text), 'Liaison':int(self.liaison.text)}
            except ValueError as e: 
                self.status.text = "Incorrect Skill Value."
                self.steward.text = "0"
                self.admin.text = "0"
                self.street.text = "0"
                self.liaison.text = "0"
                self.days.text = "7"
        print("UWP: ", self.uwp.text, "\nSkills: ", self.skills,"\nDays Looked: ", self.days.text)
        try:
# g=cm.trade_gds("A110877-E",{'Steward':1, 'Admin':2, 'Streetwise':1, 'Liaison':2}, 2)
            self.trade = cm.trade_gds(self.uwp.text, self.skills, int(self.days.text))
        except (ValueError, KeyError) as e:
            pass
        if self.trade:
            self.status.text = self.trade
            # print(self.trade)
        
    def sell(self):
        self.cargostatus.text=""
        if self.cargo.text == "":
            self.cargostatus.text = "No Cargo Code entered."
        elif len(self.uwpsell.text) != 9:
            self.cargostatus.text = "Incorrect length of UWP, should be 9 characters long."
        elif not self.uwp_pat.match(self.uwpsell.text):
            self.status.text = "Incorrect UWP Pattern."
        #g = cm.sell_price("B - Ri Cr5,100","B787AA9-E",8,4)
        try:
            trd = int(self.trade.text)
        except ValueError as e:
            trd = 0
        self.value = cm.sell_price(self.cargo.text,self.uwpsell.text, int(self.broker.text), trd)
        if self.value > 0:
            self.cargostatus.text = "Sell Price: Cr{:,}".format(self.value)
            #print("Sell Price:  Cr{:,}".format(slef.value))

class TradeUiApp(App): # <- Main Class
    def build(self):
        return MyUI()

if __name__ == '__main__':
    TradeUiApp().run()
