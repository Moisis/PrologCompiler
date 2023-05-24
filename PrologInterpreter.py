import os
import time
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import ctypes
from PIL import Image, ImageTk
from visual_automata.fa.dfa import VisualDFA
import Scanner


def is_file_path_selected(file_path):
    return file_path is not None and file_path != ""


def get_file_contents(file_path):
    """Return a string containing the file contents of the file located at the
    specified file path """
    with open(file_path, encoding="utf-8") as f:
        file_contents = f.read()

    return file_contents


class Editor(object):
    def __init__(self, root_):

        self.root = root_
        self.file_path = None
        self.root.title("Prolog Interpreter")
        self.lol = 0
        self.arthcounter = 0
        self.relcounter = 0
        self.intcounter = 0
        self.realcounter = 0
        self.commcounter = 0
        self.varcounter = 0
        self.valuecounter = 0  # done
        self.prednamecounter = 0  # done
        self.stringcounter = 0  # done
        self.specialcounter = 0
        self.charCounter = 0  #

        # Create a rule label

        self.rule_editor_label = Label(
            root, text="Prolog Code: ", padx=10, pady=1
        )

        self.rule_editor_label.grid(
            sticky="W", row=0, column=0, columnspan=2, pady=3
        )

        # Create rule editor where we can edit the rules we want to enter:

        self.rule_editor = ScrolledText(
            root, width=100, height=30, padx=10, pady=10
        )

        self.rule_editor.grid(
            sticky=W + E, row=1, column=0, columnspan=3, padx=10
        )

        self.rule_editor.config(wrap="word", undo=True)

        self.rule_editor.focus()

        # Create a query label:

        # self.query_label = Label(root, text="Prolog Query:", padx=10, pady=1)
        #
        # self.query_label.grid(sticky=W, row=2, column=0, columnspan=2, pady=3)

        # Create a Dfa label:

        self.query_label = Label(root, text="DFA:", padx=10, pady=1)

        self.query_label.grid(sticky=W, row=0, column=4, pady=3)

        # Create the Prolog query editor we'll use to query our rules:

        # self.query_editor = Text(root, width=77, height=2, padx=10, pady=10)
        #
        # self.query_editor.grid(sticky=W, row=3, column=0, pady=3, padx=10)
        #
        # self.query_editor.config(wrap="word", undo=True)

        # Create a run button which runs the query against our rules and outputs the
        # results in our solutions text box / editor.

        self.run_button = Button(
            root,
            text="PARSE",
            height=2,
            width=20,
            command=self.run_query,
        )
        # self.drawdfabutton = Button(
        #     root,
        #     text="Start Animation",
        #     height=2,
        #     width=30,
        #     command=self.drawStepbystep,
        # )
        # self.drawparsetree = Button(
        #     root,
        #     text="Draw Parse tree",
        #     height=2,
        #     width=20,
        #     command=self.draw_ParseTree,
        # )
        # self.resetanima = Button(
        #     root,
        #     text="Reset Diagram",
        #     height=2,
        #     width=20,
        #     command=self.resetanimation,
        # )

        self.run_button.grid(sticky=E, row=3, column=0, padx=10)
        # self.drawdfabutton.grid(sticky=E, row=3, column=2, pady=3, padx=10)
        # self.drawparsetree.grid(sticky=E, row=4, column=2, pady=3, padx=10)
        # self.resetanima.grid(sticky=E, row=3, column=3, pady=3, padx=10)

        # Create a solutions label

        # self.solutions_label = Label(
        #     root, text="Query Solutions:", padx=10, pady=1
        # )

        # self.solutions_label.grid(
        #     sticky="W", row=4, column=0, columnspan=2, padx=10, pady=3
        # )

        # Create a text box which we'll use to display our Prolog query solutions:
        #
        # self.solutions_display = ScrolledText(
        #     root, width=100, height=5, padx=10, pady=10
        # )
        #
        # self.solutions_display.grid(
        #     row=5, column=0, columnspan=2, padx=10, pady=7
        # )

        image = Image.open('test-graphs/darkmodedfa.png')
        photo = ImageTk.PhotoImage(image)

        self.label1 = Label(root, image=photo)
        self.label1.image = photo
        self.label1.grid(row=1, column=4)

        # LABEL LEGEND

        self.diagraminputlabel = Label(root, text="MAP LEGEND ")

        self.diagrambox = Text(root, width=50, height=4)

        self.diagrambox.grid(sticky=W, row=1, column=6)

        self.diagrambox.config(state=DISABLED, undo=True)

        self.diagraminputlabel.grid(sticky=W, row=0, column=6, pady=3)

        # Testinput

        self.diagramLEGEND = Label(root, text="Test input", padx=10, pady=1)
        self.diagramLEGEND.grid(sticky=W, row=2, column=2, columnspan=2, pady=3)
        self.legend = Text(root, width=50, height=4, padx=10, pady=10)
        self.legend.grid(row=3, column=2, columnspan=2, padx=10, pady=7)

        menu_bar = Menu(root)

        # Finally, let's create the file menu
        self.menu_bar = self.create_file_menu(menu_bar)
        self.menu_bar = self.create_Function_menu(menu_bar)
        self.menu_bar = self.create_options_menu(menu_bar)

    def create_file_menu(self, menu_bar):
        """Create a menu which will allow us to open / save our Prolog rules, run our
        query, and exit our editor interface """

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

    def create_Function_menu(self, menu_bar):
        ##VARIABLE PREDNAME SYMBOL CHAR STRING SPECIAL BUTTONS REQUIRED MY HACKAR <3

        """Create a menu for night mode  """
        # menubar = Menu(root)
        functionmenu = Menu(menu_bar, tearoff=0)

        # functionmenu.add_command(
        #     label="Draw final DFA", underline=1, command=self.drawfinalDFA
        # )
        #
        # functionmenu.add_command(
        #     label="Cycle Through DFA animation", underline=1, command=self.drawStepbystep
        # )
        # functionmenu.add_separator()
        # functionmenu.add_command(
        #     label="Draw Parse Tree", underline=1, command=self.draw_ParseTree
        # )
        # functionmenu.add_separator()
        functionmenu.add_command(
            label="dfa_arithmetic_create", underline=1, command=self.dfa_arithmetic_createfinal
        )
        functionmenu.add_command(
            label="dfa_arithmetic_animate", underline=1, command=self.animatearthmetic
        )
        functionmenu.add_separator()

        functionmenu.add_command(
            label="dfa_relational_create", underline=1, command=self.dfa_relational_createfinal
        )
        functionmenu.add_command(
            label="dfa_relational_animate", underline=1, command=self.dfa_relational_animate
        )
        functionmenu.add_separator()
        functionmenu.add_command(
            label="dfa_integer_create", underline=1, command=self.dfa_integer_createfinal
        )
        functionmenu.add_command(
            label="dfa_integer_animate", underline=1, command=self.dfa_integer_animate
        )
        functionmenu.add_separator()
        functionmenu.add_command(
            label="dfa_real_create", underline=1, command=self.dfa_real_createfinal
        )
        functionmenu.add_command(
            label="dfa_real_animate", underline=1, command=self.dfa_real_animate
        )
        functionmenu.add_separator()
        # functionmenu.add_command(
        #     label="dfa_variable_create", underline=1, command=self.dfa_variable_createfinal
        # )
        # functionmenu.add_command(
        #     label="dfa_variable_animate", underline=1, command=self.dfa_variable_animate
        # )
        # functionmenu.add_separator()
        functionmenu.add_command(
            label="dfa_comment_create", underline=1, command=self.dfa_comment_createfinal
        )
        functionmenu.add_command(
            label="dfa_comment_create", underline=1, command=self.dfa_comment_animate
        )

        menu_bar.add_cascade(label="DFAS 1", underline=0, menu=functionmenu)
        self.root.config(menu=menu_bar)
        return menu_bar

    def DarkTheme(self):
        root.tk.call("set_theme", "dark")
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        photo1 = ImageTk.PhotoImage(Image.open('test-graphs/darkmodedfa.png'))
        self.label1.config(image=photo1)
        self.label1.image = photo1

    def lighttheme(self):
        root.tk.call("set_theme", "light")
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        photo1 = ImageTk.PhotoImage(Image.open('test-graphs/lightmodedfa.png'))
        self.label1.config(image=photo1)
        self.label1.image = photo1

    def set_busy(self):
        # Show a busy cursor and update the UI
        self.root.config(cursor="watch")
        self.root.update()

    def set_not_busy(self):
        # Show a regular cursor
        self.root.config(cursor="")

    def draw_DFA(self):
        # Picture Holder

        photo1 = ImageTk.PhotoImage(Image.open('test-graphs/Digraph.png'))
        self.label1.config(image=photo1)
        self.label1.image = photo1

    # test sample
    def drawfinalDFA(self):

        query_text = self.diagrambox.get(1.0, "end-1c")
        self.dfa_create(query_text)
        self.draw_DFA()

        # Picture Holder

        photo1 = ImageTk.PhotoImage(Image.open('test-graphs/Digraph.png'))
        self.label1.config(image=photo1)
        self.label1.image = photo1

    def draw_ParseTree(self):
        print()

    def resetanimation(self):
        photo1 = ImageTk.PhotoImage(Image.open('test-graphs/original.png'))
        self.label1.config(image=photo1)
        self.label1.image = photo1

    def drawStepbystep(self):
        # f()
        self.lol += 1
        query_text = self.diagrambox.get(1.0, "end-1c")
        if self.lol > (len(query_text)):
            self.lol = 0

        else:
            query1 = ""
            for i in range(self.lol):
                query1 = query1 + query_text[i]
                print(query1)
                self.dfa_create(query1)
                self.draw_DFA()
            time.sleep(0.8)
            root.update()
            self.drawStepbystep()

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

    # arth
    def animatearthmetic(self):
        alphabetcaps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        alphabetsmall = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        arthemticoperators = ['*', '/', '+', '-']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Operaters(P) : * | / | + | - \n")
        self.diagrambox.insert(END, "Others(L) : [0-9] | [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | =")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_arithmetic_create(query)
            self.draw_DFA()
        self.arthcounter += 1
        if self.arthcounter > (len(query)):
            self.arthcounter = 0
        else:
            quert = ""
            for i in range(self.arthcounter):
                if (query[i] in arthemticoperators):
                    quert = quert + 'P'
                    print(quert)
                    self.dfa_arithmetic_create(quert)
                    self.draw_DFA()
                else:
                    quert = quert + 'L'
                    print(quert)
                    self.dfa_arithmetic_create(quert)
                    self.draw_DFA()

            time.sleep(0.8)
            root.update()
            self.animatearthmetic()

    def dfa_arithmetic_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Operaters(P) : * | / | + | - \n")
        self.diagrambox.insert(END, "Others(L) : [0-9] | [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | =")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_arithmetic_create(query2)
        arthemticoperators = ['*', '/', '+', '-']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in arthemticoperators):
                query3 = query3 + 'P'
            else:
                query3 = query3 + 'L'

        self.dfa_arithmetic_create(query3)
        self.draw_DFA()

    def dfa_arithmetic_create(self, querytext):
        dfa = VisualDFA(
            # [A-Za-z . * - + / ; : _ % ( ) < > = ]   < >
            states={"q0", "q1", "qD"},
            # input_symbols={"* / + -", "[A-Z a-z 0-9 .  ; : _ % ( ) < > = ]"},
            input_symbols={"P", "L"},
            transitions={
                # "q0": {"* / + -": "q1", "[A-Z a-z 0-9 .  ; : _ % ( ) < > = ]": "qD"},
                # "q1": {"* / + -": "qD", "[A-Z a-z 0-9 .  ; : _ % ( ) < > = ]": "qD"},
                #  "qD": {"* / + -": "qD", "[A-Z a-z 0-9 .  ; : _ % ( ) < > = ]": "qD"},
                "q0": {"P": "q1", "L": "qD"},
                "q1": {"P": "qD", "L": "qD"},
                "qD": {"P": "qD", "L": "qD"},
                # "q0": {"a": "q1", "b": "qD"},
                # "q1": {"a": "qD", "b": "qD"},
                # "qD": {"a": "qD", "b": "qD"},
            },
            initial_state="q0",
            final_states={"q1"},
        )
        dfa.show_diagram(input_str=querytext, filename='Digraph', format_type="png", path="test-graphs", view=False)

    # char
    def dfa_char_create(self, query_text):
        dfa = VisualDFA(
            states={"q0", "q1", "qD"},
            input_symbols={"[A-Z] | [a-z]", "[0-9] |.| * |- | + | / | ; | : | _ | % | ( | ) | < | > | ="},
            transitions={

                "q0": {"[A-Z] | [a-z]": "q1", "[0-9] |.| * |- | + | / | ; | : | _ | % | ( | ) | < | > | =": "qD"},
                "q1": {"[A-Z] | [a-z]": "qD", "[0-9] |.| * |- | + | / | ; | : | _ | % | ( | ) | < | > | =": "qD"},
                "qD": {"[A-Z] | [a-z]": "qD", "[0-9] |.| * |- | + | / | ; | : | _ | % | ( | ) | < | > | =": "qD"},

            },
            initial_state="q0",
            final_states={"q1"},
        )
        dfa.show_diagram(input_str=query_text, filename='Digraph', format_type="png", path="test-graphs", view=False)

    def dfa_char_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Characters(C): [A-Z] [a-z]")
        self.diagrambox.insert(END, "Others(!) : [0-9] | . | ; | : | _ | % | ( | ) | < | > | =")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_char_create(query2)
        alphabetcaps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        alphabetsmall = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in alphabetcaps or query2[i] in alphabetsmall):
                query3 = query3 + query2[i]
            else:
                query3 = query3 + '!'

        self.dfa_char_create(query3)
        self.draw_DFA()

    def dfa_char_animate(self):

        alphabetcaps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        alphabetsmall = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Operaters(O) : [A-Z] [a-z] ")
        self.diagrambox.insert(END, "Others(!) : [0-9] | . | ; | : | _ | % | ( | ) | * | / | + | -")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_char_create(query)
            self.draw_DFA()
        self.charCounter += 1
        if self.charCounter > (len(query)):
            self.charcounter = 0
        else:
            quert = ""
            for i in range(self.charCounter):
                if (query[i] in alphabetsmall or query[i] in alphabetcaps):
                    quert = quert + query[i]
                    print(quert)
                    self.dfa_char_create(quert)
                    self.draw_DFA()
                else:
                    quert = quert + '!'
                    print(quert)
                    self.dfa_char_create(quert)
                    self.draw_DFA()

            time.sleep(0.8)
            root.update()
            self.dfa_char_animate()

    # string

    def dfa_string_create(self, query_text):
        dfa = VisualDFA(
            states={"q0", "q1", "q2", "qD"},
            input_symbols={'\"', "[A-Z] | [a-z] | [0-9] | * | - | + | / | ; | : | _ | % | ( | ) | < | > | ="},
            transitions={
                "q0": {'\"': "q1", "[A-Z] | [a-z] | [0-9] | * | - | + | / | ; | : | _ | % | ( | ) | < | > | =": "qD"},
                "q1": {'\"': "q2", "[A-Z] | [a-z] | [0-9] | * | - | + | / | ; | : | _ | % | ( | ) | < | > | =": "q1"},
                "qD": {'\"': "qD", "[A-Z] | [a-z] | [0-9] | * | - | + | / | ; | : | _ | % | ( | ) | < | > | =": "qD"}

            },
            initial_state="q0",
            final_states={"q2"},
        )
        dfa.show_diagram(input_str=query_text, filename='Digraph', format_type="png", path="test-graphs", view=False)

        def dfa_string_createfinal(self):
            self.diagrambox.config(state=NORMAL)
            self.diagrambox.delete("1.0", END)
            self.diagrambox.insert(END, "String Operaters(S) : \"")
            self.diagrambox.insert(END,
                                   "Others(!) : [0-9] | [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | = | * | / | + | -")
            self.diagrambox.config(state=DISABLED)
            query2 = self.legend.get(1.0, "end-1c")
            if (query2 == ''):
                self.dfa_string_create(query2)
            stringoperators = ['\"']
            query3 = ''
            for i in range(len(query2)):
                if (query2[i] in stringoperators):
                    query3 = query3 + "\""
                else:
                    query3 = query3 + '!'

            self.dfa_string_create(query3)
            self.draw_DFA()

        def dfa_string_animate(self):

            stringOperators = ['\"']

            self.diagrambox.config(state=NORMAL)
            self.diagrambox.delete("1.0", END)
            self.diagrambox.insert(END, "String(S) : \"")
            self.diagrambox.insert(END,
                                   "Others(!) : [0-9] | [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | * | / | + | - \n")
            self.diagrambox.config(state=DISABLED)
            query = self.legend.get(1.0, "end-1c")
            if (query == ''):
                self.dfa_string_create(query)
                self.draw_DFA()
            self.stringcounter += 1
            if self.stringcounter > (len(query)):
                self.stringcounter = 0
            else:
                quert = ""
                for i in range(self.stringcounter):
                    if (query[i] in stringOperators):
                        quert = quert + "\""
                        print(quert)
                        self.dfa_string_create(quert)
                        self.draw_DFA()
                    else:
                        quert = quert + '!'
                        print(quert)
                        self.dfa_string_create(quert)
                        self.draw_DFA()

                time.sleep(0.8)
                root.update()
                self.dfa_string_animate()
        # Relational

    def dfa_relational_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "String Operaters(S) : \"")
        self.diagrambox.insert(END,
                               "Others(!) : [0-9] | [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | = | * | / | + | -")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_string_create(query2)
        stringoperators = ['\"']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in stringoperators):
                query3 = query3 + query2[i]
            else:
                query3 = query3 + '!'

        self.dfa_string_create(query3)
        self.draw_DFA()

    # Relational
    def dfa_relational_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Operaters(O) : * | / | + | - \n")
        self.diagrambox.insert(END, "Others(!) : [0-9] | [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | =")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_relational_create(query2)
        relationaloperators = ['<', '=', '>']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in relationaloperators):
                query3 = query3 + query2[i]
            else:
                query3 = query3 + '!'

        self.dfa_relational_create(query3)
        self.draw_DFA()

    def dfa_relational_animate(self):

        alphabetcaps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        alphabetsmall = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']

        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        relationaloperators = ['<', '=', '>']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Operaters(O) : < | > | =  \n")
        self.diagrambox.insert(END, "Others(!) : [0-9] | [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | * | / | + | -")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_relational_create(query)
            self.draw_DFA()
        self.relcounter += 1
        if self.relcounter > (len(query)):
            self.relcounter = 0
        else:
            quert = ""
            for i in range(self.relcounter):
                if (query[i] in relationaloperators):
                    quert = quert + query[i]
                    print(quert)
                    self.dfa_relational_create(quert)
                    self.draw_DFA()
                else:
                    quert = quert + '!'
                    print(quert)
                    self.dfa_relational_create(quert)
                    self.draw_DFA()

            time.sleep(0.8)
            root.update()
            self.dfa_relational_animate()

    def dfa_relational_create(self, string_query):
        dfa = VisualDFA(
            # [A-Za-z . * - + / ; : _ % ( ) < > = ]   <= >= :- <>
            states={"q0", "q1", "q2", "q3", "q4", "q5", "qD"},
            input_symbols={"<", ">", "=", "!"},
            transitions={
                "q0": {"<": "q1", ">": "q3", "=": "q2",
                       "!": "qD"},
                "q1": {"<": "qD", ">": "q4", "=": "q4",
                       "!": "qD"},
                "q2": {"<": "qD", ">": "qD", "=": "qD",
                       "!": "qD"},
                "q3": {"<": "qD", ">": "qD", "=": "q5",
                       "!": "qD"},
                "q4": {"<": "qD", ">": "qD", "=": "qD",
                       "!": "qD"},
                "q5": {"<": "qD", ">": "qD", "=": "qD",
                       "!": "qD"},
                "qD": {"<": "qD", ">": "qD", "=": "qD",
                       "!": "qD"},

            },
            initial_state="q0",
            final_states={"q1", "q2", "q3", "q4", "q5"},
        )
        dfa.show_diagram(input_str=string_query, filename='Digraph', format_type="png", path="test-graphs", view=False)

    # integer
    def dfa_integer_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Numbers (N) : 0-9 \n")
        self.diagrambox.insert(END,
                               "Others(!) :  [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_arithmetic_create(query2)
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in nums):
                query3 = query3 + 'N'
            else:
                query3 = query3 + '!'

        self.dfa_integer_create(query3)
        self.draw_DFA()

    def dfa_integer_animate(self):
        alphabetcaps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        alphabetsmall = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        arthemticoperators = ['*', '/', '+', '-']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Numbers(N) : 0-9 \n")
        self.diagrambox.insert(END, "Others(!): [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_integer_create(query)
            self.draw_DFA()
        self.intcounter += 1
        if self.intcounter > (len(query)):
            self.intcounter = 0
        else:
            quert = ""
            for i in range(self.intcounter):
                if (query[i] in nums):
                    quert = quert + 'N'
                    print(quert)
                    self.dfa_integer_create(quert)
                    self.draw_DFA()
                else:
                    quert = quert + '!'
                    print(quert)
                    self.dfa_integer_create(quert)
                    self.draw_DFA()

            time.sleep(0.8)
            root.update()
            self.dfa_integer_animate()

    def dfa_integer_create(self, string_query):
        dfa = VisualDFA(
            # [A-Za-z . * - + / ; : _ % ( ) < > = ]   <= >= :- <>
            states={"q0", "q1", "qD"},
            input_symbols={"N", "!"},
            transitions={
                "q0": {"N": "q1", "!": "qD"},
                "q1": {"N": "q1", "!": "qD"},
                "qD": {"N": "qD", "!": "qD"},

            },
            initial_state="q0",
            final_states={"q1"},
        )
        dfa.show_diagram(input_str=string_query, filename='Digraph', format_type="png", path="test-graphs", view=False)

    # real
    def dfa_real_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Numbers (N) : 0-9 . \n")
        self.diagrambox.insert(END,
                               "Others(!) :  [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_real_create(query2)
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in nums):
                query3 = query3 + 'N'
            elif (query2[i] == '.'):
                query3 = query3 + '.'
            else:
                query3 = query3 + '!'

        self.dfa_real_create(query3)
        self.draw_DFA()

    def dfa_real_animate(self):
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Numbers(N) : 0-9 \n")
        self.diagrambox.insert(END, "Others(!): [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_real_create(query)
            self.draw_DFA()
        self.realcounter += 1
        if self.realcounter > (len(query)):
            self.realcounter = 0
        else:
            quert = ""
            for i in range(self.realcounter):
                if (query[i] in nums):
                    quert = quert + 'N'
                    print(quert)
                    self.dfa_real_create(quert)
                    self.draw_DFA()

                elif (query[i] == '.'):
                    quert = quert + '.'
                    print(quert)
                    self.dfa_real_create(quert)
                    self.draw_DFA()

                else:
                    quert = quert + '!'
                    print(quert)
                    self.dfa_real_create(quert)
                    self.draw_DFA()

            time.sleep(0.8)
            root.update()
            self.dfa_real_animate()

    def dfa_real_create(self, query_string):
        dfa = VisualDFA(
            # [A-Za-z . * - + / ; : _ % ( ) < > = ]   <= >= :- <>
            states={"q0", "q1", "q2", "q3", "qD"},
            input_symbols={"N", ".", "!"},
            transitions={
                "q0": {"N": "q1", ".": "qD",
                       "!": "qD"},
                "q1": {"N": "q1", ".": "q2",
                       "!": "qD"},
                "q2": {"N": "q3", ".": "qD",
                       "!": "qD"},
                "q3": {"N": "q3", ".": "qD",
                       "!": "qD"},
                "qD": {"N": "qD", ".": "qD",
                       "!": "qD"},

            },
            initial_state="q0",
            final_states={"q3"},
        )
        dfa.show_diagram(input_str=query_string, filename='Digraph', format_type="png", path="test-graphs", view=False)

    # variable
    def dfa_value_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Lowercase(a): a-z \n")
        self.diagrambox.insert(END, "Uppercase & Numbers(Z): 0-9 A-Z \n")
        self.diagrambox.insert(END,
                               "Others(!): . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_value_create(query2)
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                     'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in lowercase):
                query3 = query3 + 'a'
            elif (query2[i] in uppercase or query2[i] in nums):
                query3 = query3 + 'Z'
            else:
                query3 = query3 + '!'

        self.dfa_value_create(query3)
        self.draw_DFA()

    def dfa_value_animate(self):
        uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                     'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z']
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        arthemticoperators = ['*', '/', '+', '-']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Lowercase(a): a-z \n")
        self.diagrambox.insert(END, "Uppercase & Numbers(Z): 0-9 A-Z \n")
        self.diagrambox.insert(END,
                               "Others(!): . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")

        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_value_create(query)
            self.draw_DFA()
        self.valuecounter += 1
        if self.valuecounter > (len(query)):
            self.valuecounter = 0
        else:
            quert = ""
            for i in range(self.valuecounter):
                if (query[i] in lowercase):
                    quert = quert + 'a'
                    print(quert)
                    self.dfa_value_create(quert)
                    self.draw_DFA()
                elif (query[i] in uppercase or query[i] in nums):
                    quert = quert + 'Z'
                    print(quert)
                    self.dfa_value_create(quert)
                    self.draw_DFA()

                else:
                    quert = quert + '!'
                    print(quert)
                    self.dfa_value_create(quert)
                    self.draw_DFA()

            #            if (query2[i] in lowercase):
            #                 query3 = query3 + query2[i]
            #             elif (query2[i] in uppercase or query2[i] in nums):
            #                 query3 = query3 + query2[i]

            time.sleep(0.8)
            root.update()
            self.dfa_value_animate()

    def dfa_value_create(self, string_query):
        dfa = VisualDFA(
            # [A-Za-z . * - + / ; : _ % ( ) < > = ]   <= >= :- <>
            states={"q0", "q1", "q2", "qD"},
            input_symbols={"a", "Z", "!"},
            transitions={
                "q0": {"a": "q1", "Z": "qD", "!": "qD"},
                "q1": {"a": "q1", "Z": "q1", "!": "qD"},
                "qD": {"a": "qD", "Z": "qD", "!": "qD"},

            },
            initial_state="q0",
            final_states={"q1"},
        )
        dfa.show_diagram(input_str=string_query, filename='Digraph', format_type="png", path="test-graphs", view=False)

    def dfa_predname_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Lowercase(a) : a-z \n")
        self.diagrambox.insert(END, "Others(!) : [0-9] | [A-Z] | * | / | + | - | . | ; | : | _ | % | ( | ) | < | > | =")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_predname_create(query2)
        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in lowercase):
                query3 = query3 + 'a'
            else:
                query3 = query3 + '!'

        self.dfa_predname_create(query3)
        self.draw_DFA()

    def dfa_predname_animate(self):

        alphabetcaps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        alphabetsmall = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']

        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Lowercase(a) : a-z \n")
        self.diagrambox.insert(END, "Others(!) : [0-9] | [A-Z] | < | > | = | . | ; | : | _ | % | ( | ) | * | / | + | -")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_predname_create(query)
            self.draw_DFA()
        self.prednamecounter += 1
        if self.prednamecounter > (len(query)):
            self.prednamecounter = 0
        else:
            quert = ""
            for i in range(self.prednamecounter):
                if (query[i] in lowercase):
                    quert = quert + 'a'
                    print(quert)
                    self.dfa_predname_create(quert)
                    self.draw_DFA()
                else:
                    quert = quert + '!'
                    print(quert)
                    self.dfa_predname_create(quert)
                    self.draw_DFA()

            time.sleep(0.8)
            root.update()
            self.dfa_predname_animate()

    def dfa_predname_create(self, query_string):
        dfa = VisualDFA(
            # [A-Za-z . * - + / ; : _ % ( ) < > = ]   <= >= :- <>
            states={"q0", "q1", "qD"},
            input_symbols={"[a-z]", "!"},
            transitions={
                "q0": {"a": "q1", "!": "qD"},
                "q1": {"a": "q1", "!": "qD"},
                "qD": {"a": "qD", "!": "qD"},

            },
            initial_state="q0",
            final_states={"q1"},
        )
        dfa.show_diagram(input_str=query_string, filename='Digraph', format_type="png", path="test-graphs", view=False)

    # variable begad
    def dfa_variable_createfinal(self):
        # "_", "[A-Z]", "[a-z] | [0-9]",".| * | - | + | / | ; | : \ % | ( | ) | < | > | ="}
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Uppercase(A): A-Z \n")
        self.diagrambox.insert(END, "Lowercase & Numbers(z): a-z 0-9 \n")
        self.diagrambox.insert(END,
                               "Others(!): .| * | - | + | / | ; | : \ % | ( | ) | < | > | =")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_variable_create(query2)
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                     'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in uppercase):
                query3 = query3 + 'A'

            elif (query2[i] == '_'):
                query3 = query3 + '_'

            elif (query2[i] in lowercase or query2[i] in nums):
                query3 = query3 + 'z'
            else:
                query3 = query3 + '!'

        self.dfa_variable_create(query3)
        self.draw_DFA()

    def dfa_variable_animate(self):
        uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                     'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z']
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        arthemticoperators = ['*', '/', '+', '-']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Uppercase(A): A-Z \n")
        self.diagrambox.insert(END, "Lowercase & Numbers(z): a-z 0-9 \n")
        self.diagrambox.insert(END,
                               "Others(!): . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_variable_create(query)
            self.draw_DFA()
        self.varcounter += 1
        if self.varcounter > (len(query)):
            self.varcounter = 0
        else:
            quert = ""
            for i in range(self.varcounter):
                if (query[i] in uppercase):
                    quert = quert + 'A'
                    print(quert)
                    self.dfa_variable_create(quert)
                    self.draw_DFA()

                elif (query[i] == '_'):
                    quert = quert + '_'
                    print(quert)
                    self.dfa_variable_create(quert)
                    self.draw_DFA()


                elif (query[i] in lowercase or query[i] in nums):
                    quert = quert + 'z'
                    print(quert)
                    self.dfa_variable_create(quert)
                    self.draw_DFA()

                else:
                    quert = quert + '!'
                    print(quert)
                    self.dfa_variable_create(quert)
                    self.draw_DFA()

            #            if (query2[i] in lowercase):
            #                 query3 = query3 + query2[i]
            #             elif (query2[i] in uppercase or query2[i] in nums):
            #                 query3 = query3 + query2[i]

            time.sleep(0.8)
            root.update()
            self.dfa_variable_animate()

    def dfa_variable_create(self, query_string):
        dfa = VisualDFA(
            # [A-Za-z . * - + / ; : _ % ( ) < > = ]   <= >= :- <>
            states={"q0", "q1", "q2", "qD"},
            input_symbols={"_", "A", "z", "!"},
            transitions={

                "q0": {"_": "q2", "A": "q1", "z": "qD", "!": "qD"},
                "q1": {"_": "q1", "A": "q1", "z": "q1", "!": "qD"},
                "q2": {"_": "q2", "A": "q1", "z": "q1", "!": "qD"},
                "qD": {"_": "qD", "A": "qD", "z": "qD", "!": "qD"},

            },
            initial_state="q0",
            final_states={"q1"},
        )
        dfa.show_diagram(input_str=query_string, filename='Digraph', format_type="png", path="test-graphs", view=False)

    def dfa_special_create(self, query_text):

        dfa = VisualDFA(
            states={"q0", "q1", "q2", "qD"},
            input_symbols={"S", ":", "-", "[A-Z] | [a-z] | [0-9] | * | + | / | _ | % | < | > | ="},
            transitions={
                "q0": {"S": "q1", ":": "qD", "-": "qD", "[A-Z] | [a-z] | [0-9] | * | + | / | _ | % | < | > | =": "qD"},
                "q1": {"S": "qD", ":": "qD", "-": "qD", "[A-Z] | [a-z] | [0-9] | * | + | / | _ | % | < | > | =": "qD"},
                "q2": {"S": "qD", ":": "qD", "-": "q2", "[A-Z] | [a-z] | [0-9] | * | + | / | _ | % | < | > | =": "qD"},
                "qD": {"S": "qD", ":": "qD", "-": "qD", "[A-Z] | [a-z] | [0-9] | * | + | / | _ | % | < | > | =": "qD"},

            },
            initial_state="q0",
            final_states={"q1", "q2"},
        )

        dfa.show_diagram(input_str=query_text, filename='Digraph', format_type="png", path="test-graphs", view=False)

    def dfa_special_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Special Characters (S) : - ;  .  ,  (  )")
        self.diagrambox.insert(END,
                               "Others(X) : [0-9] [A-Z] | [a-z] | _ | % | ( | ) | < | > | = | + | / | *")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_comment_create(query2)
        specialoperators = [';', '.', ',', '(', ')']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in specialoperators):
                query3 = query3 + 'S'
            elif query2[i] == ':':
                query3 = query3 + ':'

            elif query2[i] == '-':
                query3 = query3 + '-'

            else:
                query3 = query3 + 'X'

        self.dfa_special_create(query3)
        self.draw_DFA()

    def dfa_special_animate(self):
        specialoperators = [';', '.', ',', '(', ')']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Special Characters(S) : : - ;  .  ,  (  )")
        self.diagrambox.insert(END, "Others(!): [A-Z] | [a-z] | _ | % | ( | ) | < | > | = | + | / | *")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_special_create(query)
            self.draw_DFA()
        self.specialcounter += 1
        if self.specialcounter > (len(query)):
            self.specialcounter = 0
        else:
            quert = ""
            for i in range(self.specialcounter):
                if (query[i] in specialoperators):
                    quert = quert + 'S'
                    print(quert)
                    self.dfa_special_create(quert)
                    self.draw_DFA()

                elif query[i] == ':':
                    quert = quert + ':'
                    print(quert)
                    self.dfa_special_create(quert)
                    self.draw_DFA()

                elif query[i] == '-':
                    quert = quert + '-'
                    print(quert)
                    self.dfa_special_create(quert)
                    self.draw_DFA()
                else:
                    quert = quert + 'X'
                    print(quert)
                    self.dfa_special_create(quert)
                    self.draw_DFA()

            time.sleep(0.8)
            root.update()
            self.dfa_special_animate()

    # comment
    def dfa_comment_createfinal(self):
        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Comment Operators (C) : % / * \n")
        self.diagrambox.insert(END,
                               "Others(X) : [0-9] [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")
        self.diagrambox.config(state=DISABLED)
        query2 = self.legend.get(1.0, "end-1c")
        if (query2 == ''):
            self.dfa_comment_create(query2)
        commentoperators = ['*', '/', '%']
        query3 = ''
        for i in range(len(query2)):
            if (query2[i] in commentoperators):
                query3 = query3 + commentoperators[i]
            else:
                query3 = query3 + 'X'

        self.dfa_comment_create(query3)
        self.draw_DFA()

    def dfa_comment_animate(self):
        commentoperators = ['*', '/', '%' , '\n']

        self.diagrambox.config(state=NORMAL)
        self.diagrambox.delete("1.0", END)
        self.diagrambox.insert(END, "Numbers(N) : 0-9 \n")
        self.diagrambox.insert(END, "Others(!): [A-Z] | [a-z] | . | ; | : | _ | % | ( | ) | < | > | = | + | - | / | *")
        self.diagrambox.config(state=DISABLED)
        query = self.legend.get(1.0, "end-1c")
        if (query == ''):
            self.dfa_comment_create(query)
            self.draw_DFA()
        self.commcounter += 1
        if self.commcounter > (len(query)):
            self.commcounter = 0
        else:
            quert = ""
            for i in range(self.commcounter):
                if (query[i] in commentoperators):
                    quert = quert + query[i]
                    print(quert)
                    self.dfa_comment_create(quert)
                    self.draw_DFA()
                else:
                    quert = quert + 'X'
                    print(quert)
                    self.dfa_comment_create(quert)
                    self.draw_DFA()

            time.sleep(0.8)
            root.update()
            self.dfa_comment_animate()

    def dfa_comment_create(self, query_string):
        dfa = VisualDFA(
            # [A-Za-z . * - + / ; : _ % ( ) < > = ]   <= >= :- <>
            states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "qD"},
            input_symbols={"%", "/", "*", "\n", "X"},
            transitions={

                "q0": {"%": "q1", "/": "q3", "*": "qD", "\n": "q1", "X": "qD"},
                "q1": {"%": "q1", "/": "q1", "*": "q1", "\n": "q2", "X": "q1"},
                "q2": {"%": "q2", "/": "qD", "*": "qD", "\n": "q2", "X": "qD"},
                "q3": {"%": "qD", "/": "qD", "*": "q4", "\n": "qD", "X": "qD"},
                "q4": {"%": "q4", "/": "q4", "*": "q5", "\n": "q4", "X": "q4"},
                "q5": {"%": "q4", "/": "q6", "*": "q5", "\n": "q4", "X": "q4"},
                "q6": {"%": "q4", "/": "q4", "*": "q5", "\n": "q4", "X": "q4"},
                "qD": {"%": "qD", "/": "qD", "*": "qD", "\n": "qD", "X": "qD"},
            },
            initial_state="q0",
            final_states={"q2", "q6"},
        )
        dfa.show_diagram(input_str=query_string, filename='Digraph', format_type="png", path="test-graphs", view=False)

    def run_query(self):
        code = self.rule_editor.get(1.0, "end-1c")
        print(code)
        Scanner.Scan(code)





    # def handle_exception(self, error_message, exception=""):
    #     """Handle the exception by printing an error message as well as exception in
    #     our solution text editor / display """
    #     self.solutions_display.insert(END, error_message + "\n")
    #     self.solutions_display.insert(END, str(exception) + "\n")
    #     self.set_not_busy()

    # def set_rule_editor_text(self, text):
    #     self.rule_editor.delete(1.0, "end")
    #     self.rule_editor.insert(1.0, text)
    #     self.rule_editor.edit_modified(False)

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

    root.mainloop()
