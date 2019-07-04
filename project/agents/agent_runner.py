import numpy as np
import os
import random

class DummyAgent():
	def __init__(self, args = {}):
		self.args = args

	def take_action(current_state):
		return random.randint(0,1)