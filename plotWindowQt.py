import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QVBoxLayout, QDialog, )
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import sympy
from sympy import *


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class PlotWindow(QDialog):

    # constructor
    def __init__(self, equation, x_min, x_max, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.equation = equation
        self.x_min = x_min
        self.x_max = x_max

        # a figure instance to plot on
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # adding canvas to the layout
        layout.addWidget(self.canvas)

        # setting layout to the main window
        self.setLayout(layout)

        self.plot(equation, x_min, x_max)

    # action called by the push button
    def plot(self, equation, x_min, x_max):
        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

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
            if ass not in [-oo, oo, oo*I, -oo*I] and not isinstance(ass, sympy.calculus.accumulationbounds.AccumulationBounds):
                ax.axhline(ass, color='red', linestyle='--')

        # refresh canvas
        self.canvas.draw()
