import sys
import random
import re


def generate_oreo(len): #для заполнения пустот в ()
    global alphabet
    if len == 2:
        if random.randint(0,1) == 1:    
            oreo = "(" + random.choice(alphabet) + "|" + random.choice(alphabet) + ")" 
        else:
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
            regex += bukovi
            #print(regex, abc)
    #print("длина", max_len_regex)
    if max_len_regex == 0: #не осталось свободных букв? выходим
        #print("проверка перед выходом", regex)
        return(regex)
    else: #остались свободные буквы
        #print("проверка", regex, max_len_regex)
        return(random_regex(regex, max_len_regex))

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
    return regex


s = create_regex()
#print("финалочка",s)

"""
#Тестирование
for i in range(10): 
    print("регулярка номер: ", i ," ", create_regex())
"""
