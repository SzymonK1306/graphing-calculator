

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QVBoxLayout, QDialog, QMessageBox, )
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

        self.setWindowTitle("Wykres")

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
        raised = False
        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

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
            if ass not in [-oo, oo, oo*I, -oo*I] and not isinstance(ass, sympy.calculus.accumulationbounds.AccumulationBounds):
                ax.axhline(ass, color='red', linestyle='--')

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

        y_list = []
        start_idx = 0
        for asv in vertical_asymptotes:
            closest_index = np.argmin(np.abs(x_vector - asv))
            y_list.append((x_vector[start_idx:closest_index], y[start_idx:closest_index]))
            start_idx = closest_index
        y_list.append((x_vector[start_idx:-1], y[start_idx:-1]))
        if len(y_list) != 0:
            for xx, yy in y_list:
                ax.plot(xx, yy, color='blue')
        else:
            ax.plot(x_vector, y)
        ax.set_title(self.equation)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        # refresh canvas
        self.canvas.draw()

    def show_error_dialog(self, reason):
        # Function to show an error dialog
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Błąd")
        error_dialog.setText(reason)
        error_dialog.setStandardButtons(QMessageBox.Ok)

        # Show the error dialog
        error_dialog.exec_()

