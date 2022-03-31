# White_Space_Coding_Challenge
Here you may find my solutions to the two problems adapted from the coding challenge  by the White Space Solutions. The original text of the exercises was adapted  for the sake of simplicity. The solution to the first exercise uses the MST algorithm for graphs and leverages on graph and edge attributes to satisfy the requirements of the task.Find the solution in the Clean_Roads.py. <br/>
The solution to the second exercise was ultimately achieved with the cp_sat solver by Google's or.tools library. Before reaching the solution with the constraint programming approach, two other approaches were tested: Johnson's rule in the successful_sequencing_johnson.py and a sorting type of approach in the  distributing_parallel_machines.py.<br/><br/>

More about the company: <br/>
https://whitespace.energy/<br/><br/>

The adapted text of the original exercises is the following:<br/><br/>

Exercise 1:<br/>
The city has houses, malls, and single center– none of which are connected by roads. The assignment is to plan the roads. There are fast roads and slow roads. Fast roads connect malls to malls and malls to the city center. Slow roads connect houses to houses and houses to malls. 
Write a program that takes as input:<br/><br/>

-a set of H house coordinates (x,y)<br/>
-a set of M mall coordinates (x,y)<br/>
-center coordinates (x,y)<br/><br/>

and returns:<br/><br/>

-a list of planned slow roads<br/>
-a list of planned fast roads<br/>
-sum of lengths of all the slow roads<br/>
-sum of lengths of all the fast roads<br/>
-visualization of the solution<br/><br/>

Rules the algorithm must follow: <br/>
• you must be able to travel from any house to any other house<br/>
• you must be able to travel from any house to at least one mall<br/>
• you must be able to travel from any house to the city center<br/>
• travel refers to traveling via fast or slow roads, possibly via other houses or malls <br/>
• not all shops need to be connected <br/>

Objective of the task: Plan the roads such that the total road cost is minimized, with the total cost given by a weighted sum of the fast and slow total lenghts, i.e cost= a * total_lenght(slow) +(1-a)* total_lenght(fast) with a element of [0,1].*<br/><br/>

Exercise 2:<br/>
The task is to plan orders in time across two preparation and two cooking stations, given a list of orders coming in. Each order has a preparation time and a cooking time. The algorithm takes as input a list of orders of length N with their corresponding times (preparation and cooking), and it returns the sequence in which the orders must be prepared and cooked. You cannot prepare more than 2 orders at any given time. You cannot cook more than 2 orders at any given time. All orders must be prepared before they can be cooked. Orders do not need to be cooked straight after being prepared. Cooking times and preparation times are multiples of 5 minutes with a maximum duration of 1 hour (so the cooking/preparation time takes on values of 5,10,15,20...60 min). The objective is to plan the sequencing of orders such that the total time needed to deliver (prepare and cook) all orders is minimized.
