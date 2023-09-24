from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import cv2
import webbrowser
from kivy.lang import Builder

class AboutPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        
        app_name_label = MDLabel(text="CaptionifyQR", font_style="H4", halign="center", pos_hint={"center_x": 0.5, "top": 0.7})
        version_label = MDLabel(text="Version 1.0", halign="center", pos_hint={"center_x": 0.5, "top": 0.6})
        
        description_label = MDLabel(
            text="CaptionifyQR is a QR code detection app that allows you to scan QR codes and open URLs. "
                 "It provides a simple and convenient way to access online content."
                 "Developed by CaptionifyAI\nContact us at tijjanihaveev@gmail.com"
                 "Acknowledgments:\n- QR code detection library by OpenCV\n- Icons by FontAwesome",
            halign="center"
        )
        
        
    
        logo_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=((120), (120)),  # Adjust the size as needed
            pos_hint={"center_x": 0.5, "top": 0.9},  # Centered at the top
        )

        logo_image = Image(source='CaptionifyQr.png', size=(100, 100))
        logo_layout.add_widget(logo_image)
        feedback_button = MDFillRoundFlatButton(
            text="Provide Feedback",
            on_release=self.open_feedback_page
        )
        
        back_button = MDFillRoundFlatButton(text="Back to Main Page", on_release=self.back_to_main_page)
        
        self.add_widget(app_name_label)
        self.add_widget(version_label)
        self.add_widget(description_label)
        self.add_widget(feedback_button)
        self.add_widget(back_button)
        self.add_widget(logo_layout)
    
    def open_privacy_policy(self, *args):
        # Implement a function to open the privacy policy page or link
        pass 
    def open_feedback_page(self, *args):
        # Implement a function to open the feedback or contact page
        pass 
    
    def back_to_main_page(self, *args):
        app = MDApp.get_running_app()
        app.show_main_page()


               
    
    

class Qrcodedetector(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        self.detected_qrcodes = []
        self.ignored_qrcodes = []
        self.data = None

        return Builder.load_string('''
MDNavigationLayout:
    ScreenManager:
        id: screen_manager
        Screen:
            name: "main_page"
            FloatLayout:
                Image:
                    source: 'madinatu.jpg'
                    allow_stretch: True
                    keep_ratio: False
                    size_hint_y: None
                    height: root.height

                Image:
                    id: image
                    size_hint: None, None
                    size: dp(300), dp(300)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            
                

            MDFillRoundFlatButton:
                text: 'Detect URL'
                size_hint: None, None
                size: dp(200), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.1}
                on_release: app.take_picture()

        Screen:
            name: "about_page"
            AboutPage:
                name: "about_page"

    MDTopAppBar:
        title: "CaptionifyQR"
        elevation: 1
        pos_hint: {"top": 1}
        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
        icon: 'CaptionifyQr.png'
        icon_size: (48, 48)
                                   

    MDNavigationDrawer:
        id: nav_drawer
        orientation: "vertical"
        size_hint: 1, None
        height: "200dp"
        pos_hint: {"top": 1}
        BoxLayout:
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"
            
            MDTopAppBar:
                title: "CaptionifyQR"
                elevation: 10
                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

            MDFillRoundFlatButton:
                text: 'View Detected QR Codes'
                size_hint: None, None
                size: dp(200), dp(48)
                on_release: app.view_detected_qrcodes()

            MDFillRoundFlatButton:
                text: 'About'
                size_hint: None, None
                size: dp(200), dp(48)
                on_release: app.show_about_page()
''')

    def on_start(self):
        self.capture = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)

    def load_video(self, *args):
        ret, frame = self.capture.read()
        self.image_frame = frame
        data, bbox, _ = self.detector.detectAndDecode(self.image_frame)
        
        if data:
            if data not in self.ignored_qrcodes:
                self.ignored_qrcodes.append(data)  # Add to the ignored list
                if data not in self.detected_qrcodes:
                    self.detected_qrcodes.append(data)
                    print(f"Detected QR Code: {data}")
                self.data = data

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.root.ids.image.texture = texture

    def take_picture(self):
        if self.data:
            try:
                webbrowser.open(str(self.data))
            except Exception as e:
                print(f"Error opening URL: {e}")
        else:
            print("No QR code detected.")

    def view_detected_qrcodes(self, *args):
        print("View Detected QR Codes Clicked")
        dialog_content = ScrollView()
        layout = MDBoxLayout(orientation="vertical", spacing="10dp", size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        
        for qr_code_data in self.detected_qrcodes:
            qr_code_label = MDLabel(
                text=qr_code_data,
                halign="center",
                size_hint_y=None,
                height="48dp",
            )
            layout.add_widget(qr_code_label)

        dialog_content.add_widget(layout)

        scroll_view = ScrollView()
        scroll_view.add_widget(dialog_content)

        dialog = MDDialog(
            title="Detected QR Codes",
            type="simple",
            content_cls=scroll_view,
            size_hint=(None, None),
            size=("300dp", "400dp"),
            auto_dismiss=True,
            buttons=[
                MDFillRoundFlatButton(
                    text="Reset",
                    on_release=lambda x: self.reset_detected_qrcodes()
                ),
                MDFillRoundFlatButton(
                    text="Close",
                    on_release=lambda x: dialog.dismiss()
                ),
            ]
        )
        dialog.open()

    def reset_detected_qrcodes(self):
        self.detected_qrcodes = []
        self.ignored_qrcodes = []

    def show_about_page(self):
        screen_manager = self.root.ids.screen_manager
        screen_manager.current = "about_page"

    def show_main_page(self):
        screen_manager = self.root.ids.screen_manager
        screen_manager.current = "main_page"

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    Qrcodedetector().run()
