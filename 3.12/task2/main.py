import re
import os

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        if not content:
            print(f"Warnung: Die Datei {file_path} ist leer!")
        return content
    except FileNotFoundError:
        print(f"Fehler: Die Datei {file_path} wurde nicht gefunden!")
        return ""

def find_do(content, position):
    pattern = r"do\(\)"
    if re.match(pattern, content[position:]):
        return True
    return False

def find_dont(content, position):
    pattern = r"don't\(\)"
    # Prüfe, ob an der Position "don't()" beginnt
    if re.match(pattern, content[position:]):
        return True
    return False

def find_multiply(content, position):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    match = re.match(pattern, content[position:])
    if match:
        print(f"Gefunden: {match.group(0)}")  # Debug-Ausgabe
        return True
    return False

def multiply_and_add(content, position, sum):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    match = re.match(pattern, content[position:])
    
    if match:
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        sum += num1 * num2
        position += len(match.group(0))
    
    return sum, position

def main():
    file_path = 'text.txt'  # Einfach nur der Dateiname, da sie im gleichen Verzeichnis liegt
    content = read_file(file_path)
    
    if not content:
        return
        
    print("Länge des gelesenen Inhalts:", len(content))
    print("Erste 50 Zeichen:", content[:50])
    
    i = 0
    sum = 0
    length = len(content)
    while i < length:
        while not find_dont(content, i) and i < length:
            if find_multiply(content, i):
                sum, i = multiply_and_add(content, i, sum)
            else:
                i += 1
        while not find_do(content, i) and i < length:
            i += 1
    print("Summe der gültigen Multiplikationen:", sum)

if __name__ == "__main__":
    main()
