
## RUNNING code from Medlit main page calls parser_final .py and shyts off ipnb output!
import os
import numpy as np
import pandas as pd
import glob as glob
path = os.getcwd()


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


def SplitFl(path): 
    #specify the path to the chunk folders#
    # take output from parser_final.py and split it into files for ingestion by neo4J
    '''point to the folder with the files in it 
    Use example
    path='/Users/GunnarK/Dropbox/coderepos/MedLit/O-ZPubmedExtract4_15_16'
    SplitFl(path)
    '''
    print 'make sure this is in the directory with the chunks'

    os.chdir(path)
    fileLs=glob.glob("ch*")

    for n in range(len(fileLs)):
        fileCurr=pd.read_csv(fileLs[n], error_bad_lines=False, header=None, names=['Author', 'Title','PMID','Journal','Year'])
        fileCurr.drop_duplicates(['Author', 'PMID'], inplace=True)
        links=pd.concat([fileCurr['Author'], fileCurr['PMID']], axis=1)
        appendDFToCSV_void(links, 'links.csv')


        Authors=pd.concat([fileCurr['Author']], axis=1)
        Authors.drop_duplicates(['Author'],inplace = True)
        appendDFToCSV_void(Authors, 'Authors.csv')

        Papers=pd.concat([fileCurr['PMID'],fileCurr['Title'],fileCurr['Journal'],fileCurr['Year']], axis=1)
        Papers2=Papers.drop_duplicates(['PMID'], take_last=True) # trouble deduping on PMID
        appendDFToCSV_void(Papers2, 'Papers.csv')
        
        print 'done with' + str(n+1) + 'of' + str(len(fileLs))

SplitFl(path)
    