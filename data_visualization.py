import flet as ft
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from PIL import Image


class DataVisualization:
    """Data Visualization of the data frame"""
    def __init__(self, page):
        self.page = page
        self.data_frame = None


        self.row_plot = ft.Column()
        # Select a plotting
        self.label_plot = ft.Text("Choose a plot: ")

        self.plot_radio = ft.RadioGroup(content=ft.Column([
            ft.Radio(value="line", label="Line"),
            ft.Radio(value="scatter", label="Scatter"),
            ft.Radio(value="bar", label="Bar")]))

        self.submit_draw = ft.TextButton("Draw")

        self.row_plot.controls.append(self.label_plot)
        self.row_plot.controls.append(self.plot_radio)
        self.row_plot.controls.append(self.submit_draw)

    def update_data_frame(self, df):
        """Update df from file picker helper"""
        self.data_frame = df


    def draw_line(self, e):
        if self.data_frame is not None:
            try:
                fig, ax = plt.subplots()
                ax.plot(self.data_frame.iloc[:, 0], self.data_frame.iloc[:, 1])
                fig.savefig("line_plot.png")
                with Image.open("line_plot.png") as image:
                    image.show()
                self.row_plot.update()
            except Exception as e:
                print("An error occurred:", e)
        else:
            print("Data frame is None.")

