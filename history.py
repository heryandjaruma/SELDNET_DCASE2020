from dataclasses import dataclass
import pandas as pd

from separation_audio_dataframe import SeparationAudioDataframe

@dataclass
class History:
    dataframe: pd.DataFrame = None

    def set_row_audio_dataframes(self,set_row_audio_dataframes: list):
        self.row_audio_dataframes = set_row_audio_dataframes