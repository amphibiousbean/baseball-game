GAME_SPEED=0
SIM_NUM=0
PRINT=False

"""
PITCH DATA INDEX
0 : Four-seam Fastball
1 : Sinker
2 : Cutter
3 : Slider
4 : Changeup
5 : Curveball
6 : Splitter
7 : Sweeper
8 : Slurve
9 : Knuckle-curve
"""
avg_velos=[94.26, 93.58, 89.49, 85.8, 86.36, 79.76, 86.73, 82.17, 81.3, 80.4]

velo_low_bound=[86.4,86.1,83.7,79.2,77.3,66.9,82.2,72.6,79.7,70]

velo_up_bound=[99.3, 97.6, 94.2, 90.7, 93.5, 86.7, 93.6, 88.1, 83.3, 86.7]

count_ratios = {  # alters probabilities based on current count
    (0, 0): 1.0,
    (1, 0): 1.05,
    (2, 0): 1.15,
    (3, 0): 1.0,
    (3, 1): 1.4,
    (3, 2): 0.9,
    (2, 2): 0.7,
    (1, 2): 0.6,
    (0, 2): 0.3
}

def update_speed(speed):
    GAME_SPEED=speed

def update_sim_num(num):
    SIM_NUM=num

def update_print(prt):
    PRINT=prt