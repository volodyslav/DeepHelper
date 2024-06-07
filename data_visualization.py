import flet as ft
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

import threading


class DataVisualization:
    """Data Visualization of the data frame"""
    def __init__(self, page):
        self.page = page
        self.data_frame = None

        # Row for radio selection
        self.row_plot = ft.Row(alignment=ft.MainAxisAlignment.CENTER, height=50)

        # Rows for selecting right settings for a plot
        self.row_figure_size = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.row_figure_labels = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.row_draw_value = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # Slider width and height
        self.text_figure_size = ft.Text("Choose figure size", scale=1.2)

        self.width_slider = ft.Slider(min=5, max=30, divisions=25, label="{value}", value=5,
                                      on_change=self.change_width_height_sliders, tooltip="Figure width")
        self.height_slider = ft.Slider(min=5, max=30, divisions=25, label="{value}", value=5,
                                       on_change=self.change_width_height_sliders, tooltip="Figure height")
        # Grid add
        self.grid_checker = ft.Switch(value=False, label="Grid", on_change=self.change_grid_value)

        # Legend add
        self.legend_checker = ft.Switch(value=False, label="Legend", on_change=self.change_legend_value)

        # Get year when x value is date
        self.get_year_checker = ft.Switch(value=False, label="Get year", on_change=self.change_get_year)

        # Labels and title of the figure
        self.figure_title = ft.TextField(value="", label="Figure title", max_lines=2, max_length=50,
                                         on_change=self.change_labels)
        self.x_figure_label = ft.TextField(value="", label="X label", max_lines=2, max_length=50,
                                           on_change=self.change_labels)
        self.y_figure_label = ft.TextField(value="", label="Y label", max_lines=2, max_length=50,
                                           on_change=self.change_labels)

        # Button to draw a line
        self.draw_button = ft.IconButton(on_click=self.plot_data_frame, icon="draw", icon_color="blue", tooltip="Draw")

        # clear all data button
        self.clear_data_btn = ft.IconButton(on_click=self.clear_all, icon="delete", icon_color="red", tooltip="Clear")

        # Select a plotting
        self.label_plot = ft.Text("Choose a plot: ", scale=1.2)

        self.plot_radio = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="line", label="Line"),
            ft.Radio(value="scatter", label="Scatter"),
            ft.Radio(value="bar", label="Bar"),
            ft.Radio(value="pie", label="Pie")
        ]), on_change=self.change_radio, disabled=True)

        # X and Y for line
        self.x_value_line = ft.Dropdown(scale=0.8, label="Choose X value")
        self.y_value_line = ft.Column(alignment=ft.MainAxisAlignment.CENTER,
                                      wrap=True, height=200)
        self.y_value_text = ft.Text("Choose X values: ", scale=1.2)

        self.row_plot.controls.append(self.label_plot)
        self.row_plot.controls.append(self.plot_radio)

    def change_radio(self, e):
        self.delete_all_rows_data()
        self.draw_line_settings()
        if self.plot_radio.value not in ["bar", "pie"]:
            self.settings_to_add_y_value()

    def clear_all(self, e):
        """For clear button"""
        self.delete_all_rows_data()
        self.plot_radio.value = ""
        self.plot_radio.update()

    def delete_all_rows_data(self):
        """Clear all rows when needed"""
        self.row_figure_labels.controls.clear()
        self.row_figure_size.controls.clear()
        self.row_draw_value.controls.clear()
        self.row_figure_labels.update()
        self.row_draw_value.update()
        self.row_figure_size.update()

    def reset_data_frame(self):
        """Clear the data visualizer tab when the data frame is changed"""
        self.plot_radio.value = ""
        self.plot_radio.update()
        self.delete_all_rows_data()
        self.row_plot.update()

    def update_data_frame(self, df):
        """Update df from file picker helper"""
        self.data_frame = df
        self.plot_radio.disabled = False
        self.plot_radio.update()

    def draw_line_settings(self):
        """For line settings"""
        # For figure size
        self.row_figure_size.controls.append(self.text_figure_size)
        self.row_figure_size.controls.append(self.width_slider)
        self.row_figure_size.controls.append(self.height_slider)
        self.row_figure_size.controls.append(self.grid_checker)
        self.row_figure_size.controls.append(self.legend_checker)
        self.row_figure_size.controls.append(self.get_year_checker)
        self.row_figure_size.controls.append(self.draw_button)
        self.row_figure_size.controls.append(self.clear_data_btn)
        # For figure labels and titles
        self.row_figure_labels.controls.append(self.figure_title)
        self.row_figure_labels.controls.append(self.x_figure_label)
        self.row_draw_value.controls.append(self.x_value_line)

        self.row_figure_size.update()
        self.row_figure_labels.update()
        self.row_draw_value.update()
        # Show option of X and Y values

        self.x_value_line.options = [ft.dropdown.Option(column) for column in self.data_frame.columns]
        self.x_value_line.update()
        print(f"Y line = {self.x_value_line}")

    def settings_to_add_y_value(self):
        """Give y values"""
        # Draw if not equal to bar
        self.row_figure_labels.controls.append(self.y_figure_label)
        # For X nad Y value
        self.row_draw_value.controls.append(self.y_value_line)
        self.row_draw_value.update()
        self.row_figure_labels.update()
        self.y_value_line.controls.clear()
        for column in self.data_frame.columns:
            checkbox = ft.Checkbox(label=column, value=column, on_change=self.checkbox_changed, tooltip=f"Y value {column}")
            self.y_value_line.controls.append(checkbox)
        self.y_value_line.update()

    def checkbox_changed(self, e):
        # This method is called when any checkbox state changes
        self.update_selected_columns()

    def update_selected_columns(self):
        # Collect the labels of all checked checkboxes
        selected_columns = [checkbox.label for checkbox in self.y_value_line.controls if checkbox.value]
        print(f"Selected columns: {selected_columns}")

    def change_grid_value(self, e):
        """Add grid or not"""
        print(self.grid_checker.value)
        self.grid_checker.update()

    def change_legend_value(self, e):
        """Add grid or not"""
        print(self.legend_checker.value)
        self.legend_checker.update()

    def change_get_year(self, e):
        """Add grid or not"""
        print(self.get_year_checker.value)
        self.get_year_checker.update()

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
        if self.plot_radio.value != "":
            self.delete_all_rows_data()
            self.draw_line_settings()
        if self.plot_radio.value not in ["bar", "pie"]:
            self.settings_to_add_y_value()

    def draw_line(self):
        if self.data_frame is not None:
            threading.Thread(target=self.plot_data_frame).start()
        else:
            print("Data frame is None.")

    def plot_data_frame(self, e):
        if self.data_frame is not None:
            try:
                fig, ax = plt.subplots(figsize=(int(self.width_slider.value), int(self.height_slider.value)))
                # Choose a few x values to draw
                selected_columns = [checkbox.label for checkbox in self.y_value_line.controls if checkbox.value]

                # Change x value to date
                if self.get_year_checker.value:
                    self.data_frame[str(self.x_value_line.value)] = pd.to_datetime(self.data_frame[str(self.x_value_line.value)])

                if self.plot_radio.value == "line":
                    for column in selected_columns:
                        ax.plot(self.data_frame[str(self.x_value_line.value)], self.data_frame[str(column)],
                                label=column)
                elif self.plot_radio.value == "scatter":
                    for column in selected_columns:
                        ax.scatter(self.data_frame[str(self.x_value_line.value)], self.data_frame[str(column)],
                                   label=column)
                elif self.plot_radio.value == 'bar':
                    x_value_count = self.data_frame[self.x_value_line.value].value_counts()
                    print("X counts", x_value_count)
                    ax.bar(x_value_count.index, x_value_count.values, label=x_value_count.index)
                elif self.plot_radio.value == 'pie':
                    x_value_count = self.data_frame[self.x_value_line.value].value_counts()
                    print("X counts", x_value_count)
                    ax.pie(x_value_count.values, labels=x_value_count.index)
                ax.set_title(str(self.figure_title.value))
                ax.set_xlabel(str(self.x_figure_label.value))
                ax.set_ylabel(str(self.y_figure_label.value))
                ax.grid(bool(self.grid_checker.value))
                # Add legend only for line and scatter
                if bool(self.legend_checker.value) and self.plot_radio.value != "bar":
                    ax.legend()
                #plt.xticks(rotation=45)
                fig.savefig(f"line_plot.png")
                image = Image.open(f"line_plot.png")
                image.show()
                self.row_plot.update()
            except Exception as e:
                print("An error occurred:", e)
        else:
            print("Data frame is None.")


