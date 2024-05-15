import flet as ft
import numpy as np
import pandas as pd
from file_picker_helper import FilePickerHelper


def main(page: ft.Page):
    page.title = "Deep Helper"

    # Init FilePickerHelper class
    data_frame = FilePickerHelper(page)

    # Add open button
    page.add(data_frame.row_buttons)
    # Add dataframe table
    page.add(data_frame.row_table)
    # row with editing
    page.add(data_frame.row_table_editing)
    # row for y target
    #page.add(data_frame.row_target_name)
    # Row for X column
    page.add(data_frame.row_columns_name)


if __name__ == "__main__":
    ft.app(main)
