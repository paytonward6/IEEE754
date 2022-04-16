import math
from re import A

from scipy.fftpack import shift

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
    decimal = base_2_str.find('.')
    to_return = ""
    if abs(base_2) > 1:
        to_return = base_2_str[0] + "." + base_2_str[1:].replace(".", "")
    else:
        base_2_str = base_2_str[2:]
        to_return = base_2_str[:-exp] + "." + base_2_str[-exp:]
    return to_return

def get_after_decimal(num):
    decimal_num = str(get_full_decimal(num))
    decimal = decimal_num.find(".")
    return decimal_num[decimal + 1:]

def sign_bit(num):
    if num < 0:
        return 1
    else:
        return 0

def exponent_IEEE754(str_num):
    exp = get_exponent(str_num)
    return whole_num_to_binary(exp + 127)

def mantissa_maker(num):
    mantissa = get_after_decimal(num)
    while len(mantissa) < 23:
        mantissa += "0"
    return mantissa

def full_IEEE754(num):
    to_return = []
    str_num = num_to_scientific_notation(to_base_2(num))
    sign = sign_bit(num)
    exponent = exponent_IEEE754(str_num)
    mantissa = mantissa_maker(num)

    to_return.append(sign)
    to_return.append(exponent)
    to_return.append(mantissa)
    return to_return

def bin_mult(num1, num2):
    num1_str, num2_str = str(num1), str(num2)
    mult = int(num1_str, 2) * int(num2_str, 2)
    bin_result = bin(mult)[2:]
    return bin_result

def bin_sub(num1, num2, abs_val=False):
    num1_str, num2_str = str(num1), str(num2)
    sub = 0
    if abs_val:
        sub = abs(int(num1_str, 2) - int(num2_str, 2))
    else:
        sub = int(num1_str, 2) - int(num2_str, 2)
    bin_result = bin(sub)[2:]
    return bin_result

def bin_add(num1, num2, abs_val=False):
    num1_str, num2_str = str(num1), str(num2)
    sum = 0
    if abs_val:
        sum = abs(int(num1_str, 2) + int(num2_str, 2))
    else:
        sum = int(num1_str, 2) + int(num2_str, 2)
    bin_result = bin(sum)[2:]
    return bin_result

def shift_right_arith(bin_num, prepend=True):
    to_return = [0]*len(bin_num)
    if prepend:
        if bin_num[0] == '1':
            to_return[0] = 1
    else:
        to_return[0] = 0

    for i in range(1, len(bin_num)):
        to_return[i] = bin_num[i-1]
        
    to_return = "".join(str(i) for i in to_return)
    return to_return;

def ADD_exp(num1, num2):
    num1_exp, num2_exp = num1[1], num2[1]
    exp = ""
    exp_diff = int(bin_sub(num2_exp, num1_exp, abs_val=True), 2)

    if int(num1_exp, 2) > int(num2_exp, 2):
        exp = num1_exp
        shift_num2_M = num2[2]
        check = True
        for i in range(exp_diff):
            shift_num2_M = shift_right_arith(shift_num2_M, prepend=check)
            check = False
        num1[2] = "1" + num1[2]
        num2[2] = "0" + shift_num2_M
        add_mantissas(num1[2], num2[2])

    elif int(num1_exp, 2) < int(num2_exp, 2):
        exp = num2_exp
        shift_num1_M = num1[2]
        check = True
        for i in range(exp_diff):
            shift_num1_M = shift_right_arith(shift_num1_M, prepend=check)
            check = False
        num2[2] = "1" + num2[2]
        num1[2] = "0" + shift_num1_M
        add_mantissas(num2[2], num1[2])
#100.0101
#0.010

def add_mantissas(num1_M, num2_M):
    init_length = len(num1_M)
    shift = 0
    sum_M = bin_add(num1_M, num2_M) 
    if sum_M[0] == 1:
        shift = init_length - 23 - 1
    else:
        shift = x.find('1') + 1
    print(sum_M)

def main():
    num1 = float(2345.125)
    num1_IEEE754 = full_IEEE754(num1)

    num2 = float(.75)
    num2_IEEE754 = full_IEEE754(num2)
    print(num1_IEEE754)
    print(num2_IEEE754)

    ADD_exp(num1_IEEE754, num2_IEEE754)

if __name__ == '__main__':
    main()