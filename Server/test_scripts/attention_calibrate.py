import uuid
import time
import random
from pylsl import StreamInfo, StreamOutlet

warmup_trials = 3
trials_per_class = 5
perform_time = 2  #5 second delay, 40 second window of relevance
wait_time = 1
pause_every = 30
pause_duration = 1
fontsize = 30
labels = ['Now Focus', 'Now Distract']
markers = ['focus', 'distract']


info = StreamInfo(name='Focus-Markers', type='Markers', channel_count=1,
                  nominal_srate=0, channel_format='string',
                  source_id='t8u43t98u')
outlet = StreamOutlet(info)
x=input("Press [Enter] to begin")

try:
    for trial in range(1, warmup_trials+trials_per_class*len(labels)+1):
        choice = random.choice(range(len(labels)))
        print(labels[choice])
        if trial == warmup_trials:
            outlet.push_sample(['calib-begin'])
        if trial > warmup_trials:
            print("TEST")
            outlet.push_sample([markers[choice]])
        time.sleep(perform_time)
        print('pause')
        time.sleep(wait_time)
        if trial % pause_every == 0:
            time.sleep(pause_duration)
            print('pause')
except Exception as e:
    print(e)
outlet.push_sample(['calib-end'])