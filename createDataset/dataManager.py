import yaml
import os
import pandas as pd
import sys


if __name__  == "__main__":

    labelDict = {}
    sickDict = {}


    dataset = []

    for filename in os.listdir('./data/hospital/'):
        try:
            with open('./data/hospital/' + filename, 'r', encoding="utf-8") as f:
                label = filename.replace('.yml', '')
                labelDict[label] = []

                data = yaml.safe_load(f)

                for sick, sentenceList in data.items():
                    if (sick not in labelDict.get(label)):
                        labelDict[label].append(sick)

                    if (sickDict.get(sick) is None):
                        sickDict[sick] = []

                    for sentence in sentenceList:
                        if (sentence not in sickDict.get(sick)):
                            sickDict[sick].append(sentence)


        except Exception as e:
            print(e)
            ...



    for sick, sentenceList in sickDict.items():
        labelList = []
        # data = [[], '', '']
        for label, sickList in labelDict.items():
            if (sick in sickList and label not in labelList):
                labelList.append(label)
        

        for sentence in sentenceList:
            dataset.append([labelList, sick, sentence])


    df = pd.DataFrame(dataset, columns=['label', 'sick', 'content'])
    df.to_csv('./data/dataset/20230725_hospital.csv', encoding='utf8')  