from tabnanny import check
import matplotlib as mplot
import matplotlib.pyplot as pyplot
import math

spin_number = 5
check_depth = 100

results_list = []

def spin_add(num_1, num_2, spin_num):
    return (num_1 + num_2) % spin_num

def spin_mult(num_1, num_2, spin_num):
    return (num_1 * num_2) % spin_num



def test_associative_mult(spin_num):
    num_exceptions = 0
    for a in range(check_depth):
        for b in range(check_depth):
            for c in range(check_depth):
                if spin_mult(a, (spin_mult(b, c, spin_num)), spin_num) == spin_mult(spin_mult(a, b, spin_num), c, spin_num):
                    continue
                else:
                    num_exceptions += 1

    if num_exceptions == 0:
        print(i, "- multiplicative associative: no exceptions found")
    else:
        print(i, "-", num_exceptions, "out of", check_depth**3, "cases")


for i in range(2, 50):
    test_associative_mult(i)

# for i in range(200):
#     results_list.append(spin_mult(i, 2))

# pyplot.plot(results_list)
# pyplot.show()
