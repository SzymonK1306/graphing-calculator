import sys
import random
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, QMenuBar, QAction, QMessageBox)


from infoWindowQt import InfoWindow
from plotWindowQt import PlotWindow



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kalulator graficzny")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()


        # Menu bar
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu('Menu')

        # Menu actions
        option1_action = QAction('Informacje', self)
        option1_action.triggered.connect(self.option1_selected)
        file_menu.addAction(option1_action)

        option2_action = QAction('Przywróć domyślne', self)
        option2_action.triggered.connect(self.option2_selected)
        file_menu.addAction(option2_action)

        layout.setMenuBar(menubar)

        # Equation input
        eq_layout = QHBoxLayout()
        self.eq_label = QLabel("f(x) = ")
        self.eq_input = QLineEdit()
        self.eq_input.insert('x')
        eq_layout.addWidget(self.eq_label)
        eq_layout.addWidget(self.eq_input)
        layout.addLayout(eq_layout)

        # x-min input
        x_min_layout = QHBoxLayout()
        self.x_min_label = QLabel("x Min: ")
        self.x_min_input = QLineEdit()
        self.x_min_input.insert('-2')
        x_min_layout.addWidget(self.x_min_label)
        x_min_layout.addWidget(self.x_min_input)
        layout.addLayout(x_min_layout)

        # x-max input
        x_max_layout = QHBoxLayout()
        self.x_max_label = QLabel("x Max: ")
        self.x_max_input = QLineEdit()
        self.x_max_input.insert('2')
        x_max_layout.addWidget(self.x_max_label)
        x_max_layout.addWidget(self.x_max_input)
        layout.addLayout(x_max_layout)

        # Plot button
        self.plot_button = QPushButton("Narysuj wykres")
        self.plot_button.clicked.connect(self.plotEquation)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def plotEquation(self):
        equation = self.eq_input.text()
        x_min = float(self.x_min_input.text())
        x_max = float(self.x_max_input.text())

        if x_max < x_min:
            self.show_error_dialog("Wartość minimalna nie może być większa niż maksymalna")
        else:
            self.plot_window = PlotWindow(equation, x_min, x_max)
            self.plot_window.show()

    def show_error_dialog(self, reason):
        # Function to show an error dialog
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Błąd")
        error_dialog.setText(reason)
        # error_dialog.setInformativeText("Please check the details and try again.")
        # error_dialog.setDetailedText("Detailed error information can be provided here.")
        error_dialog.setStandardButtons(QMessageBox.Ok)

        # Show the error dialog
        error_dialog.exec_()
    def option1_selected(self):
        info_text = """
Ta aplikacja realizująca kalkulator graficzny posiada następujące funkcjonalności:
- Wprowadzenie wzoru funkcji w pole tekstowe
- Ograniczenie dziedziny funkcji poprzez wprowadzenie jej w pole tekstowe
- Możliwość narysowania wykresu funkcji jednej zmiennej. Dopuszczalne są funkcje
różnego rodzaju (funkcje wielomianowe, wymierne, wykładnicze, logarytmiczne,
trygonometryczne) poprzez naciśnięcie przycisku “Narysuj wykres”. Powoduje to
otwarcie nowego okna zawierającego wykres.
- Odrzucanie błędnie skonstruowanych formuł matematycznych oraz wykrywanie
błędów w dziedzinie. Wystąpienie tego rodzaju błędów jest sygnalizowane
odpowiednim oknem dialogowym
- Menu zawierające możliwość zapoznania się z krótkim opisem aplikacji oraz
wczytania domyślnych zawartości pól tekstowych

Zasady poprawnego wprowadzania wzorów funckji
- dostępne są wymienione operacje matematyczne - dodatanie (+), odejmowanie (-), mnożenie (*), dzielenie(/), potęgowanie (^)
- dostępne są wymienione funckcje - wielomiany, funckje wymierne, exp(x), ln(x), sin(x), cos(x), tg(x), sqrt(x)
- funckje wymierne należy wprowadzać z jedną kreską ułamkową
- należy wprowadzić wszystkie operacje występujące we wzorze włącznie z operatorem mnożenia

        """
        self.info_window = InfoWindow(info_text)
        self.info_window.show()

    def option2_selected(self):
        self.x_max_input.clear()
        self.x_max_input.insert('2')

        self.x_min_input.clear()
        self.x_min_input.insert('-2')

        self.eq_input.clear()
        self.eq_input.insert('x')


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
