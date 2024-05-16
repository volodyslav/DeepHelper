import flet as ft
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart

matplotlib.use("svg")


class DataVisualization:
    """Data Visualization of the data frame"""
    def __init__(self, page):
        self.page = page
        self.data_frame = None

        self.fig, self.ax = plt.subplots()
        self.row_plot = ft.Row()
        self.plot_line_btn = ft.TextButton("Plot a line", on_click=self.draw_line)

        self.row_plot.controls.append(self.plot_line_btn)

    def update_data_frame(self, df):
        """Update df from file picker helper"""
        self.data_frame = df

    def draw_line(self, e):
        if self.data_frame is not None:
            try:
                self.ax.clear()
                self.ax.plot(self.data_frame.iloc[:, 0], self.data_frame.iloc[:, 1])
                self.row_plot.controls.clear()
                self.row_plot.controls.append(MatplotlibChart(self.fig, expand=True))
                self.row_plot.update()
            except Exception as e:
                print("An error occurred:", e)
        else:
            print("Data frame is None.")

