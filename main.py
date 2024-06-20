#Imports
# PyQt5 Framework - QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QFont, QFontDatabase
from googletrans import Translator
from language import *
import speech_recognition as sr

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.click_events()


    def settings(self):
        self.resize(500,400)
        self.setWindowTitle("PyRush")

    def click_events(self):
        self.restart.clicked.connect(self.reset)
        self.translate_btn.clicked.connect(self.text_on_screen)
        self.swap.clicked.connect(self.reverse_click)

    def listen_and_translate(self):
        text = self.recognize_speech()
        if text:
            self.textbox1.setText(text)
            self.text_on_screen()
            translated_text = self.textbox2.toPlainText()

    def google_translate(self, text, dest_lang, src_lang):
        speaker = Translator()
        translation = speaker.translate(text, dest=dest_lang, src=src_lang)
        return translation.text

    def text_on_screen(self):
        
        input_lang = self.combo1.currentText()
        output_lang = self.combo2.currentText()
    
        key_from_vaule1 = [key for key, vaule in LANGUAGES.items() if vaule == input_lang]
        key_from_vaule2 = [key for key, vaule in LANGUAGES.items() if vaule == output_lang]

        self.script = self.google_translate(self.textbox1.toPlainText(), key_from_vaule2[0], key_from_vaule1[0])

        self.textbox2.setText(self.script)

    def recognize_speech(self):
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = listener.listen(source, timeout=3)
                text = listener.recognize_google(audio)
                reutrn text
            except Exception as e:
                print("Error:",e)
                self.textbox2.setText("Could not understand you....")

    def reset(self):
    self.textbox1.clear()
    self.textbox2.clear()
            
    
    def reverse_click(self):
        input1, input2 = self.combo1.currentText(), self.textbox1.toPlainText()
        output1, output2 = self.combo2.currentText(), self.textbox2.toPlainText()

        self.combo1.setCurrentText(output1)
        self.combo2.setCurrentText(input1)
        self.textbox1.setText(output2)
        self.textbox2.setText(input2)

    def initUI(self):
        #Widgets
        self.title = QLabel("PyRush")
        self.combo1 = QComboBox()
        self.combo1.setPlaceholderText("Languages...")
        self.combo2 = QComboBox()
        self.combo2.setPlaceholderText("Languages...")
        self.translate_btn = QPushButton("Translate")
        self.speech = QPushButton("Speech")
        self.restart = QPushButton("Reset")

        self.textbox1 = QTextEdit()
        self.textbox1.setPlaceholderText("Input text will show here...")
        self.swap = QPushButton("🔁")
        self.textbox2 = QTextEdit()
        self.textbox2.setPlaceholderText("Output text will show here...")

        self.combo1.addItems(values)
        self.combo2.addItems(values)


        #Create Layout
        self.master_layout = QHBoxLayout()
        self.horizontal_layout1 = QVBoxLayout()
        self.horizontal_layout2 = QVBoxLayout()



        #Add Widget to Layout
        self.horizontal_layout1.addWidget(self.title)
        self.horizontal_layout1.addWidget(self.combo1)
        self.horizontal_layout1.addWidget(self.combo2)
        self.horizontal_layout1.addWidget(self.translate_btn)
        self.horizontal_layout1.addWidget(self.speech)
        self.horizontal_layout1.addWidget(self.restart)

        self.horizontal_layout2.addWidget(self.textbox1)
        self.horizontal_layout2.addWidget(self.swap)
        self.horizontal_layout2.addWidget(self.textbox2)



        self.master_layout.addLayout(self.horizontal_layout1, 30)
        self.master_layout.addLayout(self.horizontal_layout2, 70)

        self.setLayout(self.master_layout)

        self.setStyleSheet("""
        QWidget{
            background-color: #c6f500;
        }

        QLabel{
            color: blue;
            font-size: 50px;
            font-family: Lucida Handwriting;
        }

        QPushButton{
            border: 1px solid #000;
            font-family: Times New Roman;
        }

        QPushButton:hover{
            background-color: #ffe7bf;
            border: 1px solid #000;
        }

        QTextEdit{
            border: 1px solid #000;
        }
        """)




if __name__ == "__main__":
    app = QApplication([])
    window =TranslatorApp()
    window.show()
    app.exec()