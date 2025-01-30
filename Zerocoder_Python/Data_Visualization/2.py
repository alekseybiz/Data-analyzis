import matplotlib.pyplot as plt

data = [5, 6, 7, 3, 4, 4, 4, 5, 6, 6, 6, 6, 6, 8, 9, 10, 5, 6, 7]

plt.hist(data, bins=3)

plt.xlabel("часы сна")
plt.ylabel("кол-во людей")
plt.title("Тестовая гистограмма часов сна")

plt.show()
