import xlwt
import xlrd
import copy

wbin = xlrd.open_workbook("template.xls")
template_sheet = wbin.sheet_by_index(0)
temp_arr =[]

rows = template_sheet.nrows
cols = template_sheet.ncols
            
for i in range(rows):
    temp_row=[]
    for j in range(cols):
        temp_row.append(template_sheet.cell_value(i, j))
    temp_arr.append(temp_row)
print(temp_arr)

testin = [['CS', 'MATH', 'R6', 'I3', 'MT4'], ['CS', 'PHYS', 'R4', 'I4', 'MT1'], ['CS', 'ELE', 'R5', 'I2', 'MT3'], ['CS', 'BBM', 'R1', 'I3', 'MT12'], ['CS', 'PHYS', 'R1', 'I4', 'MT20'], ['CS', 'BBM', 'R4', 'I8', 'MT5'], ['EE', 'MATH', 'R4', 'I3', 'MT15'], ['EE', 'PHYS', 'R2', 'I1', 'MT13'], ['EE', 'ELE', 'R7', 'I6', 'MT12'], ['EE', 'BBM', 'R2', 'I7', 'MT6'], ['EE', 'PHYS', 'R2', 'I5', 'MT11'], ['IE', 'MATH', 'R1', 'I7', 'MT6'], ['IE', 'PHYS', 'R6', 'I5', 'MT12'], ['IE', 'ELE', 'R2', 'I6', 'MT19'], ['IE', 'BBM', 'R3', 'I4', 'MT11'], ['ME', 'MATH', 'R4', 'I2', 'MT20'], ['ME', 'PHYS', 'R6', 'I1', 'MT5'], ['ME', 'ELE', 'R7', 'I2', 'MT19'], ['ME', 'BBM', 'R3', 'I3', 'MT10'], ['ME', 'PHYS', 'R1', 'I5', 'MT16']]


sheet = 0
last_data = testin[0][0]
temp_prog = copy.deepcopy(temp_arr)
arrlist =[]
temp_prog[0][0] = last_data


for i in testin:
    if last_data != i[0]:
        last_data = i[0]
        x = temp_prog.copy()
        arrlist.append(x)
        temp_prog = copy.deepcopy(temp_arr)
        temp_prog[0][0] = last_data

    for row in range(rows):
        for col in range(cols):
            if i[4] == temp_prog[row][col]:
                temp_prog[row][col] = i[1] + i[3]
arrlist.append(temp_prog)  

#writing to excell
wb = xlwt.Workbook()

for i in range(len(arrlist)):
    sheet = wb.add_sheet("sa"+str(i))
    for row in range(rows):
        for col in range(cols):
            if "MT" in arrlist[i][row][col] :
                arrlist[i][row][col] = "-"     
            sheet.write(row, col, arrlist[i][row][col])
                
wb.save('programs.xls')                
                
                
                
                