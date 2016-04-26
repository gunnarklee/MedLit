

## RUNNING code from Medlit main page calls parser_final .py and shyts off ipnb output!
import os
import numpy as np
import pandas as pd
import glob as glob

# a more funcitonal appender - http://stackoverflow.com/questions/17134942/pandas-dataframe-output-end-of-csv
def appendDFToCSV_void(df, csvFilePath, sep=","):
    import os
    if not os.path.isfile(csvFilePath):
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep)
    elif len(df.columns) != len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns):
        raise Exception("Columns do not match!! Dataframe has " + str(len(df.columns)) + " columns. CSV file has " + str(len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns)) + " columns.")
    elif not (df.columns == pd.read_csv(csvFilePath, nrows=1, sep=sep).columns).all():
        raise Exception("Columns and column order of dataframe and csv file do not match!!")
    else:
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep, header=False)



def CombFl(path, searchSt='links'): 
    print 'INSTRUCTIONS: move all of the summary files into the same directory as this code and number them in series'

    '''Example:
    path='/Users/GunnarK/Dropbox/coderepos/MedLit/MasterFolder'
    CombFl(path, 'links')
    CombFl(path, 'Papers')
    CombFl(path, 'Authors')'''
    
    
    #specify the path to the chunk folders#
    # take output from parser_final.py and split it into files for ingestion by neo4J
    '''point to the folder (of folders) with the files in it '''
    
    os.chdir(path)
    fileLs=glob.glob(searchSt + '*')

    for n in range(len(fileLs)):
        #fileLs=glob.glob("*")
        
        fileCurr=pd.read_csv(fileLs[n], error_bad_lines=False, header=None, names=['Author', 'Title','PMID','Journal','Year'])
        fileCurr.drop_duplicates(inplace=True)
        #links=pd.concat([fileCurr['Author'], fileCurr['PMID']], axis=1)
        appendDFToCSV_void(fileCurr, searchSt + '.csv')

        print 'done with' + str(n+1) + 'of' + str(len(fileLs))

path = os.getcwd
CombFl(path, 'links')
CombFl(path, 'Papers')
CombFl(path, 'Authors')
