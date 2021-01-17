import xlrd

def Readdata(excel):
    wb = xlrd.open_workbook(excel+".xlsx")
    output = []
    z = wb.nsheets
    for n in range(z):    
        sheet = wb.sheet_by_index(n)
        rows = sheet.nrows
        cols = sheet.ncols
        data_of_sheet = []
        for i in range(rows):
            data_of_row = []
            for j in range(cols):
                data_of_row.append(sheet.cell_value(i,j))
            data_of_sheet.append(data_of_row)
        output.append(data_of_sheet)
    return output
x = Readdata("datasheet")