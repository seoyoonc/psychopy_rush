###########################################
# ALL FUNCTIONS PERTAINING TO RUNNING THE IMPLICIT TASKS OF THE EXPERIMENT
###########################################

from psychopy import visual, core, event, gui
from psychopy.hardware import keyboard
import random

from setup import *
from window import *

def show_explicit_instructions(gui : VisualWindow):
    """Display instructions for explicit task."""
    
    gui.instruction_text.text = explicit_instructions
    gui.instruction_text.draw()
    gui.win.flip()
    event.waitKeys(keyList=['space', 'escape'])

def run_explicit_trial(gui : VisualWindow, image_path, trial_num):
    """Run a single explicit rating trial with keyboard input."""
    
    # map: keyboard a,s,d,f,g,h,j,k,l to rating -4 to +4
    key_to_rating = {
        'a': -4, 's': -3, 'd': -2, 'f': -1, 'g': 0,
        'h': 1, 'j': 2, 'k': 3, 'l': 4
    }
    
    # 1. fixation (250ms) - same as implicit task
    gui.fixation.draw()
    gui.win.flip()
    core.wait(0.25)
    
    # 2. show face with rating scale
    gui.face_stim.image = image_path
    gui.face_stim.size = (0.4, 0.4)
    gui.face_stim.pos = (0, 0.15)

    # rating instruction
    gui.rating_instruction.text = (
        "-4 (Avoid)     0 (Neutral)     +4 (Approach)"
    )
    
    # wait for valid key press
    start_time = core.getTime()
    rating = None
    key_pressed = None
    
    while rating is None:
        gui.face_stim.draw()
        gui.rating_instruction.draw()
        gui.win.flip()

        keys = event.getKeys(keyList=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'escape'])
        
        if keys:
            if 'escape' in keys:
                gui.win.close()
                core.quit()
            else:
                key_pressed = keys[0]
                rating = key_to_rating[key_pressed]
    
    rt = core.getTime() - start_time
    
    # show selected rating
    gui.face_stim.draw()
    gui.rating_instruction.draw()
    gui.rating_display.text = f"Selected: {rating:+d}"
    gui.rating_display.draw()
    gui.win.flip()
    core.wait(0.5)
    
    # brief ITI
    gui.win.flip()
    core.wait(0.3)
    
    trial_data = {
        'trial_number': trial_num,
        'image_path': image_path,
        'image_filename': os.path.basename(image_path),
        'key_pressed': key_pressed,
        'rating': rating,
        'reaction_time': rt
    }
    
    return trial_data

def run_explicit_task(gui : VisualWindow, support_imgs, stranger_imgs):
    """Run the full explicit rating task (30 trials)."""
    
    show_explicit_instructions(gui)
    
    # create trial list: 5 support + 25 strangers
    trials = support_imgs + stranger_imgs
    random.shuffle(trials)
    
    explicit_data = []
    
    for i, image_path in enumerate(trials):
        trial_num = i + 1
        
        # det detailed image type
        filename = os.path.basename(image_path)
        if image_path in support_imgs:
            image_type = 'support'
        elif filename.startswith('real_'):
            image_type = 'real-stranger'
        elif filename.startswith('ai_'):
            image_type = 'ai-stranger'
        else:
            image_type = 'stranger'
        
        trial_data = run_explicit_trial(gui, image_path, trial_num)
        trial_data['image_type'] = image_type
        explicit_data.append(trial_data)
    
    return explicit_data

