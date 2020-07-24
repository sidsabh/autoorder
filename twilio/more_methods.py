"""
This file is for even more general methods. This file should not require any imports except global variables.
"""

import g

"""
Deals with typos. Returns true if the msg contains a word that matches to one letter off.
Input: The item name to match msg with
Returns: True or False
"""
def is_similar(Word):

    Same = False

    for Sen_Word in g.msg.split(" "):
        if Word in Sen_Word: Same = True
        
        elif len(Sen_Word) == len(Word)+1:
            Left_Count=Right_Count=0
            for i, x in zip(Sen_Word, Word):
                if i == x: Left_Count += 1
                else: break
                
            Letters_Left = min(len(Sen_Word), len(Word))-Left_Count
            for i, x in zip(Sen_Word[::-1], Word[::-1]):
                if Letters_Left - Right_Count > 0 and i == x: Right_Count += 1
                else: break
            if Left_Count + Right_Count == len(Word): Same = True


        elif len(Sen_Word) == len(Word):
            Left_Count=Right_Count=0
            for i, x in zip(Sen_Word, Word):
                if i == x: Left_Count += 1
                else: break
                
            Letters_Left = min(len(Sen_Word), len(Word))-Left_Count
            for i, x in zip(Sen_Word[::-1], Word[::-1]):
                if Letters_Left - Right_Count > 0 and i == x: Right_Count += 1
                else: break
            if Left_Count + Right_Count == len(Word)-1: Same = True


        elif len(Word) == len(Sen_Word)+1:

            Left_Count=Right_Count=0
            for i, x in zip(Word, Sen_Word):
                 
                if i == x: Left_Count += 1
                else: break
            
            Letters_Left = min(len(Word), len(Sen_Word))-Left_Count
            for i, x in zip(Word[::-1], Sen_Word[::-1]):
                if Letters_Left - Right_Count > 0 and i == x: Right_Count += 1
                else: break
            if Left_Count + Right_Count == len(Sen_Word): Same = True



            
    return Same 
