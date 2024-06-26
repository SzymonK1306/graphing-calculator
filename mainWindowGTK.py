import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from infoWindowGTK import InfoWindow
from plotWindowGTK import PlotWindow


import warnings


def custom_warning_handler(message, category, filename, lineno, file=None, line=None):
    if issubclass(category, RuntimeWarning):
        show_warning_dialog(
            'Wprowadzony zakres nie pokrywa się w pełni z dziedziną funkcji, wyznaczono wartości tylko dla poprawnych punktów')


def show_warning_dialog(message):
    # Create a message dialog
    dialog = Gtk.MessageDialog(
        transient_for=None,
        flags=0,
        message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.OK,
        text="Ostrzeżenie",
    )
    dialog.format_secondary_text(message)

    dialog.run()
    dialog.destroy()

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Kalulator graficzny")
        self.set_default_size(400, 200)
        self.set_border_width(10)

        # Menu bar
        menubar = Gtk.MenuBar()
        file_menu = Gtk.Menu()

        option1_action = Gtk.MenuItem(label="Informacje")
        option1_action.connect("activate", self.option1_selected)
        file_menu.append(option1_action)

        option2_action = Gtk.MenuItem(label="Przywróć domyślne")
        option2_action.connect("activate", self.option2_selected)
        file_menu.append(option2_action)

        menu = Gtk.MenuItem(label="Menu")
        menu.set_submenu(file_menu)
        menubar.append(menu)

        # Equation input
        self.eq_label = Gtk.Label(label="f(x) = ")
        self.eq_input = Gtk.Entry()
        self.eq_input.set_text("1 - 1.15*sin(0.86*x + 1.047)*exp(-0.5*x)")

        # x-min input
        self.x_min_label = Gtk.Label(label="x Min: ")
        self.x_min_input = Gtk.Entry()
        self.x_min_input.set_text("0")

        # x-max input
        self.x_max_label = Gtk.Label(label="x Max: ")
        self.x_max_input = Gtk.Entry()
        self.x_max_input.set_text("15")

        # Plot button
        self.plot_button = Gtk.Button(label="Narysuj wykres")
        self.plot_button.connect("clicked", self.plotEquation)

        grid = Gtk.Grid()
        grid.attach(self.eq_label, 0, 0, 1, 1)
        grid.attach(self.eq_input, 1, 0, 1, 1)
        grid.attach(self.x_min_label, 0, 1, 1, 1)
        grid.attach(self.x_min_input, 1, 1, 1, 1)
        grid.attach(self.x_max_label, 0, 2, 1, 1)
        grid.attach(self.x_max_input, 1, 2, 1, 1)
        grid.attach(self.plot_button, 0, 3, 2, 1)

        vbox = Gtk.VBox()
        vbox.pack_start(menubar, False, False, 0)
        vbox.pack_start(grid, True, True, 0)

        self.add(vbox)

    def plotEquation(self, button):
        equation = self.eq_input.get_text()
        try:
            x_min = float(self.x_min_input.get_text())
            x_max = float(self.x_max_input.get_text())
            if x_max <= x_min:
                self.show_error_dialog("Wartość minimalna musi być mniejsza niż maksymalna")
            else:
                plot_window = PlotWindow(equation, x_min, x_max)
                plot_window.show()
        except ValueError:
            self.show_error_dialog("Wartość w polu powinna być liczbą dziesiętną")


    def show_error_dialog(self, reason):
        # Function to show an error dialog
        error_dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Błąd!",
        )
        error_dialog.format_secondary_text(reason)

        # Show the error dialog
        error_dialog.run()
        error_dialog.destroy()

    def option1_selected(self, widget):
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
        - dostępne są wymienione funckcje - wielomiany, funckje wymierne, exp(x), ln(x), sin(x), cos(x), sqrt(x)
        - należy wprowadzić wszystkie operacje występujące we wzorze włącznie z operatorem mnożenia
        """
        self.info_window = InfoWindow(info_text)
        self.info_window.show()

    def option2_selected(self, widget):
        self.x_max_input.set_text("15")
        self.x_min_input.set_text("0")
        self.eq_input.set_text("1 - 1.15*sin(0.86*x + 1.047)*exp(-0.5*x)")


def main():
    warnings.showwarning = custom_warning_handler
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
