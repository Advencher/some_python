import os
import csv
import sys
from os.path import join, normpath
import pandas as pd  

class DatasetImporter:

    wav_numbergb = 0
    
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        wav_numbergb = self.countWavs()

    def alterCSV (self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".csv"):
                    print(os.path.join(root, file))
                    #swap colums
                    dataFrame = pd.read_csv(file, names = ['wav_filename', 'transcript', 'wav_filesize'])
                    dataFrame = dataFrame.reindex(['wav_filename',  'wav_filesize', 'transcript'], axis="columns")

                    #reorganize csv for deeeeeeeeeeep speeeech
                    # for i, row in dataFrame.iterrows():

                    #         #CHANGE PATH TO DATASET
                    #         tmp_split = row['wav_filename'].split('/')
                    #         tmp_split.pop(0)
                    #         row['wav_filename'] = "/".join(tmp_split)
                    #         row['wav_filesize'] = os.path.getsize(row['wav_filename'])

                    #         #CHANGE PATH TO DATASET
                    #         tmp_split = row['transcript'].split('/')
                    #         tmp_split.pop(0)
                    #         row['transcript'] = "/".join(tmp_split)
                    #         with open(row['transcript'], 'r') as transcript_file:
                    #             row['transcript'] = transcript_file.read() 

                    #         print(row)
                    #         exit("end of test\n")
                    
                    dataFrame.to_csv(file, index=False)
                    #ctrl + K + C/U1
                            


    def countWavs (self):
        wav_number = 0
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".wav"):
                    wav_number += 1
        return wav_number


    def separateBetweenDirectories (self):        
        
        proccessed = 1
        train = self.path + "/train"
        dev = self.path + "/dev"
        test = self.path + "/test"

        if not (os.path.isdir(train) and os.path.isdir(dev) and os.path.isdir(test)):
            os.mkdir(train)
            os.mkdir(dev)
            os.mkdir(test)

        
        file_train = open(train + "train.csv", "w+")
        file_dev = open(dev + "dev.csv", "w+")
        file_test = open(test + "test.csv", "w+")

        if os.path.isfile(test + "proccessed_mem.txt"):
            with open(test + "proccessed_mem.txt", "r") as f:
                proccessed = int(f.read())
        
        writer_train = csv.writer(file_train, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer_dev = csv.writer(file_dev, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(file_test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer_train.writerow(['wav_filename', 'wav_filesize', 'transcript'])
        writer_dev.writerow(['wav_filename', 'wav_filesize', 'transcript'])
        writer_test.writerow(['wav_filename', 'wav_filesize', 'transcript'])        

        #separate with rate 70-20-10 percent train, dev, test
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".csv"):
                    data = csv.reader(file, delimeter = ',')
                    for row in data:
                        if row == ['wav_filename', 'wav_filesize', 'transcript']:
                            continue
                        if proccessed <= wav_numbergb * 0.7:
                            writer_train.writerow(row)
                            proccessed += 1
                        elif proccessed <= wav_numbergb * 0.9:
                            writer_dev.writerow(row)
                            proccessed += 1
                        else:
                            writer_test.writerow(row)
                            proccessed += 1

        file_mem = open(test + "proccessed_mem.txt", "w+")
        file_mem.truncate(0)
        file_mem.write(proccessed)

        file_train.close()
        file_dev.close()
        file_test.close()
        file_mem.close()

        def changeRelativePaths():
            file_train = open("/train/train.csv", "w+")
            file_dev = open("/dev/dev.csv", "w+")
            file_test = open("/test/test.csv", "w+")

            data = csv.reader(file_train, delimeter = ',')
            
        

        
                            


importer = DatasetImporter()
#importer.countWavs()
importer.alterCSV()
#importer.separateBetweenDirectories()






