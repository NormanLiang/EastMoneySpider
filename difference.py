import matplotlib.pyplot as plt
import sys
import csv
from datetime import datetime

STOCK_DIR = 'stock'

DIFFER_LIST = []
DATE_LIST = []
JIA_GE_ONE_LIST = []
JIA_GE_TWO_LIST = []

ZHEN_FU_INDEX = 7
DATE_INDEX = 0
JIA_GE_INDEX = 2

def openfile(code):

    try:
        f = open(STOCK_DIR+'/'+code+'.csv', 'r')
    except Exception as e:
        print(e)

    return f

def closefile(file):
    file.close()

def readdiff(csv_1, csv_2):
    try:
        next(csv_1)
        title_2 = next(csv_2)
        title_2 = next(csv_2)

        start = False
        for row in csv_1:
            date = row[DATE_INDEX]
        
            if date == title_2[DATE_INDEX]:
                start = True
            else:
                start = False
                while date > title_2[DATE_INDEX]:
                    title_2 = next(csv_2)
                if date == title_2[DATE_INDEX]:
                    start = True

            if start is True:
                DATE_LIST.append(date)
                JIA_GE_ONE_LIST.append(float(title_2[JIA_GE_INDEX]))
                JIA_GE_TWO_LIST.append(float(row[JIA_GE_INDEX]))
                differ = float(title_2[JIA_GE_INDEX])-float(row[JIA_GE_INDEX])
                DIFFER_LIST.append(differ)
                title_2 = next(csv_2)

    except Exception as e:
        print(e)

def drawTheDigram():
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in DATE_LIST]

    plt.plot(dates, JIA_GE_ONE_LIST, 'b', dates, JIA_GE_TWO_LIST, 'g')
    plt.xticks(rotation=20)

    plt.show()

def main(code1, code2):
    f_1 = openfile(code1)
    f_2 = openfile(code2)

    if len(f_1.readlines()) < len(f_2.readlines()):
        f_1, f_2 = f_2, f_1
        
    f_1.seek(0)
    f_2.seek(0)

    f_csv_1 = csv.reader(f_1)
    f_csv_2 = csv.reader(f_2)

    readdiff(f_csv_1, f_csv_2)
    drawTheDigram()

    closefile(f_1)
    closefile(f_2)




if __name__ == "__main__":
    main('601333', '300082')
#    if len(sys.argv) == 2:
#        main(sys.argv[1])
#    else:
#        print('give a code...')
#    main('601333')
     