from z3 import *
import sys


def rewriting(terms):
    global counter_new, Result_F, file
    term1 = terms[:terms.find("=")]
    term2 = terms[terms.find("=")+1:]

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

        coefficients[i] = arr
    str2 = str2[:-2] + ")"


    str4 = "And("
    for i in coefficients:
        for k in coefficients[i]:
            globals()[k] = Int(k)
    
    for i in coefficients:
        for k in coefficients[i]:
            if i != "free":
                str4 += k + ">=1, "
            else:
                str4 += k + ">=0, "
    #print(str4[:-2]+")")
    #print(str2)
    Result_F.add(eval(str2))
    Result_F.add(eval(str4[:-2]+")"))
    

    # необходимо из term1 и term2 сделать линейную функцию !

    term1 = line(term1)
    term2 = line(term2)

    #подсчёт множителей каждой переменной a*x -> 1 множитель  a0*a1*y -> два множителя
    c = 0
    Mn_term1 = {}
    Mn_term2 = {}
    for term in (term1, term2):
        #print("term ", term)
        factors = {}
        result = ''
        for j in variables: #берём переменную из списка который ввели в начале
            #print("variabl ", j)
            coef = ""
            check = True
            counter1 = 0
            counter2 = 0
            for k in term:
                if k == j: #ищем её в полученной функции
                    #print(counter1, counter2, k)
                    coef += term[counter2:counter1-1] + "+"
                    term = term[:counter2]+term[counter1+2:]
                    counter1 = counter2
                    counter2 = 0 
                    check = True
                    continue
                if k == "+" and counter1 !=0:
                    for m in term[counter2:counter1]:
                        if m in variables:
                            counter2 = counter1 + 1
                            check = False
                            break
                    if check :
                        result += term[counter2:counter1] + "+"
                        #print(term, counter1, counter2)
                        term = term[:counter2] + term[counter1+1:]
                        counter1 = counter2
                        counter2 = 0
                        #print(counter1)
                        continue
                if i == "+" and counter1 == 0 :
                    continue
                counter1 += 1    

            if len(coef) > 0:
                if  coef[-1] == "+":
                    coef = coef[:-1]
                    factors[j] = coef
                    #print(j, coef)

        result += term
        factors["free"] = result
        if c == 0:
            Mn_term1 = factors
            c += 1
        else:
            Mn_term2 = factors
    
    #print("Mn_term1 ", Mn_term1)
    #print("Mn_term2 ", Mn_term2)
    
    if not "free" in variables:
        variables.append("free")

    str5 = 'Or('
    for j in variables:
        if not j in Mn_term1:
            Mn_term1[j] = "0"
        if not j in Mn_term2:
            Mn_term2[j] = "0"    
        str5 += "(" + Mn_term1[j] + ">" + Mn_term2[j] + "), "
        Result_F.add(eval(Mn_term1[j] + ">=" + Mn_term2[j]))
    str5 = str5[:-2] + ")"
    Result_F.add(eval(str5))
    #print(str5)


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
                        for Result_F in (new[j].split("+")):
                            term_new += coefficients[l][j] + "*" + Result_F + "+"
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

Result_F = Solver()

expression = input()
while expression != '0':
    expression = ''.join(expression.split())
    terms.append(expression)
    expression = input()

for i in range(len(terms)):
    rewriting(terms[i])


print(Result_F.check())
if Result_F.check() == z3.sat:
    print(Result_F.model())
