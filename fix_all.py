import os

BASE = "Z:/Codes/Unterricht/Schuster/Stunde 9"

def fix_file(filepath, replacements):
    """Apply string replacements to a file."""
    path = os.path.join(BASE, filepath)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new, desc in replacements:
        if old in content:
            content = content.replace(old, new, 1)
            print(f"  FIXED: {desc}")
        else:
            print(f"  NOT FOUND: {desc}")
            # Try to find similar text
            import difflib
            lines = content.split('\n')
            for line in lines:
                if any(keyword in line.lower() for keyword in old.lower().split()[:3]):
                    print(f"    -> found similar line: {line.strip()[:100]}")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Fix gebaeude.py - Wohnhaus farbe indentation
print("=== gebaeude.py ===")
fix_file("gebaeude.py", [
    ("                                \"farbe\":   (180, 120, 200),   # Violett — Wohnungen für die Leute",
     "        \"farbe\":   (180, 120, 200),   # Violett — Wohnungen für die Leute",
     "Fix Wohnhaus farbe indentation + value"),
])

# 2. Fix ressourcen.py - Wohnhaus produktion
print("\n=== ressourcen.py ===")
fix_file("ressourcen.py", [
    ('"produktion": {"bevoelckerung": 1},                     # Produziert Bevölkrung',
     '"produktion": {"bevoelckerung": 2},                     # Produziert Bevölkrung',
     "Fix Wohnhaus produktion 1->2"),
])

# 3. Fix main.py - Bevoelkerung startwert
print("\n=== main.py ===")
fix_file("main.py", [
    ('"bevoelcheckerung": 10', '"bevoelckerung": 0', "Fix Bevölckungs-Startwert 10->0"),
])

# 4. Fix hud.py - Bevölckerung icon und text position
print("\n=== hud.py ===")
fix_file("hud.py", [
    ('"icon_pos": (500, 15),\n            "text_pos": (480, 12),',
     '"icon_pos": (480, 15),\n            "text_pos": (495, 12),',
     "Fix Bevölckerung icon/text position"),
])

print("\nDone!")
