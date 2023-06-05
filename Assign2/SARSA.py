"""
Q-Learning agent

Author: Elliot Colp
Modified by: Claude Sammut

This is an implementation of a standard Q-learning algorithm.
The original code mapped "similar" tiles to the same state, e.g. all tiles not touching any wall
mapped to one state, all tiles with a wall on the left mapped to another state, etc.
This was changed to the more common representation of one state corresponding to one tile.

update 17/1/2023: added "list" to As = list(where(Qs == maxQ)[0])
    Previously caused an error in Python 3.11 on mac

"""

from agent import *
import random
import gridworld
import numpy as np


class SARSA(Agent):
    def reset(self):
        Agent.reset(self)
        self.epsilon = 0.1
        self.alpha = 0.1
        self.gamma = 1
        self.random_array = np.loadtxt('./random_numbers.txt')
        self.random_number_index = 0

    def select_action(self, S):
        """
        Select an action based on the epsilon-greedy strategy for the given state S.
        
        Args:
            S (int): The current state of the agent.

        Returns:
            int: The index of the selected action, either the one with the highest Q value (exploitation)
            or the one with the lowest Q value (exploration), depending on the epsilon value and a random number.
        """
        # Get the action values for the current state S from the Q table
        Qs = self.Q[S]

        # Retrieve a random number from the pre-generated random_array using the random_number_index
        random_num = self.random_array[self.random_number_index]
        self.random_number_index += 1

        # If the random number is less than or equal to epsilon, perform exploration by selecting the action with the minimum Q value
        if random_num <= self.epsilon:
            min_value = Qs[0]
            min_index = 0

            for i, value in enumerate(Qs):
                if value < min_value:
                    min_value = value
                    min_index = i

            return min_index

        # If the random number is greater than epsilon, perform exploitation by selecting the action with the maximum Q value
        else:
            max_value = Qs[0]
            max_index = 0

            for i, value in enumerate(Qs):
                if value > max_value:
                    max_value = value
                    max_index = i

            return max_index

    def do_step(self, S, act, logfile=None):
        Agent.do_step(self, S, act, logfile)
        # Observation -> agent state
        S = self.get_S()
        A = self.select_action(S)

        # Observe reward and new state
        R, Sp = act(A)
        next_A = self.select_action(Sp)
        # Update return
        self.G += R
        # Update Q
        delta = R + self.gamma * self.Q[Sp][next_A] - self.Q[S][A]
        self.Q[S][A] += self.alpha*delta
        
        return Sp
        
    def update_alpha(self, event=None):
        if self.testmode: return
        
        self.alpha = self.alpha_var.get()
    
    def update_epsilon(self, event=None):
        if self.testmode: return
        
        self.epsilon = self.epsilon_var.get()
    
    def update_gamma(self, event=None):
        if self.testmode: return
        
        self.gamma = self.gamma_var.get()
        
    def set_testmode(self, enabled):
        if not self.testmode and enabled:
            self.tempAlpha = self.alpha
            self.tempEpsilon = self.epsilon
            self.alpha = 0
            self.epsilon = 0
        
        elif self.testmode and not enabled:
            self.alpha = self.tempAlpha
            self.epsilon = self.tempEpsilon
        
        Agent.set_testmode(self, enabled)

    def init_options(self, master):
        # Alpha
        frame = LabelFrame(master)
        frame["text"] = "Alpha"
        frame["padx"] = 5
        frame["pady"] = 5
        frame.grid(row=0, column=0)
        
        self.alpha_var = DoubleVar()
        self.alpha_var.set(self.alpha)
        scale = Scale(frame)
        scale["from"] = 1
        scale["to"] = 0
        scale["resolution"] = 0.05
        scale["orient"] = VERTICAL
        scale["variable"] = self.alpha_var
        scale["command"] = self.update_alpha
        scale.pack()
        
        # Epsilon
        frame = LabelFrame(master)
        frame["text"] = "Epsilon"
        frame["padx"] = 5
        frame["pady"] = 5
        frame.grid(row=1, column=0)
        
        self.epsilon_var = DoubleVar()
        self.epsilon_var.set(self.epsilon)
        scale = Scale(frame)
        scale["from"] = 1
        scale["to"] = 0
        scale["resolution"] = 0.05
        scale["orient"] = VERTICAL
        scale["variable"] = self.epsilon_var
        scale["command"] = self.update_epsilon
        scale.pack()
        
        # Gamma
        frame = LabelFrame(master)
        frame["text"] = "Gamma"
        frame["padx"] = 5
        frame["pady"] = 5
        frame.grid(row=2, column=0)
        
        self.gamma_var = DoubleVar()
        self.gamma_var.set(self.gamma)
        scale = Scale(frame)
        scale["from"] = 1
        scale["to"] = 0
        scale["resolution"] = 0.05
        scale["orient"] = VERTICAL
        scale["variable"] = self.gamma_var
        scale["command"] = self.update_gamma
        scale.pack()
