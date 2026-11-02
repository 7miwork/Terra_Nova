import difflib

lines = open(r'z:/Codes/Unterricht/Schuster/Fortgeschrittener Kurs/Terra_Nova/main.py', encoding='utf-8').read().splitlines()

# Erste Kopie: 304-957 (0-basiert: 303-956)
# Zweite Kopie: 958-1503 (0-basiert: 957-1502)
# Aber wir muessen die genauen Grenzen finden
# Erste Kopie beginnt bei Zeile 304 (Index 303), endet vor Zeile 958 (Index 957)
# Zweite Kopie beginnt bei Zeile 958 (Index 957), endet vor Zeile 1503 (Index 1502)

erste = lines[303:957]
zweite = lines[957:1503]

print(f'Erste Kopie: {len(erste)} Zeilen (304-957)')
print(f'Zweite Kopie: {len(zweite)} Zeilen (958-1503)')
print()

# Diff
diff = list(difflib.unified_diff(erste, zweite, fromfile='erste', tofile='zweite', lineterm=''))
# Zeige nur die ersten 100 Zeilen des Diffs
for line in diff[:100]:
    print(line)

if len(diff) > 100:
    print(f'\n... {len(diff)-100} weitere Zeilen')