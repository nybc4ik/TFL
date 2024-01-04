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
    print(counter)   
    if counter !=0:
        print("не хватает скобки!") 
        sys.exit()
    else:
        print("всё ок :-)")

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
    print(counter)   
    if counter !=0:
        print("не хватает скобки!") 
        sys.exit()
    else:
        print("всё ок :-)")


#Ввод данных

print('чтобы завершить ввод используйте 0:')

""" 
    пример входных данных:

      variables= x, y
      f(g(x,y))=g(h(y),x)
      h(f(x))=f(x)
      end')

"""

variables = input()
variables =  ''.join(variables.split())
variables = variables[variables.find("=")+1:]
variables = variables.split(",")

terms = []
constr = []

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
