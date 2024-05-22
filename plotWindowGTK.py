import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import warnings

import numpy as np
import sympy
from sympy import *

from matplotlib.backends.backend_gtk3agg import \
    FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

class PlotWindow(Gtk.Window):
    def __init__(self, equation, x_min, x_max):
        Gtk.Window.__init__(self, title="Wykres")

        raised = False

        self.set_default_size(800, 600)
        self.equation = equation
        self.x_min = x_min
        self.x_max = x_max

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        x = symbols('x')
        #
        # # Define your function
        function_expression = self.equation
        function_expression = function_expression.replace('^', '**')
        function_expression = function_expression.replace('tg', 'tan')
        try:
            f = eval(function_expression)  # Example function
        except SyntaxError:
            f = x
            if not raised:
                raised = True
                self.show_error_dialog('Wprowadzono błędne wyrażenie, sprawdź je i spróbuj ponownie')

        horizontal_asymptotes = [limit(f, x, oo), limit(f, x, -oo)]

        for ass in horizontal_asymptotes:
            if ass not in [-oo, oo, oo * I, -oo * I] and not isinstance(ass,
                                                                        sympy.calculus.accumulationbounds.AccumulationBounds):
                try:
                    ax.axhline(ass, color='red', linestyle='--')
                except:
                    pass

        eval_expression = self.equation.replace('exp', 'np.exp')
        eval_expression = eval_expression.replace('^', '**')
        eval_expression = eval_expression.replace('sin', 'np.sin')
        eval_expression = eval_expression.replace('cos', 'np.cos')
        eval_expression = eval_expression.replace('tg', 'np.tan')
        eval_expression = eval_expression.replace('log', 'np.log10')
        eval_expression = eval_expression.replace('ln', 'np.log')
        eval_expression = eval_expression.replace('sqrt', 'np.sqrt')

        # plot data
        x_vector = np.linspace(self.x_min, self.x_max, 400)
        try:
            y = eval(eval_expression, {'x': x_vector, 'np': np})
        except SyntaxError:
            y = np.zeros(len(x_vector))
            if not raised:
                raised = True
                self.show_error_dialog('Wprowadzono błędne wyrażenie, sprawdź je i spróbuj ponownie')
        if isinstance(y, int):
            y = y * np.ones(len(x_vector))
        y_list = []
        start_idx = 0
        try:
            domain = calculus.util.continuous_domain(f, x, S.Reals)

            potential_points = domain.boundary

            vertical_asymptotes = []

            potential_points_list = list(potential_points)
            for point in potential_points_list:
                left_limit = limit(f, x, point, dir='-')
                right_limit = limit(f, x, point, dir='+')
                if left_limit in [-oo, oo] or right_limit in [-oo, oo]:
                    vertical_asymptotes.append(point)

            # Draw vertical asymptotes
            for v_ass in vertical_asymptotes:
                ax.axvline(v_ass, color='red', linestyle='--')
                closest_index = np.argmin(np.abs(x_vector - v_ass))
                y_list.append((x_vector[start_idx:closest_index], y[start_idx:closest_index]))
                start_idx = closest_index
        except:
            pass
        y_list.append((x_vector[start_idx:-1], y[start_idx:-1]))
        if len(y_list) != 0:
            for xx, yy in y_list:
                ax.plot(xx, yy, color='blue')
        else:
            ax.plot(x_vector, y)
        ax.set_title(self.equation)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        canvas = FigureCanvas(fig)  # a Gtk.DrawingArea

        sw = Gtk.ScrolledWindow()
        sw.set_border_width(10)
        sw.add(canvas)

        self.add(sw)

        self.show_all()

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

