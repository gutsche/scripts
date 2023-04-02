#/usr/bin/env python3

from random import sample

results = []

for i in range(27):
    results.append(sample(['Andrey','Bo','Burt','Dave','Oli','Phil'],2))

print("")
print("Pairs:")
print("")
for item in results:
    print('{};{}'.format(item[0],item[1]))
print("")

sorted_results = {}
sorted_entries = {}

# distribution of pairs
for entry in results:
    entry.sort()
    entry_string = entry[0] + ' ' + entry[1]
    for item in range(2):
        if entry[item] not in sorted_entries.keys(): sorted_entries[entry[item]] = 0
        sorted_entries[entry[item]] += 1
    if entry_string not in sorted_results.keys(): sorted_results[entry_string] = 0
    sorted_results[entry_string] += 1

sorted_sorted_results = {k: sorted_results[k] for k in sorted(sorted_results)}
print(sorted_sorted_results)

sorted_sorted_entries = {k: sorted_entries[k] for k in sorted(sorted_entries)}
print(sorted_sorted_entries)