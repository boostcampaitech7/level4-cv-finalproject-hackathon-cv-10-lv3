# -*- coding: utf-8 -*-

import time

from APIs.Feedback import feedback_for_diary

log_path = "/data/ephemeral/home/level4-cv-finalproject-hackathon-cv-10-lv3/Project/ImageStudy/diarylog.txt"

def diary():
    with open(log_path, 'a', encoding='utf-8') as logfile:
        logfile.write('\n==================== ' + time.strftime('%Y.%m.%d - %H:%M:%S') + ' ====================\n')

        user_input = input()
        logfile.write(user_input)

        logfile.write('\n> feedback\n')
        feedback = feedback_for_diary(user_input)
        logfile.write(feedback)
        
        logfile.write('\n==================== diary closed ====================\n')