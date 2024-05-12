import flet as ft
import numpy as np
import pandas as pd
from file_picker_helper import FilePickerHelper


def main(page: ft.Page):
    page.title = "Deep Helper"


    # Init FilePickerHelper class
    file_picker_helper = FilePickerHelper(page)

    # Add open button
    page.add(file_picker_helper.row_buttons)
    # Add dataframe table
    page.add(file_picker_helper.row_table)


if __name__ == "__main__":
    ft.app(main)
