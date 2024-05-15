import flet as ft
import numpy as np
import pandas as pd
from file_picker_helper import FilePickerHelper


def main(page: ft.Page):
    page.title = "Deep Helper"
    # Init FilePickerHelper class
    data_frame = FilePickerHelper(page)

    tabs = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Data",
                content=ft.Container(
                    content=ft.Column([
                        data_frame.row_buttons,
                        data_frame.row_table,
                        data_frame.row_table_editing,
                        data_frame.row_columns_name
                    ])
                )
            )
        ]
    )
    page.add(tabs)

    # Add open button
    #page.add(data_frame.row_buttons)
    # Add dataframe table
    #page.add(data_frame.row_table)
    # row with editing
    #page.add(data_frame.row_table_editing)
    # Row for X column
    #page.add(data_frame.row_columns_name)




if __name__ == "__main__":
    ft.app(main)
