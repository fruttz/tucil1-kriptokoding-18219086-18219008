from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi
import sys
import uuid
import os

import extendedVigenere
import playfairCipher
import vigenere
import enigmaCipher

import numpy
import onetimepad
import pyperclip

class layarOTP(QDialog):
    def __init__(self):
        #setup cipher screen (main screen)
        super(layarOTP, self).__init__()
        loadUi("ui/layarotp.ui", self)

        #tombol switch to cipher machine
        self.backBut.clicked.connect(self.pindahlayarCipher)
        #tombol switch to enigma machine
        self.enigmaBut.clicked.connect(self.pindahlayarEnigma) 

        #tombol encrypt OTP
        self.encBut.clicked.connect(self.enkripsiOTP)
        #tombol decrypt OTP
        self.decBut.clicked.connect(self.dekripsiOTP)
        #tombol make pad OTP     
        self.padBut.clicked.connect(self.padBaru)
        
        self.padList.clear()

        i = 0
        while os.path.exists("storage/Pad%s.txt" % i):
            self.padList.addItem(f"{round(int(i),0)}")
            i += 1

    def pindahlayarCipher(self):
        cipherMachine = layarUtama()
        widget.addWidget(cipherMachine)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def pindahlayarEnigma(self):
        layarenigma = layarEnigma()
        widget.addWidget(layarenigma)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def enkripsiOTP(self):
        PadSel = self.padList.currentText()    
        with open("Storage/Pad%s.txt" % PadSel, 'r') as f:
            kuncipad = f.read()
        cipher = onetimepad.encrypt(self.inputText.toPlainText(), kuncipad)
        print("Cipher text: ", cipher)     
        
        self.outputText.setText(cipher)  
        self.outputText.repaint()  
        pyperclip.copy(cipher)    

    def dekripsiOTP(self):      
        PadSel = self.padList.currentText()   
        with open("Storage/Pad%s.txt" % PadSel, 'r') as f:
            kuncipad = f.read()           
        plainText = onetimepad.decrypt(self.inputText.toPlainText(), kuncipad)
        print("Plain text: ", plainText)
        
        self.outputText.setText(plainText)  
        self.outputText.repaint()  
        pyperclip.copy(plainText) 

    def padBaru(self):
        self.padBut.setEnabled(False)
        n = 1024 ** 2  # 1 Mb of random text
        letters = numpy.array(list(chr(ord('a') + i) for i in range(26)))    
        chars = ''.join(numpy.random.choice(letters, n))
        i = 0
        while os.path.exists("Storage/Pad%s.txt" % i):
            i += 1

        with open("Storage/Pad%s.txt" % i, 'w+') as f:
            f.write(chars)
            print("One time pad %s written to disk " %i)

        #reload pad
        self.padList.clear()
        i = 0
        while os.path.exists("Storage/Pad%s.txt" % i):
            self.padList.addItem(f"{round(int(i),0)}")
            i += 1
        self.padBut.setEnabled(True)

#initial load enigma GUI
class layarEnigma(QDialog):
    def __init__(self):
        #setup enigma screen
        super(layarEnigma, self).__init__()
        loadUi("ui/layarenigma.ui", self)

        #tombol switch to cipher machine
        self.backBut.clicked.connect(self.pindahlayarCipher)
        #tombol switch to OTP machine
        self.otpBut.clicked.connect(self.pindahlayarOTP)
        #tombol encrypt atau decrypt enigma
        self.cryptBut.clicked.connect(self.proccessEnigma)

    def pindahlayarCipher(self):
        cipherMachine = layarUtama()
        widget.addWidget(cipherMachine)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def proccessEnigma(self):
        inputText = self.textInput.toPlainText()
        rotorSet = self.rotorSetting.toPlainText()
        ringSet = self.ringSetting.toPlainText()
        reflectorSet = self.reflectorSetting.toPlainText()
        plugboardSet = self.plugboardSetting.toPlainText()
        startPos = self.startPosition.toPlainText()
        key = self.key.toPlainText()
		
        hasil = ""
		
        inition = enigmaCipher.initEnigma(rotorSet, ringSet, reflectorSet, plugboardSet)
        outputText = enigmaCipher.enigma(inition, startPos, key, inputText) 
		
        hasil += ' '.join([outputText[i: i+5] for i in range(0, len(outputText), 5)])
		
        self.outputTextArea.setPlainText(hasil)	

    def pindahlayarOTP(self):
        otpMachine = layarOTP()
        widget.addWidget(otpMachine)
        widget.setCurrentIndex(widget.currentIndex()+1)

#initial cipher GUI(main screen)
class layarUtama(QMainWindow):
    def __init__(self):
        #setup lauar utama
        super(layarUtama, self).__init__()
        loadUi("ui/layarutama.ui", self)
    
        #tombol input file
        self.inputButton.clicked.connect(self.inputFile)
        #tombol run
        self.cryptBut.clicked.connect(self.processFile)
        #tombol switch ke layar enigma
        self.enigmaBut.clicked.connect(self.pindahlayarEnigma) 
        #tombol switch ke layar OTP
        self.otpBut.clicked.connect(self.pindahlayarOTP)

        self.path = ""

    def pindahlayarEnigma(self):
        layarenigma = layarEnigma()
        widget.addWidget(layarenigma)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def pindahlayarOTP(self):
        otpMachine = layarOTP()
        widget.addWidget(otpMachine)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def inputFile(self):
        file = QtWidgets.QFileDialog.getOpenFileName()
        self.path = file[0]

        self.inputButton.setText(self.path.split('/')[-1])

    def processFile(self):
        pilihanCipher = self.cipheroption.currentText()
        plainText = self.textInput.toPlainText()
        kunci = self.kunciInput.toPlainText()

        if(self.path != ""):
            ext = os.path.splitext(self.path)[1]
            if(ext == ".txt"):
                f = open(self.path)
                plainText = f.read()
        if(len(kunci) == 0):
            return

        hasil = ""

#encrypt code
        if("encrypt" in pilihanCipher.lower()):
            if pilihanCipher == "Vigenere Cipher Encrypt":
                cipherText = vigenere.vigenerestdEnkripsi(plainText, kunci)

                hasil += "Cipher Text:\n"
                hasil += cipherText

            elif pilihanCipher == "Extended Vigenere Cipher Encrypt":
                if(self.path != ""):
                    direktori = os.path.dirname(os.path.realpath(__file__))
                    namaFile = "output/" + str(uuid.uuid4()) + os.path.splitext(self.path)[1]
                    pathFile = os.path.join(direktori, namaFile)

                    sukses = extendedVigenere.extVigenereEnkripsi(
                        self.path, 
                        kunci, 
                        pathFile
                    )
                    if(sukses):
                        hasil += "Encrypt sukses!\n\n"
                        hasil += "namaFile: %s" %(namaFile)
                    else:
                        hasil += "Gagal encrypt file"
                else:
                    hasil = "Please input file!"

            elif pilihanCipher == "Playfair Cipher Encrypt":
                # encryption
                playfairSquare = playfairCipher.createPlayfairSquare(kunci)
                hasil += playfairCipher.encrypt(plainText, playfairSquare) + '\n\n'
                for i in range(len(playfairSquare)):
                    for j in range(len(playfairSquare[0])):
                        hasil += ('{} '.format(playfairSquare[i][j]))
                    hasil += '\n'   

#decrypt code
        else:
            if pilihanCipher == "Vigenere Cipher Decrypt":
                plainText = vigenere.vigenerestdDekripsi(plainText, kunci)

                hasil += "Plain Text:\n"
                hasil += plainText

            elif pilihanCipher == "Extended Vigenere Cipher Decrypt":
                if(self.path != ""):
                    direktori = os.path.dirname(os.path.realpath(__file__))
                    namaFile = "output/" + str(uuid.uuid4()) + os.path.splitext(self.path)[1]
                    pathFile = os.path.join(direktori, namaFile)

                    sukses = extendedVigenere.extVigenereDekripsi(
                        self.path, 
                        kunci, 
                        pathFile
                    )
                    if(sukses):
                        hasil += "Decrypt sukses!\n\n"
                        hasil += "namaFile: %s" %(namaFile)
                    else:
                        hasil += "Gagal decrypt file"
                else:
                    hasil = "Please input file!"

            elif pilihanCipher == "Playfair Cipher Decrypt":
                playfairSquare = playfairCipher.createPlayfairSquare(kunci)
                hasil += playfairCipher.decrypt(plainText, playfairSquare) + '\n\n'
                for i in range(len(playfairSquare)):
                    for j in range(len(playfairSquare[0])):
                        hasil += ('{} '.format(playfairSquare[i][j]))
                    hasil += '\n'

        if("Extended Vigenere Cipher" not in pilihanCipher):
            direktori = os.path.dirname(os.path.realpath(__file__))
            namaFile = "output/" + str(uuid.uuid4()) + ".txt"
            pathFile = os.path.join(direktori, namaFile)

            f = open(pathFile, 'w')
            f.write(hasil)

            hasil += "\n\n\n\n"
            hasil += "Sukses!\n\n"
            hasil += "namaFile: %s" %(namaFile)

#refresh input
        self.outputTB.setPlainText(hasil)
        self.path = ""
        self.inputButton.setText("Atau, masukkan file ke sini!")

#main program
app = QApplication(sys.argv)
main = layarUtama()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main)
widget.setFixedWidth(1000)
widget.setFixedHeight(850)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")