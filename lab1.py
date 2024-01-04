from z3 import *
import sys


def rewriting(terms):
    term1 = terms[:terms.find("=")]
    term2 = terms[terms.find("=")+1:]
    #print(term1, term2)

    # проверка скобок (количество открытых должно совпадать с количеством закрытых)
    counter = 0 
    for i in range(len(term1)):
        str1 = term1[i]
        if str1 != "(" and str1 != ")" and str1 != ',':
            if (str1 not in constr) and (str1 not in variables):
                constr.append(str1)
        else:
            if str1 == "(":
                counter += 1
            else:
                if str1 == ")":
                    counter -= 1
    #print(counter)   
    if counter !=0:
        print("не хватает скобки!") 
        sys.exit()
    #else:
        #print("всё ок :-)")

    counter = 0 
    for i in range(len(term2)):
        str1 = term2[i]
        if str1 != "(" and str1 != ")" and str1 != ',':
            if (str1 not in constr) and (str1 not in variables):
                constr.append(str1)
        else:
            if str1 == "(":
                counter += 1
            else:
                if str1 == ")":
                    counter -= 1
    #print(counter)   
    if counter !=0:
        print("не хватает скобки!") 
        sys.exit()
    #else:
        #print("всё ок :-)")

    # подсчёт коэффициентов
    
    counter_new = 0
    str2 = "And( "
    for i in constr:
        str0 = "And( "
        str3 = ""
        counter_right = 0 
        counter_left = 0 
        counter=0
        for j in terms:
            if j == '(':
                counter_left += 1
            elif j == ')':
                counter_right += 1
            elif counter_right == counter_left:
                counter +=1
        #print("проверка подсчёта ",counter)    
        all_counter = []
        all_counter.append(counter)
        arr = []
        for k in range(counter):
            abc = str(counter_new)
            str1 = "a" + abc
            arr.append(str1)
            counter_new +=1
            if k != counter - 1:
                str0 += str1 + ">1"
            else:
                str3 = str1 + ">0"
        if len(str3) > 4:
            str3 = str3[:-2] + "), "
        else:
            str3 =""
        str2 += "Or( " + str0 + str3 + "), "
        print ("Вот так вот: ",str2)
        coefficients[i] = arr
    str2 = str2[:-2]+")"

    print('coefficients ', coefficients)
    print('test ', arr)


#Ввод данных

print('чтобы завершить ввод используйте 0:')

""" 
    пример входных данных:

      variables= x, y
      f(g(x,y))=g(h(y),x)
      h(f(x))=f(x)
      0')
"""

variables = input()
variables =  ''.join(variables.split())
variables = variables[variables.find("=")+1:]
variables = variables.split(",")

all_counter = []
terms = []
constr = []
coefficients = {}

a = ''

expression = input()
while expression != '0':
    expression = ''.join(expression.split())
    #print(expression)
    terms.append(expression)
    expression = input()

for i in range(len(terms)):
    rewriting(terms[i])
    #print(terms[i])
    #print(i)
