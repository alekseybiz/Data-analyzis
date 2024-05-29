import numpy as np
import matplotlib.pyplot as plt

random_array_1 = np.random.rand(5)  # массив из 5 случайных чисел
random_array_2 = np.random.rand(5)  # массив из 5 случайных чисел
print(random_array_1)
print(random_array_2)

plt.scatter(random_array_1, random_array_2)

plt.xlabel("x ось")
plt.ylabel("y ось")
plt.title("Тестовая диаграмма рассеяния")

plt.show()