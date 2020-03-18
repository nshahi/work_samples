# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:58:03 2020

@author: ThinkPad
"""

class Contestant():
    def __init__(self,ID,cpty,a,b,ps):
        self.ID = ID
        self.cpty = cpty
        self.a = a
        self.b = b
        self.ps = ps
        self.diverse = int(str(ID)[4])
    def __repr__(self):
        return repr((self.ID,self.cpty,self.a,self.b,self.ps,self.diverse))

    
def cal_power(team,which_team):
    power = 0
    if which_team == 'a':
        for i in range(len(team)):
            power += float(team[i].cpty * team[i].a)
    else:
        for i in range(len(team)):
            power += float(team[i].cpty * team[i].b)

    diversity_ids = []
    for i in team:
        diversity_ids.append(i.diverse)
    if(len(diversity_ids) == len(set(diversity_ids))):
        power += 120.0
        
    return(float(power))
    
def setup():
    file = open("input.txt", "r")
    search_type = None
    up_contestants = []
    team_a = []
    team_b = []
    lines = file.readlines()
    for line_num, line in enumerate(lines):
    
        if (line_num == 0):
            tot_contestants = int(line)

        elif(line_num == 1):
            search_type = line.rstrip()
            
        else:
            info = line.split(",")
            curr_c = Contestant(int(info[0]),float(info[1]),float(info[2]),float(info[3]),float(info[4]))
            if (curr_c.ps == 1):
                team_a.append(curr_c)
            elif (curr_c.ps == 2):
                team_b.append(curr_c)
            else:
                up_contestants.append(curr_c)
            
    
    return(up_contestants, team_a, team_b, tot_contestants, search_type)


#MINIMAX Algorithm
def max_value(remaining_ppl,team_a,team_b,depth):
    if (depth == 0):
        adv = float((cal_power(team_a, 'a') - cal_power(team_b, 'b')))
        return(adv)
    
    v = -float("inf")
    
    for i in range(len(remaining_ppl)):
        
        new_a = team_a.copy()
        curr_b = team_b.copy()
        
        curr_selection = remaining_ppl[i]
        next_state = remaining_ppl.copy()
        next_state.remove(curr_selection)
        new_a.append(curr_selection)
        
        ev = min_value(next_state,new_a,curr_b,depth-1)
        v = max(v,ev)

    return v

def min_value(remaining_ppl,team_a,team_b,depth):
    if (depth == 0):
        adv = (cal_power(team_a, 'a') - cal_power(team_b, 'b'))
        return(adv)
    
    v = float("inf")
    
    for i in range(len(remaining_ppl)):
        
        new_b = team_b.copy()
        curr_a = team_a.copy()
        
        curr_selection = remaining_ppl[i]
        next_state = remaining_ppl.copy()
        next_state.remove(curr_selection)
        new_b.append(curr_selection)
        
        ev = max_value(next_state,curr_a,new_b,depth-1)
        v = min(v,ev)
    
    return v

def minimax(remaining_ppl,team_a,team_b,depth):
    tmp = -float("inf")
    best_choice = None
    
    for i, person in enumerate(remaining_ppl):
        next_state = remaining_ppl.copy()
        new_a = team_a.copy()
        curr_b = team_b.copy()
        
        new_a.append(person)
        next_state.remove(person)

        max_a = min_value(next_state,new_a,curr_b,depth-1)
  
        if (max_a > tmp):
            tmp = max_a
            best_choice = i
    
    return(best_choice)

#Alpa Beta Algorithm
def max_value_ab(remaining_ppl,team_a,team_b,depth,alpha,beta):
    if (depth == 0):
        adv = float((cal_power(team_a, 'a') - cal_power(team_b, 'b')))
        return(adv)
    
    v = -float("inf")
       
    for i in range(len(remaining_ppl)):
        
        new_a = team_a.copy()
        curr_b = team_b.copy()
        
        curr_selection = remaining_ppl[i]
        next_state = remaining_ppl.copy()
        next_state.remove(curr_selection)
        new_a.append(curr_selection)
        
        ev = min_value_ab(next_state,new_a,curr_b,depth-1,alpha,beta)
        v = max(v,ev)
        alpha = max(alpha,v)
        if beta <= alpha:
            break

    return v

def min_value_ab(remaining_ppl,team_a,team_b,depth,alpha,beta):
    if (depth == 0):
        adv = (cal_power(team_a, 'a') - cal_power(team_b, 'b'))
        return(adv)
    
    v = float("inf")
    
    for i in range(len(remaining_ppl)):
        
        new_b = team_b.copy()
        curr_a = team_a.copy()
        
        curr_selection = remaining_ppl[i]
        next_state = remaining_ppl.copy()
        next_state.remove(curr_selection)
        new_b.append(curr_selection)
        
        ev = max_value_ab(next_state,curr_a,new_b,depth-1,alpha,beta)
        v = min(v,ev)
        beta = min(beta, v)
        if beta <= alpha:
            break
    
    return v

def alpha_beta(remaining_ppl,team_a,team_b,depth,alpha,beta):
    tmp = -float("inf")
    best_choice = None
    
    for i, person in enumerate(remaining_ppl):
        next_state = remaining_ppl.copy()
        new_a = team_a.copy()
        curr_b = team_b.copy()
        
        new_a.append(person)
        next_state.remove(person)

        max_a = min_value_ab(next_state,new_a,curr_b,depth-1,alpha,beta)
        
        if (max_a > tmp):
            tmp = max_a
            best_choice = i
    
    return(best_choice)

#Main Program

remaining_ppl, team_a, team_b, total_contestants, search_type = setup()
remaining_ppl = sorted(remaining_ppl,key=lambda Contestant: Contestant.ID)

if (search_type == "minimax"):
    depth = (5 - (len(team_a)))*2
    best_choice = minimax(remaining_ppl,team_a,team_b,depth)

if(search_type == 'ab'):
    depth = (5 - (len(team_a)))*2
    alpha = -float("inf")
    beta = float("inf")
    best_choice = alpha_beta(remaining_ppl,team_a,team_b,depth,alpha,beta)

f = open("output.txt", "w+")
f.write(str(remaining_ppl[best_choice].ID))
f.close()

    

