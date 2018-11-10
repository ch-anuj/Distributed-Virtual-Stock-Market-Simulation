import matplotlib.pyplot as plt
import time
# x = [1,2,3,4,5,6,7,8]
# y = [5,2,4,2,1,4,5,2]


plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
for i in range(10):
    plt.scatter(i,i*i, color='k', s=10)
    plt.pause(0.5)
plt.legend()

plt.show()
