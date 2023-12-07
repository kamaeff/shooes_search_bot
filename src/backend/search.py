import xlsxwriter
from _xlswrite import array
import os

def writer(param):
    print(param)
    folder = os.path.join("./src", "backend", "gen_imgs", "topbasket.xlsx")
    book = xlsxwriter.Workbook(folder)
    page = book.add_worksheet("товар")
    row = 0
    column = 0
    page.set_column("A:A", 20)
    page.set_column("B:B", 20)
    page.set_column("C:C", 50)
    page.set_column("D:D", 50)

    for item in param():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        page.write(row, column+2, item[2])
        row += 1
    book.close()


writer(array)    

