import sys
import random

def random_regex(max_len_regex):
    global regex
    if max_len_regex > 1:
        if len(regex) == 0:
            letter1 = random.choice(alphabet)
            if random.choice([0, 1]) == 1: 
                letter1 += "*"
            letter2 = random.choice(alphabet)
            if random.choice([0, 1]) == 1: 
                letter2 += "*"
            if random.choice([0, 1]) == 1: # выбор бинарной операции | или e
                regex += ("(" + letter1 + "|" + letter2 + ")")
            else:
                regex += (letter1 + letter2)
            max_len_regex -= 1
        else:
            letter3 = random.choice(alphabet)
            if random.choice([0, 1]) == 1: 
                letter3 += "*"
            if "(" in regex:
                if random.choice([0, 1]) == 1: # выбор бинарной операции | или e
                    index = regex.rindex("(")
                    regex = regex[:index+1] + "(" + regex[index+1:]
                    regex += ("|" + letter3 + ")")
                else:
                    regex += letter3
            else:
                regex += letter3
            max_len_regex -= 1
        random_regex(max_len_regex)
    else:
        letter4 = random.choice(alphabet)
        if random.choice([0, 1]) == 1: # выбор будет ли последняя буква иметь * или нет 
            regex += (letter4 +"*")
        else:
            regex += letter4 +"*"
    return(regex)




alpabet_size = int(input("Введите размер алфавита: "))

if alpabet_size > 5:
    print('Нам не нужны "ёжики"!!!')
    sys.exit()

# заполняем алфавит буквами
alphabet = []
letters = 'abcdf'
for i in range(alpabet_size):
    alphabet.append(letters[i])
print(alphabet)


#stars = int(input("Введите звёздную высоту: ")) # звёздная высота

regex = '' # регулярка

max_len_regex = int(input("Введите максимальное число букв в регулярке: ")) # максимальное число букв в регулярке

if max_len_regex == 0:
    print('А как...?')
    sys.exit()

# если в регулярке всего одна буква то ситуация простая
if max_len_regex == 1:
    regex = random.choice(alphabet)
    if  random.choice([0, 1]) == 1:
        regex += "*"
    print(regex)
else:
    print(random_regex(max_len_regex-1))
