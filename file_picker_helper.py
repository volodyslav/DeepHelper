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

        # Row for columns count, next table columns and previous columns
        self.row_table_editing = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        # row for columns names
        self.row_columns_names = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # Count data frame columns
        self.columns_count = ft.Text("Columns: 0")
        self.rows_count = ft.Text("Rows: 0")
        # Get columns name button
        self.get_column_button = ft.TextButton("Columns' name", disabled=True, visible=True, on_click=self.get_columns_name)
        # Get all columns' names
        self.columns_names = ft.Text("", no_wrap=False)
        self.column_name_show = False

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

        # Editing column's
        self.row_table_editing.controls.append(self.rows_count)
        self.row_table_editing.controls.append(self.columns_count)
        self.row_table_editing.controls.append(self.get_column_button)

        self.row_columns_names.controls.append(self.columns_names)


    def select_file(self, e: ft.FilePickerResultEvent):
        try:
            # File picker
            self.page.add(self.filepicker)
            self.filepicker.pick_files("Select File")
        except Exception as e:
            print("An error occurred:", e)

    def show_selected_path(self, e: ft.FilePickerResultEvent):
        try:
            # Show path of the file
            self.file_name = e.files[0].path
            if self.file_name and self.file_name.endswith(".csv"):
                self.file_path.value = self.file_name
                self.represent_csv_file()
                self.file_path.update()
        except Exception as e:
            print("An error occurred:", e)

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

    def get_row_editing_button(self):
        """Disable and make visible the get columns' name"""
        self.get_column_button.disabled = False
        self.get_column_button.visible = True
        self.get_column_button.update()

    def get_columns_name(self):
        self.column_name_show = True

    def represent_csv_file(self):
        """Represent csv file on the screen"""
        if self.file_name and self.file_name.endswith(".csv"):
            try:
                data_frame = pd.read_csv(self.file_name)
                print(data_frame.head())
                print(data_frame.columns[0])
                data_frame_head = data_frame.head()
                # Change DataTable into new columns with data
                self.table_data_frame.columns = self.show_data_frame_columns(data_frame_head)
                self.table_data_frame.rows = self.show_data_frame_rows(data_frame_head)
                self.table_data_frame.update()

                self.columns_count.value = f"Columns: {len(data_frame_head.columns)}"
                self.columns_count.update()
                self.rows_count.value = f"Rows: {len(data_frame_head)}"
                self.rows_count.update()
                # Show columns get name button
                self.get_row_editing_button()
                if self.column_name_show:
                    self.columns_names.value = "Columns' name: " + ", ".join(data_frame_head.columns)
                    self.columns_names.update()

            except FileNotFoundError:
                print("File not found.")
            except Exception as e:
                print("An error occurred:", e)
