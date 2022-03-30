# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 13:06:09 2022

@author: email
"""
#restaurant 
#idea: assign value a=(0,1)to imply the priority level 
#of a certain order
#bin stacking to select activities to go into each machine?

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


#decide what worker gets what orders.
#returns two lists representing two workers,
#with elements being tuples of the form
#(order index, prep/cook time)   

#class restaurant():
    #def __init__(self, attrs):
    #    self.attrs=attrs


def worker_distribution(attrs, action):
    times=sorted([(k,v[action]) for k,v in attrs.items()], key=lambda x: x[1], reverse=True)
    w1=[]
    w2=[]
    for x in times:
        if sum(n for i, n in w1)<=sum(n for i, n in w2):
            w1.append(x)
        else:
            w2.append(x)
    return w1, w2
    
l1, l2 = worker_distribution(attrs, 'prep')
print(l1, sum(n for i, n in l1))
print(l2,  sum(n for i, n in l2))

