from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.editor = QTextEdit()
        self.fontSizeBox = QSpinBox()

        font = QFont("JetBrainsMono", 16)
        self.editor.setFont(font)

        QFontDatabase.addApplicationFont("JetBrainsMono.ttf")
        QFontDatabase.addApplicationFont("MontserratAlternates.ttf")
        QFontDatabase.addApplicationFont("OpenSans.ttf")
        QFontDatabase.addApplicationFont("Oswald.ttf")
        QFontDatabase.addApplicationFont("Play.ttf")
        QFontDatabase.addApplicationFont("PTSans.ttf")
        QFontDatabase.addApplicationFont("PTSerif.ttf")
        QFontDatabase.addApplicationFont("Raleway.ttf")
        QFontDatabase.addApplicationFont("Roboto.ttf")
        QFontDatabase.addApplicationFont("UbuntuCondensed.ttf")

        self.path = ""
        self.setCentralWidget(self.editor)
        self.setWindowTitle("Text Editor")
        self.showMaximized()
        self.create_tool_bar()
        self.editor.setFontPointSize(16)


    def create_tool_bar(self):
        toolbar1 = QToolBar()

        toolbar1.addSeparator()

        open_action = QAction(QIcon("open.png"), "Open", self)
        open_action.triggered.connect(self.file_open)
        toolbar1.addAction(open_action)

        save_action = QAction(QIcon("save.png"), "Save", self)
        save_action.triggered.connect(self.saveFile)
        toolbar1.addAction(save_action)

        print_action = QAction(QIcon("print.png"), "Print", self)
        print_action.triggered.connect(self.file_print)
        toolbar1.addAction(print_action)

        toolbar1.addSeparator()
        toolbar1.addSeparator()

        undoBtn = QAction(QIcon("undo.png"), "Undo", self)
        undoBtn.setShortcut("Ctrl+Z")
        undoBtn.triggered.connect(self.editor.undo)
        toolbar1.addAction(undoBtn)

        redoBtn = QAction(QIcon("redo.png"), "Redo", self)
        redoBtn.setShortcut("Ctrl+Shift+Z")
        redoBtn.triggered.connect(self.editor.redo)
        toolbar1.addAction(redoBtn)

        toolbar1.addSeparator()
        toolbar1.addSeparator()

        select_action = QAction(QIcon("select-all.png"), "Select All", self)
        select_action.setShortcut("Ctrl+A")
        select_action.triggered.connect(self.editor.selectAll)
        toolbar1.addAction(select_action)

        copyBtn = QAction(QIcon("copy.png"), "Copy", self)
        copyBtn.setShortcut("Ctrl+C")
        copyBtn.triggered.connect(self.editor.copy)
        toolbar1.addAction(copyBtn)

        pasteBtn = QAction(QIcon("paste.png"), "Paste", self)
        pasteBtn.setShortcut("Ctrl+V")
        pasteBtn.triggered.connect(self.editor.paste)
        toolbar1.addAction(pasteBtn)

        cutBtn = QAction(QIcon("cut.png"), "Cut", self)
        cutBtn.setShortcut("Ctrl+X")
        cutBtn.triggered.connect(self.editor.cut)
        toolbar1.addAction(cutBtn)

        toolbar2 = QToolBar()

        toolbar2.addSeparator()

        self.fontBox = QComboBox(self)
        self.fontBox.addItems(["JetBrainsMono",
                               "MontserratAlternates",
                               "OpenSans",
                               "Oswald",
                               "Play",
                               "PTSans",
                               "PTSerif",
                               "Raleway",
                               "Roboto",
                               "UbuntuCondensed"])
        self.fontBox.activated.connect(self.setFont)
        toolbar2.addWidget(self.fontBox)

        self.fontSizeBox.setValue(16)
        self.fontSizeBox.valueChanged.connect(self.setFontSize)
        toolbar2.addWidget(self.fontSizeBox)

        toolbar2.addSeparator()
        toolbar2.addSeparator()

        leftAllign = QAction(QIcon('left-align.png'), 'Left Align', self)
        leftAllign.setShortcut("Ctrl+1")
        leftAllign.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        toolbar2.addAction(leftAllign)

        centerAllign = QAction(QIcon('center-align.png'), 'Center Align', self)
        centerAllign.setShortcut("Ctrl+2")
        centerAllign.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        toolbar2.addAction(centerAllign)

        rightAllign = QAction(QIcon('right-align.png'), 'Right Align', self)
        rightAllign.setShortcut("Ctrl+3")
        rightAllign.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        toolbar2.addAction(rightAllign)

        toolbar2.addSeparator()
        toolbar2.addSeparator()

        boldBtn = QAction(QIcon('bold.png'), 'Bold', self)
        boldBtn.setShortcut("Ctrl+B")
        boldBtn.triggered.connect(self.boldText)
        toolbar2.addAction(boldBtn)

        underlineBtn = QAction(QIcon('underline.png'), 'Underline', self)
        underlineBtn.setShortcut("Ctrl+U")
        underlineBtn.triggered.connect(self.underlineText)
        toolbar2.addAction(underlineBtn)

        italicBtn = QAction(QIcon('italic.png'), 'Italic', self)
        italicBtn.setShortcut("Ctrl+I")
        italicBtn.triggered.connect(self.italicText)
        toolbar2.addAction(italicBtn)

        self.addToolBar(toolbar1)
        self.addToolBar(toolbar2)


    def setFontSize(self):
        value = self.fontSizeBox.value()
        self.editor.setFontPointSize(value)


    def setFont(self):
        font = self.fontBox.currentText()
        self.editor.setCurrentFont(QFont(font))


    def italicText(self):
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not (state))


    def underlineText(self):
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not (state))


    def boldText(self):
        if self.editor.fontWeight != QFont.Bold:
            self.editor.setFontWeight(QFont.Bold)
            return
        self.editor.setFontWeight(QFont.Normal)


    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'ru') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()


    def saveFile(self):
        print(self.path)

        if self.path == '':
            self.file_saveas()
        text = self.editor.toPlainText()

        try: # Если файл не выбран до сохранения, выбираем или создаем, куда нужно сохранить
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()

        except Exception as e: # Сохраняем в текущий файл
            print(e)


    def file_saveas(self):
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "text documents (*.text);Text documents (*.txt);All files (*.*)")

        if self.path == '':
            return

        text = self.editor.toPlainText()

        try: # Если файл не выбран до сохранения, выбираем или создаем, куда нужно сохранить
            with open(path, 'w') as f:
                f.write(text)
                self.update_title()

        except Exception as e: # Сохраняем в текущий файл
            print(e)


    def file_print(self):
        dlg = QPrintDialog()

        if dlg.exec_():
            self.editor.print_(dlg.printer())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())