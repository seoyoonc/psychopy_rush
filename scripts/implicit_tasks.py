###########################################
# ALL FUNCTIONS PERTAINING TO RUNNING THE IMPLICIT TASKS OF THE EXPERIMENT
###########################################

from psychopy import visual, core, event, gui
from psychopy.hardware import keyboard
import random

from setup import *
from window import *

def show_implicit_instructions(gui : VisualWindow, block_type, is_practice=False):
    """Display instructions for implicit task."""
    
    practice_text = "PRACTICE TRIALS\n\n" if is_practice else ""
    
    if block_type == 'approach_support':
        instr = (
            f"{practice_text}"
            "Imagine that you are the stick figure at the bottom of this screen.\n\n"
            "If you see your support figure, press the UP arrow (↑) to approach.\n"
            "(image gets bigger)\n\n"
            "If you see a stranger, press the DOWN arrow (↓) to avoid.\n"
            "(image gets smaller)\n\n"
            "Respond as QUICKLY and ACCURATELY as possible.\n\n"
            "Press SPACE to begin."
        )
    else:  # avoid_support
        instr = (
            f"{practice_text}"
            "Imagine that you are the stick figure at the bottom of this screen.\n\n"
            "If you see your support figure, press the DOWN arrow (↓) to avoid.\n"
            "(image gets smaller)\n\n"
            "If you see a stranger, press the UP arrow (↑) to approach.\n"
            "(image gets bigger)\n\n"
            "Respond as QUICKLY and ACCURATELY as possible.\n\n"
            "Press SPACE to begin."
        )
    
    # move instruction text up to avoid overlap with manikin
    gui.instruction_text.pos = (0, 0.15)
    gui.instruction_text.text = instr
    gui.instruction_text.draw()

    # show manikin at bottom (same position as in trials)
    gui.manikin.pos = (0, -0.3)
    gui.manikin.draw()
    
    # reset instruction text position for other screens
    gui.instruction_text.pos = (0, 0)

    gui.win.flip()
    event.waitKeys(keyList=['space', 'escape'])

def create_implicit_trial_list(support_imgs, stranger_imgs, block_type):
    """Create trial list for implicit task (50 trials)."""
    trials = []
    
    # support: 5 images × 5 repetitions = 25 trials
    for img in support_imgs:
        for rep in range(5):
            trials.append({
                'image_path': img,
                'image_type': 'support',
                'block_type': block_type
            })
    
    # strangers: 25 images × 1 repetition = 25 trials
    for img in stranger_imgs:
        trials.append({
            'image_path': img,
            'image_type': 'stranger',
            'block_type': block_type
        })
    
    random.shuffle(trials)
    return trials

def create_practice_trials(support_imgs, stranger_imgs, block_type):
    """Create practice trial list (8 trials: 4 support + 4 strangers)."""
    trials = []
    
    # 4 support trials (random 4 from 5)
    practice_support = random.sample(support_imgs, min(4, len(support_imgs)))
    for img in practice_support:
        trials.append({
            'image_path': img,
            'image_type': 'support',
            'block_type': block_type
        })
    
    # 4 stranger trials
    for img in stranger_imgs[:4]:
        trials.append({
            'image_path': img,
            'image_type': 'stranger',
            'block_type': block_type
        })
    
    random.shuffle(trials)
    return trials

def run_implicit_trial(gui : VisualWindow, trial_info, trial_num, is_practice=False):
    """Run a single implicit trial."""
    
    block_type = trial_info['block_type']
    image_type = trial_info['image_type']
    
    # manikin always at bottom
    manikin_position = 'bottom'
    manikin_y = -0.3
    
    # det correct response based on block type and image type
    # manikin at bottom: UP = approach (bigger), DOWN = avoid (smaller)
    if block_type == 'approach_support':
        # approach support, avoid strangers
        if image_type == 'support':
            correct_key = 'up'  # Approach = UP
        else:
            correct_key = 'down'  # Avoid = DOWN
    else:  # avoid_support
        # avoid support, approach strangers
        if image_type == 'support':
            correct_key = 'down'  # Avoid = DOWN
        else:
            correct_key = 'up'  # Approach = UP
    
    # 1. fixation (250ms)
    gui.fixation.draw()
    gui.win.flip()
    core.wait(0.25)
    
    # 2. present face + manikin
    gui.face_stim.image = trial_info['image_path']
    gui.face_stim.size = (0.4, 0.4)
    gui.face_stim.draw()

    gui.manikin.pos = (0, manikin_y)
    gui.manikin.draw()
    
    gui.win.flip()
    
    # 3. wait for response
    gui.kb.clock.reset()
    keys = gui.kb.waitKeys(keyList=['up', 'down', 'escape'], waitRelease=False)
    
    if keys and keys[0].name == 'escape':
        gui.win.close()
        core.quit()
    
    response = keys[0].name if keys else None
    rt = keys[0].rt if keys else None
    accuracy = 1 if response == correct_key else 0
    
    # 4. visual feedback - manikin moves and image size changes
    # manikin always at bottom: UP = approach (bigger), DOWN = avoid (smaller)
    if response == 'up':
        # manikin up (toward center/approach)
        gui.manikin.pos = (0, -0.15)  # closer to image
        gui.face_stim.size = (0.6, 0.6)  # image BIGGER
    elif response == 'down':
        # manikin down (away from center/avoid)
        gui.manikin.pos = (0, -0.45)  # further from image
        gui.face_stim.size = (0.25, 0.25)  # image SMALLER

    gui.face_stim.draw()
    gui.manikin.draw()
    
    # red X feedback ONLY during practice trials
    if is_practice and accuracy == 0:
        gui.feedback_x.draw()
        
    gui.win.flip()
    core.wait(0.5)
    
    # 5. ITI - reduced to 250ms
    gui.win.flip()
    core.wait(0.25)
    
    # det detailed image type
    filename = os.path.basename(trial_info['image_path'])
    if image_type == 'support':
        detailed_image_type = 'support'
    elif filename.startswith('real_'):
        detailed_image_type = 'real-stranger'
    elif filename.startswith('ai_'):
        detailed_image_type = 'ai-stranger'
    else:
        detailed_image_type = image_type
    
    trial_data = {
        'trial_number': trial_num,
        'block_type': block_type,
        'image_type': detailed_image_type,
        'image_path': trial_info['image_path'],
        'image_filename': os.path.basename(trial_info['image_path']),
        'manikin_position': manikin_position,
        'correct_response': correct_key,
        'participant_response': response,
        'accuracy': accuracy,
        'reaction_time': rt,
        'is_practice': is_practice
    }
    
    return trial_data

def run_implicit_block(gui : VisualWindow, trial_list, block_num, is_practice=False):
    """Run a full implicit block."""
    block_data = []
    
    show_implicit_instructions(gui, trial_list[0]['block_type'], is_practice=is_practice)
    
    for i, trial_info in enumerate(trial_list):
        trial_num = i + 1
        trial_data = run_implicit_trial(gui, trial_info, trial_num, is_practice=is_practice)
        trial_data['block_number'] = block_num
        block_data.append(trial_data)
    
    return block_data

# MANIPULATION CHECK FUNCTIONS (Visit 3 only)

def run_manipulation_check(gui : VisualWindow, all_real_photos, all_ai_photos):
    """
    Manipulation check for Visit 3 only.
    Shows 2 real + 2 AI photos and asks participants to identify them.
    """
    
    # select 2 random real photos and 2 random AI photos
    selected_real = random.sample(all_real_photos, min(2, len(all_real_photos)))
    selected_ai = random.sample(all_ai_photos, min(2, len(all_ai_photos)))
    
    # combine and shuffle
    all_check_photos = selected_real + selected_ai
    random.shuffle(all_check_photos)
    
    manipulation_data = []
    
    # instructions
    gui.instruction_text.text = (
        "Final Task:\n\n"
        "You will see some faces and answer questions.\n\n"
        "Press SPACE to begin."
    )
    gui.instruction_text.draw()
    gui.win.flip()
    event.waitKeys(keyList=['space', 'escape'])
    
    # clear any remaining events before starting trials
    event.clearEvents()
    core.wait(0.5)  # brief pause after instructions
    
    # show each photo
    for i, photo_path in enumerate(all_check_photos):
        trial_num = i + 1
        
        # clear events at start of each trial to prevent carryover
        event.clearEvents()
        
        # det actual source
        filename = os.path.basename(photo_path)
        if filename.startswith('real_'):
            actual_source = 'real'
        elif filename.startswith('ai_'):
            actual_source = 'ai'
        else:
            actual_source = 'unknown'
        
        # Q1: Source identification
        gui.face_stim.image = photo_path
        gui.face_stim.size = (0.4, 0.4)
        gui.face_stim.pos = (0, 0.2)

        question_text = visual.TextStim(
            gui.win,
            text='Do you think the image you see here is taken by a human\nphotographer or generated by a computer?',
            pos=(0, -0.15),
            height=0.04,
            color='white',
            wrapWidth=1.5
        )
        
        options_text = visual.TextStim(
            gui.win,
            text='Press YELLOW keys: 1 = Human photographer   2 = Computer-generated   3 = Unsure',
            pos=(0, -0.30),
            height=0.035,
            color='yellow',
            wrapWidth=1.5
        )
        
        # wait for response
        # keys H, J, K are labeled as 1, 2, 3 on the physical keyboard
        response = None
        response_map = {'h': 'Human photographer', 'j': 'Computer-generated', 'k': 'Unsure'}
        
        while response is None:
            gui.face_stim.draw()
            question_text.draw()
            options_text.draw()
            gui.win.flip()

            keys = event.getKeys(keyList=['h', 'j', 'k', 'escape'])
            if keys:
                if 'escape' in keys:
                    gui.win.close()
                    core.quit()
                else:
                    response = response_map[keys[0]]
        
        # clear any remaining key presses before confidence question
        event.clearEvents()
        core.wait(0.3)  # brief pause to prevent accidental key carryover
        
        # Q2: Confidence rating (0-100)
        confidence_text = visual.TextStim(
            gui.win,
            text='How confident are you in your answer?\n\nType a number from 0 (not at all confident) to 100 (extremely confident) using the ORIGINAL number keys\n\nPress ENTER when done.',
            pos=(0, -0.15),
            height=0.04,
            color='white',
            wrapWidth=1.5
        )
        
        typed_number = ''
        confidence_display = visual.TextStim(
            gui.win,
            text='',
            pos=(0, -0.35),
            height=0.08,
            color='yellow',
            bold=True
        )
        
        confidence = None
        while confidence is None:
            gui.face_stim.draw()
            confidence_text.draw()
            confidence_display.text = typed_number  # show what's been typed
            confidence_display.draw()
            gui.win.flip()
            
            keys = event.getKeys(keyList=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'return', 'backspace', 'escape'])
            if keys:
                for key in keys:
                    if key == 'escape':
                        gui.win.close()
                        core.quit()
                    elif key == 'return':
                        # try to convert to number
                        if typed_number:  # only try if something was typed
                            try:
                                conf_num = int(typed_number)
                                if 0 <= conf_num <= 100:
                                    confidence = conf_num
                                else:
                                    # invalid range, reset
                                    typed_number = ''
                            except:
                                # invalid input, reset
                                typed_number = ''
                    elif key == 'backspace':
                        typed_number = typed_number[:-1]
                    elif key in '0123456789' and len(typed_number) < 3:
                        typed_number += key
        
        # save trial data
        trial_data = {
            'trial_number': trial_num,
            'image_path': photo_path,
            'image_filename': filename,
            'actual_source': actual_source,
            'participant_response': response,
            'confidence': confidence
        }
        manipulation_data.append(trial_data)
        
        # brief ITI and clear events to prevent carryover to next trial
        gui.win.flip()
        core.wait(0.5)
        event.clearEvents()  # clear any stray key presses
    
    return manipulation_data