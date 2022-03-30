# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 18:22:56 2022

@author: email
"""
#simplify the problem: 
#let's say we only have one worker preparing and one cooking.
#procssing n jobs through 2 machines.
#http://www.universalteacherpublications.com/univ/ebooks/or/Ch14/nmac2job.htm#:~:text=This%20problem%20refers%20to%20the,i.e.%2C%20passing%20is%20not%20allowed.

attrs = {0: {"kid": True, "prep": 5, "cook": 20},
         1: {"kid": False, "prep": 15, "cook": 15},
         2: {"kid": True, "prep": 20, "cook": 25},
         3: {"kid": True, "prep": 5, "cook": 55},
         4: {"kid": True, "prep": 40, "cook": 45},
          5: {"kid": False, "prep": 45, "cook": 35},
          6: {"kid": False, "prep": 50, "cook": 55},
          7: {"kid": False, "prep": 5, "cook": 10},
          8: {"kid": True, "prep": 10, "cook": 10},
          9: {"kid": True, "prep": 55, "cook": 30},
          10: {"kid": False, "prep": 25, "cook": 20},
          11: {"kid": True, "prep": 30, "cook": 40},
          12: {"kid": False, "prep": 15, "cook": 5},
          13: {"kid": True, "prep": 35, "cook": 15}}

prepT=[(k,v['prep']) for k,v in attrs.items()]
cookT= [(k,v['cook']) for k,v in attrs.items()]
#print(prepT)
#print(cookT)


#johnson's rule/ johnson's algorithm:
#n jobs and two machines.  minimizes idle time of the machines.
#assumption: orders DO need to be cooked right after being prepared.
def sequencing(prepT, cookT):
    final_sequence=list()
    while len(prepT)>0:
        minT=99
        for i in range(len(prepT)):
            if prepT[i][1]<minT:
                minT=prepT[i][1]
                selectedL=prepT
                firstI=prepT[i][0]
        for i in range(len(cookT)):
            if cookT[i][1]<minT:
                minT=cookT[i][1]
                selectedL=cookT
                lastI=cookT[i][0]
                firstI=-1
                lastI=cookT[i][0]
        if selectedL==prepT:
            final_sequence.insert(0,firstI)
            prepT=[element for element in prepT  if element[0]!=firstI]
            cookT=[element for element in cookT  if element[0]!=firstI]
        elif selectedL==cookT:
            final_sequence.append(lastI)
            prepT=[element for element in prepT  if element[0]!=lastI]
            cookT=[element for element in cookT  if element[0]!=lastI]
    return final_sequence

print(sequencing(prepT, cookT))
        
    
        
  
        
            
            

            