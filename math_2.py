import matplotlib as mplot
import matplotlib.pyplot as pyplot
import math

def calculate(n, a, b):
    for i in range (0, (int(n / a) + 1)):
        if (n - i*a) % b == 0:
            return True
    return False

def check_is_prime(number):
    # print("num being checked: ", number)
    for i in range(2, number):
        if number % i == 0:
            # print("not prime: ", number, i, number % i)
            return False
    return True
 
# print("yea:")
# print("-----------------------")


a = -1
b = -1
c_value = -1

list_index = 0
expected = 3
check_depth = 10000
last = 0
num = -1
prime_list = [[], [], []]
num_list = [[], [], []]
sheets = False

# for c in range (check_depth):
#     if calculate(c, a, b):
#         factors = []
#         for i in range(1, c+1):
#             if c % i == 0:
#                 factors.append(i)
#         # total = 0
#         # for i in range(len(factors)):
#         #     total = total + factors[i]
#         print("c:", c, "difference:", c - last)
        # print(c)
        # if c - last != expected:
        #     if c > a + b:
        #         print("exception:", c, "difference of", c - last)
        # last = c
        # print("factors", factors)
        # print("total:", total)

# print("_______________________")
# print("not possible:")
# print("-----------------------")

def set_up():
    a = 5
    b = 5
    c = 5
    check_depth = 500

    calc_over_range(50)


def calc_over_range(range_num):
    new_prime_list = []
    new_num_list = []
    num = -1
    for i in range(1, range_num):
        if i % a == 0:
            print("null")
            continue
        for c in range (check_depth):
            if not calculate(c, a, i):
                num = c
        print(i, num)
        new_num_list.append(num)
        if check_is_prime(num):
            new_prime_list.append(num)

    return new_num_list, new_prime_list

def calc_over_area(range_num, a_start_num):
    new_prime_list = []
    new_num_list = []
    num = -1
    for z in range(a_start_num, range_num):
        for i in range(1, range_num):
            for c in range (check_depth):
                if not calculate(c, z, i):
                    num = c
            num_list.append(num)
            print(i, num)
            if check_is_prime(num):
                prime_list.append(num)

    return num_list, prime_list

def calc_prime_differences(prime_list):
    prime_diff_list = []
    if not sheets:
        for i in range(2, len(prime_list)):
            prime_diff_list.append(prime_list[i] - prime_list[i-1])

    return prime_diff_list

def print_list(num_list):
    if not sheets:
        for i in range(len(num_list)):
            print(i, num_list[i])
    else:
        for i in range(len(num_list)):
            print(num_list[i], ", ")

def set_value(value, min, max):
    while True:
        try:
            if value >= min and value <= max:
                int_value = int(value)
                break
            else:
                value = input("entered value outside of designated ranges. enter new value: ")
        except ValueError:
            value = input("invalid value type; enter an integer: ")
    return int_value


print("program intitiated")
# set_up()

while True:
    print("")
    print("check depth:", check_depth, "sheets:", sheets)
    print(a, b, c_value)
    action = input("enter command: ")

    if action == "prime diff":
        print_list(calc_prime_differences(prime_list[list_index]))

    elif action == "prime list":
        print_list(prime_list[list_index])

    elif action == "toggle sheets":
        if sheets:
            sheets = False
            print("sheets set to false")
        else:
            sheets = True
            print("sheets set to true")

    elif action == "set vals":
        a = set_value(input("enter value for a: "), 1, math.inf)
        b = set_value(input("enter value for b: ", 1, math.inf))
        c_value = set_value(input("enter value for c: ", 1, math.inf))

        check_depth = set_value(input("enter value for check depth: "))

    elif action == "calc single val":
        if calculate(c_value, a, b):
            print("the given values for a, b, and c work")
        else:
            print("the given values for a, b, and c do not work")

    # elif action == "calcgreatestfail":
    #     calc_over_range(b)

    elif action == "calc range":
        num_list[list_index], prime_list[list_index] = calc_over_range(set_value(input("enter range: ")))

    elif action == "graph":
        data = input("enter name of data set: ")

        if data == "help":
            print("prime list")
            print("prime diff")

            data = input("enter name of data set: ")
        
        if data == "prime list":
            print("Prime Numbers Graph")
            print("-------------------")
            pyplot.plot(prime_list[0], prime_list[1], prime_list[2])
            pyplot.show()

        if data == "prime diff":
            print("Prime Differences Graph")
            print("-----------------------")
            graph_list = [calc_prime_differences(prime_list[0]), calc_prime_differences(prime_list[1]), calc_prime_differences(prime_list[2])]
            pyplot.plot(graph_list[0])
            pyplot.plot(graph_list[1])
            pyplot.plot(graph_list[2])
            pyplot.show()

        else:
            print("invalid data set")

    elif action == "list index":
        list_index = int(input("Enter new list index: "))

    elif action == "help":
        print("set vals")
        print("calc range")
        print("prime list")
        print("prime diff")
        print("calc single val")
        print("graph")
        print("list index")

    else:
        print("error: unknown command")
