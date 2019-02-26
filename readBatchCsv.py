import glob
import pandas as pd
from pandas import ExcelWriter

path =r'C:\PyCharm\PycharmProjects\workingExcel\csvblock' # use your path
allFiles = glob.glob(path + "/*.csv")

list_ = []

for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)

frame = pd.concat(list_, axis = 0, ignore_index = True)

# print(frame)
writer = ExcelWriter(r'C:\PyCharm\PycharmProjects\workingExcel\csvblock\outputx.xlsx')
frame.to_excel(writer,'Sheet1')
writer.save()

