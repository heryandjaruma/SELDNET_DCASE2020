from audio_processor import *

import os

from goto import Goto
goto = Goto()

def init_essential_folders() -> None:
    '''Initialize all folders needed.'''

    try:
        os.mkdir('explode_dev')
    except:
        pass
    try:
        os.mkdir('overlay_dev')

    except:
        pass

def init_mapping_folders(mapping: list) -> None:
    '''Initialize mapping folders.'''

    for m in mapping:

        goto.subf('overlay_dev')

        temp = str(m[0]) + '_' + str(m[1])

        try:
            os.mkdir(temp)
        except:
            pass
        
        goto.subf('overlay_dev',temp)

        try:
            os.mkdir('history_dev')
        except:
            pass
        try:
            os.mkdir('metadata_dev')
        except:
            pass
        try:
            os.mkdir('mix_dev')
        except:
            pass

if __name__ == '__main__':
    mapping = [
        [1,2],
        [2,1],
        [3,1],
        [4,1],
        [5,1],
        [6,1]
    ]
    init_essential_folders()
    init_mapping_folders(mapping=mapping)

    # step1 -> initialize all dataframes object
    audio_dataframes = list_audio_dataframe()
    rebrand_audio_dataframe(audio_dataframes)

    # step2 -> OVERLAY 2 audio dataframes
    for m in mapping:
        overlay_audio_dataframes(audio_dataframes[m[0]-1], audio_dataframes[m[1]-1], subfolder_name=str(m[0]) + '_' + str(m[1]))
    
    # step3 -> SEPARATION

    