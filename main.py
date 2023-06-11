import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Create fuzzy variables
temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
performa_ac = ctrl.Consequent(np.arange(0, 11, 1), 'performa_ac')

# Define membership functions for temperature
temperature['dingin'] = fuzz.trapmf(temperature.universe, [0, 0, 20, 25])
temperature['biasa'] = fuzz.trimf(temperature.universe, [20, 25, 30])
temperature['panas'] = fuzz.trapmf(temperature.universe, [29, 40, 50, 50])

# Define membership functions for cooling power
performa_ac['rendah'] = fuzz.trapmf(performa_ac.universe, [0, 0, 2, 5])
performa_ac['medium'] = fuzz.trimf(performa_ac.universe, [2, 5, 8])
performa_ac['tinggi'] = fuzz.trapmf(performa_ac.universe, [5, 8, 10, 10])

# Define fuzzy rules
aturan1 = ctrl.Rule(temperature['dingin'], performa_ac['tinggi'])
aturan2 = ctrl.Rule(temperature['biasa'], performa_ac['medium'])
aturan3 = ctrl.Rule(temperature['panas'], performa_ac['rendah'])

# Create fuzzy control system
control_system = ctrl.ControlSystem([aturan1, aturan2, aturan3])
aircon_controller = ctrl.ControlSystemSimulation(control_system)

# Set inputs and compute the output
while True:
    suhu = float(input('Suhu: '))
    if (suhu > 50 or suhu < 0):
        print('Suhu tidak tepat\n')
    else:
        break

aircon_controller.input['temperature'] = suhu
aircon_controller.compute()

# Print the output
print(aircon_controller.output['performa_ac'])
persen = aircon_controller.output['performa_ac'] / 10 * 100
print(f'Persentase power penggunaan AC: {round(persen)}%')

performa_ac.view(sim=aircon_controller)
plt.show()