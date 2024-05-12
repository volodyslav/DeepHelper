import flet as ft
import numpy as np
import pandas as pd

class FilePickerHelper:
    def __init__(self, page):
        """Open file, represent data"""
        self.page = page

        # Open buttons
        self.row_buttons = ft.Row()
        # Table's row with DataFrame data
        self.row_table = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # File name
        self.file_name = None
        # Table for csv data frame
        self.table_data_frame = ft.DataTable(columns=[ft.DataColumn(ft.Text("Columns"))], rows=[ft.DataRow(cells=[
            ft.DataCell(ft.Text("Cells"))
        ])], border_radius=10, expand=True, border=ft.border.all(2, "grey"))
        # How many columns to show in data frame
        self.show_columns = 8

        # File path
        self.file_path = ft.Text("Selected path", expand=1)
        self.filepicker = ft.FilePicker(on_result=self.show_selected_path)

        # Button for selecting file
        open_button = ft.IconButton(icon=ft.icons.FOLDER_OPEN, on_click=self.select_file)
        self.row_buttons.controls.append(open_button)
        self.row_buttons.controls.append(self.file_path)
        self.row_table.controls.append(self.table_data_frame)


    def select_file(self, e: ft.FilePickerResultEvent):
        # File picker
        self.page.add(self.filepicker)
        self.filepicker.pick_files("Select File")

    def show_selected_path(self, e: ft.FilePickerResultEvent):
        # Show path of the file
        self.file_name = e.files[0].path
        if self.file_name and self.file_name.endswith(".csv"):
            self.file_path.value = self.file_name
            self.represent_csv_file()
            self.file_path.update()

    def show_data_frame_columns(self, df: pd.DataFrame) -> list:
        """Return data frame columns"""
        return [ft.DataColumn(ft.Text(header)) for header in df.columns[:self.show_columns]]

    def show_data_frame_rows(self, df: pd.DataFrame) -> list:
        """Returns data frame rows"""
        rows = []
        for _, row in df.iterrows():
            cells = [ft.DataCell(ft.Text(str(row[header]))) for header in df.columns[:self.show_columns]]
            rows.append(ft.DataRow(cells=cells))
        return rows

    def represent_csv_file(self):
        """Represent csv file on the screen"""
        if self.file_name and self.file_name.endswith(".csv"):
            try:
                data_frame = pd.read_csv(self.file_name)
                print(data_frame.head())
                data_frame_head = data_frame.head()
                self.table_data_frame.columns = self.show_data_frame_columns(data_frame_head)
                self.table_data_frame.rows = self.show_data_frame_rows(data_frame_head)
                self.table_data_frame.update()
            except FileNotFoundError:
                print("File not found.")
            except Exception as e:
                print("An error occurred:", e)




def main(page: ft.Page):
    page.title = "Deep Helper"


    # Init FilePickerHelper class
    file_picker_helper = FilePickerHelper(page)

    # Add open button
    page.add(file_picker_helper.row_buttons)
    # Add dataframe table
    page.add(file_picker_helper.row_table)

ft.app(main)
