# project title: rush behavioral task
# author: seoyoonc
# last updated 12/31/25

# current revisions and points to look out for: practice photos excluded from explicit round, practice
#                                               photos excluded from manipulation check, confidence display
#                                               confidence display doesn't show selected numbers, clear events
#                                               so that first question doesn't get skipped.
# mention imagine you are the manikin.
# to check: participant_001 vs 002
# don't save block txt file
# put the manikin at the bottom of the screen, where it is usually positioned,
# and also put the instructions on the screen

from psychopy import visual, core, event
from psychopy.hardware import keyboard

import os
import pandas as pd
from datetime import datetime
import sys

from setup import *
from window import *
from participant import *
from allocation_task import *
from photo_handler import *
from implicit_tasks import *
from explicit_tasks import *


###########################################################################################################
# SAVE DATA
###########################################################################################################
def save_data_to_csv(data_list, participant_id, visit_num, session_time, race_ethnicity, 
                     data_dir, task_type, block_label="", date_only=""):
    """Save data to CSV file."""
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
        # calc averages for main trials only (excluding practice)
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



###########################################################################################################
# Main Experiment
###########################################################################################################
def main():
    """Run the complete experiment."""
    
    ##### SETUP #####
    participant = participant_setup()
    
    # Setup /data within participant support folder
    data_dir = os.path.join(participant.support_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    ##### Create Visual Window GUI #####
    gui = VisualWindow(1920, 1080)

    ###### Welcome screen #####
    gui.instruction_text.text = welcome_text
    gui.instruction_text.draw()
    gui.win.flip()
    event.waitKeys(keyList=['space', 'escape'])

    race_ethnicity = get_race_ethnicity_selection(gui)
    participant.race = race_ethnicity

    ##### Photo Allocation for Tasks #####
    # allocator = PhotoAllocator(data_dir)
    allocator = PhotoAllocator(base_dir, participant.support_dir)

    (support_images, 
    practice_strangers, 
    practice_stranger_filenames,
    implicit_block1_strangers, 
    implicit_block2_strangers, 
    explicit_strangers)           = main_allocation_task(allocator, gui.manikin, participant)

    ##### Setting up Implicit Task #####    
    gui.instruction_text.text = implicit_instructions

    gui.instruction_text.draw()

    gui.win.flip()

    event.waitKeys(keyList=['space', 'escape'])


    # Block 1
    block_1_type = participant.block_order[0]
    block_1_data = []

    ##### Practice Run 1 #####
    practice_trials_1 = create_practice_trials(support_images, practice_strangers, block_1_type)
    practice_data_1 = run_implicit_block(gui, practice_trials_1, block_num=1, is_practice=True)
    block_1_data.extend(practice_data_1)
    
    ##### Main Trial 1 #####
    block_1_trials = create_implicit_trial_list(support_images, implicit_block1_strangers, block_1_type)
    block_1_main_data = run_implicit_block(gui, block_1_trials, block_num=1, is_practice=False)
    block_1_data.extend(block_1_main_data)
    
    # Save Main Trial 1
    save_data_to_csv(block_1_data, participant.id, participant.visit_num, session_time,
                     participant.race, data_dir, 'implicit', block_label='block1', date_only=date_only)

    ##### Setting Up Main Trial 2 #####
    block_2_type = participant.block_order[1]
    block_2_data = []
    
    # Practice Run 2
    practice_trials_2 = create_practice_trials(support_images, practice_strangers, block_2_type)
    practice_data_2 = run_implicit_block(gui, practice_trials_2, block_num=2, is_practice=True)
    block_2_data.extend(practice_data_2)
    
    ##### Main trial 2 ######
    block_2_trials = create_implicit_trial_list(support_images, implicit_block2_strangers, block_2_type)
    block_2_main_data = run_implicit_block(gui, block_2_trials, block_num=2, is_practice=False)
    block_2_data.extend(block_2_main_data)
    
    # Save Main Trial 2
    save_data_to_csv(block_2_data, participant.id, participant.visit_num, session_time,
                     participant.race, data_dir, 'implicit', block_label='block2', date_only=date_only)
    
    # Save Combined
    all_implicit_data = block_1_data + block_2_data
    save_data_to_csv(all_implicit_data, participant.id, participant.visit_num, session_time,
                     participant.race, data_dir, 'implicit', block_label='combined', date_only=date_only)
    
    ##### Explicit Task #####    
    explicit_data = run_explicit_task(gui, support_images, explicit_strangers)
    

    
    # save explicit data
    if explicit_data:
        save_data_to_csv(explicit_data, participant.id, participant.visit_num, session_time,
                         participant.race, data_dir, 'explicit', date_only=date_only)
    else:
        print("WARNING: No explicit data to save!")
    
    ##### MANIPULATION CHECK (Visit 3 only) #####
    manipulation_data = []
    if participant.visit_num == '3':
        # collect all real and AI photos used in this session (EXCLUDING practice)
        all_real_used = []
        all_ai_used = []
        
        # from implicit blocks (main trials only, not practice)
        for photo in implicit_block1_strangers + implicit_block2_strangers:
            filename = os.path.basename(photo)
            # skip practice photos
            if filename in practice_stranger_filenames:
                continue
            if filename.startswith('real_'):
                all_real_used.append(photo)
            elif filename.startswith('ai_'):
                all_ai_used.append(photo)
        
        # from explicit task (already excludes practice photos)
        for photo in explicit_strangers:
            filename = os.path.basename(photo)
            if filename.startswith('real_'):
                all_real_used.append(photo)
            elif filename.startswith('ai_'):
                all_ai_used.append(photo)
        
        # remove duplicates
        all_real_used = list(set(all_real_used))
        all_ai_used = list(set(all_ai_used))
        
        print(f"  Available for manipulation check: {len(all_real_used)} real + {len(all_ai_used)} AI")
        print(f"  (Practice photos excluded)")
        
        manipulation_data = run_manipulation_check(gui, all_real_used, all_ai_used)
        
        print(f"\nManipulation check completed: {len(manipulation_data)} trials collected")
        
        # save manipulation check data
        if manipulation_data:
            df = pd.DataFrame(manipulation_data)
            df['session_time'] = session_time
            df['race_ethnicity'] = ''
            df.loc[0, 'race_ethnicity'] = participant.race
            
            output_filename = f'manipulation_check_{participant.id}_V{participant.visit_num}_{date_only}.csv'
            output_path = os.path.join(data_dir, output_filename)
            df.to_csv(output_path, index=False)
            print(f"✓ Saved: {output_filename}")
    
    ##### END SCREEN #####
    gui.instruction_text.text = complete_text
    gui.instruction_text.draw()
    gui.win.flip()
    event.waitKeys(keyList=['space', 'escape'])
    
    gui.close()
    return all_implicit_data, explicit_data, manipulation_data, allocator, participant


if __name__ == "__main__":
    try:
        implicit_data, explicit_data, manipulation_data, allocator, participant = main()
        
        if manipulation_data:
            print(f"Manipulation check trials: {len(manipulation_data)}")
        print(f"\nData saved to: {data_dir}")
        
        # Show allocation summary
        print("\n" + allocator.get_allocation_summary(participant.id))
        
    finally:
        pass
