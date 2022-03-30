# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:52:58 2022

@author: email
"""

import collections
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from ortools.sat.python import cp_model
import time

start_time = time.time()
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

def getJobs(attrs):
    jobs=list()
    for key, value in attrs.items():
        jobs.append([[(value['prep']//5,0),(value['prep']//5,1)],[(value['cook']//5,2),(value['cook']//5,3)]])
    return jobs

jobs_list=getJobs(attrs)

 
class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def on_solution_callback(self):
        """Called at each new solution."""
        print('Solution %i, time = %f s, objective = %i' %
              (self.__solution_count, self.WallTime(), self.ObjectiveValue()))
        self.__solution_count += 1


def fastest_food(jobs):
    # Data part.
    

    num_jobs = len(jobs)
    all_jobs = range(num_jobs)

    num_machines = 4
    all_machines = range(num_machines)

    # Model the flexible jobshop problem.
    model = cp_model.CpModel()
    
    #total time of all the tasks at hand
    horizon = 0
    for job in jobs:
        for task in job:
            horizon+=task[0][0]
    print('Horizon = %i' % horizon)
   

    # Global storage of variables.
    intervals_per_resources = collections.defaultdict(list)
    starts = {}  # indexed by (job_id, task_id).
    presences = {}  # indexed by (job_id, task_id, alt_id).
    job_ends = []

    # Scan the jobs and create the relevant variables and intervals.
    for job_id in all_jobs:
        job = jobs[job_id]
        num_tasks = len(job)
        previous_end = None
        for task_id in range(num_tasks):
            task = job[task_id]

            min_duration = task[0][0]
            max_duration = task[0][0]
            #in our case min and max duration are the same 
            #because both stations are equally fast.
            
            num_alternatives = len(task)
            all_alternatives = range(num_alternatives)
            
        
            
            # Create main interval for the task.
            suffix_name = '_job%i_task%i' % (job_id, task_id)
            start = model.NewIntVar(0, horizon, 'start' + suffix_name)
            duration = model.NewIntVar(min_duration, max_duration,
                                        'duration' + suffix_name)
            
            #this interval is a workaround becuase the model
            #expects the times on the two alternative machines
            #to be distinct.
           
            end = model.NewIntVar(0, horizon, 'end' + suffix_name)
            interval = model.NewIntervalVar(start, duration, end,
                                            'interval' + suffix_name)

            # Store the start for the solution.
            starts[(job_id, task_id)] = start

            # Add precedence with previous task in the same job,
            # i.e. make sure the preparation(0) 
            # happens before cooking (1).
            if previous_end is not None:
                model.Add(start >= previous_end)
            previous_end = end

            #Create alternative intervals.
            if num_alternatives > 1:
                l_presences = []
                for alt_id in all_alternatives:
                    alt_suffix = '_j%i_t%i_a%i' % (job_id, task_id, alt_id)
                    l_presence = model.NewBoolVar('presence' + alt_suffix)
                    l_start = model.NewIntVar(0, horizon, 'start' + alt_suffix)
                    l_duration = task[alt_id][0]
                    l_end = model.NewIntVar(0, horizon, 'end' + alt_suffix)
                    l_interval = model.NewOptionalIntervalVar(
                        l_start, l_duration, l_end, l_presence,
                        'interval' + alt_suffix)
                    l_presences.append(l_presence)

                    # Link the master variables with the local ones.
                    model.Add(start == l_start).OnlyEnforceIf(l_presence)
                    model.Add(duration == l_duration).OnlyEnforceIf(l_presence)
                    model.Add(end == l_end).OnlyEnforceIf(l_presence)

                    # Add the local interval to the right machine.
                    intervals_per_resources[task[alt_id][1]].append(l_interval)

                    # Store the presences for the solution.
                    presences[(job_id, task_id, alt_id)] = l_presence

                # Select exactly one presence variable.
                # This adds a bounded linear expression to the model,
                # which is a bool in this case, and returns
                # an instance of a constraint class.
                model.Add(sum(l_presences) == 1)
                
            else:
                intervals_per_resources[task[0][1]].append(interval)
                presences[(job_id, task_id, 0)] = model.NewConstant(1)

        job_ends.append(previous_end)

    # Create machines constraints.
    for machine_id in all_machines:
        intervals = intervals_per_resources[machine_id]
        if len(intervals) > 1:
            model.AddNoOverlap(intervals)
  

    # make Makespan objective
    makespan = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(makespan, job_ends)
    model.Minimize(makespan)

    # Solve model.
    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter()
    status = solver.Solve(model, solution_printer)
    
    # using this for easier plotting later
    number_of_colors = len(jobs)
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

    

    plot_list=[]
    for machine_id in all_machines:
        if machine_id in [0,1]:
            print('Preparation station', machine_id)
        else:
            print('Cooking station', machine_id-2)
        for job_id in all_jobs:
            for task_id in range(2):
                start_value = solver.Value(starts[(job_id, task_id)])
                machine = -1
                duration = -1
                selected = -1
                for alt_id in range(2): 
                    if solver.Value(presences[(job_id, task_id, alt_id)]):
                        duration = jobs[job_id][task_id][alt_id][0]
                        machine = jobs[job_id][task_id][alt_id][1]
                        selected = alt_id
                if machine_id==machine:
                    #print('  Job_%i Task_%i starts at %i (duration %i)' %
                    #(job_id, task_id, start_value, duration))
                    plot_list.append(dict(Machine=machine, Job=job_id, Start=start_value, Finish=start_value+duration, Duration=duration, Color=color[job_id]))  
    
    #PRINT GANTT CHART
    df=pd.DataFrame(plot_list)
    proj_start = df.Start.min()
 
    # minutes from project start to task start
    df['start_num'] = (df.Start-proj_start)
    # minutes from project start to end of tasks
    df['end_num'] = (df.Finish-proj_start)
    # mins between start and end of each task
    df['mins_start_to_end'] =  (df.end_num - df.start_num)
    fig, ax = plt.subplots(1, figsize=(16,6))
    # bars
    ax.barh(df.Machine, df.mins_start_to_end, left=df.start_num, color=df.Color)
    xticks_minor = np.arange(0, df.end_num.max()+1, 1)
    yticks=[0,1,2,3]
    yticks_labels=['Prep1', 'Prep2', 'Cook1', 'Cook2']
    ax.set_yticks(yticks)
    ax.set_xticks(xticks_minor, minor=True)
    ax.set_yticklabels(yticks_labels)


    plt.show()
    
    #print sequences per machine ordered chronologically:
    prep1=list()
    prep2=list()
    cook1=list()
    cook2=list()
    
    for dic in plot_list:
        if dic['Machine']==0:
            prep1.append((dic['Job'] ,dic['Finish'])) #job_id, start, 
        if dic['Machine']==1:
             prep2.append((dic['Job'] ,dic['Finish'])) #job_id, start, 
        if dic['Machine']==2:
             cook1.append((dic['Job'] ,dic['Finish'])) #job_id, start, 
        if dic['Machine']==3:
            cook2.append((dic['Job'] ,dic['Finish'])) #job_id, start, 
    ordered_sequences=[prep1,prep2,cook1,cook2]
    for x in ordered_sequences:
        x.sort(key = lambda x: x[1])
        if x==prep1:
            print('Preparation station 1: ')
        if x==prep2:
            print('Preparation station 2: ')
        if x==cook1:
            print('Cooking station 1: ')
        if x==cook2:
             print('Cooking station 2: ')
        for element in x:
            print('\t Job {} finishing at time {}'.format(element[0],element[1]))
                
            
                

    print('Solve status: %s' % solver.StatusName(status))
    print('Optimal objective value: %i' % solver.ObjectiveValue())
    print('Statistics')
    #print('  - conflicts : %i' % solver.NumConflicts())
    print('  - branches  : %i' % solver.NumBranches())
    #number of branches explored in a binary search tree
    return time.time() - start_time


fastest_food(jobs_list)
print("--- %s seconds ---" % (time.time() - start_time))

#--------------TIME-------------
#generate datasets of various times and measure how well your model scales.

#dataset generator
# orders=[5,10,20,50,100,150,200, 350, 500] #500,1000,2000,5000,10000,50000,100000,1000000
# orders_and_times=list() #list of tupples w number of orders and times of execution
# for i in orders:
#     print('Currently obtaining time for the order',i)
#     dic=dict()
#     for j in range(i):
#         dic[j]={'kid':bool(random.getrandbits(42)), 'prep':random.randrange(5,60,5), 'cook':random.randrange(5,60,5)}
#     t=fastest_food(getJobs(dic))
#     orders_and_times.append((i,t))
# plt.plot(*zip(*orders_and_times))
# plt.show()
        
        

