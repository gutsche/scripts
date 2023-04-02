#/usr/bin/env python3

from random import sample
import numpy as np

counts = np.zeros(6)
steps=0
while np.max(counts) > 9 or np.min(counts) < 9:
      steps=steps+1
      results = []

      for i in range(27):
         results.append(sample(['Andrey','Bo','Burt','Dave','Oli','Phil'],2))

      sorted_results = {}
      sorted_entries = {}

      # distribution of pairs
      for entry in results:
         entry.sort()
         entry_string = entry[0] + ' ' + entry[1]
         for item in range(2):
            if entry[item] not in sorted_entries.keys(): sorted_entries[entry[item]] = 0
            sorted_entries[entry[item]] += 1


      sorted_sorted_entries = {k: sorted_entries[k] for k in sorted(sorted_entries)}

      for ii, k in enumerate(sorted_sorted_entries):
          counts[ii] = sorted_sorted_entries[k]
      print(sorted_sorted_entries)
      print(counts, np.sum(counts))
      #counts = np.zeros(6)+9
      print('total steps: ', steps)
print(results)
