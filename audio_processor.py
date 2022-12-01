from overlay_audio_dataframe import OverlayAudioDataframe
from separation_audio_dataframe import SeparationAudioDataframe 
from history import History
import numpy as np
import librosa
import soundfile as sf
from pydub.audio_segment import AudioSegment
import pandas as pd
from colorama import Fore
import os
import nussl

from goto import Goto
goto = Goto()

def process_audio_segments(audio_multis: list) -> list:
    '''Process audio multi into individual AudioSegment.
    Return list of AudioSegment object.'''


def explode_audio_multi(audio_dataframe: OverlayAudioDataframe) -> list:
    '''Explode audio_multi into separate wav audio.'''

    goto.subf('raw_dev','foa_dev')
    f,sr = librosa.load(audio_dataframe.origin+'.wav',sr=None,mono=False)

    audio_dataframe.audio_multi = f

    goto.subf('explode_dev')
    temp = list()
    for index,item in enumerate(f):

        name = audio_dataframe.origin+'_channel'+str(index+1)+'.wav'
        sf.write(name, item, sr, subtype='PCM_24')

        temp.append(AudioSegment.from_file(name))
    
    return temp

def process_origin_details(origin: str) -> dict:
    '''Process csv into its details'''

    ret = dict(list(enumerate(origin.split('_'))))

    return ret

def list_audio_dataframe() -> list:
    '''Read all wav/csv from raw_dev.
    Return list of AudioDataframe object.'''

    print('Listing AudioDataframes')

    goto.subf('raw_dev','foa_dev')
    wavs = os.listdir()

    goto.subf('raw_dev','metadata_dev')
    csvs = os.listdir()

    files = list()
    for w,c in zip(wavs, csvs):
        temp_dataframe = pd.read_csv(c, header=None)
        temp_dataframe.columns = ['Frm', 'Class', 'Track', 'Azmth', 'Elev']
        files.append(OverlayAudioDataframe(str(w[:-4]),w,temp_dataframe))

    return files
    
def rebrand_audio_dataframe(audio_dataframes: list) -> None:
    '''Rebrand list of AudioDataframe with more properties.'''

    print('Rebranding AudioDataframes')

    for item in audio_dataframes:
        tables = process_origin_details(item.origin)
        item.set_origin_details(tables)

        audio_segments = explode_audio_multi(item)
        item.set_audio_segments(audio_segments)

        item.set_particles()

def overlay_audio_dataframes(*object: OverlayAudioDataframe, subfolder_name: str, skip_export: bool = False) -> None:
    '''Overlay 2 OverlayAudioDataframe object.'''

    if skip_export:
        return

    history = pd.DataFrame()

    print('Now processing', Fore.LIGHTMAGENTA_EX, object[0].origin, Fore.WHITE , 'with', Fore.LIGHTMAGENTA_EX, object[1].origin, Fore.WHITE)
    print(f'There will be {object[0].count_particle*object[1].count_particle} possible combinations.\nStart processing...')
    print()

    increment = 1
    # p : particle
    for p1 in object[0].particles:

        original_dataframe = object[0].dataframe
        original_audio_segments = object[0].audio_segments

        increment_tunggal_cut = 1
        for p2 in object[1].particles:

            # notify the running process
            print(Fore.GREEN, f"Processing #{increment} AudioDataframe...", Fore.WHITE)
            print('\tCombining class', Fore.LIGHTYELLOW_EX, p1.sound_class, Fore.WHITE, 'with class', Fore.LIGHTYELLOW_EX, p2.sound_class,Fore.WHITE)

            p2_dataframe = p2.dataframe
            p2_audio_segments = p2.audio_segments

            # process audio into 3 parts
            original_dataframe = original_dataframe.set_index('Frm')
            initial_original_dataframe = original_dataframe.loc[:p1.time_start-1,:]
            main_original_dataframe = original_dataframe.loc[p1.time_start:p1.time_end,:]
            final_original_dataframe = original_dataframe.loc[p1.time_end+1:,:]

            main_original_dataframe = main_original_dataframe.reset_index()
            dataframe_combined = pd.DataFrame()
            dataframe_combined = pd.concat([initial_original_dataframe])

            dataframe1 = main_original_dataframe
            dataframe2 = p2_dataframe
            dataframe1['unique_id'] = np.arange(0, dataframe1.shape[0]*2,2)
            dataframe2['unique_id'] = np.arange(1, dataframe2.shape[0]*2,2)

            temp_audio_segments = list()

            TUNGGAL_CUT_BASE_NAME1 = str(object[0].fold) + '_' + str(object[0].room) + '_' + str(object[0].mix) + '_' + str(p1.sound_class) + '_%0d'%(increment_tunggal_cut)
            TUNGGAL_CUT_BASE_NAME2 = str(object[1].fold) + '_' + str(object[1].room) + '_' + str(object[1].mix) + '_' + str(p1.sound_class) + '_%0d'%(increment_tunggal_cut)
            
            if p1.duration < p2.duration:
                
                maximum_duration = p1.duration

                # ! entity df2 is longer, then df2 duration will be cut according to ae1 duration
                dataframe2['Frm'] = dataframe1['Frm']

                goto.subf('overlay_dev', subfolder_name,'cut_dev')
                for index,(item1, item2) in enumerate(zip(p1.audio_segments,p2_audio_segments)):

                    item2 = item2[:p1.duration*100]
                    temp_audio_segments.append(item2)

                    # wav tungal cut buat nussl
                    TUNGGAL_CUT_NAME1 = TUNGGAL_CUT_BASE_NAME1 + '_channel%d'%(index+1) + '.wav'
                    item2.export(TUNGGAL_CUT_NAME1)

                    # punya nya item 1
                    TUNGGAL_CUT_NAME2 = TUNGGAL_CUT_BASE_NAME2 + '_channel%d'%(index+1) + '.wav'
                    item1.export(TUNGGAL_CUT_NAME2)

            else:

                maximum_duration = p2.duration

                # ! entity df1 is longer, then df1 frame will be copied into df2 frame, but the duration will be cut to match df2
                dataframe2['Frm'] = dataframe1['Frm'].iloc[:p1.duration]

                goto.subf('overlay_dev', subfolder_name,'cut_dev')
                for index,(item1,item2) in enumerate(zip(p1.audio_segments,p2_audio_segments)):
                
                    temp_audio_segments.append(item2)

                    # wav tungal cut buat nussl
                    TUNGGAL_CUT_NAME2 = TUNGGAL_CUT_BASE_NAME2 + '_channel%d'%(index+1) + '.wav'
                    item2.export(TUNGGAL_CUT_NAME2)

                    # punya nya item 1
                    item1 = item1[:p2.duration*100]
                    TUNGGAL_CUT_NAME1 = TUNGGAL_CUT_BASE_NAME1 + '_channel%d'%(index+1) + '.wav'
                    item1.export(TUNGGAL_CUT_NAME1)
            
            new_dataframe = pd.concat([dataframe1,dataframe2])
            new_dataframe = new_dataframe.sort_values(by=['unique_id'])
            new_dataframe = new_dataframe.drop(columns='unique_id')

            new_dataframe = new_dataframe.dropna()
            new_dataframe['Frm'] = new_dataframe['Frm'].astype(int)
            new_dataframe = new_dataframe.set_index('Frm')

            dataframe_combined = pd.concat([dataframe_combined, new_dataframe])
            dataframe_combined = pd.concat([dataframe_combined, final_original_dataframe])

            original_dataframe = original_dataframe.reset_index()

            # name of overlay
            OVERLAY_BASE_NAME = '_'.join([str(object[0].fold), str(object[0].room), 'mix%03d'%increment, 'ov2'])

            # export csv
            CSV_NAME = OVERLAY_BASE_NAME + '.csv'
            goto.subf('overlay_dev', subfolder_name,'metadata_dev')
            dataframe_combined.to_csv(CSV_NAME, header=False)
            print('\tCSV exported: ', Fore.LIGHTMAGENTA_EX, CSV_NAME, Fore.WHITE)

            # export audio
            overlayed = None
            for index,(original,layer) in enumerate(zip(original_audio_segments,temp_audio_segments)):
                goto.subf('overlay_dev', subfolder_name,'mix_dev')
                overlayed = original.overlay(layer,position=p1.time_start*100)

                WAV_NAME_CHANNEL = OVERLAY_BASE_NAME + '_' + 'channel%d'%(index+1)  + '.wav'

                overlayed.export(WAV_NAME_CHANNEL)
                print('\tWAV exported: ', Fore.LIGHTBLUE_EX, WAV_NAME_CHANNEL, Fore.WHITE)

                # mix wav tunggal cut buat nussl
                goto.subf('overlay_dev', subfolder_name,'cutmerge_dev')
                WAV_NAME_MERGE_CUT = OVERLAY_BASE_NAME + '_cutmerge_' + 'channel%d'%(index+1) + '.wav'
                overlayed = overlayed[p1.time_start*100 : (p1.time_start+maximum_duration)*100]
                overlayed.export(WAV_NAME_MERGE_CUT)

            row_history = np.array([
                object[0].origin+'.wav',
                object[1].origin+'.wav',
                p1.sound_class,
                p2.sound_class,
                OVERLAY_BASE_NAME,
                TUNGGAL_CUT_BASE_NAME1,
                TUNGGAL_CUT_BASE_NAME2,
                OVERLAY_BASE_NAME + '_cutmerge'
            ])
            history_dataframe = pd.DataFrame(row_history.reshape(1,-1))
            history = pd.concat([history, history_dataframe])

            increment += 1
            increment_tunggal_cut += 1
    
    # EXPORT HISTORY
    history_name = object[0].origin + '_OVERLAY_' + object[1].origin + '.csv'
    goto.subf('overlay_dev', subfolder_name,'history_dev')
    history.to_csv(history_name,header=False,index=False)
    goto.bwardf(2)

    print('History exported', Fore.LIGHTMAGENTA_EX, history_name, Fore.WHITE)

def get_history_dataframe(subfolder_name: str) -> History:
    '''Convert history into History Object.'''

    print('Getting History')

    goto.subf('overlay_dev',subfolder_name,'history_dev')
    history = os.listdir()

    dataframe = pd.read_csv(history[0],header=None)   

    return History(dataframe=dataframe)

def separate_history(history: History, subfolder_name: str) -> None:
    '''Do Separation for each row in history dataframe.'''

    print('Separating AudioDataframe')

    temp = list()
    
    new_history = pd.DataFrame()

    for index,r in history.dataframe.iterrows():

        dataMix = list()
        dataMix_name = r[5]
        for i in range(1,5):
            cutmerge_path = goto.subf('overlay_dev',subfolder_name,'cutmerge_dev') + f'\{dataMix_name}_channel{i}.wav'
            dataMix.append(nussl.AudioSignal(cutmerge_path))

        for iteration,item_num in enumerate(range(5,7)):
            pass

        print(dataMix)
        input()

        

    # history.set_row_audio_dataframes(temp)