import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import numpy as np
import sympy
from sympy import *

from matplotlib.backends.backend_gtk3agg import \
    FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

class PlotWindow(Gtk.Window):
    def __init__(self, equation, x_min, x_max):
        Gtk.Window.__init__(self, title="Plot")

        self.set_default_size(800, 600)
        self.equation = equation
        self.x_min = x_min
        self.x_max = x_max

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
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
        y = eval(eval_expression, {'x': x_vector, 'np': np})

        x = symbols('x')
        #
        # # Define your function
        function_expression = self.equation
        function_expression = function_expression.replace('^', '**')
        function_expression = function_expression.replace('tg', 'tan')
        f = eval(function_expression)  # Example function
        print(f)
        horizontal_asymptotes = [limit(f, x, oo), limit(f, x, -oo)]
        #
        # # Calculate horizontal asymptotes
        print(horizontal_asymptotes)

        ax.plot(x_vector, y)
        ax.set_title(self.equation)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        for ass in horizontal_asymptotes:
            if ass not in [-oo, oo, oo * I, -oo * I] and not isinstance(ass,
                                                                        sympy.calculus.accumulationbounds.AccumulationBounds):
                ax.axhline(ass, color='red', linestyle='--')

        canvas = FigureCanvas(fig)  # a Gtk.DrawingArea

        sw = Gtk.ScrolledWindow()
        sw.set_border_width(10)
        sw.add(canvas)

        self.add(sw)

        self.show_all()