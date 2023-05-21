#!/usr/bin/env python
# coding: utf-8

# In[49]:


import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import*
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
    Identifier = 18
    Constant = 19
    Real = 20
    predicate = 21
    predicate_name = 22
    Error = 23
    notEqual = 24
    clause = 25
    goal = 26
    integer = 27
    real = 28
    string = 29
    char = 30
    symbol = 31
    anonymous = 32
    readString = 33
    readint = 34
    readchar = 35
    write = 36
    value = 37
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
                 ",": Token_type.And,
                 ";": Token_type.Or,
                 "(": Token_type.openBracket,
                 ")": Token_type.closeBracket,
                 "Not": Token_type.Not,
                "Predicate": Token_type.predicate,
                "Clause": Token_type.clause,
                "Goal": Token_type.goal,
                "int": Token_type.integer,
                "real": Token_type.real,
                "string": Token_type.string,
                 "char": Token_type.char,
                 "symbol": Token_type.symbol,
                 # "_": Token_type.anonymous,
                 "readln": Token_type.readString,
                 "readint":  Token_type.readint,
                 "readchar": Token_type.readchar,
                 "write": Token_type.write,



                 }
Operators = {".": Token_type.Dot,
             "=": Token_type.AssignOp,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "/": Token_type.DivideOp,
             "*": Token_type.MultiplyOp,
             ">": Token_type.greaterThan,
             "<": Token_type.smallerThan,
             ">=": Token_type.greaterOrEqual,
             "<=": Token_type.smallerOrEqual,
             "<>": Token_type.notEqual  ####



             }
Tokens = []  # to add tokens to list
errors=[]

def split_token(text):
    word1 =[]
    temp = ""
    colonFlag = False
    greaterThanFLag = False
    smallerThanFlag = False

    for char in text:
        if colonFlag:
            if temp != "":
                word1.append(temp)
                temp = ""
            if char == '-':
                word1.append(":-")
            else:
                word1.append(":")
                temp = temp + char
            colonFlag = False

        elif greaterThanFLag:
            if temp != "":
                word1.append(temp)
                temp = ""
            if char == '=':
                word1.append(">=")
                temp = ""
            else:
                word1.append(">")
            greaterThanFLag = False

        elif smallerThanFlag:
            if temp != "":
                word1.append(temp)
                temp = ""
            if char == '=':
                word1.append("<=")
            elif char == '>':
                word1.append("<>")
            else:
                word1.append("<")
            smallerThanFlag = False

        elif char in ReservedWords:
            if temp != "":
                if char=='(':
                    if not (temp in ReservedWords):
                        temp=temp+char
                word1.append(temp)
                temp =""
            word1.append(char)

        elif char == ':':
            colonFlag = True
            continue

        elif char == ">":
            greaterThanFLag = True
        elif char == "<":
            smallerThanFlag = True

        elif char in Operators:
            if temp != "":
                word1.append(temp)
                temp =""
            word1.append(char)

                                                ######ELDOT WEL END
        # elif char=='.':
        #     if temp != "":
        #         temp = temp + char
        #         continue
        #     else:
        #         word1.append(char)

        else:
            temp = temp + char
    if len(temp) > 0:
        word1.append(temp)
    return word1



def find_token(text):
   tokens = split_token(text)
   for word in tokens:
    if word in ReservedWords:
        print("is Reserved word")
        Tokens.append(token(word, ReservedWords[word]))
    elif word in Operators:
        print(" is operator")
        Tokens.append(token(word, Operators[word]))
    elif re.match("^[A-Z _][a-z A-Z 0-9 _]*$", word):
        print("is Identifier")
        Tokens.append(token(word, Token_type.Identifier))
    elif re.match("^[0-9]+$", word):
        print("is Integer")
        Tokens.append(token(word, Token_type.Constant))
    elif re.match("^[0-9]+\.[0-9]*$", word):
        print("is real")
        Tokens.append(token(word, Token_type.Real))
    # elif re.match("^[a-z A-Z][a-z A-Z 0-9]*[(][a-z A-Z 0-9]+(,[a-z A-Z 0-9]+)*[)]",word):
    #     print("is predicate")
    #     Tokens.append(token(word, Token_type.predicate))
    elif re.match("^[a-z]+[(]$", word):
        print("is predicate name")
        word=word[:-1]
        Tokens.append(token(word, Token_type.predicate_name))
    elif re.match("^[a-z]+[A-Z a-z 0-9]*$", word):
        print("is value")
        Tokens.append(token(word, Token_type.value))
    else:
        Tokens.append(token(word, Token_type.Error))

                                                    ########## GRAMMAR ################

def Parse():
    j = 0
    Children = []
    Predicate_dict = Predicate(j)
    Children.append(Predicate_dict["node"])  ###############
    # dic_output = Match(Token_type.Dot, Predicate_dict["index"])
    # Children.append(dic_output["node"])
    Node = Tree('Program', Children)

    return Node

def Predicate(j):
    children = []
    output=dict()

    # out=Match(Token_type.Predicate,j)
    # children.append(out["node"])    out["index"]
    Pre_dict = Pre(j)
    children.append(Pre_dict["node"])
    # out1=Match(Token_type.Identifier,j)
    # children.append(out1["node"])
    Node = Tree('Predicate',children)
    output["node"]=Node
    output["index"]=Pre_dict["index"]                    # out["index"]

    return output
def Pre(j):
    output = dict()
    children = []
    out=Match(Token_type.predicate_name,j)
    children.append(out["node"])
    out1=Match(Token_type.openBracket,out["index"])
    children.append(out1["node"])
    Pl_dict=Pl(out1["index"])
    children.append(Pl_dict["node"])
    out2=Match(Token_type.closeBracket,Pl_dict["index"])
    children.append(out2["node"])
    out3=Match(Token_type.End,out2["index"])
    children.append(out3["node"])
    Node = Tree('Pre', children)
    output["node"] = Node
    output["index"] = out3["index"]
    return output
def Pl(j):
     output = dict()
     children = []
     temp=Tokens[j+1].to_dict()

     if(temp['token_type'] == Token_type.And):
        Data_dict=Data(j)
        children.append(Data_dict["node"])
        out = Match(Token_type.And, Data_dict["index"])
        children.append(out["node"])
        X_dict = X(out["index"])
        children.append(X_dict["node"])
        Node = Tree('Pl', children)
        output["node"] = Node
        output["index"] = X_dict["index"]
        return output
     else:
        Data_dict = Data(j)
        children.append(Data_dict["node"])
        Node = Tree('Pl', children)
        output["node"] = Node
        output["index"] = Data_dict["index"]
        return output
def X(j):
    output = dict()
    children = []
    Pl_dict = Pl(j)
    children.append(Pl_dict["node"])
    Node = Tree('X', children)
    output["node"] = Node
    output["index"] = Pl_dict["index"]
    return output
def Data(j):
    output = dict()
    children = []
    temp = Tokens[j].to_dict()
    if temp == Token_type.string:
        out1 = Match(Token_type.string, j)
        children.append(out1["node"])
        Node = Tree('Data', children)
        output["node"] = Node
        output["index"] = out1["index"]
        return output
    elif temp == Token_type.integer:
        out = Match(Token_type.integer, j)
        children.append(out["node"])
        Node = Tree('Data', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

    elif temp == Token_type.real :
        out2 = Match(Token_type.real, j)
        children.append(out2["node"])
        Node = Tree('Data', children)
        output["node"]=Node
        output["index"]=out2["index"]
        return output
    elif temp == Token_type.symbol:
        out3 = Match(Token_type.symbol, j)
        children.append(out3["node"])
        Node = Tree('Data', children)
        output["node"]=Node
        output["index"]=out3["index"]
        return output
    elif temp==Token_type.char:
        out4 = Match(Token_type.symbol, j)
        children.append(out4["node"])
        Node = Tree('Data', children)
        output["node"] = Node
        output["index"] = out4["index"]
        return output
    else:
        out = Match(Token_type.integer, j)
        children.append(out["node"])
        Node = Tree('Data', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

########################
def Header(j):
    output=dict()
    children=[]
    # out=Match(Token_type.Program,j)
    # children.append(out["node"])
    out1=Match(Token_type.Identifier,j)
    children.append(out1["node"])
    Node = Tree('Header',children)
    output["node"]=Node
    output["index"]=out1["index"]
    return output

def Match(a, j):
    output = dict()
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j + 1
            errors.append("Syntax error : " + Temp['Lex'] + " Expected dot")
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


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
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
root.mainloop()














# # GUI
# root = tk.Tk()
#
# canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
# canvas1.pack()
#
# label1 = tk.Label(root, text='Scanner Phase')
# label1.config(font=('helvetica', 14))
# canvas1.create_window(200, 25, window=label1)
#
# label2 = tk.Label(root, text='Source code:')
# label2.config(font=('helvetica', 10))
# canvas1.create_window(200, 100, window=label2)
#
# entry1 = tk.Entry(root)
# canvas1.create_window(200, 140, window=entry1)
#
#
# def Scan():
#     x1 = entry1.get()
#     find_token(x1)
#     df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
#     print(df)
#     label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
#     canvas1.create_window(200, 210, window=label3)
#
#     label4 = tk.Label(root, text="Token_type" + x1, font=('helvetica', 10, 'bold'))
#     canvas1.create_window(200, 230, window=label4)
#     # rule_editor = ScrolledText(
#     #     root, width=100, height=30, padx=10, pady=10
#     # )
#     # # diagrambox = tk.Text(root, padx=10, pady=10)
#     # # diagrambox.grid(sticky=W, row=3, column=2, pady=3, padx=10)
#     # canvas1.create_window(190, 240, window=rule_editor)
#
# button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
# canvas1.create_window(200, 180, window=button1)
#
# root.mainloop()

# In[ ]:




