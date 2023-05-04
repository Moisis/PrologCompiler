import tkinter as tk
from enum import Enum
import re
import pandas


class Token_type(Enum):  # listing all tokens type
    Begin = 1
    End = 2
    Do = 3
    Else = 4
    EndIf = 5
    If = 6
    Integer = 7
    Dot = 8
    Semicolon = 9
    EqualOp = 10
    LessThanOp = 11
    GreaterThanOp = 12
    NotEqualOp = 13
    PlusOp = 14
    MinusOp = 15
    MultiplyOp = 16
    DivideOp = 17
    Identifier = 18
    Constant = 19
    Error = 20


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Reserved word Dictionary
ReservedWords = {"IF": Token_type.If,
                 "END": Token_type.End,
                 "BEGIN": Token_type.Begin,
                 "DO": Token_type.Do,
                 "ElSE": Token_type.Else,
                 "ENDIF": Token_type.EndIf,
                 "INTEGER": Token_type.Integer
                 }
Operators = {".": Token_type.Dot,
             ";": Token_type.Semicolon,
             "=": Token_type.EqualOp,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             }
Tokens = []  # add tokens to list


def find_token(text):
    print(text)
    tokens = text.split()
    for word in tokens:
        print(word)
        if word in ReservedWords:
            Tokens.append(token(word, ReservedWords[word]))
        elif word in Operators:
            Tokens.append(token(word, Operators[word]))
        elif re.match("^[a-zA-Z][a-zA-Z0-9]*$", word):
            Tokens.append(token(word, Token_type.Identifier))
        elif re.match("^[0-9]+$", word):
            Tokens.append(token(word, Token_type.Constant))
        elif re.match("^[0-9]+\.[0-9]*$", word):
            Tokens.append(token(word, Token_type.Constant))
        else:
            Tokens.append(token(word, Token_type.Error))


# GUI
root = tk.Tk()
root.title("Hi ")

canvas1 = tk.Canvas(root, width=1000, height=500, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)

def clear():
    print()
     #Todo
def Scan():
    clear()
    x1 = entry1.get()
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    print(df)

    label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)

    label4 = tk.Label(root, text="Token_type" + x1, font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Scan', command=Scan, bg='green', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()
