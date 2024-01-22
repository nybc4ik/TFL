import sys
import random

def random_regex(max_len_regex):
    global regex, alphabet, stars
    if max_len_regex > 1:
        if len(regex) == 0:
            letter1 = random.choice(alphabet)
            if random.choice([0, 1]) == 1: 
                letter1 += "*"* random.randint(0, stars)
            letter2 = random.choice(alphabet)
            if random.choice([0, 1]) == 1: 
                letter2 += "*"*random.randint(0, stars)
            if random.choice([0, 1]) == 1: # выбор бинарной операции | или e
                regex += ("(" + letter1 + "|" + letter2 + ")")
                if random.choice([0, 1]) == 1: 
                    regex += "*"*random.randint(0, stars)
            else:
                regex += (letter1 + letter2)
            max_len_regex -= 1
        else:
            letter3 = random.choice(alphabet)
            if random.choice([0, 1]) == 1: 
                letter3 += "*"*random.randint(0, stars)
            if "(" in regex:
                if random.choice([0, 1]) == 1: # выбор бинарной операции | или e
                    index = regex.rindex("(")
                    regex = regex[:index+1] + "(" + regex[index+1:]
                    regex += ("|" + letter3 + ")")
                    if random.choice([0, 1]) == 1: 
                        regex += "*"*random.randint(0, stars)
                else:
                    regex += letter3
            else:
                regex += letter3
            max_len_regex -= 1
        random_regex(max_len_regex)
    else:
        letter4 = random.choice(alphabet)
        if random.choice([0, 1]) == 1: # выбор будет ли последняя буква иметь * или нет 
            regex += (letter4 +"*"*random.randint(0, stars))
        else:
            regex += letter4 +"*"*random.randint(0, stars)
    return(regex)



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

    regex = '' # регулярка

    #звёздная высота
    #stars = int(input)
    stars = 5

    #max_len_regex = int(input("Введите максимальное число букв в регулярке: ")) # максимальное число букв в регулярке
    max_len_regex = 20
    if max_len_regex == 0:
        print('А как...?')
        sys.exit()

    # если в регулярке всего одна буква то ситуация простая
    if max_len_regex == 1:
        regex = random.choice(alphabet)
        if  random.choice([0, 1]) == 1:
            regex += "*"
        #print(regex)
    else:
        regex = random_regex(max_len_regex-1)
        #print(random_regex(max_len_regex-1))
    #print(regex)
    return regex
s = create_regex()
#print(s)