import os
from datetime import datetime

# AUTO GENERATE DATE AND SESSION TIMESTAMP
date_only = datetime.now().strftime('%Y-%m-%d')
session_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# FILE PATHS - Define early for race selection CSV
base_dir = os.path.dirname(os.path.join(os.path.abspath("."), os.pardir, os.pardir))

# manikin
manikin_path = os.path.join(base_dir, 'stimuli', 'stickmanikin.png')


welcome_text =  (
                    "Welcome!\n\n"
                    "Press SPACE to begin."
                )

implicit_instructions = (
                            "In this task, you will see faces appear on the screen.\n"
                            "You will use arrow keys to move toward or away from faces.\n\n"
                            "When you move TOWARD, the image grows bigger.\n"
                            "When you move AWAY, the image shrinks smaller.\n\n"
                            "We'll start with practice trials.\n\n"
                            "Press SPACE to continue."
                        )

explicit_instructions = (
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

complete_text = (
                    "You have completed all tasks!\n\n"
                    "Thank you for your participation.\n\n"
                    "Press SPACE to finish."
                )