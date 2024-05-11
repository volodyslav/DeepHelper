import flet as ft


class FilePickerHelper:
    def __init__(self, page):
        self.page = page
        self.row_buttons = ft.Row(vertical_alignment="center")
        self.file_path = ft.Text("Selected path", expand=1)
        self.filepicker = ft.FilePicker(on_result=self.show_selected_path)

        open_button = ft.IconButton(icon=ft.icons.FOLDER_OPEN, on_click=self.select_file)
        self.row_buttons.controls.append(open_button)
        self.row_buttons.controls.append(self.file_path)

    def select_file(self, e: ft.FilePickerResultEvent):
        self.page.add(self.filepicker)
        self.filepicker.pick_files("Select File")

    def show_selected_path(self, e: ft.FilePickerResultEvent):
        file_name = e.files[0].path
        if file_name:
            self.file_path.value = file_name
            self.file_path.update()


def main(page: ft.Page):
    page.title = "Deep Helper"
    page.vertical_alignment = ft.MainAxisAlignment.START

    file_picker_helper = FilePickerHelper(page)
    page.add(file_picker_helper.row_buttons)


ft.app(main)
