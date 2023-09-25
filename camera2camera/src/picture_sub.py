import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import sys

path = sys.argv[1]
save_path = sys.argv[2]

# path = '../results/camera2camera/datasets1/sub.txt'
# path = '../results/camera2camera/datasets2/sub.txt'
# path = '../results/camera2camera/datasets3/sub.txt'

x = []
with open(path, encoding='utf-8') as file:
    y = file.read()
    y = y.rstrip()
y = y.rsplit('\n')
y = [eval(i) for i in y]

y_max = (int(max(y)/5) + 1)*5

# y = [0.8776, 0.7770, 0.5816, 0.1174, 0.8333, 0.3700, 0.3549, 0.5285, 1.9779, 1.3164, 0] # datasets_1 theta
# y = [0.4774, 0.7872, 0.3016, 0.4213, 0.2399, 0.4576, 0.4023, 0, 0.5830, 0.4470, 0.2076, 0.3911] # datasets_2 theta

for i in range(len(y)):
    img_index = 'jpg' + str(i + 1)
    x.append(str(img_index))
# print(x)
plt.figure(figsize=(6, 4), dpi=100)
axes = plt.axes()
axes.set_ylim(0, y_max)
axes.spines['top'].set_visible(False)
axes.spines['right'].set_visible(False)
axes.spines['bottom'].set_visible(False)
axes.spines['left'].set_visible(False)
plt.annotate('', 
             xy=(1.13, 0), xycoords='axes fraction',
             xytext=(-0.06, 0), textcoords='axes fraction',
             arrowprops=dict(facecolor='black', shrink=0.05, width = 2),
             zorder=5)
# 绘制 y 轴方向的箭头
plt.annotate('', 
             xy=(0, 1.13), xycoords='axes fraction',
             xytext=(0, -0.06), textcoords='axes fraction',
             arrowprops=dict(facecolor='black', shrink=0.05, width = 2),
             zorder=5)


plt.plot(x, y, c='red')
plt.scatter(x, y, c='red')

# y_ticks = range(10)
# print(y_ticks[::5])
# plt.yticks(y_ticks[::5])
plt.grid(False)
# plt.grid(True, linestyle='--', alpha=0.5)

font_S = fm.FontProperties(family='Stebcil', size=16, stretch=0)
font_M = fm.FontProperties(family='Mtebcil', size='large', stretch=1000)

plt.xlabel("image", fontproperties = font_M)
plt.ylabel("score", fontproperties = font_M)
plt.title("sub_error_no_working", fontproperties = font_S)
# plt.plot(x, y)
plt.tight_layout()
# plt.legend(loc = "best")
plt.savefig(save_path)
plt.show()


