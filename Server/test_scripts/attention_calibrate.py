import uuid
import time
import matplotlib
import matplotlib.pyplot as plt
import random
from pylsl import StreamInfo, StreamOutlet

warmup_trials = 10
trials_per_class = 60
perform_time = 45  #5 second delay, 40 second window of relevance
wait_time = 5
pause_every = 30
pause_duration = 10
fontsize = 30
labels = ['Now Focus', 'Now Distract']
markers = ['focus', 'distract']

matplotlib.rcParams.update({'font.size': fontsize})


info = StreamInfo(name='MotorImag-Markers', type='Markers', channel_count=1,
                  nominal_srate=0, channel_format='string',
                  source_id='t8u43t98u')
outlet = StreamOutlet(info)


x=raw_input("Press [Enter] to begin")

hFigure, ax = plt.subplots()
ax.set_yticklabels([''])
ax.set_xticklabels([''])
t = plt.text(0.5, 0.5, '', horizontalalignment='center')
plt.xlim(xmin=0, xmax=1)
plt.ylim(ymin=0, ymax=1)
plt.ion()
plt.draw()
plt.show()
try:
    for trial in range(1, warmup_trials+trials_per_class*len(labels)+1):
        if not plt.fignum_exists(hFigure.number):
            break
        choice = random.choice(range(len(labels)))
        t.set_text(labels[choice])
        if trial == warmup_trials:
            outlet.push_sample(['calib-begin'])
        if trial > warmup_trials:
            outlet.push_sample([markers[choice]])
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
        time.sleep(perform_time)
        t.set_text('')
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
        time.sleep(wait_time)
        if trial % pause_every == 0:
            t.set_text('Pause')
            hFigure.canvas.draw()
            hFigure.canvas.flush_events()
            time.sleep(pause_duration)
            t.set_text('')
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
except Exception as e:
    print(e)
outlet.push_sample(['calib-end'])