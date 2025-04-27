import Pitcher as Pitcher
import Batter as Batter
import Team as Team
import display as display
import bases as bases
import time
import random
import collections as c

outcomes=[1,2,3,4]
runner1="1"
runner2="2"
runner3="3"
test_runner="test"
base_states = [
    [runner1, None, None],
    [None, runner1, None],
    [None, None, runner1],
    [runner1, runner2, None],
    [runner1, None, runner2],
    [None, runner1, runner2],
    [runner1, runner2, runner3]
]

def test_bases():
    for state in base_states:
        bases_state=bases.bases(state)
        print("\nstate : " + str(state))
        temp_counter=1
        for outcome in outcomes:

            print("outcome : " + str(outcome))
            temp_runner=test_runner + str(temp_counter)
            scored=bases_state.update_hit(outcome, temp_runner)
            print("runs : " + str(scored))
            temp_counter+=1

test_bases() #tested, works!


