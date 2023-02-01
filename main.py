from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
import sys
import uuid
import os

import vigenereCypher as vig
import playfairCypher as pfc
import extendedVigenere as ev

import numpy as np
import onetimepad as otp
import pyperclip

#MAIN SCREEN
class main_screen(QMainWindow):
    def __init__(self):
        super(main_screen, self).__init__()
        loadUi("ui/cryptogui.ui",self)

        self.inputBut.clicked.connect(self.input_file)
        self.cryptBut.clicked.connect(self.process_file)
        self.otpBut.clicked.connect(self.to_otp)

        self.path = ""
    
    def input_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName()
        self.path = file[0]
        self.inputBut.setText(self.path.split('/')[-1])
    
    def process_file(self):
        cipher_method = self.cipheroption.currentText()
        plain_text = self.textInput.toPlainText()
        key = self.keyInput.toPlainText()

        if(self.path != ""):
            ext = os.path.splitext(self.path)[1]
            if(ext == ".txt"):
                f = open(self.path)
                plain_text = f.read()
        if(len(key) == 0):
            return
        result = ""

        #ENCRYPTION
        if ("encrypt" in cipher_method.lower()):
            if cipher_method == "Vigenere Cipher Encrypt":
                cipher_text = vig.vigenere_encrypt(plain_text, key)
                result += "Cipher Text:\n"
                result += cipher_text
                result += "\n\nCipher (per 5): \n"
                result += ' '.join([cipher_text[i: i+5] for i in range(0, len(cipher_text), 5)])
            
            elif cipher_method == "Extended Vigenere Cipher Encrypt":
                if(self.path != ""):
                    directory = os.path.dirname(os.path.realpath(__file__))
                    file_name = "output/" + str(uuid.uuid4()) + os.path.splitext(self.path)[1]
                    file_path = os.path.join(directory, file_name)

                    success = ev.extended_vigenere_encrypt(self.path, key, file_path)
                    if(success):
                        result += "Enkripsi berhasil!\n\n"
                        result += f"Nama file: {file_name}"
                    else:
                        result += "Enkripsi gagal"
                else:
                    result = "Silakan masukkan file!"
            
            elif cipher_method == "Playfair Cipher Enrcypt":
                playfair_square = pfc.make_playfair_square(key)
                result += pfc.encrypt(plain_text, playfair_square) + '\n\n'
                for i in range(len(playfair_square)):
                    for j in range(len(playfair_square[0])):
                        result += ('{} '.format(playfair_square[i][j]))
                    result += '\n'
            
        #DECRYPTION
        else:
            if cipher_method == "Vigenere Cipher Decrypt":
                plain_text = vig.vigenere_decrypt(plain_text, key)

                result += "Plain Text:\n"
                result += plain_text
                result += "\n\nPlain Text (per 5): \n"
                result += ' '.join([plain_text[i: i+5] for i in range(0, len(plain_text), 5)])
            
            elif cipher_method == "Extended Vigenere Cipher Decrypt":
                if(self.path != ""):
                    directory = os.path.dirname(os.path.realpath(__file__))
                    file_name = "output/" + str(uuid.uuid4()) + os.path.splitext(self.path)[1]
                    file_path = os.path.join(directory, file_name)

                    success = ev.extended_vigenere_decrypt(self.path, key, file_path)
                    if success:
                        result += "Dekripsi berhasil!\n\n"
                        result += f"Nama file: {file_name}"
                    else:
                        result += "Dekripsi gagal"
                else:
                    "Silakan masukkan file"
            
            elif cipher_method == "Playfair Cipher Decrypt":
                playfair_square = pfc.make_playfair_square(key)
                result += pfc.decrypt(plain_text, playfair_square)
                for i in range(len(playfair_square)):
                    for j in range(len(playfair_square[0])):
                        result += ('{} '.format(playfair_square[i][j]))
                    result += '\n'

        if("Extended Vigenere Cipher" not in cipher_method):
            directory = os.path.dirname(os.path.realpath(__file__))
            file_name = "output/" + str(uuid.uuid4()) + ".txt"
            file_path = os.path.join(directory, file_name)

            f = open(file_path, 'w')
            f.write(result)

            result += "\n\n\n\n"
            result += "Berhasil!\n\n"
            result += f"Nama file: {file_name}"
        
        self.outputTB.setPlainText(result)
        self.path = ""
        self.inputBut.setText("Atau, masukkan file ke sini!")
    
    def to_otp(self):
        otp_machine = otp_screen()
        widget.addWidget(otp_machine)
        widget.setCurrentIndex(widget.currentIndex()+1)

#ONE TIME PAD
class otp_screen(QDialog):
    def __init__(self):
        super(otp_screen, self).__init__()
        loadUi("ui/otpgui.ui", self)
        self.backBut.clicked.connect(self.to_main)
        self.encBut.clicked.connect(self.otp_encrypt)
        self.decBut.clicked.connect(self.otp_decrypt)
        self.padBut.clicked.connect(self.new_pad)
        self.padList.clear()

        i = 0
        while os.path.exists(f"storage/Pad{i}.txt"):
            self.padList.addItem(f"{round(int(i),0)}")
            i += 1
        
    def otp_encrypt(self):
        pad_cell = self.padList.currentText()
        with open(f"Storage/Pad{pad_cell}.txt", 'r') as f:
            keypad = f.read()
        cipher_text = otp.encrypt(self.inputText.toPlainText(), keypad)
        print("Cipher text: ", cipher_text)
        self.outputText.setText(cipher_text)
        self.outputText.repaint()
        pyperclip.copy(cipher_text)
    
    def otp_decrypt(self):
        pad_cell = self.padList.currentText()
        with open(f"Storage/Pad{pad_cell}.txt", 'r') as f:
            keypad = f.read()
        plain_text = otp.decrypt(self.inputText.toPlainText(), keypad)
        print("Cipher text: ", plain_text)
        self.outputText.setText(plain_text)
        self.outputText.repaint()
        pyperclip.copy(plain_text)
    
    def new_pad(self):
        self.padBut.setEnabled(False)
        n = 1024 ** 2
        letters = np.array(list(chr(ord('a') + i) for i in range(26)))
        chars = ''.join(np.random.choice(letters,n))
        i = 0
        while os.path.exists(f"Storage/Pad{i}.txt"):
            i += 1
        with open(f"Storage/Pad{i}.txt",'w+') as f:
            f.write(chars)
            print(f"One time pad {i} berhasil disimpan")
        
        self.padList.clear()
        i = 0
        while os.path.exists(f"Storage/Pad{i}.txt"):
            self.padList.addItem(f"{round(int(i),0)}")
            i += 1
        self.padBut.setEnabled(True)

    def to_main(self):
        main = main_screen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)

#Driver
app = QApplication(sys.argv)
main = main_screen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main)
widget.setFixedWidth(1000)
widget.setFixedHeight(850)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")





            
        

