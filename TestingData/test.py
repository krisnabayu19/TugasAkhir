import csv

# with open('employee_birthday.txt') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
#             line_count += 1
#     print(f'Processed {line_count} lines.')


# myData = ['Good Morning', 'Good Evening', 'Good Afternoon'],['Good Morning', 'Good Evening', 'Good Afternoon'],
# myFile = open('csvexample3.csv', 'w')
# with myFile:
#    writer = csv.writer(myFile)
#    writer.writerows(myData)

# r = open("stopwordsfix.csv", "r")
# print(r.read())


# with open('csvfile.csv','wb') as file:
#     for line in text:
#         file.write(line)
#         file.write('\n')

# f = open('csvfile.csv','w')
# f.write('hi there\n') #Give your csv text here.
# ## Python will convert \n to os.linesep
# f.close()
