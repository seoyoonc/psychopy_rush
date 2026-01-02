###################################
# MAIN ALLOCATION TASK #
# COMBINES IMPLICIT AND EXPLICIT TASKS IMAGE ALLOCATIONS
# THIS SETS UP THE IMPLICIT TAST AND EXPLICIT TASKS
###################################

from psychopy import visual, core, event, gui
from psychopy.hardware import keyboard
import os

from setup import *
from photo_handler import *
from participant import *
from exception import *

def main_allocation_task(allocator, manikin, participant):
    # load support figures
    try:
        support_images = load_images_from_folder(participant.support_dir)
    except NotFiveSupportImagesError as e:
        print(e)
        print("looked in folder:", participant.support_dir)
    except FileNotFoundError as e:
        print(e)


    # allocate stranger photos for implicit blocks
    implicit_block1_allocation = allocator.allocate_photos(participant, 'block1', 'implicit')
    implicit_block2_allocation = allocator.allocate_photos(participant, 'block2', 'implicit')

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
    practice_stranger_filenames = []  # Track filenames to exclude from explicit task
    all_races = ['white', 'asian', 'black', 'hispanic']

    print(f"\nSelecting practice strangers (need 4: 1 of each race including {participant.race})...")

    # get exactly 1 AI stranger from EACH race (all 4 races)
    for race in all_races:
        race_ai = [f for f in allocator.ai_pool.get(race, []) if f.startswith('ai_')]
        
        if race_ai:
            selected = random.choice(race_ai)
            full_path = os.path.join(base_dir, 'stimuli', 'strangers', 'ai', selected)
            practice_strangers.append(full_path)
            practice_stranger_filenames.append(selected)  # Track filename
            print(f"Practice stranger {len(practice_strangers)}: {race} - {selected}")
        else:
            print(f"WARNING: No AI photos available for {race}")

    if len(practice_strangers) < 4:
        print(f"ERROR: Only got {len(practice_strangers)} practice strangers, need 4!")
    else:
        print(f"Practice: {len(practice_strangers)} strangers (1 of each race, can repeat across visits)")

    # allocate photos for explicit task (EXCLUDING practice photos)
    print("\nAllocating photos for Explicit Task...")
    explicit_allocation = allocator.allocate_photos(participant, 'explicit', 'explicit')

    # FILTER OUT practice photos from explicit task
    explicit_strangers_all = allocator.get_photo_paths(
        explicit_allocation['real'] + explicit_allocation['ai']
    )

    # Remove any photos that were used in practice
    explicit_strangers = []
    for photo in explicit_strangers_all:
        filename = os.path.basename(photo)
        if filename not in practice_stranger_filenames:
            explicit_strangers.append(photo)
        else:
            print(f"Excluding practice photo from explicit: {filename}")

    # If we filtered out photos, we might have fewer than 25
    if len(explicit_strangers) < 25:
        print(f"WARNING: Only {len(explicit_strangers)} strangers after excluding practice photos")
    else:
        print(f"Explicit: {len(explicit_strangers)} strangers allocated (practice photos excluded)")

    return support_images, practice_strangers, practice_stranger_filenames, implicit_block1_strangers, implicit_block2_strangers, explicit_strangers