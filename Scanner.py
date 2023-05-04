#!/usr/bin/env python
# coding: utf-8

# In[49]:


import tkinter as tk
from enum import Enum
import re
from tkinter.scrolledtext import ScrolledText

import pandas


class Token_type(Enum):  # listing all tokens type
    If = 1
    End = 2
    And = 3
    Or = 4
    Not = 5
    openBracket = 6
    closeBracket = 7
    Dot = 8
    AssignOp = 9
    PlusOp = 10
    MinusOp = 11
    DivideOp = 12
    MultiplyOp = 13
    greaterThan = 14
    smallerThan = 15
    greaterOrEqual = 16
    smallerOrEqual = 17
    Identifier =18
    Constant =19
    Real = 20
    predicate =21
    predicate_name = 22
    Error =23



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
ReservedWords = {":-": Token_type.If,
                 ".": Token_type.End,
                 "," : Token_type.And,
                 ";": Token_type.Or,
                 "Not":Token_type.Not,
                 "("  :Token_type.openBracket,
                 ")"  :Token_type.closeBracket
                 }
Operators = {".": Token_type.Dot,
             "=": Token_type.AssignOp,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             ">": Token_type.greaterThan,
             "<":Token_type.smallerThan,
             ">=":Token_type.greaterOrEqual,
             "<=":Token_type.smallerOrEqual
             }
Tokens = []  # to add tokens to list

def slit_token(text):
    word1 =[]
    temp = ""
    for word in text:
        if not(word in ReservedWords) and not(word in Operators) :
            temp=temp + word
        elif (word == ":" or word =="-"):
            if(word ==":"):
                continue
            word1.append(":-")
            temp=""
        else:
            if len(temp) >0:
                word1.append(temp)
            word1.append(word)
            if(word == ')'):
               word1.append(text)
            temp =""
    if len(temp)>0:
        word1.append(temp)
    return word1


# if word == ReservedWords or word == Operators:
#     if len(temp) > 0:
#         word1.append(word)


def find_token(text):
   tokens = slit_token(text)
   for word in tokens:
    if word in ReservedWords:
        print("is Reserved word")
        Tokens.append(token(word, ReservedWords[word]))
    elif word in Operators:
        print(" is operator")
        Tokens.append(token(word, Operators[word]))
    elif re.match("^[A-Z _][a-z A-Z 0-9]*$", word):
        print("is Identifier")
        Tokens.append(token(word, Token_type.Identifier))
    elif re.match("^[0-9]+$", word):
        print("is Integer")
        Tokens.append(token(word, Token_type.Constant))
    elif re.match("^[0-9]+\.[0-9]*$", word):
        print("is real")
        Tokens.append(token(word, Token_type.Real))
    elif re.match("^[a-z A-Z][a-z A-Z 0-9]*[(][a-z A-Z 0-9]+(,[a-z A-Z 0-9]+)*[)]",word):
        print("is predicate")
        Tokens.append(token(word, Token_type.predicate))
    elif re.match("[a-z]+", word):
        print("is predicate name")
        Tokens.append(token(word, Token_type.predicate_name))
    else:
        Tokens.append(token(word, Token_type.Error))
    # complete


# GUI
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def Scan():
    x1 = entry1.get()
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    print(df)
    label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)

    label4 = tk.Label(root, text="Token_type" + x1, font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 230, window=label4)
    # rule_editor = ScrolledText(
    #     root, width=100, height=30, padx=10, pady=10
    # )
    # # diagrambox = tk.Text(root, padx=10, pady=10)
    # # diagrambox.grid(sticky=W, row=3, column=2, pady=3, padx=10)
    # canvas1.create_window(190, 240, window=rule_editor)

button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()

# In[ ]:




