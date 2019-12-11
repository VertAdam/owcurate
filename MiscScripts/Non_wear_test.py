# ====================================================================================================
# ==================== THIS SCRIPT WAS MADE TO TEST METHODS OF NON-WEAR ALGORITHMS ON REAL DATA
# ==================== DAVID DING
# ==================== NEUROSCIENCE BALANCE AND MOBILITY LAB
# ==================== UNIVERSITY OF WATERLOO
# ====================================================================================================
from Files.Converters import *
from Sensor.Sensor import *
import datetime
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
from matplotlib import style


# INITIALIZATION
register_matplotlib_converters()
LW = Sensor()
RW = Sensor()
LA = Sensor()
RA = Sensor()

subject_ID = input()
trial_num = input()

print(" ======================================== READING FILES ========================================")
EDFToSensor(LA, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_%s_%s_GA_LAnkle_Accelerometer.EDF"
            % (subject_ID, trial_num), "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_%s_%s_GA_LAnkle_Temperature.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_%s_%s_GA_LAnkle_Light.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_%s_%s_GA_LAnkle_Button.EDF"
            % (subject_ID, trial_num))

EDFToSensor(RA, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_%s_%s_GA_RAnkle_Accelerometer.EDF"
            % (subject_ID, trial_num), "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_%s_%s_GA_RAnkle_Temperature.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_%s_%s_GA_RAnkle_Light.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_%s_%s_GA_RAnkle_Button.EDF"
            % (subject_ID, trial_num))

EDFToSensor(LW, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_%s_%s_GA_LWrist_Accelerometer.EDF"
            % (subject_ID, trial_num), "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_%s_%s_GA_LWrist_Temperature.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_%s_%s_GA_LWrist_Light.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_%s_%s_GA_LWrist_Button.EDF"
            % (subject_ID, trial_num))

EDFToSensor(RW, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_%s_%s_GA_RWrist_Accelerometer.EDF"
            % (subject_ID, trial_num), "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_%s_%s_GA_RWrist_Temperature.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_%s_%s_GA_RWrist_Light.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_%s_%s_GA_RWrist_Button.EDF"
            % (subject_ID, trial_num))

print(" ======================================== GENERATING TIMES ========================================")
LA_TIMES = LA.generate_times(LA.accelerometer.frequency, len(LA.accelerometer.x))
RA_TIMES = RA.generate_times(RA.accelerometer.frequency, len(RA.accelerometer.x))
LW_TIMES = LW.generate_times(LW.accelerometer.frequency, len(LW.accelerometer.x))
RW_TIMES = RW.generate_times(RW.accelerometer.frequency, len(RW.accelerometer.x))

print(" ======================================== CALCULATING SVMS ======================================== ")
LA.accelerometer.calculate_svms()
LW.accelerometer.calculate_svms()
RA.accelerometer.calculate_svms()
RW.accelerometer.calculate_svms()

print(" ======================================== LEFT WRIST NONWEAR ========================================")
LW.VanHeesNonWear()
LW.Check_Temperature()

print(" ======================================== RIGHT WRIST NONWEAR ========================================")
RW.VanHeesNonWear()
RW.Check_Temperature()

print(" ======================================== LEFT ANKLE NONWEAR ========================================")
LA.VanHeesNonWear()
LA.Check_Temperature()

print(" ======================================== RIGHT ANKLE NONWEAR ========================================")
RA.VanHeesNonWear()
RA.Check_Temperature()

print(" ======================================== DONE ========================================")


sns.set()
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
ax1.plot(LW_TIMES[::2], LW.accelerometer.svms[::2])
ax2.plot(RW_TIMES[::2], RW.accelerometer.svms[::2])

ax3.plot(LA_TIMES[::2], LA.accelerometer.svms[::2])
ax4.plot(RA_TIMES[::2], RA.accelerometer.svms[::2])


for i in LW.non_wear_starts:
    ax1.axvline(LW_TIMES[i], color='black')
for i in LW.non_wear_ends:
    ax1.axvline(LW_TIMES[i], color='red')

for i in RW.non_wear_starts:
    ax2.axvline(RW_TIMES[i], color='black')
for i in RW.non_wear_ends:
    ax2.axvline(RW_TIMES[i], color='red')

for i in LA.non_wear_starts:
    ax3.axvline(LA_TIMES[i], color='black')
for i in LA.non_wear_ends:
    ax3.axvline(LA_TIMES[i], color='red')

for i in RA.non_wear_starts:
    ax4.axvline(RA_TIMES[i], color='black')
for i in RA.non_wear_ends:
    ax4.axvline(RA_TIMES[i], color='red')


ax1.set_title("Left Wrist")
ax2.set_title("Right Wrist")
ax3.set_title("Left Ankle")
ax4.set_title("Right Wrist")

fig.autofmt_xdate()
fig.tight_layout()





