import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

"""
Instrukcja:
pip install scikit-fuzzy
pip install matplotlib

lub instalacja z pliku requirements.txt (pip install -r requirements.txt)

Autorzy: 

- Damian Brzoskowski (s18499), Rafał Sochacki (s20047)

Opis:
Program do symulowania mechanizmu otwierania okna na podstawie trzech zmiennych wejściowych: 
- temperatura wewnątrz pomieszczenia
- wilgotność wewnątrz pomieszczenia 
- temperatura na zewnątrz
Rezultatem tego jest informacja na ile stopni powinnismy uchylic okno:
- kąt uchylenia okna

"""

# Zakres danych dla wykresów generowanych przy uruchamianiu
temperature_outside = ctrl.Antecedent(np.arange(15, 31, 1), 'temperature_outside')
temperature_inside = ctrl.Antecedent(np.arange(18, 31, 1), 'temperature_inside')
humidity_inside = ctrl.Antecedent(np.arange(15, 55, 1), 'humidity_inside')
window_angle_position = ctrl.Consequent(np.arange(0, 31, 1), 'window_angle_position')

# Automatycznie przypisanie funkcji określających 3 stany (poor, average, good)
temperature_outside.automf(3)
temperature_inside.automf(3)
humidity_inside.automf(3)

window_angle_position['closed'] = fuzz.trimf(window_angle_position.universe, [0, 0, 0])
window_angle_position['tilted'] = fuzz.trimf(window_angle_position.universe, [0, 15, 15])
window_angle_position['wide_open'] = fuzz.trimf(window_angle_position.universe, [16, 31, 31])

# Reguły dla symulacji
rule1 = ctrl.Rule(temperature_inside['good'] & humidity_inside['good'] & temperature_outside['poor'],
                  window_angle_position['wide_open'])
rule2 = ctrl.Rule(temperature_inside['good'] & humidity_inside['poor'] & temperature_outside['average'],
                  window_angle_position['wide_open'])
rule3 = ctrl.Rule(temperature_inside['good'] & humidity_inside['poor'] & temperature_outside['poor'],
                  window_angle_position['wide_open'])
rule4 = ctrl.Rule(temperature_inside['good'] & humidity_inside['good'] & temperature_outside['average'],
                  window_angle_position['wide_open'])

rule5 = ctrl.Rule(temperature_inside['average'] & humidity_inside['average'] & temperature_outside['poor'],
                  window_angle_position['closed'])
rule6 = ctrl.Rule(temperature_inside['average'] & humidity_inside['average'] & temperature_outside['good'],
                  window_angle_position['closed'])
rule7 = ctrl.Rule(temperature_inside['poor'] & humidity_inside['average'] & temperature_outside['good'],
                  window_angle_position['closed'])
rule8 = ctrl.Rule(temperature_inside['poor'] & humidity_inside['average'] & temperature_outside['poor'],
                  window_angle_position['closed'])

rule9 = ctrl.Rule(temperature_inside['good'] & humidity_inside['average'] & temperature_outside['average'],
                  window_angle_position['tilted'])
rule10 = ctrl.Rule(temperature_inside['good'] & humidity_inside['average'] & temperature_outside['poor'],
                   window_angle_position['tilted'])
rule11 = ctrl.Rule(temperature_inside['good'] & humidity_inside['good'] & temperature_outside['average'],
                   window_angle_position['tilted'])
rule12 = ctrl.Rule(temperature_inside['good'] & humidity_inside['good'] & temperature_outside['poor'],
                   window_angle_position['tilted'])
rule13 = ctrl.Rule(temperature_inside['average'] & humidity_inside['good'] & temperature_outside['poor'],
                   window_angle_position['tilted'])
rule14 = ctrl.Rule(temperature_inside['average'] & humidity_inside['average'] & temperature_outside['average'],
                   window_angle_position['tilted'])
rule15 = ctrl.Rule(temperature_inside['average'] & humidity_inside['good'] & temperature_outside['average'],
                   window_angle_position['tilted'])
rule16 = ctrl.Rule(temperature_inside['poor'] & humidity_inside['good'] & temperature_outside['poor'],
                   window_angle_position['tilted'])
rule17 = ctrl.Rule(temperature_inside['poor'] & humidity_inside['good'] & temperature_outside['average'],
                   window_angle_position['tilted'])
rule18 = ctrl.Rule(temperature_inside['poor'] & humidity_inside['average'] & temperature_outside['average'],
                   window_angle_position['tilted'])
rule19 = ctrl.Rule(temperature_inside['poor'] & humidity_inside['average'] & temperature_outside['poor'],
                   window_angle_position['tilted'])
rule20 = ctrl.Rule(temperature_inside['good'] | humidity_inside['good'], window_angle_position['tilted'])

window_angle_positioning_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
                                                    rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17,
                                                    rule18, rule19, rule20])


window_angle_positioning = ctrl.ControlSystemSimulation(window_angle_positioning_ctrl)

window_angle_positioning.input['temperature_inside'] = 30
window_angle_positioning.input['temperature_outside'] = 26
window_angle_positioning.input['humidity_inside'] = 30

window_angle_positioning.compute()

print(window_angle_positioning.output['window_angle_position'])
window_angle_position.view(sim=window_angle_positioning)

plt.show()
