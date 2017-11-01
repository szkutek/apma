import matplotlib.pyplot as plt

y1 = [4, 2, 7, 3]
y2 = [-7, 0, -1, -3]

plt.figure()
plt.plot(y1)
plt.savefig('figure1.png')
plt.clf()

plt.figure()
plt.plot(y2)

plt.show()
# plt.clf()
plt.close('all')
