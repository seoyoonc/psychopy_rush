# project title: RUSH approach-avoid task
# author: seoyoonc
# last updated 12/5/25

from psychopy import visual, core, event, gui
from psychopy.hardware import keyboard
from photo_allocator import PhotoAllocator
import random
import os
import pandas as pd
from datetime import datetime
import sys

# PARTICIPANT INFO
exp_info = {
    'Participant ID': '',
    'Visit Number': ['2', '3']
}

dlg = gui.DlgFromDict(dictionary=exp_info, title='Approach-Avoidance Tasks', sortKeys=False)
if not dlg.OK:
    core.quit()

participant_id = exp_info['Participant ID']
visit_num = exp_info['Visit Number']
date_only = datetime.now().strftime('%Y-%m-%d')
session_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# RACE/ETHNICITY SELECTION
def get_race_ethnicity_selection():
    """race/ethnicity selection screen."""
    selection_win = visual.Window(
        size=[1200, 800],
        fullscr=False,
        color='black',
        units='height'
    )
    
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
    
    options = ['White', 'Asian', 'Black', 'Hispanic', 'None of the above']
    buttons = []
    button_texts = []
    
    y_start = 0.05
    y_spacing = -0.12
    
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
    selection_win.close()
    
    # if "none of the above" selected, quit
    if selected_option == 'None of the above':
        core.quit()
    
    return selected_option

race_ethnicity = get_race_ethnicity_selection()
race_folder = race_ethnicity.lower()
print(f"\nSelected race/ethnicity: {race_ethnicity}")

# FILE PATHS, PHOTO ALLOCATION *SUPER NECESSARY*
base_dir = os.path.dirname(os.path.abspath(__file__))

# initialize photo allocator
allocator = PhotoAllocator(base_dir)

# data directory
data_dir = os.path.join(base_dir, 'data')
os.makedirs(data_dir, exist_ok=True)

# support figures directory pulled from id directly
support_dir = os.path.join(base_dir, 'stimuli', 'support', participant_id)

# manikin
manikin_path = os.path.join(base_dir, 'stimuli', 'stickmanikin.png')

print(f"\nParticipant: {participant_id}")
print(f"Visit: {visit_num}")
print(f"Race: {race_ethnicity}")

# BLOCK ORDER, COUNTERBALANCED
# 001: approach_support first
# 002: avoid_support first

participant_str = str(participant_id)
last_digit = int(participant_str[-1])

if last_digit % 2 == 1:  # 001
    block_order = ['approach_support', 'avoid_support']
else:  # 002
    block_order = ['avoid_support', 'approach_support']

# LOAD PHOTOS
print("\n" + "="*60)
print("LOADING PHOTOS")
print("="*60)

# load support figures
def load_images_from_folder(folder_path):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = []
    
    if os.path.exists(folder_path):
        for filename in sorted(os.listdir(folder_path)):
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                images.append(os.path.join(folder_path, filename))
    
    return images

support_images = load_images_from_folder(support_dir)
print(f"Loaded {len(support_images)} support figures")

if len(support_images) != 5:
    print(f"WARNING: Expected 5 support images, found {len(support_images)}")

# allocate stranger photos for implicit blocks
print("\nAllocating photos for Implicit Task...")
implicit_block1_allocation = allocator.allocate_photos(
    participant_id, race_folder, int(visit_num), 'block1', 'implicit'
)
implicit_block2_allocation = allocator.allocate_photos(
    participant_id, race_folder, int(visit_num), 'block2', 'implicit'
)

# get full paths
implicit_block1_strangers = allocator.get_photo_paths(
    implicit_block1_allocation['real'] + implicit_block1_allocation['ai']
)
implicit_block2_strangers = allocator.get_photo_paths(
    implicit_block2_allocation['real'] + implicit_block2_allocation['ai']
)

print(f"Block 1: {len(implicit_block1_allocation['real'])} real + {len(implicit_block1_allocation['ai'])} AI = {len(implicit_block1_strangers)} total strangers")
print(f"Block 2: {len(implicit_block2_allocation['real'])} real + {len(implicit_block2_allocation['ai'])} AI = {len(implicit_block2_strangers)} total strangers")

# get practice strangers (4 AI - 1 of EACH race including participant's own)
# practice photos CAN be reused across visits to save photos for randomization
practice_strangers = []
all_races = ['white', 'asian', 'black', 'hispanic']

print(f"\nSelecting practice strangers (need 4: 1 of each race including {race_folder})...")

# get exactly 1 AI stranger from EACH race (all 4 races)
for race in all_races:
    race_ai = [f for f in allocator.ai_pool.get(race, []) if f.startswith('ai_')]
    
    if race_ai:
        selected = random.choice(race_ai)
        full_path = os.path.join(base_dir, 'stimuli', 'strangers', 'ai', selected)
        practice_strangers.append(full_path)
        print(f"Practice stranger {len(practice_strangers)}: {race} - {selected}")
    else:
        print(f"WARNING: No AI photos available for {race}")

if len(practice_strangers) < 4:
    print(f"ERROR: Only got {len(practice_strangers)} practice strangers, need 4!")
else:
    print(f"Practice: {len(practice_strangers)} strangers (1 of each race, can repeat across visits)")

# allocate photos for explicit task
print("\nAllocating photos for Explicit Task...")
explicit_allocation = allocator.allocate_photos(
    participant_id, race_folder, int(visit_num), 'explicit', 'explicit'
)
explicit_strangers = allocator.get_photo_paths(
    explicit_allocation['real'] + explicit_allocation['ai']
)
print(f"Explicit: {len(explicit_strangers)} strangers allocated")

print("="*60)

# SETTING UP PSYCHOPY WINDOW AND STIMULI
win = visual.Window(
    size=[1920, 1080],
    fullscr=True,
    color='black',
    units='height'
)

win.mouseVisible = False
kb = keyboard.Keyboard()

# face image
face_stim = visual.ImageStim(
    win,
    size=(0.4, 0.4),
    pos=(0, 0)
)

# manikin
manikin = visual.ImageStim(
    win,
    image=manikin_path,
    size=(0.1, 0.1)
)
manikin.contrast = -1

# fixation cross
fixation = visual.TextStim(
    win,
    text='+',
    height=0.08,
    color='white'
)

# feedback X
feedback_x = visual.TextStim(
    win,
    text='X',
    height=0.15,
    color='red',
    bold=True
)

# instruction text
instruction_text = visual.TextStim(
    win,
    text='',
    height=0.04,
    color='white',
    wrapWidth=1.5
)

# rating display text (for explicit task)
rating_instruction = visual.TextStim(
    win,
    text='',
    height=0.04,
    color='white',
    pos=(0, -0.25),
    wrapWidth=1.5
)

rating_display = visual.TextStim(
    win,
    text='',
    height=0.08,
    color='yellow',
    bold=True,
    pos=(0, -0.35)
)

# IMPLICIT TASK FUNCTIONS
def show_implicit_instructions(block_type, is_practice=False):    
    practice_text = "PRACTICE TRIALS\n\n" if is_practice else ""
    
    if block_type == 'approach_support':
        instr = (
            f"{practice_text}"
            "Imagine that you are the stick figure at the bottom of this screen.\n\n"
            "If you see your support figure, press the UP arrow (↑) to approach (image gets bigger).\n\n"
            "If you see a stranger, press the DOWN arrow (↓) to avoid (image gets smaller).\n\n"
            "Respond as QUICKLY and ACCURATELY as possible.\n\n"
            "Press SPACE to begin."
        )
    else:  # avoid_support
        instr = (
            f"{practice_text}"
            "Imagine that you are the stick figure at the bottom of this screen.\n\n"
            "If you see your support figure, press the DOWN arrow (↓) to avoid (image gets smaller).\n\n"
            "If you see a stranger, press the UP arrow (↑) to approach (image gets bigger).\n\n"
            "Respond as QUICKLY and ACCURATELY as possible.\n\n"
            "Press SPACE to begin."
        )
    
    instruction_text.pos = (0, 0.13)
    instruction_text.text = instr
    instruction_text.draw()
    
    # show manikin at bottom (same position as in trials)
    manikin.pos = (0, -0.3)
    manikin.draw()
    
    # reset instruction text position for other screens
    instruction_text.pos = (0, 0)
    
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])

def create_implicit_trial_list(support_imgs, stranger_imgs, block_type):
    """trial list for implicit task (50 trials)."""
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

def run_implicit_trial(trial_info, trial_num, is_practice=False):
    """single implicit trial."""
    
    block_type = trial_info['block_type']
    image_type = trial_info['image_type']
    
    # manikin always at bottom
    manikin_position = 'bottom'
    manikin_y = -0.3
    
    # determine correct response based on block type and image type
    # manikin at bottom: UP = approach (bigger), DOWN = avoid (smaller)
    if block_type == 'approach_support':
        # should approach support, avoid strangers
        if image_type == 'support':
            correct_key = 'up'  # approach = UP
        else:
            correct_key = 'down'  # avoid = DOWN
    else:  # avoid_support
        # should avoid support, approach strangers
        if image_type == 'support':
            correct_key = 'down'  # avoid = DOWN
        else:
            correct_key = 'up'  # approach = UP
    
    # 1. fixation (250ms)
    fixation.draw()
    win.flip()
    core.wait(0.25)
    
    # 2. present face + manikin
    face_stim.image = trial_info['image_path']
    face_stim.size = (0.4, 0.4)
    face_stim.draw()
    
    manikin.pos = (0, manikin_y)
    manikin.draw()
    
    win.flip()
    
    # 3. wait for response
    kb.clock.reset()
    keys = kb.waitKeys(keyList=['up', 'down', 'escape'], waitRelease=False)
    
    if keys and keys[0].name == 'escape':
        win.close()
        core.quit()
    
    response = keys[0].name if keys else None
    rt = keys[0].rt if keys else None
    accuracy = 1 if response == correct_key else 0
    
    # 4. visual feedback - manikin moves and image size changes
    # manikin always at bottom: UP = approach (bigger), DOWN = avoid (smaller)
    if response == 'up':
        # move manikin up (toward center/approach)
        manikin.pos = (0, -0.15)  # Closer to image
        face_stim.size = (0.6, 0.6)  # Image BIGGER
    elif response == 'down':
        # move manikin down (away from center/avoid)
        manikin.pos = (0, -0.45)  # Further from image
        face_stim.size = (0.25, 0.25)  # Image SMALLER
    
    face_stim.draw()
    manikin.draw()
    
    # red X feedback ONLY during practice trials
    if is_practice and accuracy == 0:
        feedback_x.draw()
    
    win.flip()
    core.wait(0.5)
    
    # 5. ITI - reduced to 250ms
    win.flip()
    core.wait(0.25)
    
    # determine detailed image type
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

def run_implicit_block(trial_list, block_num, is_practice=False):
    """full implicit block."""
    block_data = []
    
    show_implicit_instructions(trial_list[0]['block_type'], is_practice=is_practice)
    
    for i, trial_info in enumerate(trial_list):
        trial_num = i + 1
        trial_data = run_implicit_trial(trial_info, trial_num, is_practice=is_practice)
        trial_data['block_number'] = block_num
        block_data.append(trial_data)
    
    return block_data

# EXPLICIT TASK FUNCTIONS
def show_explicit_instructions():
    instr = (
        "You will see a picture of a face on the screen.\n\n"
        "Imagine standing face-to-face with the person shown and rate your tendency\n"
        "to approach or avoid this person using the scale provided on the keyboard\n"
        "(-4 to +4).\n\n"
        "'0' means you would neither approach nor avoid; other numbers correspond\n"
        "to steps you would make toward (+) or away from (-) the person.\n\n"
        "Do not rate based on attractiveness or trustworthiness, but only on their\n"
        "emotional expression.\n\n"
        "Press SPACE to begin."
    )
    
    instruction_text.text = instr
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])

def run_explicit_trial(image_path, trial_num):
    """single explicit rating trial"""
    
    # mapping keyboard 1-9 to rating -4 to +4
    key_to_rating = {
        '1': -4, '2': -3, '3': -2, '4': -1, '5': 0,
        '6': 1, '7': 2, '8': 3, '9': 4
    }
    
    # 1. fixation (250 ms) - same as implicit task
    fixation.draw()
    win.flip()
    core.wait(0.25)
    
    # 2. show face with rating scale
    face_stim.image = image_path
    face_stim.size = (0.4, 0.4)
    face_stim.pos = (0, 0.15)
    
    # rating instruction
    rating_instruction.text = (
        "-4 (Avoid)     0 (Neutral)     +4 (Approach)"
    )
    
    # wait for valid key press
    start_time = core.getTime()
    rating = None
    key_pressed = None
    
    while rating is None:
        face_stim.draw()
        rating_instruction.draw()
        win.flip()
        
        keys = event.getKeys(keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9', 'escape'])
        
        if keys:
            if 'escape' in keys:
                win.close()
                core.quit()
            else:
                key_pressed = keys[0]
                rating = key_to_rating[key_pressed]
    
    rt = core.getTime() - start_time
    
    # show selected rating
    face_stim.draw()
    rating_instruction.draw()
    rating_display.text = f"Selected: {rating:+d}"
    rating_display.draw()
    win.flip()
    core.wait(0.5)
    
    # brief ITI
    win.flip()
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

def run_explicit_task(support_imgs, stranger_imgs):
    """full explicit rating task (30 trials)."""
    
    show_explicit_instructions()
    
    # create trial list: 5 support + 25 strangers
    trials = support_imgs + stranger_imgs
    random.shuffle(trials)
    
    explicit_data = []
    
    for i, image_path in enumerate(trials):
        trial_num = i + 1
        
        # determine detailed image type
        filename = os.path.basename(image_path)
        if image_path in support_imgs:
            image_type = 'support'
        elif filename.startswith('real_'):
            image_type = 'real-stranger'
        elif filename.startswith('ai_'):
            image_type = 'ai-stranger'
        else:
            image_type = 'stranger'
        
        trial_data = run_explicit_trial(image_path, trial_num)
        trial_data['image_type'] = image_type
        explicit_data.append(trial_data)
    
    return explicit_data

# SAVE EVERYTHING
def save_data_to_csv(data_list, participant_id, visit_num, session_time, race_ethnicity, 
                     data_dir, task_type, block_label="", date_only=""):
    if not data_list:
        print(f"No data to save for {block_label}")
        return None
    
    df = pd.DataFrame(data_list)
    
    # add session_time to all rows (keep timestamp for each trial)
    df['session_time'] = session_time
    
    # add race_ethnicity only in first row
    df['race_ethnicity'] = ''
    df.loc[0, 'race_ethnicity'] = race_ethnicity
    
    # only calculate averages for implicit task (which has is_practice column)
    if task_type == 'implicit':
        # calculate averages for main trials only (excluding practice)
        main_trials = df[df['is_practice'] == False]
        
        # for combined implicit CSV, add overall averages in first row only
        if block_label == 'combined':
            if len(main_trials) > 0:
                avg_accuracy = main_trials['accuracy'].mean()
                avg_rt = main_trials['reaction_time'].mean()
                
                # init columns with empty strings
                df['average_accuracy'] = ''
                df['average_reaction_time'] = ''
                
                # set only first row to have the average values
                df.loc[0, 'average_accuracy'] = avg_accuracy
                df.loc[0, 'average_reaction_time'] = avg_rt
        
        # for individual block files, add block-specific averages in first row only
        elif block_label in ['block1', 'block2']:
            if len(main_trials) > 0:
                avg_accuracy = main_trials['accuracy'].mean()
                avg_rt = main_trials['reaction_time'].mean()
                
                # init columns with empty strings
                df['average_accuracy'] = ''
                df['average_reaction_time'] = ''
                
                # set only first row to have the average values
                df.loc[0, 'average_accuracy'] = avg_accuracy
                df.loc[0, 'average_reaction_time'] = avg_rt
    
    # create filename - format: implicit_001_V2_block1_2025-12-02.csv
    if block_label:
        output_filename = f'{task_type}_{participant_id}_V{visit_num}_{block_label}_{date_only}.csv'
    else:
        output_filename = f'{task_type}_{participant_id}_V{visit_num}_{date_only}.csv'
    
    output_path = os.path.join(data_dir, output_filename)
    df.to_csv(output_path, index=False)
    
    print(f"Saved: {output_filename}")
    
    return output_path

# MAIN EXPERIMENT!!!!
def run_experiment():    
    # welcome screen
    instruction_text.text = (
        "Welcome!\n\n"
        "Press SPACE to begin."
    )
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])
    
    # IMPLICIT TASK
    print("\n" + "="*60)
    print("STARTING IMPLICIT TASK")
    print("="*60)
    
    instruction_text.text = (
        "In this task, you will see faces appear on the screen.\n"
        "You will use arrow keys to move toward or away from faces.\n\n"
        "We'll start with practice trials.\n\n"
        "Press SPACE to continue."
    )
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])
    
    # block 1
    block_1_type = block_order[0]
    block_1_data = []
    
    # practice
    practice_trials_1 = create_practice_trials(support_images, practice_strangers, block_1_type)
    practice_data_1 = run_implicit_block(practice_trials_1, block_num=1, is_practice=True)
    block_1_data.extend(practice_data_1)
    
    # main trials
    block_1_trials = create_implicit_trial_list(support_images, implicit_block1_strangers, block_1_type)
    block_1_main_data = run_implicit_block(block_1_trials, block_num=1, is_practice=False)
    block_1_data.extend(block_1_main_data)
    
    # save block 1
    save_data_to_csv(block_1_data, participant_id, visit_num, session_time, 
                     race_ethnicity, data_dir, 'implicit', block_label='block1', date_only=date_only)
    
    # block 2 (no break screen)
    block_2_type = block_order[1]
    block_2_data = []
    
    # practice
    practice_trials_2 = create_practice_trials(support_images, practice_strangers, block_2_type)
    practice_data_2 = run_implicit_block(practice_trials_2, block_num=2, is_practice=True)
    block_2_data.extend(practice_data_2)
    
    # main trials
    block_2_trials = create_implicit_trial_list(support_images, implicit_block2_strangers, block_2_type)
    block_2_main_data = run_implicit_block(block_2_trials, block_num=2, is_practice=False)
    block_2_data.extend(block_2_main_data)
    
    # save block 2
    save_data_to_csv(block_2_data, participant_id, visit_num, session_time,
                     race_ethnicity, data_dir, 'implicit', block_label='block2', date_only=date_only)
    
    # save combined
    all_implicit_data = block_1_data + block_2_data
    save_data_to_csv(all_implicit_data, participant_id, visit_num, session_time,
                     race_ethnicity, data_dir, 'implicit', block_label='combined', date_only=date_only)
    
    # EXPLICIT TASK    
    print("\n" + "="*60)
    print("STARTING EXPLICIT TASK")
    print("="*60)
    
    explicit_data = run_explicit_task(support_images, explicit_strangers)
    
    print(f"\nExplicit task completed: {len(explicit_data)} trials collected")
    
    # save explicit data
    if explicit_data:
        save_data_to_csv(explicit_data, participant_id, visit_num, session_time,
                         race_ethnicity, data_dir, 'explicit', date_only=date_only)
    else:
        print("WARNING: No explicit data to save!")
    
    # REACHED THE END
    instruction_text.text = (
        "You have completed all tasks!\n\n"
        "Thank you for your participation.\n\n"
        "Press SPACE to finish."
    )
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])
    
    return all_implicit_data, explicit_data

# RUN EXPERIMENT
try:
    implicit_data, explicit_data = run_experiment()
    
    print("\n" + "="*60)
    print("EXPERIMENT COMPLETE")
    print("="*60)
    print(f"\nParticipant: {participant_id}")
    print(f"Visit: {visit_num}")
    print(f"Race: {race_ethnicity}")
    print(f"\nImplicit trials: {len(implicit_data)}")
    print(f"Explicit trials: {len(explicit_data)}")
    print(f"\nData saved to: {data_dir}")
    
    # show allocation summary
    print("\n" + allocator.get_allocation_summary(participant_id))
    
finally:
    win.close()
    core.quit()