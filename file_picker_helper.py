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

        # For data frame when open the file
        self.data_frame_head = None
        self.data_frame = None

        # Row for columns count, next table columns and previous columns
        self.row_table_editing = ft.Row(alignment=ft.MainAxisAlignment.CENTER, scale=1.3, height=60)

        # row for choosing the y target
        self.row_target_name = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # For X columns
        self.row_columns_name = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # Row for choosing the X columns
        self.row_columns_name = ft.Column(alignment=ft.MainAxisAlignment.CENTER, wrap=True, scroll=ft.ScrollMode.ALWAYS,
                                          height=200)

        # Count data frame columns
        self.columns_count = ft.Text("Columns: 0")
        self.rows_count = ft.Text("Rows: 0")
        # For scrolling dataframe's columns
        self.next_column = ft.IconButton(icon=ft.icons.ARROW_FORWARD, disabled=True,
                                         on_click=self.increase_dataframe_column)
        self.previous_column = ft.IconButton(icon=ft.icons.ARROW_BACK, disabled=True,
                                             on_click=self.decrease_dataframe_column)

        # Get y target
        self.columns_names = ft.Dropdown(on_change=self.update_option_selected, scale=0.8, label="Choose y target")
        self.y_target_name = ft.Text("")

        # File name
        self.file_name = None
        # Table for csv data frame
        self.table_data_frame = ft.DataTable(columns=[ft.DataColumn(ft.Text("Columns"))], rows=[ft.DataRow(cells=[
            ft.DataCell(ft.Text("Cells"))
        ])], border_radius=10, expand=True, border=ft.border.all(2, "grey"))

        # Number for data frame columns
        self.number_column = 6
        # How many columns to show in data frame
        self.show_columns = self.number_column
        # if we have many more than 8 columns, for next and prev buttons
        self.show_count = 0

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
        self.row_table_editing.controls.append(self.next_column)
        self.row_table_editing.controls.append(self.previous_column)

        self.row_table_editing.controls.append(self.columns_names)
        self.row_table_editing.controls.append(self.y_target_name)

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


    def update_next_prev(self):
        """Update next and prev buttons"""
        self.next_column.update()
        self.previous_column.update()

    def check_disable_next_prev(self):
        """Make next and prev buttons disable or able"""
        print("show col", self.show_columns)
        print("df len", len(self.data_frame_head.columns))
        if self.number_column <= self.show_columns < len(self.data_frame_head.columns):
            self.next_column.disabled = False
            self.previous_column.disabled = False
            self.update_next_prev()
        if self.show_columns >= len(self.data_frame_head.columns):
            self.next_column.disabled = True
            self.previous_column.disabled = False
            self.update_next_prev()
        if self.show_columns <= self.number_column:
            self.next_column.disabled = False
            self.previous_column.disabled = True
            self.update_next_prev()

    def increase_dataframe_column(self, e):
        """Adding new column which are not visible, works with button next"""
        self.show_columns += self.number_column
        self.show_count += self.number_column
        self.table_data_frame.columns = self.show_data_frame_columns(self.data_frame_head)
        self.table_data_frame.rows = self.show_data_frame_rows(self.data_frame_head)
        self.table_data_frame.update()
        self.check_disable_next_prev()

    def decrease_dataframe_column(self, e):
        """Subtracting column which are not visible, works with button previous"""
        self.show_columns -= self.number_column
        self.show_count -= self.number_column
        self.table_data_frame.columns = self.show_data_frame_columns(self.data_frame_head)
        self.table_data_frame.rows = self.show_data_frame_rows(self.data_frame_head)
        self.table_data_frame.update()
        self.check_disable_next_prev()

    def show_data_frame_columns(self, df: pd.DataFrame) -> list:
        """Return data frame columns"""
        return [ft.DataColumn(ft.Text(f"{header}, {dtype}")) for header, dtype in
                zip(df.columns[self.show_count:self.show_columns], df.dtypes[self.show_count:self.show_columns])]

    def show_data_frame_rows(self, df: pd.DataFrame) -> list:
        """Returns data frame rows"""
        rows = []
        for _, row in df.iterrows():
            cells = [ft.DataCell(ft.Text(str(row[header]))) for header in df.columns[self.show_count:self.show_columns]]
            rows.append(ft.DataRow(cells=cells))
        return rows

    def update_option_selected(self, e):
        self.y_target_name.value = self.columns_names.value
        self.y_target_name.update()
        print(self.columns_names)

    def represent_csv_file(self):
        """Represent csv file on the screen"""
        if self.file_name and self.file_name.endswith(".csv"):
            try:
                self.data_frame = pd.read_csv(self.file_name)
                print(self.data_frame.head())
                self.data_frame_head = self.data_frame.head()
                # Change DataTable into new columns with data
                self.table_data_frame.columns = self.show_data_frame_columns(self.data_frame_head)
                self.table_data_frame.rows = self.show_data_frame_rows(self.data_frame_head)
                self.table_data_frame.update()

                self.columns_count.value = f"Columns: {len(self.data_frame_head.columns)}"
                self.columns_count.update()
                self.rows_count.value = f"Rows: {len(self.data_frame_head)}"
                self.rows_count.update()

                self.columns_names.options = [ft.dropdown.Option(column) for column in self.data_frame_head.columns]
                self.columns_names.update()

                # X columns
                self.row_columns_name.controls.clear()
                for column in self.data_frame_head.columns:
                    checkbox = ft.Checkbox(label=column, value=column)
                    #print(checkbox.value)
                    self.row_columns_name.controls.append(checkbox)
                self.row_columns_name.update()
                print("checkbox", self.row_columns_name.data)


                self.check_disable_next_prev()


            except FileNotFoundError:
                print("File not found.")
            except Exception as e:
                print("An error occurred:", e)

