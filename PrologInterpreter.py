import time
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import ctypes
import graphviz
from PIL import Image, ImageTk
from visual_automata.fa.dfa import VisualDFA
import automata.regex.regex as re

import lol


def is_file_path_selected(file_path):
    return file_path is not None and file_path != ""


def get_file_contents(file_path):
    """Return a string containing the file contents of the file located at the
    specified file path """
    with open(file_path, encoding="utf-8") as f:
        file_contents = f.read()

    return file_contents


class Foo(object):
    counter = 0

    def __call__(self):
        Foo.counter += 1


class Editor(object):
    def __init__(self, root_):

        self.root = root_
        self.file_path = None
        self.root.title("Prolog Interpreter")

        # Create a rule label

        self.rule_editor_label = Label(
            root, text="Prolog Rules: ", padx=10, pady=1
        )

        self.rule_editor_label.grid(
            sticky="W", row=0, column=0, columnspan=2, pady=3
        )

        # Create rule editor where we can edit the rules we want to enter:

        self.rule_editor = ScrolledText(
            root, width=100, height=30, padx=10, pady=10
        )

        self.rule_editor.grid(
            sticky=W + E, row=1, column=0, columnspan=2, padx=10
        )

        self.rule_editor.config(wrap="word", undo=True)

        self.rule_editor.focus()

        # Create a query label:

        self.query_label = Label(root, text="Prolog Query:", padx=10, pady=1)

        self.query_label.grid(sticky=W, row=2, column=0, columnspan=2, pady=3)

        # Create a Dfa label:

        self.query_label = Label(root, text="DFA:", padx=10, pady=1)

        self.query_label.grid(sticky=W, row=0, column=2, columnspan=2, pady=3)

        # Create the Prolog query editor we'll use to query our rules:

        self.query_editor = Text(root, width=77, height=2, padx=10, pady=10)

        self.query_editor.grid(sticky=W, row=3, column=0, pady=3, padx=10)

        self.query_editor.config(wrap="word", undo=True)

        # Create a run button which runs the query against our rules and outputs the
        # results in our solutions text box / editor.

        self.run_button = Button(
            root,
            text="Find Query Solutions",
            height=2,
            width=20,
            command=self.run_query,
        )
        self.drawdfabutton = Button(
            root,
            text="Draw DFA",
            height=2,
            width=20,
            command=self.draw_DFA,
        )
        self.drawparsetree = Button(
            root,
            text="Draw Parse tree",
            height=2,
            width=20,
            command=self.draw_ParseTree,
        )
        self.lol = Button(
            root,
            text="lolbutton",
            height=2,
            width=20,
            command=self.lol,
        )

        self.run_button.grid(sticky=E, row=3, column=1, pady=3, padx=10)
        self.drawdfabutton.grid(sticky=E, row=3, column=2, pady=3, padx=10)
        self.drawparsetree.grid(sticky=E, row=4, column=2, pady=3, padx=10)
        self.lol.grid(sticky=E, row=4, column=1, pady=3, padx=10)

        # Create a solutions label

        self.solutions_label = Label(
            root, text="Query Solutions:", padx=10, pady=1
        )

        self.solutions_label.grid(
            sticky="W", row=4, column=0, columnspan=2, padx=10, pady=3
        )

        # Create a text box which we'll use to display our Prolog query solutions:

        self.solutions_display = ScrolledText(
            root, width=100, height=5, padx=10, pady=10
        )

        self.solutions_display.grid(
            row=5, column=0, columnspan=2, padx=10, pady=7
        )

        image = Image.open('test-graphs/original.png')
        photo = ImageTk.PhotoImage(image)

        self.label1 = Label(root, image=photo)
        self.label1.image = photo
        self.label1.grid(row=1, column=2)

        menu_bar = Menu(root)
        # Finally, let's create the file menu
        self.menu_bar = self.create_file_menu(menu_bar)
        self.menu_bar = self.create_options_menu(menu_bar)

    def create_file_menu(self, menu_bar):
        """Create a menu which will allow us to open / save our Prolog rules, run our
        query, and exit our editor interface """

        # menu_bar = Menu(root)

        file_menu = Menu(menu_bar, tearoff=0)

        file_menu.add_command(
            label="Open...", underline=1, command=self.open_file
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Save", underline=1, command=self.save_file
        )
        file_menu.add_command(
            label="Save As...", underline=5, command=self.save_file_as
        )
        file_menu.add_separator()
        file_menu.add_command(label="Run", underline=1, command=self.run_query)

        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", underline=2, command=self.root.destroy
        )

        menu_bar.add_cascade(label="File", underline=0, menu=file_menu)

        self.root.config(menu=menu_bar)
        return menu_bar

    def create_options_menu(self, menu_bar):
        """Create a menu for night mode  """
        # menubar = Menu(root)
        optionsmenu = Menu(menu_bar, tearoff=0)

        optionsmenu.add_command(
            label="ThemeLight", underline=1, command=self.lighttheme
        )
        optionsmenu.add_command(
            label="ThemeDark", underline=1, command=self.DarkTheme
        )
        menu_bar.add_cascade(label="Options", underline=0, menu=optionsmenu)
        self.root.config(menu=menu_bar)
        return menu_bar

    def DarkTheme(self):
        root.tk.call("set_theme", "dark")

    def lighttheme(self):
        root.tk.call("set_theme", "light")

    def set_busy(self):
        # Show a busy cursor and update the UI
        self.root.config(cursor="watch")
        self.root.update()

    def set_not_busy(self):
        # Show a regular cursor
        self.root.config(cursor="")

    def draw_DFA(self):
        self.solutions_display.delete("1.0", END)
        self.solutions_display.insert(END, "DFA DRAWN")

        # Picture Holder

        photo1 = ImageTk.PhotoImage(Image.open('test-graphs/Digraph.png'))
        self.label1.config(image=photo1)
        self.label1.image = photo1

    def draw_ParseTree(self):
        self.solutions_display.delete("1.0", END)
        self.solutions_display.insert(END, "Parse Tree")

    def lol(self):
        query_text = self.query_editor.get(1.0, "end-1c")
        # Create an object instance of class "Foo," called "foo"
        f()
        if f.counter <= len(query_text):
            query1 = ""
            for i in range(f.counter):
                query1 = query1 + query_text[i]
                print(query1)
            self.dfa_create(query1)
        else:
            f.counter=0
            photo1 = ImageTk.PhotoImage(Image.open('test-graphs/original.png'))
            self.label1.config(image=photo1)
            self.label1.image = photo1



    def dfa_create(self, query_text):
        dfa = VisualDFA(
            states={"q0", "q1", "q2", "q3", "q4"},
            input_symbols={"0", "1"},
            transitions={
                "q0": {"0": "q3", "1": "q1"},
                "q1": {"0": "q3", "1": "q2"},
                "q2": {"0": "q3", "1": "q2"},
                "q3": {"0": "q4", "1": "q1"},
                "q4": {"0": "q4", "1": "q1"},
            },
            initial_state="q0",
            final_states={"q2", "q4"},
        )
        dfa.show_diagram(input_str=query_text, filename='Digraph', format_type="png", path="test-graphs", view=False)

        self.draw_DFA()

    def run_query(self):
        """Interpret the entered rules and query and display the results in the
        solutions text box """

        # Delete all of the text in our solutions display text box
        self.solutions_display.delete("1.0", END)

        # Fetch the raw rule / query text entered by the user
        rules_text = self.rule_editor.get(1.0, "end-1c")
        query_text = self.query_editor.get(1.0, "end-1c")
        print(len(query_text))
        query1 = ""
        for i in range(len(query_text)):
            query1 = query1 + query_text[i]
            print(query1)
            self.dfa_create(query1)
            time.sleep(0.2)

        # self.dfa_create(query_text)

        # # Create a new solver so we can try to query for solutions.
        # try:
        #     solver = Solver(rules_text)
        # except Exception as e:
        #     self.handle_exception("Error processing prolog rules.", str(e))
        #     return
        #
        # # Attempt to find the solutions and handle any exceptions gracefully
        # try:
        #     solutions = solver.find_solutions(query_text)
        # except Exception as e:
        #     self.handle_exception("Error processing prolog query.", str(e))
        #     return
        #
        # # If our query returns a boolean, we simply display a 'Yes' or a 'No'
        # # depending on its value
        # if isinstance(solutions, bool):
        #     self.solutions_display.insert(END, "Yes." if solutions else "No.")
        #
        # # Our solver returned a map, so we display the variable name to value mappings
        # elif isinstance(solutions, dict):
        #     self.solutions_display.insert(
        #         END,
        #         "\n".join(
        #             "{} = {}"
        #             # If our solution is a list contining one item, we show that
        #             # item, otherwise we display the entire list
        #             .format(variable, value[0] if len(value) == 1 else value)
        #             for variable, value in solutions.items()
        #         ),
        #     )
        # else:
        #
        #     # We know we have no matching solutions in this instance so we provide
        #     # relevant feedback
        #     self.solutions_display.insert(END, "No solutions found.")
        #
        # self.set_not_busy()

    def handle_exception(self, error_message, exception=""):
        """Handle the exception by printing an error message as well as exception in
        our solution text editor / display """
        self.solutions_display.insert(END, error_message + "\n")
        self.solutions_display.insert(END, str(exception) + "\n")
        self.set_not_busy()

    def set_rule_editor_text(self, text):
        self.rule_editor.delete(1.0, "end")
        self.rule_editor.insert(1.0, text)
        self.rule_editor.edit_modified(False)

    def open_file(self, file_path=None):

        # Open a a new file dialog which allows the user to select a file to open
        if file_path is None:
            file_path = filedialog.askopenfilename()

        if is_file_path_selected(file_path):
            file_contents = get_file_contents(file_path)

            # Set the rule editor text to contain the selected file contents
            self.set_rule_editor_text(file_contents)
            self.file_path = file_path

    def save_file(self):
        """If we have specified a file path, save the file - otherwise, prompt the
        user to specify the file location prior to saving the file """
        if self.file_path is None:
            result = self.save_file_as()
        else:
            result = self.save_file_as(file_path=self.file_path)

        return result

    def write_editor_text_to_file(self, file):
        editor_text = self.rule_editor.get(1.0, "end-1c")
        file.write(bytes(editor_text, "UTF-8"))
        self.rule_editor.edit_modified(False)

    def save_file_as(self, file_path=None):
        # If there is no file path specified, prompt the user with a dialog which
        # allows him/her to select where they want to save the file
        if file_path is None:
            file_path = filedialog.asksaveasfilename(
                filetypes=(
                    ("Text files", "*.txt"),
                    ("Prolog files", "*.pl *.pro"),
                    ("All files", "*.*"),
                )
            )

        try:

            # Write the Prolog rule editor contents to the file location
            with open(file_path, "wb") as file:
                self.write_editor_text_to_file(file)
                self.file_path = file_path
                return "saved"

        except FileNotFoundError:
            return "cancelled"

    def undo(self):
        self.rule_editor.edit_undo()

    def redo(self):
        self.rule_editor.edit_redo()


if __name__ == "__main__":
    root = Tk()
    root.tk.call("source", "Themes/azure.tcl")
    root.tk.call("set_theme", "dark")
    editor = Editor(root)
    root.iconbitmap("assets/icons8-python-96.ico")
    myappid = 'PrologInterpreter'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # Don't allow users to re-size the editor
    root.resizable(width=FALSE, height=FALSE)

    f =Foo()

    root.mainloop()