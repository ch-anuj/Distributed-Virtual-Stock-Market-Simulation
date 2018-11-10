import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0))
ax1.grid(True)

X = range(1, 50)
Y = [value * 3 for value in X]
for x in range(1,50):
    y = x*3
    plt.scatter(x, y)
    plt.pause(0.01)

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(45)

ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))

plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('Draw a line.')
# shows the current axis limits values

plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)


plt.show()
