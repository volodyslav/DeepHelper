import flet as ft
import numpy as np
import pandas as pd
from file_picker_helper import FilePickerHelper

from data_visualization import DataVisualization



def main(page: ft.Page):
    page.title = "Deep Helper"

    # Init Data Visualizer
    data_plot = DataVisualization(page)
    # Init FilePickerHelper class
    data_frame = FilePickerHelper(page, data_plot)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Data Representation",
                content=ft.Container(
                    content=ft.Column([
                        data_frame.row_buttons,
                        data_frame.row_table,
                        data_frame.row_table_editing,

                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ),
            ft.Tab(
                text="Data Visualization",
                content=ft.Container(
                    content=ft.Column([
                        data_plot.row_plot,
                        data_plot.row_figure_size,
                        data_plot.row_figure_labels,
                        data_plot.row_draw_value
                    ])
                )
            )
        ]
    )
    page.add(tabs)



if __name__ == "__main__":
    ft.app(main)
