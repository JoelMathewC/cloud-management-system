import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    f = open("../client-log.txt", "r")

    res_arr_vm1 = []
    res_arr_vm2 = []
    x_vm1 = []
    x_vm2 = []

    res_count = 0
    for line in f:
        arr = line.split(" ")

        # Check if it is a response line
        if arr[0][0] == "T" or arr[0][0] == "G":
            val = line.split("|")
            if val[1] == "   Server: vm1  ":
                res_arr_vm1.append(float(arr[-1].strip()))
                res_count += 1
                x_vm1.append(res_count)
            else:
                res_arr_vm2.append(float(arr[-1].strip()))
                res_count += 1
                x_vm2.append(res_count)

    print(res_arr_vm1)
    np_vm1_y = np.array(res_arr_vm1)
    np_vm1_x = np.array(x_vm1)

    np_vm2_y = np.array(res_arr_vm2)
    np_vm2_x = np.array(x_vm2)

    plt.plot(np_vm1_x, np_vm1_y,'b-',label="VM1")
    plt.plot(np_vm2_x, np_vm2_y,'r-',label="VM2")

    plt.title("Request vs. Response time graph")
    plt.xlabel("Request Id")
    plt.ylabel("Response Time (in sec)")
    plt.legend()
    plt.show()