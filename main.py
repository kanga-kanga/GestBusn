from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import BoxLayout, MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.textfield import MDTextField
from datetime import datetime
import os
import sqlite3


Window.size = (350, 600)
Window.set_icon("images/previous.png")

class MyApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"

        global sm
        sm = ScreenManager()
        sm.add_widget(PreApp(name = "preapp"))
        sm.add_widget(MainScreen(name = "main_screen"))
        sm.add_widget(AddClientScreen(name = "add_client"))

        return sm
    
    def on_start(self):
        Clock.schedule_once(self.mainscreen, 5)

    def mainscreen(self, *args):
        sm.current = "main_screen"


Builder.load_string("""
<PreApp>
    MDFloatLayout:
        #md_bg_color: "#00FFFF"
        Image:
            source:"images/previous.png"

    MDBoxLayout:
        orientation: "vertical"
        size_hint: 1, .1
        MDLabel:
            text: "from dieta startup"
            halign: "center"
            theme_text_color : "Custom"
            text_color: "#00FFFF"

""")

class PreApp(Screen):
    pass


class DatabaseClient():
    def __init__(self, database_name : str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS element (Nom_etablissement text , Adresse text, Numero_de_telephone integer, Quantite integer, Prix_de_ventes integer, Jour_de_depot text, Heure_de_depot text, Note text)")
        self.con.commit()
        cur.close()

    def add_new_client(self, Nom_etablissement, Adresse, Numero_de_telephone, quantite, prix_de_vente):
        cursor = self.con.cursor()
        query = f"INSERT INTO element (Nom_etablissement, Adresse, Numero_de_telephone, Quantite, Prix_de_ventes) VALUES (?, ?, ?, ?, ?);"
        cursor.execute(query, (Nom_etablissement, Adresse, Numero_de_telephone, quantite, prix_de_vente))
        self.con.commit()
        cursor.close()

    def update_client(self, Nom_etablissement, quantite, prix, Date, heure, note):
        cursor = self.con.cursor()
        query = f"UPDATE element SET Quantite = ?, Prix_de_ventes = ?,Jour_de_depot = ?, Heure_de_depot = ?, Note = ? WHERE Nom_etablissement = ? ;"
        cursor.execute(query, (Nom_etablissement, quantite, prix, Date, heure, note))
        self.con.commit()
        cursor.close()

    def view_products(self) :
        cursor = self.con.cursor()
        query = f"SELECT * FROM element"
        cursor.execute(query, ())
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def supprimer(self, nom):
        cursor = self.con.cursor()
        query = f"DELETE FROM element WHERE Nom_etablissement = ? ;"
        cursor.execute(query, (nom,))
        cursor.close()
        self.con.commit()
        



Builder.load_string("""

#<ContentCustomSheet@MDBoxLayout>

<CardBilan>
    orientation: "vertical"
    radius: 12
    elevation: 3
    md_bg_color: "#000000"

    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            orientaion: 'vertical'

            MDLabel:
                font_style: "Overline"
                theme_text_color : "Custom"
                text_color : "#1E90FF"
                text: "Valeur monnaitaire :"
                #theme_text_color: "Hint"
                halign: "left"

            MDLabel:
                theme_text_color : "Custom"
                text_color : "#1E90FF"
                text: "Quantite :"
                halign: "left"
                font_style: "Caption"

            MDLabel:
                theme_text_color : "Custom"
                text_color : "#1E90FF"
                text: "Nbr Client M"
                halign: "left"
                font_style: "Caption"
        MDBoxLayout:
            orientaion: 'vertical'

            MDLabel:
                theme_text_color : "Custom"
                text_color : "#1E90FF"
                id: valeur_monnaitaire
                font_style: "Overline"
                text: "0 Fc"
                halign: "left"

            MDLabel:
                theme_text_color : "Custom"
                text_color : "#1E90FF"
                id: qte_produits
                text: "0 Piece(s)"
                halign: "left"
                font_style: "Caption"

            MDLabel:
                theme_text_color : "Custom"
                text_color : "#1E90FF"
                id: nbr_clients
                text: "0 client(s)"
                halign: "left"
                font_style: "Caption"

<MainScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'images/1.jpg'
        MDTopAppBar:
            md_bg_color: "#4682B4"
            MDBoxLayout:
                orientation: "horizontal"
                MDLabel:
                    text: "Caisse"
                    pos_hint: {"center_x": .2, "center_y": .8}
                MDIconButton:
                    icon: "pen-plus"
                    halign: "left"
                    on_press:
                        root.manager.transition.direction = 'left' 
                        root.manager.current = 'add_client'
                        pos_hint: {"center_x": .5, "center_y": .8}
            
        MDBoxLayout:
            orientation: "vertical"
            size_hint: 1, .3
            padding: "18sp"
            spacing: "18sp"
            CardBilan:
                padding: "7.5dp"

        MDBoxLayout:
            adaptive_height: True

            MDBoxLayout:
                orientation : "horizontal"
                padding: "18sp"
                spacing: "18sp"
                #size_hint: 1, .6

                MDIconButton:
                    icon: 'magnify'

                MDTextField:
                    hint_text: 'Rechercher un client'
                    on_text: root.search_item(self.text, True)
                    line_color_normal: "#E6E6EA"

        MDBoxLayout:
            orientation: "vertical"
            ListClient
                Screen:
                    ScrollView:
                        MDList:
                            id: container

                    
            
""")

class ListClient(Screen):
    pass

class CardBilan(MDCard):
    def on_enter(self):
        
        liste_produit = database_handler.view_products()
        self.produits = sorted(liste_produit)
        nombre_client = len(self.produits)

        Qte_produits_vendues = 0
        valeur_monaitaire = 0

        for i in liste_produit:
            Qte_produits_vendues += i[3]


        for i in liste_produit:
            valeur_monaitaire += (i[3] * i[4])

        valeur_monnait = str(valeur_monaitaire)
        qte_produits = str(Qte_produits_vendues)

        self.ids.valeur_monnaitaire.text = f"{valeur_monnait} Fc"
        self.ids.nbr_clients.text = f"{nombre_client} Client(s)"
        self.ids.qte_produits.text = f"{qte_produits} Pièce(s)"


database_handler = DatabaseClient("base_donnee.db")

class MainScreen(Screen):
    dialogue = None

    def on_enter(self):
        self.ids.container.clear_widgets()
        liste_produit = database_handler.view_products()
        self.produits = sorted(liste_produit)
        
        if len(self.produits) == 0:
            afficher = MDLabel(text="Aucun élément à afficher pour le moment",
                               halign="center",
                               theme_text_color = "Custom",
                               text_color = "red",
                               font_style= "Overline")
            return self.ids.container.add_widget(afficher)
        else:
            for i in self.produits :
                container = BoxLayout(orientation = 'horizontal', size_hint = (None, None), size_hint_x = 1, height = '40dp')
                item = OneLineListItem(text = str(i[0]),theme_text_color = "Custom", text_color = ("#00FFFF"))
                button = MDIconButton(icon='arrow-right', text_color = ("#00FFFF"),theme_text_color = "Custom")
                item.bind(on_release=lambda x, info=i: self.print_information(info))
                button.bind(on_release = lambda x, info = i: self.Bottom_sheet(info))

                container.add_widget(item)
                container.add_widget(button)
                self.ids.container.add_widget(container)
                #self.ids.container.add_widget(button)

    def search_item(self, text="", search=False):

        self.ids.container.clear_widgets()
        self.produits
        if len(self.produits) == 0:
            afficher = MDLabel(text="Aucun élément à afficher pour le moment",
                               halign="center",
                               theme_text_color = "Custom",
                               text_color = "red",
                               font_style= "Overline")
            return self.ids.container.add_widget(afficher)
        
        else:
            for i in self.produits:
                if search:
                    if text.lower() in i[0].lower():
                        container = BoxLayout(orientation = 'horizontal', size_hint = (None, None), size_hint_x = 1, height = '40dp')
                        item = OneLineListItem(text = str(i[0]),theme_text_color = "Custom", text_color = ("#00FFFF"))
                        button = MDIconButton(icon='arrow-right', text_color = ("#00FFFF"),theme_text_color = "Custom")
                        item.bind(on_release=lambda x, info=i: self.print_information(info))
                        button.bind(on_release = lambda x, info = i: self.Bottom_sheet(info))

                        container.add_widget(item)
                        container.add_widget(button)
                        self.ids.container.add_widget(container)
                else:
                    item = OneLineListItem(text = str(i[0]))
                    button = MDIconButton(icon='start')
                    item.bind(on_release=lambda x, info=i: self.Bottom_sheet(info))
                    self.ids.container.add_widget(item)
                    self.ids.container.add_widget(button)


    def Bottom_sheet(self, info):
        self.information = info
        self.text_field_qte = MDTextField(
            max_height = "50dp",
            mode = "round",
            pos_hint = {"center_x": .3, "center_y": .9},
            padding = "18sp",
            input_type = "number"
        )
        self.text_field_prix = MDTextField(
            max_height = "50dp",
            mode = "round",
            pos_hint = {"center_x": .3, "center_y": .9},
            padding = "18sp",
            input_type = "number"
        )
        self.text_field_note = MDTextField(
            max_height = "70dp",
            mode = "rectangle",
            pos_hint = {"center_x": .3, "center_y": .9},
            padding = "18sp"
        )

        self.custom_sheet = MDCustomBottomSheet(screen = MDBoxLayout(
            MDLabel(
                text = info[0],
                pos_hint = {"center_x": .8, "center_y": .9},
                theme_text_color = "Custom",
                text_color = "green"

        ),
            
            MDBoxLayout(
            MDLabel(
                text = "Quantite",
                pos_hint = {"center_x": .2, "center_y": .9},
                theme_text_color = "Custom",
                text_color = "blue"
            ),
            self.text_field_qte,
            orientation = "horizontal",
            pos_hint = {"center_x": .5, "center_y": .8},
            padding = "18sp",
            spacing = "18sp"
            ),

            MDBoxLayout(
            MDLabel(
                text = "Prix de vente",
                pos_hint = {"center_x": .2, "center_y": .9},
                theme_text_color = "Custom",
                text_color = "blue"
            ),
            self.text_field_prix,
            orientation = "horizontal",
            pos_hint = {"center_x": .5, "center_y": .5},
            padding = "18sp",
            spacing = "18sp"
            ),

            MDBoxLayout(
            MDLabel(
                text = "Note",
                pos_hint = {"center_x": .2, "center_y": .9},
                theme_text_color = "Custom",
                text_color = "blue"
            ),
            self.text_field_note,
            orientation = "horizontal",
            pos_hint = {"center_x": .5, "center_y": .3},
            padding = "18sp",
            spacing = "18sp"
            ),

            MDBoxLayout(
            MDFillRoundFlatButton(
                text = "Valider",
                icon = "android",
                text_color = "white",
                on_release = self.add_news
            ),
            orientation = "horizontal",
            pos_hint = {"center_x": .85, "center_y": .5},
            padding = "18sp",
            spacing = "18sp"
            ),
            
            orientation = "vertical",
            size_hint_y = None,
            height = "500dp",
            pos_hint = {"center_x": .5, "center_y": 1}
        ),
        )

        try:
            self.text_field_prix.text = str(info[4])
            self.text_field_qte.text = str(info[3])
            self.text_field_note.text = info[-1]
        except:
            pass
        self.custom_sheet.open()

    def add_news(self, *args):
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        heure = now.strftime("%H:%M")
        etablissement = self.information[0]

        quantite = self.text_field_qte.text
        prix = self.text_field_prix.text
        note = self.text_field_note.text

        database_handler.update_client(quantite, prix, date, heure, note, etablissement)


    def print_information(self, info):
        
        if not self.dialogue:
            self.dialog = MDDialog(
                text= ("                          Soja" + "\nNom : " + str(info[0]) + "\nAdresse : " + str(info[1]) + "\nTel : " + str(info[2]) + "\nQuantite : " + str(info[3]) + "\nPrix : " + str(info[4]) + " Fc" + "\nDate : " + str(info[5]) + "\nHeure : " + str(info[6]) + "\n\n" + str(info[7]) ),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=lambda btn: self.dialog.dismiss(),
                                ),
                        ],
            )
        self.dialog.open()

Builder.load_string("""
<AddClientScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        #size_hint: 1, 1
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'images/17.png'

        MDTopAppBar:
            md_bg_color: "#4682B4"
            MDBoxLayout:
                orientation: "horizontal"
                MDIconButton:
                    icon: "arrow-left"
                    on_press:
                        root.manager.transition.direction = 'right'
                        root.manager.current = 'main_screen'
                        pos_hint: {"center_x": .5, "center_y": .8}
                MDLabel:
                    text: "Ajouter"
                    #anchor_title: "right"
                    pos_hint: {"center_x": .2, "center_y": .8}
                MDIconButton:
                    icon: "content-save"
                    on_release: root.recuperer_donner()
                    pos_hint: {"center_x": .8, "center_y": .8}

        MDBoxLayout:
            orientation: "vertical"
            size_hint: 1, .8
            padding: "15dp"
            spacing: "10sp"
            MDTextField:
                id: nom
                mode: "rectangle"
                pos_hint: {'center_x': .5, 'center_y': 1}
                size_hint_x: None
                width: "300dp"
                hint_text: "Nom de l'etablissement"
                icon_right: "warehouse"

            MDTextField:
                id: adresse
                mode: "rectangle"
                pos_hint: {'center_x': .5, 'center_y': .7}
                size_hint_x: None
                width: "300dp"
                hint_text: "Adresse"
                input_type: "number"

            MDTextField:
                id: telephone
                mode: "rectangle"
                pos_hint: {'center_x': .5, 'center_y': .5}
                size_hint_x: None
                width: "300dp"
                hint_text: "Numero de telephone"
                input_type: "number"
                icon_right: "file-phone"

            MDLabel:
                pos_hint: {"center_x": .5, "center_y": .8}
                halign: "center"
                id: error_text
                text: ""
                theme_text_color : "Custom"
                text_color: 1, 0, 0, 1
                font_style: "Body2"#"Overline"

            MDBoxLayout:
                orientation: "vertical"
                size_hint: 1, .2
                MDFlatButton:
                    on_release: root.dialogue_delete()
                    text: "Supprimer"
                    theme_text_color: "Custom"
                    text_color: "orange"
                    size_hint: 1, 1
""")

database_handler = DatabaseClient("base_donnee.db")

class AddClientScreen(Screen):
    dial = None

    def recuperer_donner(self):

        self.nom = self.ids.nom.text
        self.adresse = self.ids.adresse.text
        self.telephone = self.ids.telephone.text
        quantite = 0
        prix = 0

        if self.nom == "" or self.adresse == "":
            self.ids.error_text.theme_text_color = "Custom"
            self.ids.error_text.text_color = "red"
            self.ids.error_text.text = ("Vous devez remplir le nom et l'adresse au minimum ! ")
        else:
            database_handler.add_new_client(self.nom, self.adresse, self.telephone, quantite, prix)
            self.ids.error_text.text = ("Le client a bien été ajouter ! ")
            self.ids.error_text.theme_text_color = "Custom"
            self.ids.error_text.text_color = "#00FFFF"
            self.ids.nom.text = ""
            self.ids.adresse.text = ""
            self.ids.telephone.text = ""

    def dialogue_delete(self):
        self.nom_s = self.ids.nom.text
        if not self.dial:
            self.dialoge = MDDialog(
                text= (f"Voulez-vous vraiment supprimer ' {self.nom_s} ' ? "),
                buttons=[
                    MDFlatButton(
                        text="Oui",
                        theme_text_color="Custom",
                        #on_release= lambda btn: self.dialoge.dismiss(),self.delete_user,
                        on_release=lambda btn: [self.dialoge.dismiss(),self.delete_user()]
                                ),
                    MDFlatButton(
                        text="Annuler",
                        theme_text_color="Custom",
                        on_release=lambda btn: self.dialoge.dismiss(),
                                ),
                        ],
            )
        self.dialoge.open()

    def delete_user(self, *args):
        nom_etablissement = self.nom_s

        liste_produit = database_handler.view_products()
        for i in liste_produit:
            if nom_etablissement == i[0]:
                database_handler.supprimer(nom_etablissement)  
                self.ids.error_text.text = (f"Le client ' {nom_etablissement} ' a bien été supprimer ! ")
                self.ids.error_text.theme_text_color = "Custom"
                self.ids.error_text.text_color = "#00FFFF"
                self.ids.nom.text = ""
                self.ids.adresse.text = ""
                self.ids.telephone.text = ""
                return
    
        self.ids.error_text.text = (f"Le client {nom_etablissement} n'a pas ete trouver ! ")
        self.ids.error_text.theme_text_color = "Custom"
        self.ids.error_text.text_color = "red"



if __name__ == '__main__':
    MyApp().run()