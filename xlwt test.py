import xlwt

sheets = 3
meeting_times = 10
days = ["","M","T","W","Th","F","S","Sn"]
wb = xlwt.Workbook()

for sheet in range(sheets):
    ws = wb.add_sheet("Sheet"+str(sheet))
    for row in range(meeting_times + 1):
        for col in range(8):
            if row == 0:
                ws.write(row, col, days[col])
                
wb.save('example.xls')