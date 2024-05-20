import gtk
import numpy as np
import matplotlib.pyplot as plt


class MainWindow:
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("Kalkulator graficzny")
        self.window.set_size_request(400, 200)
        self.window.connect("destroy", gtk.main_quit)

        self.layout = gtk.VBox()

        # Equation input
        self.eq_label = gtk.Label("f(x) = ")
        self.eq_input = gtk.Entry()
        self.eq_input.set_text("x")
        self.eq_layout = gtk.HBox()
        self.eq_layout.pack_start(self.eq_label, False, False, 5)
        self.eq_layout.pack_start(self.eq_input, True, True, 5)
        self.layout.pack_start(self.eq_layout, False, False, 5)

        # x-min input
        self.x_min_label = gtk.Label("x Min: ")
        self.x_min_input = gtk.Entry()
        self.x_min_input.set_text("-2")
        self.x_min_layout = gtk.HBox()
        self.x_min_layout.pack_start(self.x_min_label, False, False, 5)
        self.x_min_layout.pack_start(self.x_min_input, True, True, 5)
        self.layout.pack_start(self.x_min_layout, False, False, 5)

        # x-max input
        self.x_max_label = gtk.Label("x Max: ")
        self.x_max_input = gtk.Entry()
        self.x_max_input.set_text("2")
        self.x_max_layout = gtk.HBox()
        self.x_max_layout.pack_start(self.x_max_label, False, False, 5)
        self.x_max_layout.pack_start(self.x_max_input, True, True, 5)
        self.layout.pack_start(self.x_max_layout, False, False, 5)

        # Plot button
        self.plot_button = gtk.Button(label="Narysuj wykres")
        self.plot_button.connect("clicked", self.plot_equation)
        self.layout.pack_start(self.plot_button, False, False, 5)

        self.window.add(self.layout)
        self.window.show_all()

    def plot_equation(self, widget):
        equation = self.eq_input.get_text()
        x_min = float(self.x_min_input.get_text())
        x_max = float(self.x_max_input.get_text())

        x = np.linspace(x_min, x_max, 100)
        y = eval(equation)

        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Wykres funkcji')
        plt.grid(True)
        plt.show()


def main():
    gtk.main()


if __name__ == "__main__":
    main()
