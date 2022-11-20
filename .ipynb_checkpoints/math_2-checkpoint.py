
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

expected = 3
check_depth = 10000
last = 0
num = -1
prime_list = []
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

def calc_over_range(range_num):
    num = -1
    for i in range(1, range_num):
        for c in range (check_depth):
            if not calculate(c, a, i):
                num = c
        print(i, num)
        if check_is_prime(num):
            prime_list.append(num)

def print_prime_differences(prime_list):
    if not sheets:
        for i in range(2, len(prime_list)):
            print(i, prime_list[i] - prime_list[i-1])
    else:
        for i in range(2, len(prime_list)):
            print(prime_list[i] - prime_list[i-1], ", ")

def print_list(num_list):
    if not sheets:
        for i in range(len(num_list)):
            print(i, num_list[i])
    else:
        for i in range(len(num_list)):
            print(num_list[i], ", ")

print("program intitiated")

while True:
    action = input()

    if action == "prime diff":
        print_prime_differences(prime_list)

    elif action == "prime list":
        print_list(prime_list)

    elif action == "toggle sheets":
        if sheets:
            sheets = False
            print("sheets set to false")
        else:
            sheets = True
            print("sheets set to true")

    elif action == "set vals":
        a = int(input("enter value for a: "))
        b = int(input("enter value for b: "))
        c_value = int(input("enter value for c: "))
        check_depth = int(input("enter value for check depth: "))

    elif action == "calc single val":
        if calculate(c_value, a, b):
            print("the given values for a, b, and c work")
        else:
            print("the given values for a, b, and c do not work")

    # elif action == "calcgreatestfail":
    #     calc_over_range(b)

    elif action == "calc range":
        calc_over_range(int(input("enter range: ")))

    elif action == "help":
        print("set vals")
        print("calc range")
        print("prime list")
        print("prime diff")
        print("calc single val")

    else:
        print("error: unknown command")
