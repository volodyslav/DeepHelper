import flet as ft
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


matplotlib.use("svg")


class DataVisualization:
    """Data Visualization of the data frame"""
    def __init__(self, page, data_frame):
        self.page = page
        self.data_frame = data_frame

        self.fig, self.ax = plt.subplots()

        print("Data frame", self.data_frame)

    def draw_line(self):
        try:
            self.ax.plot(self.data_frame[0], self.data_frame[1])
        except Exception as e:
            print("An error: ", e)

