from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit


class InfoWindow(QDialog):
    def __init__(self, info_text):
        super().__init__()

        self.setWindowTitle("Informacje")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(info_text)
        self.text_edit.setReadOnly(True)

        layout.addWidget(self.text_edit)

        self.setLayout(layout)