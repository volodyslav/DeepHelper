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
        self.row_figure_size = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.row_figure_labels = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # Slider width and height
        self.text_figure_size = ft.Text("Choose figure size")
        self.width_slider = ft.Slider(min=5, max=30, divisions=25, label="{value}", value=5,
                                      on_change=self.change_width_height_sliders)
        self.height_slider = ft.Slider(min=5, max=30, divisions=25, label="{value}", value=5,
                                       on_change=self.change_width_height_sliders)

        # Labels and title of the figure
        self.figure_title = ft.TextField(value="title", label="Figure title", max_lines=2, max_length=50,
                                         on_change=self.change_labels)
        self.x_figure_label = ft.TextField(value="", label="X label", max_lines=2, max_length=50,
                                           on_change=self.change_labels)
        self.y_figure_label = ft.TextField(value="", label="Y label", max_lines=2, max_length=50,
                                           on_change=self.change_labels)

        # Button to draw a line
        self.draw_line_button = ft.TextButton("Draw line", on_click=self.plot_data_frame)

        self.column_settings.controls.append(self.row_figure_size)
        self.column_settings.controls.append(self.row_figure_labels)



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

    def draw_line_settings(self):
        """For line settings"""
        # For figure size
        self.row_figure_size.controls.append(self.text_figure_size)
        self.row_figure_size.controls.append(self.width_slider)
        self.row_figure_size.controls.append(self.height_slider)
        self.row_figure_size.controls.append(self.draw_line_button)
        # For figure labels and titles
        self.row_figure_labels.controls.append(self.figure_title)
        self.row_figure_labels.controls.append(self.x_figure_label)
        self.row_figure_labels.controls.append(self.y_figure_label)

        self.row_figure_size.update()
        self.row_figure_labels.update()
        self.column_settings.update()
        # Disable button when choose a plot
        self.submit_draw.disabled = True
        self.submit_draw.update()

    def change_labels(self, e):
        """Update the labels and title"""
        self.figure_title.update()
        self.x_figure_label.update()
        self.y_figure_label.update()
        print(f"X label = {str(self.x_figure_label.value)}, "
              f"Y label = {str(self.y_figure_label.value)}, "
              f"Figure title = {str(self.figure_title.value)}")

    def change_width_height_sliders(self, e):
        """Changes the value of figure width and height sliders """
        self.width_slider.update()
        self.height_slider.update()
        print("Width slider", int(self.width_slider.value))
        print("Height slider", int(self.height_slider.value))

    def select_radio(self, e):
        if self.plot_radio.value == "line":
            self.draw_line_settings()

    def draw_line(self):
        if self.data_frame is not None:
            threading.Thread(target=self.plot_data_frame).start()
        else:
            print("Data frame is None.")

    def plot_data_frame(self, e):
        if self.data_frame is not None:
            try:
                fig, ax = plt.subplots(figsize=(int(self.width_slider.value), int(self.height_slider.value)))
                ax.plot(self.data_frame.iloc[:, 0], self.data_frame.iloc[:, 1])
                ax.set_title(str(self.figure_title.value))
                ax.set_xlabel(str(self.x_figure_label.value))
                ax.set_ylabel(str(self.y_figure_label.value))
                fig.savefig(f"line_plot.png")
                webbrowser.open(f"line_plot.png")
                self.column_plot.update()
            except Exception as e:
                print("An error occurred:", e)
        else:
            print("Data frame is None.")

