import re
import xlsxwriter


def extract_integer_from_string_or_return_zero(_str):
    integers = re.findall(r"\d+", _str)
    if len(integers) == 0:
        return 0
    else:
        return int(integers[0])

def export_xlsx(filepath, data):
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()

    for i in range(len(data)):
        for j in range(len(data[i])):
            worksheet.write(i, j, data[i][j])
    workbook.close()

def export_txt(filepath, data):
    file = open(filepath, "w")

    for i in range(len(data)):
        for j in range(len(data[i])):
            file.write(data[i][j] + "\t")
        file.write("\n")

    file.close()

