import sys
import random
import re


def add_stars(input_string, num_stars): #случайно добавляет звёздочки в строку (очень важная вещь, а ещё экономит место)
    if num_stars <= 0 or num_stars > len(input_string):
        return input_string

    positions = random.sample(range(len(input_string)), num_stars)
    output = ''
    for i, char in enumerate(input_string):
        if i in positions:
            output += char + '**'
        else:
            output += char
    return output


def generate_oreo(len): #для заполнения пустот в ()
    global alphabet, stars
    if len == 2:
        oreo = "(" + random.choice(alphabet) + "|" + random.choice(alphabet) + ")"
        #print(oreo)
        return(oreo)
    elif len == 3: 
        if random.randint(0,1) == 1:
            oreo = "(" + random.choice(alphabet) + "|" + random.choice(alphabet) + random.choice(alphabet)  + ")"
            #print(oreo)
            return(oreo)
        else:
            oreo = "(" + random.choice(alphabet) + random.choice(alphabet)+ "|" + random.choice(alphabet) + ")"
            #print(oreo)
            return(oreo)
    elif len >=  4: #возможен вариант с двойными скобками! ((|)|(|)) 
        if random.randint(0,1) == 1: #будут скобки
            if len % 2 == 0:
                left_part = generate_oreo(int(len/2))
                right_part = generate_oreo(int(len/2))
            else:
                if random.randint(0,1) == 1:
                    left_part = generate_oreo(int((len/2)+1))
                    right_part = generate_oreo(int(len/2))
                else:
                    left_part = generate_oreo(int(len/2))
                    right_part = generate_oreo(int((len/2)+1))
            #обработка исключений
            if left_part == None:
                print("ошибка слева!")
                return("Eror_left")
            elif right_part == None:
                print("ошибка справа!")
                return("Eror_right")
            oreo = "(" + left_part + "|" + right_part + ")"
            #print(oreo)
            return(oreo)
        else: #или нет
            if len % 2 == 0:
                left_part1 = ''.join(random.choice(alphabet) for _ in range(int(len/2)))  
                right_part1 = ''.join(random.choice(alphabet) for _ in range(int(len/2)))   
            else:
                if random.randint(0,1) == 1:
                    left_part1 = ''.join(random.choice(alphabet) for _ in range(int((len/2)+1)))  
                    right_part1 = ''.join(random.choice(alphabet) for _ in range(int(len/2)))
                else:
                    left_part1 = ''.join(random.choice(alphabet) for _ in range(int(len/2)))   
                    right_part1 = ''.join(random.choice(alphabet) for _ in range(int((len/2)+1)))  
            oreo = "(" + left_part1 + "|" + right_part1 + ")"
            #print(oreo)
            return(oreo)
    elif len == 1:
        if random.randint(0,1) == 1:    
            return(random.choice(alphabet)) + "*"*stars
        else: 
            return(random.choice(alphabet))
            

def random_regex(regex, max_len_regex):
    global alphabet, stars
    #print("полученые данные:")
    #print("длина регулярка", max_len_regex)
    #print("реуглярка", regex)
    amount_of_letters = 0   
    if max_len_regex == 1: #если длина 1, то добавляем букву ... другого выхода у нас нет 
        if random.randint(0,1) == 1: #звёздная высота 
            regex += random.choice(alphabet) + "*"*stars
            #print("лови звёздочки!!", regex)
        else:
            regex += random.choice(alphabet)
        amount_of_letters += 1
        return(regex)
    if max_len_regex >=2: #если длина больше двух, то добавляем операцию (или не добавляем)
        if random.randint(0,1) == 1:
            abc = random.randint(2,max_len_regex)
            max_len_regex -= abc
            amount_of_letters += abc
            regex += generate_oreo(abc)
            #print("проверка 1", regex, abc)
        else:
            abc = random.randint(2,max_len_regex)
            max_len_regex -= abc
            amount_of_letters += abc
            bukovi = ''.join(random.choice(alphabet) for _ in range(abc)) 
            if random.randint(0,1) == 1: #добавим звёздочек
                #print("добавляем звёздочки")
                boukovi2 = add_stars(bukovi, stars)
                regex += boukovi2
            else: 
                regex += bukovi
            #print(regex, abc)
    #print("длина", max_len_regex)
    if max_len_regex == 0: #не осталось свободных букв? выходим
        #print("проверка перед выходом", regex)
        return(regex)
    else: #остались свободные буквы
        #print("проверка", regex, max_len_regex)
        return(random_regex(regex, max_len_regex))
        

def split_with_brackets(expression): 
    result = []
    count = 0
    temp = ""
    for char in expression:
        if char == "(":
            count += 1
            temp += char
        elif char == ")":
            count -= 1
            temp += char
            if count == 0:
                result.append(temp)
                temp = ""
        elif count > 0:
            temp += char
        else:
            result.append(char)
    return result


def stars_ading(regex, stars):
    if random.randint(0,1) == 0: #простой (позитивный случай) добавляем в конец все звёздочки
        regex +=  "*"*stars
    else:
        num1 = random.randint(0,stars)
        left_part = "*"*num1 +"|"
        num2 = random.randint(0,stars)
        right_part = "*"*num2 + ")"
        regex = regex.replace("|", left_part)
        regex = regex.replace(")", right_part)
        if num1 > num2:
            regex +=  "*"*(stars - num1)
        else:
            regex +=  "*"*(stars - num2) 
    return(regex)


def add_stars_brac(regex, stars):
    arr_regex = split_with_brackets(regex)
    for i in range(len(arr_regex)):
        if "(" in arr_regex[i]:
            arr_regex[i] = stars_ading(arr_regex[i], stars)
    return(arr_regex)

def create_regex():
    global regex, alphabet, stars
    #alpabet_size = int(input("Введите размер алфавита: "))
    alpabet_size = 3
    if alpabet_size > 5:
        print('Нам не нужны "ёжики"!!!')
        sys.exit()

    # заполняем алфавит буквами
    alphabet = []
    letters = 'abcdf'
    for i in range(alpabet_size):
        alphabet.append(letters[i])
    #print(alphabet)
    #звёздная высота
    #stars = int(input)
    stars = 2

    #max_len_regex = int(input("Введите максимальное число букв в регулярке: ")) # максимальное число букв в регулярке
    max_len_regex = 10
    if max_len_regex == 0:
        print('А как...?')
        sys.exit()

    # если в регулярке всего одна буква то ситуация простая
    if max_len_regex == 1:
        regex = random.choice(alphabet)
        if  random.choice([0, 1]) == 1:
            regex += "*"*stars
    else:
        regex = ''
        regex = random_regex(regex, max_len_regex)
    #добавим звёздную высоту в скобки!
    if random.randint(0,1) == 1: 
        regex = add_stars_brac(regex, stars)
        regex = ''.join(map(str,regex))
    return regex


s = create_regex()
#print("финалочка",s)

"""
#Тестирование
for i in range(10):
    s =  create_regex()
    print("регулярка номер: ", i ," ", s)
"""
