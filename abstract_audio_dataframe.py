from abc import ABC
from dataclasses import dataclass
import numpy as np
import pandas as pd

from particle import Particle

@dataclass
class IAudioDataframe(ABC):

    origin: str = None
    audio_multi: np.array(np.float32) = None
    dataframe: pd.DataFrame = None

    def set_origin_details(self, tables: dict) -> None:
        '''Set origin details into Audio Object'''

        self.fold = tables[0]
        self.room = tables[1]
        self.mix = tables[2]
        self.ov = tables[3]
    
    def set_audio_segments(self, audio_segments: list) -> None:
        '''Set audio multi into individual AudioSegment.'''
        
        self.audio_segments = audio_segments
    
    def set_particles(self):
        '''Set particles to the audio segment.'''

        self.particles = list()

        self.count_particle = 0
        existed_class = set()

        first_row = self.dataframe.iloc[0]
        time_start = time_end = first_row['Frm']
        sound_class = first_row['Class']

        for i,row in self.dataframe.iterrows():
            if row['Class'] == sound_class:
                # ! if the row has the same class before, which mean the audio is still running, then continue to the next row
                time_end=row['Frm']
                continue
            else:
                # ! create the entity first
                particle=Particle(
                    self.dataframe,
                    sound_class,
                    time_start,
                    time_end,
                    self.count_particle,
                    self.audio_segments
                )

                # ! before append to the main list, check the availibility of the newly created entity on the existed_class
                if particle.sound_class not in existed_class:
                    self.particles.append(particle)
                    existed_class.add(particle.sound_class)
                    self.count_particle+=1
                time_start = time_end = row['Frm']
                sound_class = row['Class']
        
        # ! create the entity first
        particle=Particle(
            self.dataframe,
            sound_class,
            time_start,
            time_end,
            self.count_particle,
            self.audio_segments
        )

        # ! before append to the main list, check the availibility of the newly created entity on the existed_class
        if particle.sound_class not in existed_class:
            self.particles.append(particle)
            existed_class.add(particle.sound_class)
            self.count_particle+=1
        time_start = time_end = row['Frm']
        sound_class = row['Class']            
