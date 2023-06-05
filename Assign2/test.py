import matplotlib.pyplot as plt
import numpy as np

stepsQLearning=np.loadtxt("students/stepsperepisodeQLearning.txt")
stepsSARSA=np.loadtxt("students/stepsperepisodeSARSA.txt")

limit = 400
plt.plot(stepsQLearning[0:limit], label="Q-learning")
plt.plot(stepsSARSA[0:limit], label="SARSA")

plt.xlim(0,limit)
plt.legend(loc="best",prop={"size":10})
plt.title("Steps performed by Q-learning and SARSA")
plt.xlabel("Episodes")
plt.ylabel("Steps")
plt.grid()
plt.show()