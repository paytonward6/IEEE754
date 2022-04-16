import math

# Python 3.8.10 on CSX Server
def whole_num_to_binary(num):
    return '{0:08b}'.format(num)

#0.75
def float_to_binary(num):
    to_return = ""
    for i in range(len(str(num)) - 2):
        tmp = num * 2
        if tmp < 1:
            to_return += "0"
        else:
            to_return += "1"
        num = tmp
    to_return = "0." + to_return
    return float(to_return)

def num_to_scientific_notation(num):
    return "{:e}".format(num)

def get_exponent(str_num):
    start = str_num.find('e') + len('e')
    end = len(str_num)
    exponent = str_num[start:end]

    return int(exponent)

def split_num(num):
    to_return = ""
    if abs(num) < 1:
        to_return = [str(num)]
    else:
        to_return = str(num).split(".")
        if len(to_return) == 2:
            to_return[1] = "0." + to_return[1]
    return to_return

def to_base_2(num):
    num = split_num(abs(num))
    to_return = ""
    if len(num) == 1:
        if abs(float(num[0])) < 1:
            return float_to_binary(float(num[0]))
        else:
            return whole_num_to_binary(int(num[0]))
    else:
        whole = whole_num_to_binary(int(num[0]))
        frac = float_to_binary(float(num[1]))
        return float(str(whole) + str(frac)[1:])

def get_full_decimal(num):
    base_2 = to_base_2(num)
    base_2_str = str(base_2)
    exp = get_exponent(num_to_scientific_notation(base_2))
    #if exp < 0:
    print(exp)
    decimal = base_2_str.find('.')
    print(decimal)
    to_return = ""
    if abs(base_2) > 1:
        to_return = base_2_str[0] + "." + base_2_str[1:].replace(".", "")
    else:
        base_2_str = base_2_str[2:]
        to_return = base_2_str[:-exp] + "." + base_2_str[-exp:]
    return to_return

def sign_bit(num):
    if num < 0:
        return 1
    else:
        return 0

def exponent_IEEE754(str_num):
    exp = get_exponent(str_num)
    return whole_num_to_binary(exp + 127)

def main():
    num = 0.825

    x = to_base_2(num)
    print(get_full_decimal(num))

if __name__ == '__main__':
    main()