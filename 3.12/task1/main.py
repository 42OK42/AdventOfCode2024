import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def find_and_multiply(content):
    # Regex für gültige mul(X,Y) Anweisungen
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.finditer(pattern, content)
    
    total_sum = 0
    for match in matches:
        x = int(match.group(1))
        y = int(match.group(2))
        total_sum += x * y
    
    return total_sum

def main():
    file_path = 'text.txt'
    content = read_file(file_path)
    result = find_and_multiply(content)
    print("Summe der gültigen Multiplikationen:", result)

if __name__ == "__main__":
    main()
