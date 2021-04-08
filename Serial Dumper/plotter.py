import matplotlib.pyplot as plt
import math

phase = []
mag = []
labels = []

file = open("dump.txt", "r")
i = 0
count =0;
content_list = content = file.read().split(",")
for val in content_list:
    #print(count)
    if(i == 0):
        tempval = val
        i = 1
    else:
        i = 0
        count +=1
        calcPhase = math.atan2(float(tempval), float(val))
        calcMag = math.sqrt(float(tempval)*float(tempval) + float(val)*float(val))
        phase.append(calcPhase)
        mag.append(calcMag)
        labels.append(count)

fig,ax = plt.subplots(1)
ax.set_yticklabels([])
ax.plot(labels, mag)
ax.set_ylabel('magnitude')
ax.set_xlabel('Frame')
plt.show()

print("Done!")
