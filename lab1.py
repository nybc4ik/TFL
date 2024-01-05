from z3 import *
import sys


def rewriting(terms):
    global counter_new
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
    #print(constr, "\n", counter) 
    if counter != 0:
        print("не хватает скобки!") 
        sys.exit()
    #else:
        #print("всё ок :-)")

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
    #print(constr, "\n", counter)  
    if counter != 0:
        print("не хватает скобки!") 
        sys.exit()
    #else:
        #print("всё ок :-)")

    # подсчёт коэффициентов
    
    str2 = "And( "
    for i in constr:
        str0 = "And("
        str3 = ""
        counter_right = 0 
        counter_left = 0 
        counter = 1
        check1 = False
        for j in terms:
            if j == i:
                check1 = True
            if check1:
                if j == '(':
                    counter_left += 1
                if j == ')':
                    counter_right += 1
                if  counter_left - counter_right == 1 and j== ',':
                    counter += 1
                if  counter_left == counter_right and counter_left != 0:
                    counter +=1
                    break
        #print("проверка подсчёта ",counter)    
                
        all_counter = []
        all_counter.append(counter)
        arr = []
        for k in range(counter):
            abc = str(counter_new)
            str1 = "a" + abc
            arr.append(str1)
            counter_new += 1
            if k == counter - 1:
                str3 = str1 + ">0 "
            else:
                str0 += str1 + ">1, "
        if len(str0) > 4:
            str0 = str0[:-2] + "), "
        else:
            str0 = ""
        str2 += "Or( " + str0 + str3 + "), "
        #print ("Вот так вот: ",str2)
        coefficients[i] = arr
    str2 = str2[:-2] +")"

    #print('coefficients ', coefficients)
    #print('test ', arr)

    str4 = "And( "
    for i in coefficients:
        for k in coefficients[i]:
            if i != "free":
                str4 += k + ">=1, "
            else:
                str4 += k + ">=0, "
    print(str4[:-2]+")")
    print(str2)
#    a.add(eval(str2))
#    a.add(eval(str4[:-2]+")"))
    

    # необходимо из term1 и term2 сделать линейную функцию !
    print("before")
    print(term1, "\n", term2)
    term1 = line(term1)
    term2 = line(term2)
    print("after")
    print(term1, "\n", term2)
    
def line(term):
    term_left = 0
    term_right = 0
    counter = 0
    term_left_arr = []

    while counter == 0:
        for i in term:
            if i == "(":
                term_left += 1
                term_left_arr.append(counter)
            if i == ")":
                term_right += 1
                if term_left == 1 and term_right == 1:
                    l = term[0]
                    #print("коэфиценты ", coefficients[l])
                    start_new = term.index('(')+1
                    finish_new = term.index(')')
                    new = term[start_new:finish_new].split(',')
                    term_new = ''
                    for j in range(len(new)):
                        for k in (new[j].split("+")):
                            term_new += coefficients[l][j] + "*" + k + "+"
                    term_new += coefficients[l][len(coefficients[l])-1]
                    #print("что-то новое ", term_new)
                    return term_new
                else:
                    left_arr = term_left_arr.pop()
                    new1 = line(term[left_arr-1:counter+1])
                    new2 = term[left_arr-1:counter+1]
                    term = term.replace(new2, new1)
                    counter = 0 
                    break

            counter += 1

    return term

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

counter_new = 0
all_counter = []
terms = []
constr = []
coefficients = {}

a = Solver()

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
