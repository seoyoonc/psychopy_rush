##################### SETUP OF WINDOW OF PSYCHOPY EXPERIMENT #####################
##################### THIS FILE CONTAINS PARAMETERS SUCH AS WINDOW SIZE AND VISUAL EFFECTS ############################
### IT ALSO CONTAINS 2 FUNCTIONS FOR THE SETUP OF THE EXPERIMENT
### get_initial_dialog()
### get_race_ethnicity_selection()

from psychopy import visual, core, event
from psychopy import gui as g
from psychopy.hardware import keyboard
import os

from setup import *

########################################################################################################
# SETTING UP PSYCHOPY WINDOW AND STIMULI
class VisualWindow():
    def __init__(self, x, y):
        self.win = visual.Window(
        size=[1920, 1080],
        fullscr=True,
        color='black',
        units='height'
        )

        self.win.mouseVisible = False
        self.kb = keyboard.Keyboard()

        # face image
        self.face_stim = visual.ImageStim(
            self.win,
            size=(0.4, 0.4),
            pos=(0, 0)
        )

        # manikin
        self.manikin = visual.ImageStim(
            self.win,
            image=manikin_path,
            size=(0.1, 0.1)
        )
        self.manikin.contrast = -1

        # fixation cross
        self.fixation = visual.TextStim(
            self.win,
            text='+',
            height=0.08,
            color='white'
        )

        # Feedback X
        self.feedback_x = visual.TextStim(
            self.win,
            text='X',
            height=0.15,
            color='red',
            bold=True
        )

        # instruction text
        self.instruction_text = visual.TextStim(
            self.win,
            text='',
            height=0.04,
            color='white',
            wrapWidth=1.5
        )

        # Rating display text (for explicit task)
        self.rating_instruction = visual.TextStim(
            self.win,
            text='',
            height=0.04,
            color='white',
            pos=(0, -0.25),
            wrapWidth=1.5
        )

        self.rating_display = visual.TextStim(
            self.win,
            text='',
            height=0.08,
            color='yellow',
            bold=True,
            pos=(0, -0.35)
        )
        
    def show_fixation(self):
        print(f"In show_fixation, self.win = {self.win}")
        print(f"Type: {type(self.win)}")
        if self.win is None:
            print("ERROR: Window is None!")
            return
        self.fixation.draw()
        self.win.flip()
    
    def close(self):
        self.win.close()
        core.quit()


# Initial Participant Setup window
def get_initial_dialog():
    exp_info = {
                'Participant ID': '',
                'Visit Number': ['2', '3']
            }

    dlg = g.DlgFromDict(dictionary=exp_info, title='Approach-Avoidance Tasks', sortKeys=False)

    if not dlg.OK:
        core.quit()

    return exp_info['Participant ID'], exp_info['Visit Number']

# RACE/ETHNICITY SELECTION
def get_race_ethnicity_selection(visual_window : VisualWindow):
    """Display race/ethnicity selection screen."""

    selection_win = visual_window.win
    selection_win.mouseVisible = True
    mouse = event.Mouse(win=selection_win)
    
    title = visual.TextStim(
        selection_win,
        text='Race/Ethnicity Identification',
        pos=(0, 0.35),
        height=0.06,
        color='white',
        bold=True
    )
    
    question = visual.TextStim(
        selection_win,
        text='Which race/ethnicity do you most identify with?',
        pos=(0, 0.20),
        height=0.045,
        color='white',
        wrapWidth=1.5
    )
    
    options = ['White', 'Asian', 'Black', 'Hispanic']
    buttons = []
    button_texts = []
    
    y_start = 0.1
    y_spacing = -0.15
    
    for i, option in enumerate(options):
        y_pos = y_start + (i * y_spacing)
        
        button = visual.Rect(
            selection_win,
            width=0.6,
            height=0.09,
            pos=(0, y_pos),
            fillColor='gray',
            lineColor='white',
            lineWidth=3
        )
        
        button_text = visual.TextStim(
            selection_win,
            text=option,
            pos=(0, y_pos),
            height=0.04,
            color='white',
            bold=True
        )
        
        buttons.append(button)
        button_texts.append(button_text)
    
    selected_option = None
    
    while selected_option is None:
        title.draw()
        question.draw()
        
        for i, (button, button_text) in enumerate(zip(buttons, button_texts)):
            if mouse.isPressedIn(button):
                selected_option = options[i]
                button.fillColor = 'green'
            
            button.draw()
            button_text.draw()
        
        selection_win.flip()
        
        if 'escape' in event.getKeys():
            selection_win.close()
            core.quit()
    
    core.wait(0.3)
#    selection_win.close()
    
    return selected_option.lower()
