from datetime import date
import jsonlines

date_min = date.max
date_max = date.min
counter = 0

# Change DB filename to retrieve some information...
fileName = "retsinformation.jsonl"
file = jsonlines.open(fileName, 'r')
for line in file:
    date_tmp = date.fromisoformat(line['date_decision'])

    if date_tmp < date_min:
        date_min = date_tmp
    if date_tmp > date_max:
        date_max = date_tmp
    
    # print(line['date_decision'])
    counter = counter + 1
file.close()

print()
print("Date min = " + date_min.isoformat())
print("Date max = " + date_max.isoformat())
print("Nr. Articles = " + str(counter))