#!/usr/bin/env python
# coding: utf-8

# In[49]:

import tkinter as tk
import re
import pandas
import pandastable as pt
from nltk.tree import*
from enum import Enum
from tkinter.scrolledtext import ScrolledText

class Token_type(Enum):  # listing all tokens type
    spaceline = 43
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
    word = 38
    space =39
    singlecomment=40
    Startcomment=41
    Endcomment=42
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
                "predicates": Token_type.predicate,
                "clauses": Token_type.clause,
                "goal": Token_type.goal,
                "integer": Token_type.integer,
                "real": Token_type.real,
                "string": Token_type.string,
                 "char": Token_type.char,
                 "symbol": Token_type.symbol,
                 # "_": Token_type.anonymous,
                 "readln": Token_type.readString,
                 "readint":  Token_type.readint,
                 "readchar": Token_type.readchar,
                 "write": Token_type.write,
                 "\n": Token_type.space,
                 " ":Token_type.spaceline
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
             "<>": Token_type.notEqual,
             "\"": Token_type.word,
             "%":Token_type.singlecomment,
             "/*":Token_type.Startcomment,
             "*/":Token_type.Endcomment
             }
Tokens = []  # to add tokens to list
errors=[]

def split_token(text):
    word1 =[]
    temp = ""
    colonFlag = False
    greaterThanFLag = False
    smallerThanFlag = False
    DivisionFlag = False
    MultiplyFlag=False

    for char in text:
        #
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
                temp = temp + char
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
                temp = temp + char
            smallerThanFlag = False

        elif DivisionFlag: #  /  2
            if temp !="":
                word1.append(temp)
                temp=""
            if char == '*':
                word1.append("/*")
            else:
                word1.append("/")
                temp = temp + char
            DivisionFlag=False

        elif MultiplyFlag:
            if temp !="":
                word1.append(temp)
                temp=""
            if char == '/':
                word1.append("*/")
            else:
                word1.append("*")
                temp = temp + char

            MultiplyFlag=False

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

        elif char =="/":
            DivisionFlag=True
        elif char == "*":
            MultiplyFlag=True

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
            #any other char
            temp = temp + char
    if len(temp) > 0:
        word1.append(temp)
    return word1

def find_token(text):
   Tokens.clear()
   errors.clear()
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
    elif re.match("^[a-z]+[A-Z a-z]*[(]$", word):
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
    Clause_dict=Clause(Predicate_dict["index"])      #######Predicate_dict["index"]
    Children.append(Clause_dict["node"])
    Goal_dict=Goal(Clause_dict["index"])         ######Clause_dict["index"]
    Children.append(Goal_dict["node"])
    Node = Tree('Program', Children)
    return Node
                        ####################################### Predicate
def Predicate(j):
    children = []
    output=dict()
    out=Match(Token_type.predicate,j)
    children.append(out["node"])
    out1 = Match(Token_type.space,out["index"])
    #children.append(out1["node"])
    Pre_dict = Pre(out1["index"])
    children.append(Pre_dict["node"])
    Node = Tree('Predicate',children)
    output["node"]=Node
    output["index"]=Pre_dict["index"]
    return output
def Pre(j):
    output = dict()
    children = []
    if(j<len(Tokens)):
        Temp=Tokens[j].to_dict()
        if(Temp['token_type']==Token_type.predicate_name):
            out=Match(Token_type.predicate_name,j)
            children.append(out["node"])
            Prey_dict=Prey(out["index"])
            children.append(Prey_dict["node"])
            Node = Tree('Pre', children)
            output["node"] = Node
            output["index"] = Prey_dict["index"]
            return output
        elif (Temp['token_type'] == Token_type.value):
            out = Match(Token_type.value, j)
            children.append(out["node"])
            Prey_dict = Prey(out["index"])
            children.append(Prey_dict["node"])
            Node = Tree('Pre', children)
            output["node"] = Node
            output["index"] = Prey_dict["index"]
            return output
        else:
            children.append("Epsilon")
            Node = Tree('Pre', children)
            output["node"] = Node
            output["index"] = j
            return output
    else:
        children.append("Epsilon")
        Node = Tree('Pre', children)
        output["node"] = Node
        output["index"] = j
        return output

def Prey(j) :
    output = dict()
    children = []
    if (j < len(Tokens)):
        temp = Tokens[j].to_dict()
        if (temp['token_type'] == Token_type.openBracket):
            out1 = Match(Token_type.openBracket, j)
            children.append(out1["node"])
            Pl_dict = Pl(out1["index"])
            children.append(Pl_dict["node"])
            out2 = Match(Token_type.closeBracket, Pl_dict["index"])
            children.append(out2["node"])
            out4 = Match(Token_type.space, out2["index"])
            #children.append(out4["node"])
            Y_dict = Y(out4["index"])
            children.append(Y_dict["node"])
            Node = Tree('Prey',children)
            output["node"] = Node
            output["index"] =  Y_dict["index"]
            return output
        else:
            out4 = Match(Token_type.space, j)
            Y_dict = Y(out4["index"])
            children.append(Y_dict["node"])
      
            #children.append(out4["node"])
            Node = Tree('Prey', children)
            output["node"] = Node
            output["index"] = Y_dict["index"]
            return output
    else:
        Y_dict = Y(j)
        children.append(Y_dict["node"])
        out4 = Match(Token_type.space, Y_dict["index"])
        #children.append(out4["node"])
        Node = Tree('Prey', children)
        output["node"] = Node
        output["index"] = out4["index"]
        return output

def Y(j):
    output = dict()
    children = []
    if(j < len(Tokens)):
        temp = Tokens[j].to_dict()
        if(temp['token_type'] == Token_type.predicate_name or temp['token_type'] == Token_type.value):
            Pre_dict=Pre(j)
            children.append(Pre_dict["node"])
            Node = Tree('Y', children)
            output["node"] = Node
            output["index"] = Pre_dict["index"]
            return output
        else:
            children.append("Epsilon")
            Node = Tree('Y', children)
            output["node"] = Node
            output["index"] =j
            return output
    else:
        children.append("Epsilon")
        Node = Tree('Y', children)
        output["node"] = Node
        output["index"] = j
        return output



def Pl(j):
     output = dict()
     children = []
     Data_dict = Data(j)
     children.append(Data_dict["node"])
     Ply_dict=Ply(Data_dict["index"])
     children.append(Ply_dict["node"])
     Node = Tree('Pl', children)
     output["node"] = Node
     output["index"] = Ply_dict["index"]
     return output
def Ply(j):
    output = dict()
    children = []
    temp = Tokens[j].to_dict()
    if (temp['token_type'] == Token_type.And):
        out=Match(Token_type.And,j)
        children.append(out["node"])
        X_dict=X(out["index"])
        children.append(X_dict["node"])
        Node = Tree('Ply', children)
        output["node"] = Node
        output["index"] = X_dict["index"]
        return output
    else:
        children.append("Epsilon")
        Node = Tree('Ply', children)
        output["node"] = Node
        output["index"] = j
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
    if temp['token_type'] == Token_type.string:
        out1 = Match(Token_type.string, j)
        children.append(out1["node"])
        Node = Tree('Data', children)
        output["node"] = Node
        output["index"] = out1["index"]
        return output
    elif temp['token_type'] == Token_type.integer:
        out = Match(Token_type.integer, j)
        children.append(out["node"])
        Node = Tree('Data', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

    elif temp['token_type'] == Token_type.real :
        out2 = Match(Token_type.real, j)
        children.append(out2["node"])
        Node = Tree('Data', children)
        output["node"]=Node
        output["index"]=out2["index"]
        return output
    elif temp['token_type'] == Token_type.symbol:
        out3 = Match(Token_type.symbol, j)
        children.append(out3["node"])
        Node = Tree('Data', children)
        output["node"]=Node
        output["index"]=out3["index"]
        return output
    elif temp['token_type']==Token_type.char:
        out4 = Match(Token_type.char, j)
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

                              ####################################  Clause
def Clause(j):
    output = dict()
    children = []
    out=Match(Token_type.clause,j)  ## open when split work
    children.append(out["node"])
    out1 = Match(Token_type.space, out["index"])  # fix split
   # children.append(out1["node"])
    C_dict = C(out1["index"])                    #out["index"]
    children.append(C_dict["node"])
    Node = Tree('Clause', children)
    output["node"] = Node
    output["index"] = C_dict["index"]
    return output
def C(j) :
    output=dict()
    children=[]
    Cl_dict=Cl(j)
    children.append(Cl_dict["node"])
    Cx_dict=Cx(Cl_dict["index"])
    children.append(Cx_dict["node"])
    Node = Tree('C', children)
    output["node"] = Node
    output["index"] = Cx_dict["index"]
    return output

def Cx(j):
    output=dict()
    children=[]
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.End:
        out = Match(Token_type.End,j)
        children.append(out["node"])
        out1=Match(Token_type.space,out["index"])
        #children.append(out1["node"])
        Cxy_dict=Cxy(out1["index"])
        children.append(Cxy_dict["node"])
        Node = Tree('Cx', children)
        output["node"] = Node
        output["index"] = Cxy_dict["index"]
        return output
    elif(Temp['token_type'] == Token_type.If):
        out = Match(Token_type.If, j)
        children.append(out["node"])
        B_dict = B(out["index"])
        children.append(B_dict["node"])
        out1=Match(Token_type.End,B_dict["index"])
        children.append(out1["node"])
        out2=Match(Token_type.space,out1["index"])
        Cxy_dict = Cxy(out2["index"])
        children.append(Cxy_dict["node"])
        Node = Tree('Cx', children)
        output["node"] = Node
        output["index"] = Cxy_dict["index"]
        return output
    else:
        out = Match(Token_type.End, j)
        children.append(out["node"])
        Node = Tree('Cx', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

def Cxy(j):
    output=dict()
    children=[]
    if (j < len(Tokens)):
        temp = Tokens[j].to_dict()
        if (temp['token_type'] == Token_type.predicate_name):
            C_dict = C(j)
            children.append(C_dict["node"])
            Node = Tree('Cxy', children)
            output["node"] = Node
            output["index"] = C_dict["index"]
            return output
        elif (temp['token_type'] == Token_type.value):
            C_dict = C(j)
            children.append(C_dict["node"])
            Node = Tree('Cxy', children)
            output["node"] = Node
            output["index"] = C_dict["index"]
            return output
        else:
            children.append("Epsilon")
            Node = Tree('Cxy', children)
            output["node"] = Node
            output["index"] = j
            return output
    else:
        children.append("Epsilon")
        Node = Tree('Cxy', children)
        output["node"] = Node
        output["index"] = j
        return output
def Cl(j):
    output=dict()
    children=[]
    if (j < len(Tokens)):
        temp = Tokens[j].to_dict()
        if (temp['token_type'] == Token_type.predicate_name):
            out = Match(Token_type.predicate_name, j)
            children.append(out["node"])
            Cly_dict=Cly(out["index"])
            children.append(Cly_dict["node"])
            Node = Tree('Cl', children)
            output["node"] = Node
            output["index"] = Cly_dict["index"]
            return output
        elif (temp['token_type'] == Token_type.value):
            out = Match(Token_type.value, j)
            children.append(out["node"])
            Node = Tree('Cl', children)
            output["node"] = Node
            output["index"] = out["index"]
            return output
        else:
            out = Match(Token_type.predicate_name, j)
            children.append(out["node"])
            Node = Tree('Cl', children)
            output["node"] = Node
            output["index"] = out["index"]
            return output
    else:
        out = Match(Token_type.predicate_name, j)
        children.append(out["node"])
        Node = Tree('Cl', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

def Cly(j):
    output = dict()
    children = []
    if (j < len(Tokens)):
        temp = Tokens[j].to_dict()
        if (temp['token_type'] == Token_type.openBracket):
            out1 = Match(Token_type.openBracket, j)
            children.append(out1["node"])
            Ids_dict = Ids(out1["index"])
            children.append(Ids_dict["node"])
            out2 = Match(Token_type.closeBracket, Ids_dict["index"])
            children.append(out2["node"])
            Node = Tree('Cly', children)
            output["node"] = Node
            output["index"] = out2["index"]
            return output
        else:
            children.append("Epsilon")
            Node = Tree('Cly', children)
            output["node"] = Node
            output["index"] = j
            return output

    else:
        children.append("Epsilon")
        Node = Tree('Cly', children)
        output["node"] = Node
        output["index"] = j
        return output

def Ids(j):
    output = dict()
    children = []
    Cldata_dict = Cldata(j)
    children.append(Cldata_dict["node"])
    Idsy_dict = Idsy(Cldata_dict["index"])
    children.append(Idsy_dict["node"])
    Node = Tree('Ids', children)
    output["node"] = Node
    output["index"] = Idsy_dict["index"]
    return output
def Idsy(j):
    output = dict()
    children = []
    temp = Tokens[j].to_dict()
    if (temp['token_type'] == Token_type.And):
        out=Match(Token_type.And,j)
        children.append(out["node"])
        Clx_dict=Clx(out["index"])
        children.append(Clx_dict["node"])
        Node = Tree('Idsy', children)
        output["node"] = Node
        output["index"] = Clx_dict["index"]
        return output
    else:
        children.append("Epsilon")
        Node = Tree('Idsy', children)
        output["node"] = Node
        output["index"] = j
        return output
def Clx(j):
    output = dict()
    children = []
    Ids_dict = Ids(j)
    children.append(Ids_dict["node"])
    Node = Tree('D', children)
    output["node"] = Node
    output["index"] = Ids_dict["index"]
    return output
def Cldata(j):
    output = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.Identifier:
        out = Match(Token_type.Identifier, j)
        children.append(out["node"])
        Node = Tree('Cldata', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif Temp['token_type'] == Token_type.value:
        out = Match(Token_type.value, j)
        children.append(out["node"])
        Node = Tree('Cldata', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif Temp['token_type'] == Token_type.Constant:
        out = Match(Token_type.Constant, j)
        children.append(out["node"])
        Node = Tree('Cldata', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif Temp['token_type'] == Token_type.Real:
        out = Match(Token_type.Real, j)
        children.append(out["node"])
        Node = Tree('Cldata', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    else:
        out = Match(Token_type.Identifier, j)
        children.append(out["node"])
        Node = Tree('Cldata', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
 ##########################################

def B(j):
    output = dict()
    children = []
    Body_dict=Body(j)
    children.append(Body_dict["node"])
    By_dict=By(Body_dict["index"])
    children.append(By_dict["node"])
    Node = Tree('B', children)
    output["node"] = Node
    output["index"] = By_dict["index"]
    return output
def By(j):
    output = dict()
    children = []
    if(j<len(Tokens)):
        Temp = Tokens[j].to_dict()
        if(Temp['token_type']==Token_type.Or):
            out=Match(Token_type.Or,j)
            children.append(out["node"])
            B_dict=B(out["index"])
            children.append(B_dict["node"])
            Node = Tree('By', children)
            output["node"] = Node
            output["index"] = B_dict["index"]
            return output
        elif(Temp['token_type']==Token_type.And):
            out = Match(Token_type.And, j)
            children.append(out["node"])
            B_dict = B(out["index"])
            children.append(B_dict["node"])
            Node = Tree('By', children)
            output["node"] = Node
            output["index"] = B_dict["index"]
            return output
        else:
            children.append("Epsilon")
            Node = Tree('V', children)
            output["node"] = Node
            output["index"] = j
            return output
    else:
        children.append("Epsilon")
        Node = Tree('V', children)
        output["node"] = Node
        output["index"] = j
        return output

def Body(j):
    output=dict()
    children=[]
    Temp = Tokens[j].to_dict()
    if(Temp['token_type']==Token_type.readchar or Temp['token_type']==Token_type.readint or Temp['token_type']==Token_type.readString or Temp['token_type']==Token_type.write):
        BuiltFunction_dict=BuiltFunction(j)
        children.append(BuiltFunction_dict["node"])
        Node = Tree('Body', children)
        output["node"] = Node
        output["index"] = BuiltFunction_dict["index"]
        return output
    elif(Temp['token_type']==Token_type.Identifier):
        temp=Tokens[j+1].to_dict()
        if(temp['token_type']==Token_type.PlusOp or temp['token_type']==Token_type.MinusOp or temp['token_type']==Token_type.MultiplyOp or temp['token_type']==Token_type.DivideOp ):
            Expression_dict=Expression(j)
            children.append(Expression_dict["node"])
            Node = Tree('Body', children)
            output["node"] = Node
            output["index"] = Expression_dict["index"]
            return output
        else:
            RelationExpression_dict = RelationExpression(j)
            children.append(RelationExpression_dict["node"])
            Node = Tree('Body', children)
            output["node"] = Node
            output["index"] = RelationExpression_dict["index"]
            return output
    else:
        Comment_dict = Comment(j)
        children.append(Comment_dict["node"])
        Node = Tree('Body', children)
        output["node"] = Node
        output["index"] = Comment_dict["index"]
        return output
def BuiltFunction(j):
    output=dict()
    children=[]
    Temp = Tokens[j].to_dict()
    if(Temp['token_type']==Token_type.readint):
        out=Match(Token_type.readint,j)
        children.append(out["node"])
        out1=Match(Token_type.openBracket,out["index"])
        children.append(out1["node"])
        out2=Match(Token_type.Identifier,out1["index"])
        children.append(out2["node"])
        out3=Match(Token_type.closeBracket,out2["index"])
        children.append(out3["node"])
        Node = Tree('BuiltFunction', children)
        output["node"] = Node
        output["index"] = out3["index"]
        return output
    elif (Temp['token_type']==Token_type.readchar):
        out=Match(Token_type.readchar,j)
        children.append(out["node"])
        out1=Match(Token_type.openBracket,out["index"])
        children.append(out1["node"])
        out2=Match(Token_type.Identifier,out1["index"])
        children.append(out2["node"])
        out3=Match(Token_type.closeBracket,out2["index"])
        children.append(out3["node"])
        Node = Tree('BuiltFunction', children)
        output["node"] = Node
        output["index"] = out3["index"]
        return output
    elif (Temp['token_type'] == Token_type.readString):
        out = Match(Token_type.readString, j)
        children.append(out["node"])
        out1 = Match(Token_type.openBracket, out["index"])
        children.append(out1["node"])
        out2 = Match(Token_type.Identifier, out1["index"])
        children.append(out2["node"])
        out3 = Match(Token_type.closeBracket, out2["index"])
        children.append(out3["node"])
        Node = Tree('BuiltFunction', children)
        output["node"] = Node
        output["index"] = out3["index"]
        return output
    elif (Temp['token_type'] == Token_type.write):
        out = Match(Token_type.write, j)
        children.append(out["node"])
        out1 = Match(Token_type.openBracket, out["index"])
        children.append(out1["node"])
        out2 = Match(Token_type.word, out1["index"])
        children.append(out2["node"])
        Parameter_dict = Parameter(out2["index"])
        children.append(Parameter_dict["node"])
        out3 = Match(Token_type.word,Parameter_dict["index"])
        children.append(out3["node"])
        out4 = Match(Token_type.closeBracket, out3["index"])
        children.append(out4["node"])
        Node = Tree('BuiltFunction', children)
        output["node"] = Node
        output["index"] = out4["index"]
        return output
    else:
        out = Match(Token_type.write, j)
        children.append(out["node"])
        Node = Tree('BuiltFunction', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
def Parameter(j):
    output = dict()
    children = []
    if(j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if(Temp['token_type']==Token_type.Identifier):
            out = Match(Token_type.Identifier,j)
            children.append(out["node"])
            V_dict= V(out["index"])
            children.append(V_dict["node"])
            Node = Tree('Parameter', children)
            output["node"] = Node
            output["index"] = V_dict["index"]
            return output
        elif (Temp['token_type'] == Token_type.value):
            out = Match(Token_type.value, j)
            children.append(out["node"])
            V_dict = V(out["index"])
            children.append(V_dict["node"])
            Node = Tree('Parameter', children)
            output["node"] = Node
            output["index"] = V_dict["index"]
            return output
        elif (Temp['token_type']==Token_type.PlusOp or Temp['token_type']==Token_type.MinusOp or Temp['token_type']==Token_type.MultiplyOp or Temp['token_type']==Token_type.DivideOp):
            Operator_dict=Operator(j)
            children.append(Operator_dict["node"])
            V_dict = V(Operator_dict["index"])
            children.append(V_dict["node"])
            Node = Tree('Parameter', children)
            output["node"] = Node
            output["index"] = V_dict["index"]
            return output
        elif (Temp['token_type'] == Token_type.greaterThan or Temp['token_type'] == Token_type.greaterOrEqual or Temp['token_type'] == Token_type.smallerThan or Temp['token_type'] == Token_type.smallerOrEqual ):
            Relationaloperators_dict=Relationaloperators(j)
            children.append(Relationaloperators_dict["node"])
            V_dict = V(Relationaloperators_dict["index"])
            children.append(V_dict["node"])
            Node = Tree('Parameter', children)
            output["node"] = Node
            output["index"] = V_dict["index"]
            return output
        elif (Temp['token_type'] == Token_type.End):
            out = Match(Token_type.End, j)
            children.append(out["node"])
            V_dict = V(out["index"])
            children.append(V_dict["node"])
            Node = Tree('Parameter', children)
            output["node"] = Node
            output["index"] = V_dict["index"]
            return output
        elif (Temp['token_type'] == Token_type.AssignOp):
            out = Match(Token_type.AssignOp, j)
            children.append(out["node"])
            V_dict = V(out["index"])
            children.append(V_dict["node"])
            Node = Tree('Parameter', children)
            output["node"] = Node
            output["index"] = V_dict["index"]
            return output
        else:
            out = Match(Token_type.Identifier, j)
            children.append(out["node"])
            V_dict = V(out["index"])
            children.append(V_dict["node"])
            Node = Tree('Parameter', children)
            output["node"] = Node
            output["index"] = V_dict["index"]
            return output
    else:
        out = Match(Token_type.Identifier, j)
        children.append(out["node"])
        # V_dict = V(out["index"])
        # children.append(V_dict["node"])
        Node = Tree('Parameter', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

def V(j):
    output = dict()
    children = []
    if(j<len(Tokens)):
        Temp = Tokens[j].to_dict()
        if(Temp['token_type'] == Token_type.spaceline):
            out1 = Match(Token_type.spaceline, j)
            #children.append(out1["node"])
            Parameter_dict=Parameter(out1["index"])
            children.append(Parameter_dict["node"])
            Node = Tree('V', children)
            output["node"] = Node
            output["index"] = Parameter_dict["index"]
            return output
        else:
            children.append("Epsilon")
            Node = Tree('V', children)
            output["node"] = Node
            output["index"] = j
            return output
    else:
        children.append("Epsilon")
        Node = Tree('V', children)
        output["node"] = Node
        output["index"] = j
        return output
def Operator(j):
    output = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if(Temp['token_type']==Token_type.PlusOp):
        out =Match(Token_type.PlusOp,j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif (Temp['token_type'] == Token_type.MinusOp):
        out = Match(Token_type.MinusOp, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif (Temp['token_type'] == Token_type.MultiplyOp):
        out = Match(Token_type.MultiplyOp, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif (Temp['token_type'] == Token_type.DivideOp):
        out = Match(Token_type.DivideOp, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif(Temp['token_type'] == Token_type.AssignOp):
        out = Match(Token_type.AssignOp, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    else:
        out = Match(Token_type.PlusOp, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
def Relationaloperators(j):
    output = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if (Temp['token_type'] == Token_type.greaterThan):
        out = Match(Token_type.greaterThan, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif (Temp['token_type'] == Token_type.greaterOrEqual):
        out = Match(Token_type.greaterOrEqual, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif (Temp['token_type'] == Token_type.smallerThan):
        out = Match(Token_type.smallerThan, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif (Temp['token_type'] == Token_type.smallerOrEqual):
        out = Match(Token_type.smallerOrEqual, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    else:
        out = Match(Token_type.greaterThan, j)
        children.append(out["node"])
        Node = Tree('Operator', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
def Expression(j):
    output = dict()
    children = []
    out=Match(Token_type.Identifier,j)
    children.append(out["node"])
    Operator_dict=Operator(out["index"])
    children.append(Operator_dict["node"])
    Expressionx_dict=Expressionx(Operator_dict["index"])
    children.append(Expressionx_dict["node"])
    Node = Tree('Expression', children)
    output["node"] = Node
    output["index"] = Expressionx_dict["index"]
    return output
def Expressionx(j):
    output = dict()
    children = []
    Temp = Tokens[j+1].to_dict()
    if(Temp['token_type']==Token_type.PlusOp or Temp['token_type']==Token_type.MinusOp or Temp['token_type']==Token_type.MultiplyOp or Temp['token_type']==Token_type.DivideOp or Temp['token_type']==Token_type.AssignOp):
        Expression_dict=Expression(j)
        children.append(Expression_dict["node"])
        Node = Tree('Expressionx', children)
        output["node"] = Node
        output["index"] = Expression_dict["index"]
        return output
    else:
        Dataexp_dict =Dataexp(j)
        children.append(Dataexp_dict["node"])
        Node = Tree('Expressionx', children)
        output["node"] = Node
        output["index"] = Dataexp_dict["index"]
        return output
def Dataexp(j):
    output = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if (Temp['token_type'] == Token_type.Identifier):
        out = Match(Token_type.Identifier, j)
        children.append(out["node"])
        Node = Tree('Dataexp', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif (Temp['token_type'] == Token_type.Constant):
        out = Match(Token_type.Constant, j)
        children.append(out["node"])
        Node = Tree('Dataexp', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    elif (Temp['token_type'] == Token_type.Real):
        out = Match(Token_type.Real, j)
        children.append(out["node"])
        Node = Tree('Dataexp', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
    else:
        out = Match(Token_type.Identifier, j)
        children.append(out["node"])
        Node = Tree('Dataexp', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

def RelationExpression(j):
    output = dict()
    children = []
    out = Match(Token_type.Identifier, j)
    children.append(out["node"])
    Relationaloperators_dict = Relationaloperators(out["index"])
    children.append(Relationaloperators_dict["node"])
    RelationExpressionx_dict = RelationExpressionx(Relationaloperators_dict["index"])
    children.append(RelationExpressionx_dict["node"])
    Node = Tree('RelationExpression', children)
    output["node"] = Node
    output["index"] = RelationExpressionx_dict["index"]
    return output
def RelationExpressionx(j):
    output = dict()
    children = []
    Temp = Tokens[j+1].to_dict()
    if(Temp['token_type']==Token_type.PlusOp or Temp['token_type']==Token_type.MinusOp or Temp['token_type']==Token_type.MultiplyOp or Temp['token_type']==Token_type.DivideOp):
        Expression_dict=Expression(j)
        children.append(Expression_dict["node"])
        Node = Tree('Expressionx', children)
        output["node"] = Node
        output["index"] = Expression_dict["index"]
        return output
    else:
        Dataexp_dict =Dataexp(j)
        children.append(Dataexp_dict["node"])
        Node = Tree('Expressionx', children)
        output["node"] = Node
        output["index"] = Dataexp_dict["index"]
        return output

def Comment(j):
    output = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if(Temp["token_type"]==Token_type.Startcomment):
        out = Match(Token_type.Startcomment,j)
        children.append(out["node"])
        Parameter_dict=Parameter(out["index"])
        children.append(Parameter_dict["node"])
        out1=Match(Token_type.Endcomment,Parameter_dict["index"])
        children.append(out1["node"])
        Node = Tree('Comment', children)
        output["node"] = Node
        output["index"] = out1["index"]
        return output
    elif(Temp["token_type"]==Token_type.singlecomment):
        out=Match(Token_type.singlecomment,j)
        children.append(out["node"])
        Parameter_dict=Parameter(out["index"])
        children.append(Parameter_dict["node"])
        Node = Tree('Comment', children)
        output["node"] = Node
        output["index"] = Parameter_dict["index"]
        return output
    else:
        out = Match(Token_type.singlecomment, j)
        children.append(out["node"])
        Node = Tree('Comment', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output


                           ###################################   Goal
def Goal(j):
    output=dict()
    children=[]
    out=Match(Token_type.goal,j)      ## open when split work
    children.append(out["node"])
    out1 = Match(Token_type.space, out["index"])  # fix split
   # children.append(out1["node"])
    G_dict=G(out1["index"])                          #out["index"]
    children.append(G_dict["node"])
    Node = Tree('Goal', children)
    output["node"] = Node
    output["index"] = G_dict["index"]
    return output
def G(j):
    output = dict()
    children = []
    if (j < len(Tokens)):
        temp = Tokens[j].to_dict()
        if (temp['token_type'] == Token_type.predicate_name):
            out = Match(Token_type.predicate_name, j)
            children.append(out["node"])
            Gpy_dict=Gpy(out["index"])
            children.append(Gpy_dict["node"])
            Node = Tree('G', children)
            output["node"] = Node
            output["index"] = Gpy_dict["index"]
            return output
        elif (temp['token_type'] == Token_type.value):
            out = Match(Token_type.value, j)
            children.append(out["node"])
            Gpy_dict = Gpy(out["index"])
            children.append(Gpy_dict["node"])
            Node = Tree('G', children)
            output["node"] = Node
            output["index"] = Gpy_dict["index"]
            return output
        else:
            out = Match(Token_type.value, j)
            children.append(out["node"])
            Node = Tree('G', children)
            output["node"] = Node
            output["index"] = out["index"]
            return output
    else:
        out = Match(Token_type.value, j)
        children.append(out["node"])
        Node = Tree('G', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output
def Gp(j):
    output=dict()
    children=[]
    if (j < len(Tokens)):
        temp = Tokens[j].to_dict()
        if (temp['token_type'] == Token_type.predicate_name):
            children.append("Error")
            Node = Tree('Gp', children)
            output["node"] = Node
            output["index"] = j
            return output
        else:
            children.append("Epsilon")
            Node = Tree('Gp', children)
            output["node"] = Node
            output["index"] = j
            return output
    else:
        children.append("Epsilon")
        Node = Tree('Gp', children)
        output["node"] = Node
        output["index"] = j
        return output



def Gpy(j):
    output = dict()
    children = []
    if (j < len(Tokens)):
        temp = Tokens[j].to_dict()
        if (temp['token_type'] == Token_type.openBracket):
            out1 = Match(Token_type.openBracket, j)
            children.append(out1["node"])
            Gpl_dict = Gpl(out1["index"])
            children.append(Gpl_dict["node"])
            out2 = Match(Token_type.closeBracket, Gpl_dict["index"])
            children.append(out2["node"])
            out3 = Match(Token_type.End, out2["index"])
            children.append(out3["node"])
            Gp_dict=Gp(out3["index"])
            children.append(Gp_dict["node"])
            Node = Tree('Gpy', children)
            output["node"] = Node
            output["index"] = Gp_dict["index"]
            return output
        elif(temp['token_type'] == Token_type.End):
            out3 = Match(Token_type.End, j)
            children.append(out3["node"])
            Gp_dict = Gp(out3["index"])
            children.append(Gp_dict["node"])
            Node = Tree('Gpy', children)
            output["node"] = Node
            output["index"] = Gp_dict["index"]
            return output
        else:
            out1 = Match(Token_type.openBracket, j)
            children.append(out1["node"])
            Node = Tree('Gpy', children)
            output["node"] = Node
            output["index"] = out1["index"]
            return output
    else:
        out1 = Match(Token_type.openBracket, j)
        children.append(out1["node"])
        Node = Tree('Gpy', children)
        output["node"] = Node
        output["index"] = out1["index"]
        return output

def Gpl(j):
    output = dict()
    children = []
    Vardata_dict = Vardata(j)
    children.append(Vardata_dict["node"])
    Gply_dict = Gply(Vardata_dict["index"])
    children.append(Gply_dict["node"])
    Node = Tree('GPl', children)
    output["node"] = Node
    output["index"] = Gply_dict["index"]
    return output
def Gply(j):
    output = dict()
    children = []
    if(j<len(Tokens)):
        temp = Tokens[j].to_dict()
        if (temp['token_type'] == Token_type.And):
            out=Match(Token_type.And,j)
            children.append(out["node"])
            D_dict=D(out["index"])
            children.append(D_dict["node"])
            Node = Tree('Gply', children)
            output["node"] = Node
            output["index"] = D_dict["index"]
            return output
        else:
            children.append("Epsilon")
            Node = Tree('GPly', children)
            output["node"] = Node
            output["index"] = j
            return output
    else:
        children.append("Epsilon")
        Node = Tree('GPly', children)
        output["node"] = Node
        output["index"] = j
        return output
def D(j):
    output = dict()
    children = []
    Gpl_dict = Gpl(j)
    children.append(Gpl_dict["node"])
    Node = Tree('D', children)
    output["node"] = Node
    output["index"] = Gpl_dict["index"]
    return output
def Vardata(j):
    output = dict()
    children=[]
    if(j<len(Tokens)):
        Temp = Tokens[j].to_dict()
        if Temp['token_type']==Token_type.Identifier:
            out = Match(Token_type.Identifier, j)
            children.append(out["node"])
            Node = Tree('Vardata', children)
            output["node"] = Node
            output["index"] = out["index"]
            return output
        elif Temp['token_type']==Token_type.value:
            out = Match(Token_type.value, j)
            children.append(out["node"])
            Node = Tree('Vardata', children)
            output["node"] = Node
            output["index"] = out["index"]
            return output
        else:
            out = Match(Token_type.Identifier, j)
            children.append(out["node"])
            Node = Tree('Vardata', children)
            output["node"] = Node
            output["index"] = out["index"]
            return output
    else:
        out = Match(Token_type.Identifier, j)
        children.append(out["node"])
        Node = Tree('Vardata', children)
        output["node"] = Node
        output["index"] = out["index"]
        return output

########################

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
            output["index"] = j+1
            errors.append("Syntax error : " + Temp['Lex'] + " Expected dot")
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


def Scan(x1):
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # print(df)

    #
    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    #start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()








