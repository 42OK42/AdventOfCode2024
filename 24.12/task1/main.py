def read_wire_values(file_path):
    wire_values = {}
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if ':' not in line:  
                    break
                    
                wire, value = line.strip().split(':')
                wire_values[wire.strip()] = int(value.strip())
                
        return wire_values
        
    except FileNotFoundError:
        print(f"Error: File {file_path} not found!")
        return {}

def read_gates(file_path):
    gates = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if ':' in line:
                    continue
                
                parts = line.strip().split()
                if len(parts) == 5 and parts[3] == '->':
                    gate_info = {
                        'wire1': parts[0],
                        'gate': parts[1],
                        'wire2': parts[2],
                        'result': parts[4]
                    }
                    gates.append(gate_info)
                
        return gates
        
    except FileNotFoundError:
        print(f"Error: Datei {file_path} nicht gefunden!")
        return []

def can_resolve_gate(gate, wire_values):
    wire1_exists = gate['wire1'] in wire_values
    wire2_exists = gate['wire2'] in wire_values
    
    return wire1_exists and wire2_exists

def resolve_and_gate(value1, value2):
    return 1 if value1 == 1 and value2 == 1 else 0

def resolve_or_gate(value1, value2):
    return 1 if value1 == 1 or value2 == 1 else 0

def resolve_xor_gate(value1, value2):
    return 1 if value1 != value2 else 0

def resolve_gate(gate, wire_values):
    if not can_resolve_gate(gate, wire_values):
        return None
        
    value1 = wire_values[gate['wire1']]
    value2 = wire_values[gate['wire2']]
    
    if gate['gate'] == 'AND':
        result = resolve_and_gate(value1, value2)
    elif gate['gate'] == 'OR':
        result = resolve_or_gate(value1, value2)
    elif gate['gate'] == 'XOR':
        result = resolve_xor_gate(value1, value2)
    else:
        print(f"Unbekannter Gate-Typ: {gate['gate']}")
        return None
        
    return result

def get_binary_from_z_wires(wire_values):
    z_wires = [wire for wire in wire_values.keys() if wire.startswith('z')]
    
    z_wires.sort(key=lambda x: int(x[1:]))
    
    print("\nZ-Wire Werte in Reihenfolge (LSB zuerst):")
    binary = ''
    for wire in z_wires:
        value = wire_values[wire]
        binary = str(value) + binary
        print(f"{wire}: {value}")
    
    print(f"\nKomplette Binärzahl: {binary}")
    decimal = int(binary, 2)
    print(f"Dezimalzahl: {decimal}")
    return binary, decimal

def main():
    file_path = "input.txt"
    wire_values = read_wire_values(file_path)
    gates = read_gates(file_path)
    
    print(f"Anzahl der Wires zu Beginn: {len(wire_values)}")
    print(f"Anzahl der Gates zu Beginn: {len(gates)}")
    
    prev_solved = -1
    current_solved = len(wire_values)
    
    while prev_solved != current_solved and gates:
        prev_solved = current_solved
        solved_gates = []
        
        for gate in gates:
            if can_resolve_gate(gate, wire_values):
                result = resolve_gate(gate, wire_values)
                if result is not None:
                    wire_values[gate['result']] = result
                    print(f"Gate gelöst: {gate['wire1']} {gate['gate']} {gate['wire2']} -> {gate['result']} = {result}")
                    solved_gates.append(gate)
        
        for gate in solved_gates:
            gates.remove(gate)
            
        current_solved = len(wire_values)
        print(f"Verbleibende Gates: {len(gates)}, Gelöste Wires: {current_solved}")
    
    if gates:
        print("\nUngelöste Gates:")
        for gate in gates:
            print(f"\nGate mit Result '{gate['result']}':")
            print(f"{gate['wire1']} {gate['gate']} {gate['wire2']} -> {gate['result']}")
            if gate['wire1'] in wire_values:
                print(f"  {gate['wire1']}: {wire_values[gate['wire1']]}")
            else:
                print(f"  Fehlender Input: {gate['wire1']}")
            if gate['wire2'] in wire_values:
                print(f"  {gate['wire2']}: {wire_values[gate['wire2']]}")
            else:
                print(f"  Fehlender Input: {gate['wire2']}")
    
    binary, decimal = get_binary_from_z_wires(wire_values)

if __name__ == "__main__":
    main()
