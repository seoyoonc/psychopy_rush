# project title: RUSH photo allocator
# author: seoyoonc
# last updated 12/5/25
# --> random selection
# --> tracks photos across blocks, visits 2 and 3

import json
import os
import random
from typing import Dict, List, Set, Tuple

from participant import *
from exception import *

def load_images_from_folder(folder_path):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = []
    
    if os.path.exists(folder_path):
        for filename in sorted(os.listdir(folder_path)):
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                images.append(os.path.join(folder_path, filename))
    
    else:
        raise FileNotFoundError(f"Folder not found: {folder_path}")
        return images
    
    if len(images) != 5: raise NotFiveSupportImagesError(len(images))

    return images


class PhotoAllocator:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.allocation_file = os.path.join(base_dir, 'photo_allocations.json')
        
        # load or init allocations
        self.allocations = self._load_allocations()
        
        # photo pools
        self.strangers_dir = os.path.join(base_dir, 'stimuli', 'strangers')
        self.real_pool = self._build_real_pool()
        self.ai_pool = self._build_ai_pool()
    
    def _load_allocations(self) -> Dict:
        if os.path.exists(self.allocation_file):
            with open(self.allocation_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'participants': {},
                'used_real': [],
                'used_ai': []
            }
    
    # save current allocations to file
    def _save_allocations(self):
        os.makedirs(os.path.dirname(self.allocation_file), exist_ok=True)
        with open(self.allocation_file, 'w') as f:
            json.dump(self.allocations, indent=2, fp=f)
    
    # build pool of available REAL photos
    def _build_real_pool(self) -> Dict[str, List[str]]:
        pool = {'white': [], 'asian': [], 'black': [], 'hispanic': []}
        real_dir = os.path.join(self.strangers_dir, 'real')
        
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        if os.path.exists(real_dir):
            for filename in sorted(os.listdir(real_dir)):
                if any(filename.lower().endswith(ext) for ext in valid_extensions):
                    # extract race from filename: real_white_01.jpg -> white
                    parts = filename.split('_')
                    if len(parts) >= 2:
                        race = parts[1]
                        if race in pool:
                            pool[race].append(filename)
        
        return pool
    
    # build pool of available AI photos
    def _build_ai_pool(self) -> Dict[str, List[str]]:
        pool = {'white': [], 'asian': [], 'black': [], 'hispanic': []}
        ai_dir = os.path.join(self.strangers_dir, 'ai')
        
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        if os.path.exists(ai_dir):
            for filename in sorted(os.listdir(ai_dir)):
                if any(filename.lower().endswith(ext) for ext in valid_extensions):
                    # extract race from filename: ai_white_001.jpg -> white
                    parts = filename.split('_')
                    if len(parts) >= 2:
                        race = parts[1]
                        if race in pool:
                            pool[race].append(filename)
        
        return pool
    
    # all photos ALREADY used by the participant
    def _get_participant_used_photos(self, participant_id: str) -> Dict[str, Set[str]]:
        used = {'real': set(), 'ai': set()}
        
        if participant_id not in self.allocations['participants']:
            return used
        
        participant_data = self.allocations['participants'][participant_id]
        
        for visit_data in participant_data.get('visits', {}).values():
            for block_data in visit_data.values():
                used['real'].update(block_data.get('real', []))
                used['ai'].update(block_data.get('ai', []))
        
        return used
    
    def allocate_photos(self, participant: Participant, 
                       block: str, task: str) -> Dict[str, List[str]]:
        """
        purpose: to allocate photos for a specific block/task.
        
        args:
            participant_id
            race: 'white', 'asian', 'black', 'hispanic'
            visit: 2/3
            block: 'block1', 'block2' for implicit, 'explicit' for explicit
            task: implicit/explicit
        
        returns:
            dict with 'real' and 'ai' lists of filenames
        """
        
        # init participant if new
        if participant.id not in self.allocations['participants']:
            self.allocations['participants'][participant.id] = {
                'race': participant.race,
                'visits': {}
            }
        
        participant_data = self.allocations['participants'][participant.id]
        
        # init visit if new
        if str(participant.visit_num) not in participant_data['visits']:
            participant_data['visits'][str(participant.visit_num)] = {}
        
        visit_data = participant_data['visits'][str(participant.visit_num)]
        
        # check if already allocated
        block_key = f"{task}_{block}" if task == 'implicit' else task
        if block_key in visit_data:
            print(f"  Using existing allocation for {block_key}")
            return visit_data[block_key]
        
        # get photos already used by this participant
        participant_used = self._get_participant_used_photos(participant.id)
        
        # allocate new photos
        allocation = self._allocate_new_photos(participant.race, participant_used, task)
        
        # save allocation
        visit_data[block_key] = allocation
        
        self.allocations['used_real'].extend(allocation['real'])
        self.allocations['used_ai'].extend(allocation['ai'])
        
        # save to file
        self._save_allocations()
        
        return allocation
    
    def _allocate_new_photos(self, participant_race: str, 
                            participant_used: Dict[str, Set[str]],
                            task: str) -> Dict[str, List[str]]:
        """
        to allocate new photos based on task requirements.
        
        For 220 total AI photos (55 per race):
        implicit: 4 real (1 per race) + 21 AI (9 race-matched + 12 race-different: 4 per other race)
        explicit: 4 real (1 per race) + 21 AI (9 race-matched + 12 race-different: 4 per other race)
        
        total per block: 25 strangers
        """
        allocation = {'real': [], 'ai': []}
        
        other_races = [r for r in ['white', 'asian', 'black', 'hispanic'] 
                      if r != participant_race]
        
        # allocate real faces (1 of each race)
        for race in ['white', 'asian', 'black', 'hispanic']:
            available = [f for f in self.real_pool[race] 
                        if f not in participant_used['real']]
            
            if not available:
                available = self.real_pool[race]
            
            if available:
                selected = random.choice(available)
                allocation['real'].append(selected)
        
        # allocate AI faces - 9 race-matched + 12 race-different (4 per other race)
        ai_counts = {participant_race: 9}
        for race in other_races:
            ai_counts[race] = 4
        
        # select AI photos
        for race, count in ai_counts.items():
            available = [f for f in self.ai_pool[race] 
                        if f not in participant_used['ai']]
            
            if len(available) < count:
                print(f"WARNING: Only {len(available)} {race} AI photos available, need {count}")
                count = len(available)
            
            if available:
                selected = random.sample(available, count)
                allocation['ai'].extend(selected)
        
        return allocation
    
    def get_photo_paths(self, filenames: List[str]) -> List[str]:
        paths = []
        
        for filename in filenames:
            if filename.startswith('real_'):
                folder = os.path.join(self.strangers_dir, 'real')
            elif filename.startswith('ai_'):
                folder = os.path.join(self.strangers_dir, 'ai')
            else:
                continue
            
            # first try the filename
            path = os.path.join(folder, filename)
            if os.path.exists(path):
                paths.append(path)
                continue
            
            # other
            base_name = os.path.splitext(filename)[0]
            for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                alt_path = os.path.join(folder, base_name + ext)
                if os.path.exists(alt_path):
                    paths.append(alt_path)
                    break
            else:
                print(f"WARNING: Could not find file: {filename} in {folder}")
        
        return paths
    
    def get_allocation_summary(self, participant_id: str) -> str:
        if participant_id not in self.allocations['participants']:
            return f"No allocations found for participant {participant_id}"
        
        p_data = self.allocations['participants'][participant_id]
        
        summary = []
        summary.append(f"Participant {participant_id} ({p_data['race']})")
        summary.append("="*60)
        
        for visit, visit_data in p_data['visits'].items():
            summary.append(f"\nVisit {visit}:")
            for block, block_data in visit_data.items():
                real_count = len(block_data.get('real', []))
                ai_count = len(block_data.get('ai', []))
                summary.append(f"  {block}: {real_count} real + {ai_count} AI = {real_count + ai_count} total")
        
        return "\n".join(summary)


