import random
import re
import time


def close_skobka_blin(regex, open_skobka_number):
    counter_skobk = 0
    for i in range(open_skobka_number + 1, len(regex)):
         #print(i, counter_skobk)
        if regex[i] == "(":
            counter_skobk += 1
        if regex[i] == ")":
            if counter_skobk == 0:
                return i
            else:
                counter_skobk -= 1
    return "error"


def no_or(regex):
    i = 0
    while i < len(regex):
        if regex[i] == "|":
            return False
        if regex[i] == "(":
            i = close_skobka_blin(regex, i)
        i += 1
    return True


def pars(regex): #добавляем скобочек
    if len(regex) == 0:
        return regex

    result = ""
    for i in range(0, len(regex)-1):
        if regex[i+1] == "*" and regex[i] != ")":
            result += "("+regex[i]+")"
        else:
            result += regex[i]
    result += regex[-1]
    return liner(result)


counter = 0
variables = []
def liner(regex):
    if len(regex) == 1:
        if regex == "|" or regex == "&":
            return regex
        else:
            #print(regex)
            global counter
            counter += 1
            global variables
            new_regex = regex + str(counter)
            variables.append(new_regex)
            return new_regex
        
    elif regex[0] == "(" and close_skobka_blin(regex, 0) == len(regex) - 2 and regex[-1] == "*":
        if len(regex) == 4:
            return [[liner(regex[1])], "*"]
        return [liner(regex[1:-2]), "*"]
    elif regex[0] == "(" and close_skobka_blin(regex, 0) == len(regex)-1:
        if len(regex) == 3:
            return liner(regex[1])
        return liner(regex[1:-1])
    elif no_or(regex):
        Arr = []
        counter_start = 0
        i = 0
        while i < len(regex):
            if regex[i] != "(":
                if i != len(regex) - 1 and regex[i + 1] == "*":
                    Arr.append([regex[counter_start:i+1], "*"])
                    i+=1
                    counter_start = i + 2
                    
                else:
                    Arr.append(regex[counter_start:i + 1])
                    counter_start = i + 1 
                Arr.append("&")
                #print("проверка1 ", Arr)
            else:
                i = close_skobka_blin(regex, i)
                if i != len(regex)-1 and regex[i+1] == "*":
                    i += 1
                Arr.append(regex[counter_start:i+1])
                Arr.append("&")
                #print("проверка2 ", Arr)
                counter_start = i + 1
            i += 1
        for j in range(len(Arr)):
            Arr[j] = liner(Arr[j])
        return Arr[:-1]

    Arr = []
    counter_start = 0
    i = 0
    while i < len(regex):
        if regex[i] == "(":
            i = close_skobka_blin(regex, i)
        elif regex[i] == "|":
            Arr.append(regex[counter_start:i])
            Arr.append("|")
            #print("проверка3 ", Arr)
            counter_start = i+1
        i += 1
    Arr.append(regex[counter_start:i])

    for j in range(len(Arr)):
        Arr[j] = liner(Arr[j])
    return Arr


#ищем First
def first(regex):
    return first1(regex)[0]
def first1(regex):
    if isinstance(regex, str):
        return [regex], False

    if len(regex) == 1:
        return first1(regex[0])

    elif len(regex) == 2 and regex[1] == "*":
        return first1(regex[0])[0], True

    elif len(regex) >= 3 and regex[1] == "&":
        data, data2 = first1(regex[0])
        if data2:
            l, data1 = first1(regex[2:])
            return data + l, data1
        else:
            return data, False

    else:
        result = []
        data2 = False
        for i in range(0, len(regex), 2):
            data, data1 = first1(regex[i])
            result += data
            data2 = data2 or data1

    return result, data2


#ищем Last
def last(regex):
    return last1(regex)[0]


def last1(regex):
    if isinstance(regex, str):
        return [regex], False

    elif len(regex) == 1:
        return last1(regex[0])

    elif len(regex) == 2 and regex[1] == "*":
        return last1(regex[0])[0], True

    elif len(regex) >= 3 and regex[1] == "&" :
        data, data2 = last1(regex[-1])
        if data2:
            l, data1 = last1(regex[0:-2])
            return l + data, data1
        else:
            return data, False

    else:
        result = []
        data2 = False
        for i in range(0, len(regex), 2):
            data, data1 = last1(regex[i])
            result += data
            data2 = data2 or data1

        return result, data2


#ищем follow
def follow_(regex, var):
    if isinstance(regex, str):
        return []
    elif len(regex) == 1:
        return follow_(regex[0], var)
    elif len(regex) == 2 and regex[1] == "*":
        result = follow_(regex[0], var)
        if var in last(regex[0]):
            result += first(regex[0])

        return result

    elif len(regex) >= 3 and regex[1] == "|":
        result = []
        for i in range(0, len(regex), 2):
            result += follow_(regex[i], var)
        return result
    elif len(regex) >= 3 and regex[1] == "&":
        result = []
        for i in range(0, len(regex), 2):
            result += follow_(regex[i], var)
            # if i < len(regex)-2 and var in last(regex[i]):
            if var in last(regex[i]):
                for j in range(i+2, len(regex), 2):
                    result += first(regex[j])
                    if not(len(regex[j]) == 2 and regex[j][1] == "*"):
                        break

                # result += first(regex[i+2])
        return result
    else:
        return ["!"]


last_regex = []
def make_automata(regex):
    global last_regex
    regex1 = pars(regex)
    #print("regex после линеризации", regex1)

    first_regex = first(regex1)
    last_regex = last(regex1)
    #print("first ", first_regex)
    #print("last ", last_regex)

    result = []
    for i in range(len(first_regex)):
        result.append(("S", first_regex[i][0], first_regex[i]))
    for i in range(len(variables)):
        follows = follow_(regex1, variables[i])
        #print(follows, variables[i])
        for j in range(len(follows)):
            result.append((variables[i], follows[j][0], follows[j]))

    return result

regex = input("Введите регулярку: ") #"((((((b*|c)|a*)a|b*)|b)|b*)c|c)c*"

automata = make_automata(regex)
#print(automata)


#постройка матрицы достижимости
Arr_k = []
def reachability_for_variables(k, automata):
    result = []
    for i in range(len(automata)):
        if automata[i][0] == k:
            global Arr_k
            if not (automata[i][2] in Arr_k):
                result.append(automata[i][2])
                Arr_k.append(automata[i][2])
                result += reachability_for_variables(automata[i][2], automata)
    return result


def reachability_matrix(automata):
    result = []
    result.append(("S", variables))
    for k in variables:
        global Arr_k
        Arr_k = []
        result.append((k, reachability_for_variables(k, automata)))
    return result
#print("matrix ", reachability_matrix(automata))


# матрица достижимости из себя
def reachability_from_itself(matrix):
    result = []
    for i in range(len(matrix)):
        if matrix[i][0] in matrix[i][1]:
            result.append(matrix[i][0])
    return result


def find_next_step(k, reach_list, reach_matrix):
    # next_step = []
    for i in range(len(reach_matrix)):
        if reach_matrix[i][0] == k:
            next_step = []
            for j in range(len(reach_matrix[i][1])):
                if reach_matrix[i][1][j] in reach_list:
                    next_step.append(reach_matrix[i][1][j])
            return next_step


def first_index(sb, strok):
    result = []
    for i in range(len(strok)):
        if strok[i][0] == sb:
            result.append(i)
    if len(result) == 1:
        return result[0]
    else:
        return result
    

#создаём слово 
def word_creator(first_letter, last_letter, automat):
    word = ""
    next_letter = []
    if first_letter == last_letter and last_letter in reach_matrix[first_index(first_letter, reach_matrix)][1]:
        return ""
    if last_letter in reach_matrix[first_index(first_letter, reach_matrix)][1]:
        for i in range(len(automat)):
            if automat[i][0] == first_letter:
                if last_letter in reach_matrix[first_index(automat[i][2], reach_matrix)][1] or last_letter==automat[i][2]:
                    next_letter.append(automat[i][2])
        if len(next_letter) == 0:
            return last_letter[0]
        if len(next_letter) == 1:
            if next_letter == first_letter:
                 word += next_letter[0][0]*random.randint(100, 500)
            else:
                word += next_letter[0][0]
            nq = next_letter[0]
        else:

            nq = random.choice(next_letter)
            if nq == first_letter:
                wn = nq[0][0]*random.randint(100, 500)
                word += wn
            else:
                word += nq[0][0]
        return word + word_creator(nq, last_letter, automat)
    else:
        return ""
    

#матрица достижимости 
global reach_matrix
reach_matrix = reachability_matrix(automata)
reach_list = reachability_from_itself(reach_matrix) 
#print(reach_list)
last_letter = random.choice(last_regex)
final_word = word_creator("S", last_letter, automata)
#print(final_word)


#накачка слова
done = False
def cycle(Q, last, automat, done):
    next_letter = []
    word = ""
    if not done:
        for i in range(len(automat)):
            if automat[i][0] == Q and last in reach_matrix[first_index(automat[i][2], reach_matrix)][1]:
                next_letter.append(automata[i][2])
        if len(next_letter) == 1:
            if next_letter == Q:
                word += next_letter[0][0]
            else:
                word += next_letter[0][0]
            nq = next_letter[0]
        else:
            nq = random.choice(next_letter)
            if nq == Q:
                wn = nq[0][0]
                word += wn
            else:
                word += nq[0]
        if nq == last:
            done = True
        return word + cycle(nq, last, automat, done)
    else:
        return ""

cycl = False
for i in range(len(reach_list)):
    if reach_list[i] in last_regex:
        is_cycl = True


new_reach_list = []
for k in last_regex:
        for i in range(len(reach_list)):
            #print(reach_list[i], i)
            if k in reach_matrix[first_index(reach_list[i], reach_matrix)][1]:
                if reach_list[i] in reach_matrix[first_index(k, reach_matrix)][1]:
                    new_reach_list.append(reach_list[i])


reach_list = new_reach_list

for k in range(10):
        if len(reach_list) == 0 or not is_cycl:
            last_letter = random.choice(last_regex)
            final_word = word_creator("S", last_letter, automata)
        else:
            result = ["S"]
            next_step = reach_list
            is_continue = 1
            while is_continue and len(next_step) !=0 :
                r = random.randint(0, len(next_step)-1)
                result.append(next_step[r])
                result.append(next_step[r])
                if next_step[r] not in last_regex:
                    is_continue = 1
                else:
                    is_continue = random.randint(0, 1)
                next_step = find_next_step(next_step[r], reach_list, reach_matrix)
            #print(result)
            final_word = ""

            for i in range(len(result)-1):
                if result[i] == result[i+1]:
                    repeat = random.randint(300, 1000)
                    final_word += cycle(result[i], result[i], automata, False)*repeat
                else:
                    final_word += word_creator(result[i], result[i+1], automata)



print("слово ", final_word)

final_word += "Ъ" #добавляем символ которого ТОЧНО НЕТ в регулярке 


#необходимо союлюдать звёздную высоту!
star_hight = 100 #пусть будет 100 звёздочек!!!
def shorten_chars(match):
    return match.group(0)[:star_hight]
final_word = re.sub(r'(.)\1+', shorten_chars, final_word)
print("обрезанное слов: ", final_word)


#тут я сравниваю время 
def match(pattern, word):
    return re.fullmatch(pattern, word)


regular1 = regex #оригинальная регулярка
regular2 = input("Введите оптимизированное выражение: ") #оптимизированная регулярка


#оригинальная регулярка
check = True
while True:
    start_time = time.time()
    sravnim = match(regular1, final_word)
    end_time = time.time()
    if end_time - start_time < 30:
        check = True
        break
    else:
        check = False
        break

if check == False:
    print("превышено время ожидания...")
else:
    print("время с оригинальная регуляркой: ", end_time - start_time, " регулярка: ", regular1)
print('\n')


#оптимизированная регулярка
start_time = time.time()
sravnim = match(regular2, final_word)
end_time = time.time()
print("время с оптимизированной регуляркой: ", end_time - start_time, " регулярка: ", regular2)
