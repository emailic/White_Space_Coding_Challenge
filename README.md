# White_Space_Coding_Challenge
Here you might find my solutions to the two problems from the coding challenge by the White Space Solutions. The original text of the exercises was adapted here for the sake of simplicity. The solution to the first exercise uses the MST algorithm for graphs and leverages on graph and edge attributes to satisfy the requirements of the task.Find the solution in the Clean_Roads.py. 
The solution to the second exercise was ultimately achieved with the cp_sat solver by Google's or.tools library. Before reaching the solution with the constraint programming approach, two other approaches were tested: Johnson's rule in the successful_sequencing_johnson.py and a sorting type of approach in the  distributing_parallel_machines.py.

More about the company: 
https://whitespace.energy/

The adapted text of the original exercises is the following:

Exercise 1:
The city has houses, shops, and single hospital– none of which are connected by roads. My assignment is to plan the roads. There are fast roads and slow roads. Fast roads connect shops to shops and shops to the hospital. Slow roads connect houses to houses and houses to shops. 
Write a program that takes as input:

-a set of H house coordinates (x,y)
-a set of S shop coordinates (x,y)
-hospital coordinates (x,y)

and returns:

-a list of planned slow roads
-a list of planned fast roads
-sum of lengths of all the slow roads
-sum of lengths of all the fast roads
-visualization of the solution

Rules the algorithm must follow: 
• you must be able to travel from any house to any other house
• you must be able to travel from any house to at least one shop
• you must be able to travel from any house to the hospital
• travel refers to traveling via fast or slow roads, possibly via other houses or malls 
• not all shops need to be connected Objective of the task: Plan the roads such that the total road cost is minimized, with the total cost given by a weighted sum of the fast and slow total lenghts, i.e cost= a * total_lenght(slow) +(1-a)* total_lenght(fast) with a element of [0,1].*

Exercise 2:
The task is to plan orders in time across two preparation and two cooking stations, given a list of orders coming in. Each order has a preparation time and a cooking time. The algorithm takes as input a list of orders of length N with their corresponding times (preparation and cooking), and it returns the sequence in which the orders must be prepared and cooked. You cannot prepare more than 2 orders at any given time. You cannot cook more than 2 orders at any given time. All orders must be prepared before they can be cooked. Orders do not need to be cooked straight after being prepared. Cooking times and preparation times are multiples of 5 minutes with a maximum duration of 1 hour (so the cooking/preparation time takes on values of 5,10,15,20...60 min). The objective is to plan the sequencing of orders such that the total time needed to deliver (prepare and cook) all orders is minimized.
