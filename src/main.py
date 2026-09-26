import sys 


def main():
    print("CLI Smoke Test funktioniert")
    print("Python Version:", sys.version)

    name = input("Wie ist dein Name? ")
    print(f"Hallo, {name} das CLI Programm funktioniert!")

if __name__ == "__main__":
    main()

def add(a, b):
    return a + b    

