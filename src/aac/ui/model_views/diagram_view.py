from tkinter import font, PanedWindow, Canvas, Text, Button, Frame, Label, LEFT, RIGHT, END, TOP
from tkinter.ttk import Notebook
from tkinter.font import BOLD


def get_diagram_view(parent_window: PanedWindow):
    tabs_notebook = Notebook(parent_window)

    diagram_tab = _get_diagram_tab_frame(tabs_notebook)
    properties_tab = _get_properties_tab_frame(tabs_notebook)
    imports_tab = _get_imports_tab_frame(tabs_notebook)

    tabs_notebook.add(diagram_tab, text="Diagram")
    tabs_notebook.add(properties_tab, text="Properties")
    tabs_notebook.add(imports_tab, text="Imports")
    return tabs_notebook


def _get_diagram_tab_frame(root_notebook: Notebook) -> Frame:
    diagram_frame = Frame(root_notebook)
    diagram_frame.pack(fill="both", expand=True)

    model_canvas = Canvas(diagram_frame)
    model_canvas.pack(side=TOP, fill="both", expand=True)

    # Replace these with the model diagram content
    model_canvas.create_line(0, 0, 2000, 1129)
    model_canvas.create_line(0, 960, 1700, 0)

    return diagram_frame


def _get_properties_tab_frame(root_notebook: Notebook) -> Frame:
    properties_frame = Frame(root_notebook)
    properties_frame.pack()

    # Properties Name Frame #
    properties_name_frame = Frame(properties_frame)
    properties_name_frame.pack(fill="x", expand=True, padx=25)

    properties_name_label = Label(properties_name_frame, text="Name")
    properties_name_label.pack(side=LEFT, padx=(0, 20))

    properties_name_text = Text(properties_name_frame, height=1)
    properties_name_text.insert(END, "A")
    properties_name_text.pack(side=RIGHT, fill="x", expand=True)

    # Properties Description Frame #
    properties_description_frame = Frame(properties_frame)
    properties_description_frame.pack(fill="x", expand=True, padx=25)

    properties_description_label = Label(properties_description_frame, text="Description")
    properties_description_label.pack(side=LEFT, padx=(0, 20))

    properties_description_text = Text(properties_description_frame, height=1)
    properties_description_text.insert(END, "")
    properties_description_text.pack(side=RIGHT, fill="x", expand=True)

    # Properties Components Frame #
    properties_components_frame = Frame(properties_frame)
    properties_components_frame.pack(fill="x", expand=True, padx=25)

    properties_components_label = Label(properties_components_frame, text="Components")
    properties_components_label.pack(side=LEFT, padx=(0, 20))

    properties_components_plus_button_font = font.Font(size=11, weight=BOLD)
    properties_components_plus_button = Button(properties_components_frame, text="+", command=not_implemented, font=properties_components_plus_button_font)
    properties_components_plus_button.pack(side=RIGHT)

    properties_components_text = Text(properties_components_frame, height=1)
    properties_components_text.insert(END, "Component 3")
    properties_components_text.pack(side=RIGHT, fill="x", expand=True, padx=(0, 20))

    # Properties Behavior Frame #
    properties_behavior_frame = Frame(properties_frame)
    properties_behavior_frame.pack(fill="x", expand=True, padx=25)

    properties_behavior_name_label = Label(properties_behavior_frame, text="Behavior")
    properties_behavior_name_label.pack(side=LEFT, padx=(0, 20))

    properties_behavior_plus_button_font = font.Font(size=11, weight=BOLD)
    properties_behavior_plus_button = Button(properties_behavior_frame, text="+", command=not_implemented, font=properties_behavior_plus_button_font)
    properties_behavior_plus_button.pack(side=RIGHT)

    properties_behavior_name_text = Text(properties_behavior_frame, height=1)
    properties_behavior_name_text.insert(END, "Behavior 2")
    properties_behavior_name_text.pack(side=RIGHT, fill="x", expand=True, padx=(0, 20))

    return properties_frame


def _get_imports_tab_frame(root_notebook: Notebook) -> Frame:
    imports_frame = Frame(root_notebook)
    imports_frame.pack()

    # Imports Name Frame #
    imports_name_frame = Frame(imports_frame)
    imports_name_frame.pack(side=TOP, fill="x", expand=True, padx=25)

    imports_name_label = Label(imports_name_frame, text="Name")
    imports_name_label.pack(side=LEFT, padx=(0, 20))

    imports_plus_button_font = font.Font(size=11, weight=BOLD)
    imports_plus_button = Button(imports_name_frame, text="+", command=not_implemented, font=imports_plus_button_font)
    imports_plus_button.pack(side=RIGHT)

    imports_name_text = Text(imports_name_frame, height=1)
    imports_name_text.insert(END, "")
    imports_name_text.pack(side=RIGHT, fill="x", expand=True, padx=(0, 20))

    return imports_frame


def not_implemented():
    print("Not implemented")
