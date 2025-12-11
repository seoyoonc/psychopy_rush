# RUSH PsychoPy Protocol
##### Author: Seoyoon
##### Last updated: 12/5/25

---
## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Folder Structure](#folder-structure)
- [Photo Requirements](#photo-requirements)
- [Running the Experiment](#running-the-experiment)
- [Data Output](#data-output)
- [Counterbalancing](#counterbalancing)
- [Troubleshooting](#troubleshooting)

---

## Overview

The behavioral task consists of two tasks:

### Implicit Approach-Avoidance Task
- **Trials:** 116 per visit (divided into 16 practice + 100 main across 2 blocks)
- Participants use arrow keys to move a stick figure toward or away from faces
- Block 1: One mapping (e.g., approach support figures, avoid strangers)
- Block 2: Reversed mapping
- Outcomes are reaction time and accuracy, and this data is exported automatically once the block is finished.

### Explicit Rating Task
- **Trials:** 30 per visit
- Participants rate faces on -4 (avoid) to +4 (approach) scale
- Uses keyboard keys A-L (labeled as -4 to +4)
- Outcomes are rating and reaction time, and this data is exported automatically once the block is finished.

### Study Design
- **2 visits per participant** (Visit 2 and Visit 3)
- **No photo repeats** between visits (within participant)
- **Personalized support figures** (5 photos per participant)
- **Race-matched and race-different strangers**

---

## Requirements

### System Requirements
- **Operating System:** Windows
- **PsychoPy:** Has been only tested with (v20251.1)
- **Display:** Minimum 1920×1080 resolution (fullscreen). Make sure that you go to Settings > Personalization > Taskbar > Taskbar behaviors > check 'Automatically hide the taskbar'.
- **Input:** Standard keyboard with arrow keys (up/down) for implicit task, letter keys A-L for explicit task, esc key to exit out of task window, space key to proceed through instructions

### Photo Requirements Summary
- **Support Figures**: 5 per participant, can be JPG/PNG, 800×800 px
- **Real Strangers**: 24 total (6 per race), can be JPG/PNG, 800×800 px
- **AI Strangers**: 220 total (55 per race), can be JPG/PNG, 800×800 px
- **Manikin**: just one, PNG format, uploaded to repo

**Total:** 245 stranger photos + 5 per participant + 1 manikin

---

## Installation Process: PLS READ THROUGH CAREFULLY!

**For software, PsychoPy is the only thing that you need** (this is the experiment software, Python is built-in, so don't worry about downloading Python AT ALL.)

### FIRST, make sure that Psychopy v20251.1 is installed on your desktop/laptop.

### SECOND, download the files in this repository as a zip file.

### THIRD, make sure the project directory is organized appropriately.
Create the main folder in Turbo, name it RUSH_project.
Place these files in the project directory:
- `approach_avoidance_tasks.py` - Main experiment script
- `photo_allocator.py` - Photo management system

---

## Folder Structure: PLS FOLLOW THIS EXACTLY!

```
lsa-annelism-win.turbo.storage.umich.edu/lsa-annelism/RUSH_Study/RUSH_Psychopy
├── approach_avoidance_tasks.py
├── photo_allocator.py
├── stimuli/
│   ├── support/
│   │   ├── 001_{participant_id}_001/
│   │   │   ├── support_01.jpg
│   │   │   ├── support_02.jpg
│   │   │   ├── support_03.jpg
│   │   │   ├── support_04.jpg
│   │   │   └── support_05.jpg
│   │   ├── 002_{participant_id}_002/
│   │   │   ├── support_01.jpg
│   │   │   ├── support_02.jpg
│   │   │   ├── support_03.jpg
│   │   │   ├── support_04.jpg
│   │   │   └── support_05.jpg
│   │   └── 003_{participant_id}_001/
│   │       └── ... (5 files, same as above)
│   ├── strangers/
│   │   ├── real/
│   │   │   ├── real_white_01.jpg
│   │   │   ├── real_white_02.jpg
│   │   │   ├── ... (6 white photos)
│   │   │   ├── real_asian_01.jpg
│   │   │   ├── ... (6 asian photos)
│   │   │   ├── real_black_01.jpg
│   │   │   ├── ... (6 black photos)
│   │   │   ├── real_hispanic_01.jpg
│   │   │   └── ... (6 hispanic photos)
│   │   └── ai/
│   │       ├── ai_white_001.jpg
│   │       ├── ... (55 white photos)
│   │       ├── ai_asian_001.jpg
│   │       ├── ... (55 asian photos)
│   │       ├── ai_black_001.jpg
│   │       ├── ... (55 black photos)
│   │       ├── ai_hispanic_001.jpg
│   │       └── ... (55 hispanic photos)
│   └── stickmanikin.png
└── data/
    └── (auto-created, DO NOT CREATE THIS FOLDER YOURSELF.)
```

---

## Photo Requirements

#### All Face Photos
- **Dimensions:** 800 × 800 pixels (square)
- **Format:** JPG or PNG
- **File Size:** < 500 KB recommended

#### Photo Quality Guidelines
- **Centered face**
- **Full face visible**
- **Relatively dark background** (the manikin is white, so having a white background would make it hard to see the manikin approaching the image)
- **Clear, in-focus** images

### Naming Conventions: PLS READ THROUGH THIS CAREFULLY!

#### Support Figures
**Location:** `stimuli/support/{participant_id}/`

**Format:** `support_01.jpg`, `support_02.jpg`, ..., `support_05.jpg`

**Rules:**
- Exactly 5 photos per participant
- Numbered 01 through 05
- File extension: `.jpg`, `.jpeg`, or `.png`
- **Folder name must match participant ID exactly**

**Examples:**
```
stimuli/support/001_124261_001/support_01.jpg
stimuli/support/002_124262_001/support_02.jpg
stimuli/support/003_123349_001/support_01.jpg
```

#### Real Stranger Photos
**Location:** `stimuli/strangers/real/`

**Format:** `real_{race}_{number}.{ext}`

**Rules:**
- `{race}`: Must be exactly `white`, `asian`, `black`, or `hispanic` (lowercase)
- `{number}`: Two digits, 01-06 for each race
- `{ext}`: `.jpg`, `.jpeg`, or `.png`

**Required Files (24 total):**
```
real_white_01.jpg through real_white_06.jpg (6 photos)
real_asian_01.jpg through real_asian_06.jpg (6 photos)
real_black_01.jpg through real_black_06.jpg (6 photos)
real_hispanic_01.jpg through real_hispanic_06.jpg (6 photos)
```

#### AI Stranger Photos
**Location:** `stimuli/strangers/ai/`

**Format:** `ai_{race}_{number}.{ext}`

**Rules:**
- `{race}`: Must be exactly `white`, `asian`, `black`, or `hispanic` (lowercase)
- `{number}`: Three digits, 001-055 for each race
- `{ext}`: `.jpg`, `.jpeg`, or `.png`

**Required Files (220 total):**
```
ai_white_001.jpg through ai_white_055.jpg (55 photos)
ai_asian_001.jpg through ai_asian_055.jpg (55 photos)
ai_black_001.jpg through ai_black_055.jpg (55 photos)
ai_hispanic_001.jpg through ai_hispanic_055.jpg (55 photos)
```

**Note:** all files must follow the naming pattern exactly.

#### Manikin
**Location:** `stimuli/stickmanikin.png`

### Photo Allocation Details

#### Per Visit Usage:

**Implicit Task (2 blocks per visit):**
- Block 1: 4 real (1 per race) + 21 AI (9 race-matched + 4+4+4 race-different)
- Block 2: 4 real (1 per race) + 21 AI (9 race-matched + 4+4+4 race-different)
- Practice: 4 AI strangers (1 per race, can repeat across visits)

**Explicit Task:**
- 4 real (1 per race) + 21 AI (9 race-matched + 4+4+4 race-different)

#### Total per Participant (2 visits):
- **Real photos:** 24 (12 per visit, all 6 per race used across 2 visits)
- **AI photos:** 126 (63 per visit)
  - Race-matched: 54 (27 per visit)
  - Race-different: 72 (36 per visit)

---

## Running the Experiment

### Before Starting

#### 1. Prepare Participant's Support Figures
For each new participant:
```bash
# Create folder with their ID
mkdir stimuli/support/{participant_id}

# Add 5 photos named support_01.jpg through support_05.jpg
```

#### 2. Label Keyboard Keys
Use tape or stickers to label keys 1-9 as:
```
┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
│-4 │-3 │-2 │-1 │ 0 │+1 │+2 │+3 │+4 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┘
  1   2   3   4   5   6   7   8   9  ← Actual keys
```

### Running the Experiment

#### 1. Navigate to Project Directory
```bash
cd /path/to/project_directory
```

#### 2. Run Experiment
```bash
python approach_avoidance_tasks.py
```

#### 3. Enter Participant Information
**Dialog will appear with 2 fields:**
- **Participant ID:** Enter exactly as it appears in support folder
  - Examples: `001`, `002`, `RUSH_12345`, `SUB_042`
- **Visit Number:** Select `2` or `3` from dropdown

**Click OK to start**

#### 4. Race/Ethnicity Selection
Participant clicks one button:
- White
- Asian
- Black
- Hispanic
- None of the above (experiment exits)

#### 5. Experiment Flow
1. **Welcome screen** → Press SPACE
2. **Implicit Block 1 instructions** (manikin shown at bottom) → Press SPACE
3. **Practice trials** (8 trials with Red X feedback on errors)
4. **Main Block 1** (50 trials, no feedback)
5. **Implicit Block 2 instructions** (manikin shown at bottom) → Press SPACE
6. **Practice trials** (8 trials with Red X feedback on errors)
7. **Main Block 2** (50 trials, no feedback)
8. **Explicit task instructions** → Press SPACE
9. **Explicit trials** (30 trials)
10. **Thank you screen** → Press SPACE to finish

**Total Duration:** ~20-25 minutes

### Emergency Stop (PRESS ONLY IF THERE IS AN EMERGENCY!)
Press **ESC** at any time to quit (data saved up to last completed block)

---

## Data Output

### File Structure
```
data/
├── photo_allocations.json                   # Tracks photo usage
├── implicit_{ID}_V2_block1_{date}.csv       # Block 1 data
├── implicit_{ID}_V2_block2_{date}.csv       # Block 2 data
├── implicit_{ID}_V2_combined_{date}.csv     # Both blocks together
└── explicit_{ID}_V2_{date}.csv              # Explicit ratings
```

### CSV Files Created Per Session

#### Implicit Block CSVs
**Columns:**
- `trial_number` - Trial number within block (1-58)
- `block_type` - `approach_support` or `avoid_support`
- `image_type` - `support`, `ai-stranger`, or `real-stranger`
- `image_path` - Full path to image file
- `image_filename` - Just filename
- `manikin_position` - Always `bottom`
- `correct_response` - `up` or `down`
- `participant_response` - `up` or `down`
- `accuracy` - 1 (correct) or 0 (incorrect)
- `reaction_time` - Response time in seconds
- `is_practice` - True or False
- `block_number` - 1 or 2
- `session_time` - Full timestamp (YYYY-MM-DD_HH-MM-SS)
- `race_ethnicity` - Selected race (first row only)
- `average_accuracy` - Mean accuracy for main trials (first row only)
- `average_reaction_time` - Mean RT for main trials (first row only)

**Row count:** 59 rows (1 header + 58 trials: 8 practice + 50 main)

#### Implicit Combined CSV
Same columns as block files, contains both Block 1 and Block 2 data.

**Row count:** 117 rows (1 header + 116 trials)

#### Explicit CSV
**Columns:**
- `trial_number` - Trial number (1-30)
- `image_path` - Full path to image file
- `image_filename` - Just filename
- `image_type` - `support`, `ai-stranger`, or `real-stranger`
- `key_pressed` - Which key (1-9)
- `rating` - Actual rating (-4 to +4)
- `reaction_time` - Response time in seconds
- `session_time` - Full timestamp
- `race_ethnicity` - Selected race (first row only)

**Row count:** 31 rows (1 header + 30 trials)

### Photo Allocations JSON
**Purpose:** Tracks which photos each participant has seen to prevent repeats

**Important:** Do NOT delete `photo_allocations.json` during study! It ensures no photo repeats between visits.

---

## Counterbalancing

### Block Order Assignment
Determined by **last digit** of participant ID:

**Examples:**
- ID `001` → Last digit 1 (odd) → Approach-support first
- ID `002` → Last digit 2 (even) → Avoid-support first
- ID `001_12345_001` → Last digit 1 (odd) → Approach-support first

**Consistency:** Same ID always produces same block order (even across visits)

---

## Troubleshooting

### Common Issues

#### "Support folder not found"
**Problem:** No folder exists for participant ID

**Solution:**
```bash
# Check folder exists
ls stimuli/support/{participant_id}

# If not, create and add 5 photos
mkdir stimuli/support/{participant_id}
# Add support_01.jpg through support_05.jpg
```

#### "Could not find file"
**Problem:** Photos named incorrectly or missing

**Solution:**
- Check file naming matches exactly: `ai_white_001.jpg` (not `AI_White_1.jpg`)
- Race names must be lowercase: `white`, `asian`, `black`, `hispanic`
- Check file extensions: `.jpg`, `.jpeg`, or `.png`

#### "Only got X strangers, need 25"
**Problem:** Not enough photos in pool or naming issues

**Solution:**
- Verify you have 24 real photos (6 per race)
- Verify you have 220 AI photos (55 per race)
- Check all files follow naming convention exactly

#### Experiment crashes mid-session

I haven't really encountered this, but we have data saved up to the last completed block. In the case where it crashes, we will have to start over.
DO NOT click the windows key when the task bar is hidden, and DO NOT press the esc key.

**RECOMMENDED STEPS:** 
- Check console output for error messages, contact Seoyoon
- Verify all photo files exist in the exact participant folder
- Delete `photo_allocations.json` if starting fresh with test data (CHECK WITH SEOYOON FIRST. NEVER DELETE A FILE YOURSELF.)

---

## Technical Details

### Display Settings
- **Window:** Fullscreen (1920×1080 recommended)
- **Color:** Gray background (#808080)
- **Units:** Normalized (-1 to +1)

### Image Sizing
- **Normal:** 0.4 × 0.4 units (~216×216 px on 1080p screen)
- **Bigger (approach):** 0.6 × 0.6 units (~324×324 px)
- **Smaller (avoid):** 0.25 × 0.25 units (~135×135 px)

### Timing
- **Fixation:** 500ms
- **Feedback display:** 500ms (Red X in practice only)
- **ITI:** 250ms

### Keyboard Mapping

#### Implicit Task
- **UP arrow:** Approach (image bigger)
- **DOWN arrow:** Avoid (image smaller)
- Manikin always positioned at bottom of screen

#### Explicit Task
- **Keys 1-9:** Ratings -4 to +4
- **Key 5:** Neutral (0)

---

## QCing For Experiment

### Before Each Participant
- [ ] Create support folder with 5 photos (800×800 px)
- [ ] Verify keyboard labels (1-9 as -4 to +4)
- [ ] Make sure to enter the participant_id in the window exactly as it is stored in Turbo.

### After Each Session
- [ ] Verify 4 CSV files created
- [ ] Check file sizes (not 0 bytes)
- [ ] Quick visual check of data

### Data Management
- [ ] Never delete `photo_allocations.json` during study. Pls ask Seoyoon if you have any concerns about this!
- [ ] Recommended to keep backup of original photos
- [ ] Document any issues
- [ ] Save data to folder (note to Seoyoon: to go over with Jack)

---

## Versions

- **Current version** 
  - Implicit approach-avoidance task with counterbalanced blocks
  - Explicit rating task
  - Photo allocation system preventing repeats
  - 2-visits with race-matched stimuli
  - Manikin always positioned at bottom
  - 800×800 px image specifications
