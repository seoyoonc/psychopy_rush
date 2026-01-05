import os
import time

from setup import *
from window import *

class Participant:
    def __init__(self, base_dir, id_string, visit_num, race=None):
        self.participant_num = None 
        self.id = None
        self.visit_num = visit_num
        self.race = race
        self.block_order = []

        self.split_id_string(id_string)
        self.set_block_order()

        self.base_dir = os.path.join(base_dir, 'stimuli', 'support') 
        self.support_dir = os.path.join(self.base_dir, id_string)
            
    def split_id_string(self, id_string):
        separated_string = id_string.split('_')
        self.participant_num = int(separated_string[0])
        self.id = int(separated_string[-1])

    def set_block_order(self):
        if self.id % 2 == 1:  
            self.block_order = ['approach_support', 'avoid_support']

        else: 
            self.block_order = ['avoid_support', 'approach_support']

    def PrintParticipant(self):
        print(f"Participant:{self.participant_num}; id:{self.id}; visit:{self.visit_num}; race:{self.race}")

# gui dialogue to construct participant
def participant_setup():
    # Get Basic Participant info
    id_string, visit_num = get_initial_dialog()
    time.sleep(1)

    # Create Participant based on GUI info
    participant = Participant(base_dir, id_string, visit_num)

    return participant