import flet as ft
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import webbrowser
import threading


class DataVisualization:
    """Data Visualization of the data frame"""
    def __init__(self, page):
        self.page = page
        self.data_frame = None

        # Column for radio selection
        self.column_plot = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
        # Column for selecting right settings for a plot
        self.column_settings = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

        # Select a plotting
        self.label_plot = ft.Text("Choose a plot: ")

        self.plot_radio = ft.RadioGroup(content=ft.Column([
            ft.Radio(value="line", label="Line"),
            ft.Radio(value="scatter", label="Scatter"),
            ft.Radio(value="bar", label="Bar")]))

        self.submit_draw = ft.TextButton("Submit", on_click=self.select_radio, disabled=True)

        self.column_plot.controls.append(self.label_plot)
        self.column_plot.controls.append(self.plot_radio)
        self.column_plot.controls.append(self.submit_draw)

    def update_data_frame(self, df):
        """Update df from file picker helper"""
        self.data_frame = df
        self.submit_draw.disabled = False
        self.submit_draw.update()

    def select_radio(self, e):
        if self.plot_radio.value == "line":
            self.draw_line()

    def draw_line(self):
        if self.data_frame is not None:
            threading.Thread(target=self.plot_data_frame).start()
        else:
            print("Data frame is None.")

    def plot_data_frame(self):
        if self.data_frame is not None:
            try:
                fig, ax = plt.subplots()
                ax.plot(self.data_frame.iloc[:, 0], self.data_frame.iloc[:, 1])
                fig.savefig("line_plot.png")
                webbrowser.open("line_plot.png")
                self.column_plot.update()
            except Exception as e:
                print("An error occurred:", e)
        else:
            print("Data frame is None.")

