# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:54:32 2023

@author: Li Chao
"""

import sys, os
sys.path.append(os.getcwd())

from Agri_Encoder import Encoder_FullContentMaker
from Searcher_ModelTrainer import TransformerBlock

from glob import glob
from google.oauth2.service_account import Credentials
import numpy as np
import os
import pandas as pd
from pandas_gbq import to_gbq
import tensorflow.keras as keras
import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model
from transformers import TFBertModel

CPT_esg_trendency = '`quixotic-sol-387506.CPT_results.CPT_esg_trendency_agri_ESG06`'

def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    actual_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (actual_positives + K.epsilon())
    return recall

def ModelLoader(Model_Address):
    custom_objects = {
        'TFBertModel': TFBertModel,
        'TransformerBlock': TransformerBlock
    }
    try:
        model = load_model(Model_Address, custom_objects=custom_objects)
    except:
        with keras.utils.custom_object_scope({'precision': precision, 'recall': recall}):
            model = keras.models.load_model(Model_Address, custom_objects=custom_objects)
    return model


if __name__ == '__main__':
    Begin_Point = 1
    End_Point = -1
    Seq_Length = 60
    Model_Version = '0.1.1'
    
    print(f"Analyses are running based on CPT with version {Model_Version}")
    model_i0 = ModelLoader("CPT_demo_2_378k_i0.h5")
    model_i1 = ModelLoader("CPT_demo_2_378k_i1.h5")
    model_i2 = ModelLoader("CPT_demo_2_378k_i2.h5")
    model_i3 = ModelLoader("CPT_demo_2_378k_i3.h5")
    model_i4 = ModelLoader("CPT_demo_2_378k_i4.h5")
    model_i5 = ModelLoader("CPT_demo_2_378k_i5.h5")
    model_i6 = ModelLoader("CPT_demo_2_378k_i6.h5")
    model_i7 = ModelLoader("CPT_demo_2_378k_i7.h5")
    model_i8 = ModelLoader("CPT_demo_2_378k_i8.h5")
    model_i9 = ModelLoader("CPT_demo_2_378k_i9.h5")
    model_i10 = ModelLoader("CPT_demo_2_378k_i10.h5")
    model_i11 = ModelLoader("CPT_demo_2_378k_i11.h5")
    model_i12 = ModelLoader("CPT_demo_2_378k_i12.h5")
    
    model_list = (model_i0, model_i1, model_i2, model_i3,
                  model_i4, model_i5, model_i6, model_i7,
                  model_i8, model_i9, model_i10, model_i11,
                  model_i12)

    
    file_list = glob("AnnualReport-10K/*.pdf")
    
    file_to_use_no_duplicate = []
    
    for file in file_list:
        if file[-5] != ')':
            file_to_use_no_duplicate.append(file)
    
    done_df = pd.read_csv('Data/ArgiDoneBigquery.csv')
    done_list = done_df['nake_name'].to_list()
    
    file_to_use = []
    for file in file_to_use_no_duplicate:
        if file not in done_list:
            file_to_use.append(file)
    
    file_to_use_sorted = sorted(file_to_use)[Begin_Point: End_Point]
    result_dict_list = []
    for i, single_file in enumerate(file_to_use_sorted):
        print(f'we are in {i+Begin_Point} file!')
        
        result_dict = {}
        result_dict['nake_name'] = single_file
        result_dict['version'] = Model_Version
        result_dict['Seq_Length'] = Seq_Length
        
        try:
            tokens = Encoder_FullContentMaker(single_file)
            result_dict['no_valid_file'] = False
                
            dataX = []
            for j in range(0, len(tokens) - Seq_Length-1 , 1):
                seq_in = tokens[j:j + Seq_Length]
                dataX.append(seq_in)
            result_dict['length'] = len(dataX)
            result_dict['model_i0_index'] = np.mean(model_list[0].predict(dataX)[:,1])
            result_dict['model_i1_index'] = np.mean(model_list[1].predict(dataX)[:,1])
            result_dict['model_i2_index'] = np.mean(model_list[2].predict(dataX)[:,1])
            result_dict['model_i3_index'] = np.mean(model_list[3].predict(dataX)[:,1])
            result_dict['model_i4_index'] = np.mean(model_list[4].predict(dataX)[:,1])
            result_dict['model_i5_index'] = np.mean(model_list[5].predict(dataX)[:,1])
            result_dict['model_i6_index'] = np.mean(model_list[6].predict(dataX)[:,1])
            result_dict['model_i7_index'] = np.mean(model_list[7].predict(dataX)[:,1])
            result_dict['model_i8_index'] = np.mean(model_list[8].predict(dataX)[:,1])
            result_dict['model_i9_index'] = np.mean(model_list[9].predict(dataX)[:,1])
            result_dict['model_i10_index'] = np.mean(model_list[10].predict(dataX)[:,1])
            result_dict['model_i11_index'] = np.mean(model_list[11].predict(dataX)[:,1])
            result_dict['model_i12_index'] = np.mean(model_list[12].predict(dataX)[:,1])
            dataX = None
            print(result_dict)
        except:
            result_dict['no_valid_file'] = True
            print(result_dict)
        
        df = pd.DataFrame([result_dict])
        credentials = Credentials.from_service_account_file('Key/BQ_key.json')
        to_gbq(df, destination_table = 'CPT_results.CPT_esg_trendency_agri_ESG06',
               project_id='quixotic-sol-387506', if_exists='append',
               credentials=credentials, progress_bar=False)
        
        print(f'\nwe are in {i+Begin_Point} file!')
        




