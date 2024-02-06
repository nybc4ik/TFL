import sys
import random
import re

def random_regex(regex):
    global alphabet, stars, max_len_regex
    operation = ["|", ""]
    amount_of_letters = 0
    if regex == []:
        if random.randint(0, 1) == 1:
            regex.append("(")
        else:
            regex.append(random.choice(alphabet))    
        # print(res)
    else:
        amount_of_letters = regex.count("a") + regex.count("b") + regex.count("c") + regex.count("d") + regex.count("f")
        if amount_of_letters + 2 < max_len_regex:
            if regex[len(regex)-1] in alphabet or  (regex[len(regex)-1] == ")") or(regex[len(regex)-1] == ")" + "*"*stars):
                if regex.count("(") > (regex.count(")") + regex.count(")" + "*"*stars)):
                    regex.append(random.choice(operation+[")", ")"+"*"*stars, "*"*stars, "("]))
                else:
                    regex.append(random.choice(operation + ["*"*stars, "("]))
            if regex[len(regex)-1] in operation or (regex[len(regex)-1] == "*"*stars) or (regex[len(regex)-1] == "("):
                regex.append(random.choice(alphabet + ["("]))
        else:
            if regex[len(regex)-1] in alphabet  or  (regex[len(regex)-1] == ")"):
                if regex.count("(") > (regex.count(")") + regex.count(")"+"*"*stars)):
                    regex.append(random.choice([")", ")"+"*"*stars, "*"*stars, "("]))
                else:
                    regex.append(random.choice(["*"*stars, "("]))
            if regex[len(regex)-1] in operation or (regex[len(regex)-1] == "(") or (regex[len(regex)-1] == "*"*stars) or (regex[len(regex)-1] == ")"+"*"*stars):
                regex.append(random.choice(alphabet + ["("]))

    if amount_of_letters == max_len_regex:
        if regex.count("(")>(regex.count(")") + regex.count(")"+"*"*stars)):
            regex.append(random.choice([")"*(regex.count("(") - regex.count(")") - regex.count(")"+"*"*stars)), ")"*(regex.count("(")-regex.count(")") - regex.count(")"+"*"*stars))+"*"*stars]))
        final_regex = ""
        for i in range(len(regex)):
            final_regex += regex[i]

        #print("проверочка 1", final_regex)
        for i in range(len(final_regex)):
            final_regex = final_regex.replace("()"+"*"*stars, "")
            final_regex = final_regex.replace("()", "")
        #print("проверочка 2", final_regex)
        return final_regex
    else:
        return random_regex(regex)


   

def create_regex():
    global regex, alphabet, stars, max_len_regex
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
    max_len_regex = 6
    if max_len_regex == 0:
        print('А как...?')
        sys.exit()

    # если в регулярке всего одна буква то ситуация простая
    if max_len_regex == 1:
        regex = random.choice(alphabet)
        if  random.choice([0, 1]) == 1:
            regex += "*"*stars
        #print(regex)
    else:
        regex = []
        regex = random_regex(regex)
        #print(random_regex(max_len_regex-1))
    #print(regex)
    #print(re.sub(r'(\S)\|(S)', r'\1(\|\2)', regex)
    #regex = (re.sub(r'(\S)\|(S)', r'\1(\|\2)', regex))
    #уборка 
     
    pattern = r'\(([a-zA-Z])\)'
    matches = re.finditer(pattern, regex)
    for match in matches:
        if len(match.group(1)) == 1:
            regex = regex[:match.start()] + match.group(1) + regex[match.end():]
    return regex
#s = create_regex()
#print(s)
