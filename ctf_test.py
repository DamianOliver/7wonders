def check_for_tag(pos_1_x, pos_1_y, pos_2_x, pos_2_y):
        if abs(pos_1_x - pos_2_x) <= 10 + (10 * 0.5) + (10 * 0.5):
            if abs(pos_1_y - pos_2_y) <= 10 + (10 * 0.5) + (10 * 0.5):
                print("oh no")
                return True
        return False

if check_for_tag(1225, 1265, 580, 500):
    print("whyyyyyyy?")