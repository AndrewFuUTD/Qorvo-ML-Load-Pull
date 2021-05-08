# Filename:  mdfParser.py
# Date:      04/01/2021
# Author:    Rutvij Shah
# Email:     rutvij.shah@utdallas.edu
# Version:   1.3
# Copyright: 2021, All Rights Reserved
#
# Written for the senior design project, Load Pull Analysis Team.
#
# Description:
#   Parse load pull data from .mdf files
#   Current version accounts for different numbers of variables
#   but the names are hard coded, changing boolean conditions
#   within the elif statement checking 'VAR<>', can account for
#   other named variables.
#   Future versions should implement this as well as the spliting of
#   the gamma tuple to discrete gamma value columns.
#   Another addition can be reading in values of S1 through S3 in the header
#   and the value of Z_0.
#
#
#   Refer to the this documentation for information on mdf files generated by AWR Cadence
#   - https://awrcorp.com/download/faq/english/docs/users_guide/data_file_formats.html



import pandas as pd
import numpy as np
import pickle

# instructions: change fileName to the name of the mdf file to open,
# just the name without the extension

#The mdf file's name goes here
def readMDF(fileName):

    with open(fileName + "\\" + fileName + '.mdf', 'r') as inFile:

        mdfFile = inFile.readlines()
        skipWhile = 0
        numGammaSweeps = 0
        blockSize = 4
        blocksRead = 0
        dataList = []

        '''
        gammaX three tuple int => (iGammaL1, iGammaL2, iGammaL3)
            power int => (iPower)
                    harmonic int => harm
                    (a1R, a1I) two tuple float => a1 complex
                    (b1R, b1I) two tuple float => b1 complex
                    (a2R, a2I) two tuple float => a2 complex
                    (b2R, b2I) two tuple float => b2 complex
                    v1 float => V1
                    i1 float => I1
                    v2 float => V2
                    i2 float => I2


        Each gamma tuple has n power points and each power point has 3 harmonics
        Each gamma has 3n points
        '''

        #columnList = ['gammaTuple','power','harmonic','a1','b1','a2','b2','v1','i1','v2','i2']
        #df = pd.DataFrame(columns = columnList)
        dictList = []


        i = 0
        s = 0
        while i < len(mdfFile):
            if mdfFile[i].startswith('!'):
                i+=1
                continue
            elif mdfFile[i].startswith('BEGIN'):
                l1 = mdfFile[i].split()
                if l1[1].startswith('HEADER'):
                    i += 3
                    continue
                elif l1[1].startswith('ABWAVES'):
                    i += 5
                    continue
            elif mdfFile[i].startswith('VAR<>'):
                l1 = mdfFile[i].split()
                if l1[1].startswith('iPower'):
                    i+=1
                    continue
                elif l1[1].startswith('iGamma'):
                    i+=1
                    numGammaSweeps+=1
                    blockSize+=1
                    continue

            if mdfFile[i][0].isdigit():
                blocksRead = 0
                power = int(mdfFile[i])
                i+=1
                gammaX = tuple(int(mdfFile[i+k]) for k in range(numGammaSweeps))
                i+=numGammaSweeps
                for j in range (1, 4):
                    lineList = mdfFile[i].split()
                    lineList = list(map(float, lineList))
                    harm = lineList[0]
                    a1 = complex(lineList[1], lineList[2])
                    b1 = complex(lineList[3], lineList[4])
                    a2 = complex(lineList[5], lineList[6])
                    b2 = complex(lineList[7], lineList[8])
                    if j == 1:
                        v1, i1, v2, i2 = (lineList[x] for x in range(9, 13))
                    else:
                        v1, i1, v2, i2 = tuple(np.nan for i in range(4))
                    dictList.append({'gammaTuple': gammaX,
                    'power': power,
                    'harmonic': int(harm),
                    'a1': a1,
                    'b1': b1,
                    'a2': a2,
                    'b2': b2,
                    'V1': v1,
                    'I1': i1,
                    'V2': v2,
                    'I2': i2
                    })
                    i+=1
                blocksRead+=1
            i+=1

        df = pd.DataFrame.from_dict(dictList)
        df['Pin'] = 0.5*((abs(df['a1']**2) - abs(df['b1'])**2))
        df['Pout'] = 0.5*((abs(df['b2']**2) - abs(df['a2'])**2))
        df['Gain'] = df['Pout']/df['Pin']
        df['Pdc1'] = df['V1']*df['I1']
        df['Pdc2'] = df['V2']*df['I2']
        df['PAE'] = (df['Pout']-df['Pin'])/df['Pdc2']
        df['Load Gamma'] = df['a2']/df['b2']
        column_a1 = df["Load Gamma"]
        r = []
        jx = []
        for index, value in column_a1.iteritems():
            r.append(value.real)
            jx.append(value.imag)


        df['r'] = r
        df['x'] = jx

        #store the data frame as a pickled object that can be accessed by unpickling
        #this retains the type information as it was originally defined in the DF
        pickle.dump(df, open(fileName + "\\" + fileName + '.pick', 'wb'))
        #export the data as a csv for easier visulisation in excel
        df.to_csv(fileName + "\\" + fileName + '.csv')
