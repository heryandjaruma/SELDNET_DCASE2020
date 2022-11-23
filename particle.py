class Particle:
    def __init__(self, set_dataframe, set_sound_class, set_time_start, set_time_end, set_order_number, parent_audio_segments: list) -> None:
        pass

        self.dataframe = set_dataframe
        self.set_time_start_end(set_time_start, set_time_end)
        self.duration = self.time_end-self.time_start
        self.order_number = set_order_number
        self.sound_class = set_sound_class
        self.set_particle_dataframe()
        self.duration_dataframe = self.dataframe.shape[0]

        self.set_particle_audio_segments(parent_audio_segments)
    
    def set_time_start_end(self,set_time_start,set_time_end) -> None:
        '''Set time start and time end.'''

        self.time_start=set_time_start
        self.time_end=set_time_end
    
    def set_particle_dataframe(self) -> None:
        '''Set dataframe that belongs on particle's part.'''

        self.dataframe = self.dataframe.set_index('Frm')
        self.dataframe = self.dataframe.loc[self.time_start:self.time_end,:]
        self.dataframe = self.dataframe.reset_index()

    def set_particle_audio_segments(self, audio_segments: list) -> None:
        '''Set AudioSegment that belongs on particle's part.'''

        self.audio_segments = list()

        for item in audio_segments:
            self.audio_segments.append(item[self.time_start*100 : self.time_end*100])

            