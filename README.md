# RUSH PsychoPy Behavioral Task
Behavioral task including implicit and explicit tasks, plus manipulation check for Visit 3.

## Requirements

- PsychoPy
- Pictures (220 AI, 24 real strangers, 5 support)

## Structure

```
RUSH_Psychopy/
├── scripts/
│   ├── allocation_task.py
│   ├── approach_avoidance_tasks.py (main)
│   ├── exception.py
│   ├── explicit_tasks.py
│   ├── gui_functions.py
│   ├── implicit_tasks.py
│   └── participant.py
│   └── photo_handler.py
│   └── setup.py
│   └── window.py
├── stimuli/
│   ├── stickmanikin.png
│   ├── support/
│   │   └── {participant_folders}/
│   └── strangers/
│       ├── ai/ (220 photos)
└──     └── real/ (24 photos)
```

## Required Photos

AI folder (220 photos - 55 per race) Naming Convention
- ai_white_001.jpg to ai_white_055.jpg
- ai_asian_001.jpg to ai_asian_055.jpg
- ai_black_001.jpg to ai_black_055.jpg
- ai_hispanic_001.jpg to ai_hispanic_055.jpg

Real folder (24 photos - 6 per race) Naming Convention
- real_white_01.jpg to real_white_06.jpg
- real_asian_01.jpg to real_asian_06.jpg
- real_black_01.jpg to real_black_06.jpg
- real_hispanic_01.jpg to real_hispanic_06.jpg

Support folder (5 each)
- support_1.jpg (or .png or .jpeg)
- support_2.jpg
- support_3.jpg
- support_4.jpg
- support_5.jpg

## Participant ID

Format is `XXX_{PARTICIPANT_ID}_001` or `XXX_{PARTICIPANT_ID}_002`

The last 3 digits (001 or 002) determine block order:
- 001 (odd) = approach support first, avoid support second
- 002 (even) = avoid support first, approach support second

## Keyboard Setup

Label keyboard keys before running experiment, specifically keys A, S, D, F, G, H, J, K, L with labels -4 to +4

Some keys will be used for different parts of the experiment:
- +1, +2, +3 (explicit task)
- +1, +2, +3 (for manipulation check)

## Running the Experiment

1. Make sure photos are properly named and in correct folders
2. Select all .py scripts, drag and drop into the PsychoPy Coder
3. Run: `approach_avoidance_tasks.py`
4. Enter participant ID that matches support folder
5. Select visit number (2 or 3)
6. Participant selects their race/ethnicity
7. Experiment runs

## Data Output

Visit 2 (4 files):
- `implicit_{ID}_V2_block1_{date}.csv`
- `implicit_{ID}_V2_block2_{date}.csv`
- `implicit_{ID}_V2_combined_{date}.csv`
- `explicit_{ID}_V2_{date}.csv`

Visit 3 (5 files):
- `implicit_{ID}_V3_block1_{date}.csv`
- `implicit_{ID}_V3_block2_{date}.csv`
- `implicit_{ID}_V3_combined_{date}.csv`
- `explicit_{ID}_V3_{date}.csv`
- `manipulation_check_{ID}_V3_{date}.csv`

All files saved to data/ folder within each support folder.
