import xlrd

loc = ("vsi_dijaki.xlsx")

wb = xlrd.open_workbook(loc)

sheet = wb.sheet_by_index(0)


def vsiRazredi():
    return wb.sheet_names()


# Give the location of the file

def dijakiPoRazredu(razred):
    if razred == None:
        return
    dijaki = []

    sheet = wb.sheet_by_name(razred)
    for i in range(2, sheet.nrows):
        dijaki.append(sheet.cell_value(i, 1))
        print(sheet.cell_value(i, 1))
    return dijaki



def najdiRazred(prisotni):
    sum = 0
    max = 0
    indeks = 0
    for i, vr in enumerate(vsiRazredi()):

        dijaki = dijakiPoRazredu(vr)

        for p in prisotni:

            if p in dijaki:
                sum += 1

        print(sum)
        if (sum > max):
            max = sum
            indeks = i
        sum = 0
    print(indeks)

    return (vsiRazredi()[indeks])
