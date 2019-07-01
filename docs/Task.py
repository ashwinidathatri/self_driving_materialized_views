#Task 1
Fill array of table names

#Task 2
Fill array of queries

#Task 3
Go to the picking of the queries and make the logic to pick them not uniformly at random, but based on probabilities given in an array. Then, fihsgure out how to create a zipfian/biased distribution in this array.

#TASK 4
Decide on the LRU data structure

#TASK 5 
Replace the following 3 lines with a function CANDIDATE_PICKER that (you also need to sync this with self._next_observation()): 
if the queue is empty, picks a query (first randomly), enqueues the candidates from the query.. it also adds this query to the HISTORY
(not if and else, but if and then if) next, if your queue is not empty: picks a candidte from the queue and adds this to your observation space (the second row).
---------------------------------------------------------
sampled_action = self.action_space.sample()
temp = np.eye(N_JOIN_COMBINATIONS)
self.candidate=dummy_candidate = temp[np.random.choice(temp.shape[0], size=1)].squeeze()
--------------------------------------------------------

#TASK 6
Look at your candidate, in the observation space, and mark it as "used in the lru"

#Task 7
Time to let go of the random rewards... We're starting with some real ones.
def get_cost_of_episode(self):
  Intialize a totalRuntimeCounter=0
  Initialize an array to keep track of the views that you will create.
    Go through your history: 
      - every time you see a query: run it, get the time and add it to totalRuntimeCounter.
      - every time you see the request to create a MV, create it: get the time and add it to totalRuntimeCounter.
        - every time you see the request to delete a MV, delete it (dont get the time, for this, as it can be done asynchronously)
      - every time you see a view that is just seen (nothing is created), do nothing
    
    By the end, you should have a totalTime. Return 1000 over that as your reward for the episode. (this we will change, so I mark it with an asterisk (*)).
    Here remember to drop all the views that you created (by using the tracking array). Also delete the tracking array.

#Task 8
Meet with Gabriel, design tests, run them...he 
return random.randint(1, 100)

#TASK 9
Check if eviction is needed, and evict, based on the LRU.

#TASK 10
Mark MV as deleted in history, and also mark the new MV created. If no action is done, still mark the view as something seen.


#TASK 11
Double check that you delete your history, that the init and reset work fine.
self.history = { }

---------------------------------------------------------------------------------

#Task 12: Hawc: 

credit_tracker = {
  candidate: {
    query -> credit = runtime_after_MV_creation / runtime_before_MV_creation
  }
}

views_created = []
window = -10
total_runtime = 0
baseline = { query: time it will take without any MV }
runtime_baseline = sum of all runtimes in baseline
total_runtime += runtime_baseline

if MV is created:
  total_runtime += time_to_create_MV
  # Give credit to created MV


We need a dictionary data structure to track credit that has for each candidate a nested dictionary, that in turn goes from query to credit. 
We need to again track with an array the views that you to are creating.
Initialize your window  -10
We need a dictionary called baseline, which goes from query (identified by the position) to runtime previous to view creation (before view was created)
NOTE: In many cases queries will be need to be tracked by their position.
Go through your history:
  if window is > 0:
    - look at what is in history position window
    - if it is a query, 
      - then delete it from the baseline, and from the credit tracking.
    - if it is a candidate, do nothing.
    - every time you see a query: run it, get the time and add it to totalRuntimeCounter. put this to the baseline.
    - every time you see you see a MV that was either seen or created:
    - we will create it (if it does not exist), so:
      - add to totalRuntimeCounter, the time of creating it.
      - once we create it we need to give it credit, so, go through each item in baseline, and run the query now that the view was created. The division of the this new runtime, by what was in baseline for that query will go into the credit tracker as the entry for that candidate query pair.
            - put now into the baseline for that query the time that was your numerator in the previous line.
            - if the number of views in the credit tracker is greater than the limit
              - then we need to delete one: for this we go through the credit tracker and sum the credits for all views; we  delete the one  with the smallest credit. we also delete the view from the actual database.
          - if the view exists in the credit tracker
            - then you need to update its credit with all queries that it has no credit for within the window.
        - every time you see the request to delete a MV: do nothing
    - increase your window counter by 1
        - every time you see a view that is just seen (nothing is created), do nothing

    - (After going through the history) Delete the views that you created, according to the tracking array.
    - Finally, use 1000/the time that you got for Hawc for calculating the real reward= ((Us/Hawc) *100)
