import random, math, sys
from RationalNumber import RationalNumber
from Matrix import Matrix

class Main(object):
    def __init__(self):
        rn = RationalNumber(1 ,1)
    
        while True:
            r = int(input("Row count: "))
            c = int(input("Column count: "))
            
            m = Matrix(r, c)
            entries = []
            for i in range(r):
                entries += [rn.toRN(i.strip()) for i in input(f"{i+1}. row (Separate by commas, enter {c} values) : ").split(",")]
            
            m.setEntries(entries)
            
            print ("Matrix input: ")
            print (m)
            
            options = ["Row echelon form", "Reduced row echelon form", "New matrix", "Quit"]
            ch = ""
            while True:
                for i in range(len(options)):
                    print (f"{i+1} - {options[i]}")
            
                ch = input("Choice > ")
                
                if ch == "1":
                    m.rowEchelonForm()
                elif ch == "2":
                    m.reducedRowEchelonForm()
                elif ch == "3":
                    break
                elif ch == "4":
                    sys.exit(0)
                else:
                    print("Invalid input.")
            

if __name__ == "__main__":
    main = Main()