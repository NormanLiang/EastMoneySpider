import matplotlib.pyplot as plt
import sys
import csv

STOCK_DIR = 'stock'

#x = [1, 2, 3, 4]
#y = [1.2, 2.4, 3.0, 5.8]

#plt.plot(x, y, color="r", linestyle="--", marker="*", linewidth=1.0)

#plt.show()
ZHEN_FU_LIST = []

def openfile(code):

    try:
        f = open(STOCK_DIR+'/'+code+'.csv', 'r')
        f_csv = csv.reader(f)
    except Exception as e:
        print(e)

    return f, f_csv

def closefile(file):
    file.close()

def readzhenfu(f_csv):
    title = next(f_csv)

    for row in f_csv:
        ZHEN_FU_LIST.append(row)

def main(code):
    f, f_csv = openfile(code)
    readzhenfu(f_csv)

    closefile(f)




if __name__ == "__main__":
#    if len(sys.argv) == 2:
#        main(sys.argv[1])
#    else:
#        print('give a code...')
    main('300082')
     