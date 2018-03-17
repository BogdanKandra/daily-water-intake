"""
Created on Mon Nov 20 17:09:42 2017

@author: Bogdan Kandra

Soft Computing Project: Water Intake Calculator
------------------------------------------------
Fuzzy Control System which computes the recommended daily water intake,
taking into account four input variables: age, body-mass index, physical
activity and food type
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Input Variables
age = ctrl.Antecedent(np.arange(18, 66), 'age') # years
bmi = ctrl.Antecedent(np.arange(14, 40), 'bmi') # kg/m2
physical_activity = ctrl.Antecedent(np.arange(301), 'physical_activity') # minutes/week
food_type = ctrl.Antecedent(np.arange(4), 'food_type')  # singleton model

# Output Variable
water_amount = ctrl.Consequent(np.arange(5, 26), 'water_amount')  # 250ml cups/day

# Membership Functions
age['young']       = fuzz.trimf(age.universe, [18, 18, 42])
age['middle_aged'] = fuzz.trimf(age.universe, [18, 42, 65])
age['senior']      = fuzz.trimf(age.universe, [42, 65, 65])

bmi['underweight'] = fuzz.trapmf(bmi.universe, [8, 12, 16, 20])
bmi['normal']      = fuzz.trimf(bmi.universe, [18, 23, 28])
bmi['overweight']  = fuzz.trimf(bmi.universe, [23, 28, 33])
bmi['obese']       = fuzz.trapmf(bmi.universe, [28, 33, 38, 46])

physical_activity['low']       = fuzz.trapmf(physical_activity.universe, [-85, -30, 25, 80])
physical_activity['moderate']  = fuzz.trimf(physical_activity.universe, [25, 100, 175])
physical_activity['high']      = fuzz.trimf(physical_activity.universe, [100, 175, 250])
physical_activity['very_high'] = fuzz.trapmf(physical_activity.universe, [200, 250, 300, 350])

food_type['salty']   = fuzz.trimf(food_type.universe, [0, 0, 0])
food_type['sweet']   = fuzz.trimf(food_type.universe, [1, 1, 1])
food_type['fresh']   = fuzz.trimf(food_type.universe, [2, 2, 2])
food_type['neutral'] = fuzz.trimf(food_type.universe, [3, 3, 3])

water_amount['less']    = fuzz.trapmf(water_amount.universe, [0, 4, 6, 10])
water_amount['normal']  = fuzz.trimf(water_amount.universe, [6, 11, 16])
water_amount['more']    = fuzz.trimf(water_amount.universe, [12, 17, 22])
water_amount['extreme'] = fuzz.trapmf(water_amount.universe, [17, 22, 25, 30])

#age.view()
#bmi.view()
#physical_activity.view()
#food_type.view()
#water_amount.view()

# Define the Rules of Inference
# Automatically generate all possible rules
r_age = [2, 0, -2]
r_bmi = [-2, 0, 2, 4]
r_activity = [0, 2, 4, 8]
r_food_type = [-1.1, 1, -1, 0]

r_water_amount = ['less', 'normal', 'more', 'extreme']

rules = []
rules2 = []
rulesFinal = []

for a in r_age:
    for b in r_bmi:
        for c in r_activity:
            for d in r_food_type:
                rule = 'IF age IS ' + str(a) + ' AND bmi IS ' + str(b) + ' AND physical_activity IS ' + str(c) + ' AND food_type IS ' + str(d) + ' THEN water_amount IS '
                suma = a + b + c + d
                if suma < 10:
                    rule += 'less'
                    rules.append(rule)
                elif suma == 10:
                    rule += 'normal'
                    rules.append(rule)
                else:
                    if suma <= 13:
                        rule += 'more'
                        rules.append(rule)
                    else:
                        rule += 'extreme'
                        rules.append(rule)

for rule in rules:
    rule = (rule.replace('age IS 2', 'age IS young')
                .replace('age IS 0', 'age IS middle_aged')
                .replace('age IS -2', 'age IS senior')
                .replace('bmi IS -2', 'bmi IS underweight')
                .replace('bmi IS 0', 'bmi IS normal')
                .replace('bmi IS 2', 'bmi IS overweight')
                .replace('bmi IS 4', 'bmi IS obese')
                .replace('physical_activity IS 0', 'physical_activity IS low')
                .replace('physical_activity IS 2', 'physical_activity IS moderate')
                .replace('physical_activity IS 4', 'physical_activity IS high')
                .replace('physical_activity IS 8', 'physical_activity IS very_high')
                .replace('food_type IS -1.1', 'food_type IS salty')
                .replace('food_type IS 1', 'food_type IS sweet')
                .replace('food_type IS -1', 'food_type IS fresh')
                .replace('food_type IS 0', 'food_type IS neutral')
            )
    rules2.append(rule)
    
for rule in rules2:
    start   = rule.find('age IS ') + 7
    end     = rule.find(' AND bmi')
    ageTerm = rule[start:end]
    
    start   = rule.find('bmi IS ') + 7
    end     = rule.find(' AND physical_activity')
    bmiTerm = rule[start:end]
    
    start   = rule.find('physical_activity IS ') + 21
    end     = rule.find(' AND food_type')
    activityTerm = rule[start:end]
    
    start   = rule.find('food_type IS ') + 13
    end     = rule.find(' THEN')
    foodTerm= rule[start:end]
    
    start     = rule.find('water_amount IS ') + 16
    end       = len(rule)
    waterTerm = rule[start:end]
    
    newRule = ctrl.Rule(age[ageTerm] & bmi[bmiTerm] & physical_activity[activityTerm] & food_type[foodTerm], water_amount[waterTerm])
    rulesFinal.append(newRule)

# Set up the fuzzy control system
water_ctrl = ctrl.ControlSystem(rulesFinal)
water_consumption = ctrl.ControlSystemSimulation(water_ctrl)

# Pass inputs to the Fuzzy Control System
water_consumption.input['age'] = 50
water_consumption.input['bmi'] = 20
water_consumption.input['physical_activity'] = 30
water_consumption.input['food_type'] = 0

# Evaluate the system
water_consumption.compute()

# Print the output
print(water_consumption.output['water_amount'])
water_amount.view(sim=water_consumption)
