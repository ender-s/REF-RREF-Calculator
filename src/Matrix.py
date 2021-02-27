from RationalNumber import RationalNumber

class Matrix(object):
    rowNumber = 0
    columnNumber = 0
    values = []
    randomInit = False
    maxLength = 1
    DEBUG = False

    def __init__(self, rowN, columnN, initializeRandomly = False):
        self.rowNumber = rowN
        self.columnNumber = columnN
        self.randomInit = initializeRandomly
        self.initializeMatrix()
    
    def initializeMatrix(self, forceZeroInitialization = False):
        
        if self.randomInit and not forceZeroInitialization:
            self.values = [[self.toRN(random.randint(0,20)) for j in range(self.columnNumber)] for i in range(self.rowNumber)]
        else:
            self.values = [[self.toRN(0) for j in range(self.columnNumber)] for i in range(self.rowNumber)]
        
        self.findMaxLength()
    
    def printMatrix(self):
        print (self)

    def getRow(self, row):
        return self.values[row]

    def getColumn(self, column):
        return [i[column] for i in self.values]

    def setRow(self, r, row):
        row = [self.toRN(i) for i in row]
        self.values[r] = row
        self.findMaxLength()
        
    def findMaxLength(self):
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if len(str(self.getEntry(i, j))) > self.maxLength:
                    self.maxLength = len(str(self.getEntry(i, j)))
    
    def setColumn(self, c, column):
        for i in range(self.rowNumber):
            self.values[i][c] = self.toRN(column[i])
        self.findMaxLength()

    def setEntry(self, i, j, val):
        val = self.toRN(val)
        self.values[i][j] = val
        if len(str(val)) > self.maxLength:
            self.maxLength = len(str(val))

    def getEntry(self, i, j):
        return self.values[i][j]

    def getDimension(self):
        return (self.rowNumber, self.columnNumber)

    def setEntries(self, l):
        if len(l) == self.rowNumber * self.columnNumber:
            for i in range(self.rowNumber):
                for j in range(self.columnNumber):
                    self.setEntry(i, j, self.toRN(l[i*self.columnNumber+j]))
            self.findMaxLength()
    
    def toRN(self, n):
        if type(n) == RationalNumber:
            return n 
        
        if (type(n) == tuple or type(n) == list) and len(n) == 2:
            return RationalNumber(n[0], n[1])
        
        if type(n) == str:
            if "/" in n:
                return RationalNumber(int(n.split("/")[0]), int(n.split("/")[1]))
            else:
                return RationalNumber(int(n), 1)
        
        s = str(n)
        if not "." in s:
            return RationalNumber(n, 1)
        else:
            power = len(s)-s.index(".")-1
            num = int(n*math.pow(10, power))
            den = int(math.pow(10, power))
            return RationalNumber(num, den)
    
    def getEntries(self):
        l = []
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                l.append(self.getEntry(i, j))
        
        return l


    def scalarMultiple(self, l, k):
        return [i.mul(k) for i in l]
    
    def addition(self, l1, l2):
        return [l1[i].add(l2[i]) for i in range(len(l1))]
    
    def elementaryRowOperation(self, target, coefficients, output = True):
        if output and self.DEBUG:
            print ("elementaryRowOperation method was called.")
            print (f"target Row: R_{target+1}")
    
        newRow = [self.toRN(0) for i in range(self.columnNumber)]
        for i in range(len(coefficients)):
            newRow = self.addition(newRow, self.scalarMultiple(self.getRow(i), coefficients[i]))
        
        self.setRow(target, newRow)
    
    def interchangeRows(self, n1, n2):
        temp = self.getRow(n1)
        self.setRow(n1, self.getRow(n2))
        self.setRow(n2, temp)
    
    def copy(self):
        copied = Matrix(self.rowNumber, self.columnNumber)
        
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                copied.setEntry(i, j, self.getEntry(i, j).copy())

        return copied
    
    def reducedRowEchelonForm(self, output = True):
        ref, counter = self.rowEchelonForm(output)
        leadingOnes = ref.detectLeadingOnes()
        for i, j in leadingOnes:
            counter = ref.makeZeroAboveOfThePosition(i, j, counter, output)
        return ref
    
    def detectLeadingOnes(self):
        leadingOnes = []
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if self.getEntry(i, j).equals(1):
                    leadingOnes.append((i, j))
                    break
        
        return leadingOnes
        
    
    def rowEchelonForm(self, output = True):
        m = self.copy()
        i = 0
        j = -1
        
        if m.firstNonzeroColumnAfter(j) == m.columnNumber:
            return m
        
        counter = 1
        while i < m.rowNumber and j < m.columnNumber:
            j = m.firstNonzeroColumnAfter(j)
            if j >= m.columnNumber:
                break
            entry = m.getEntry(i, j)
            if output and self.DEBUG:
                print (j, "is the nonzero column")
                print (f"Analyzing {entry} at pos({i},{j})")
                
            if not entry.equals(1):
                if entry.equals(0) == False:
                    
                    if output:
                        print (f"Step {counter}: ")
                        print (f"R_{i+1} <--- R_{i+1}/{entry}")
                        
                    m.elementaryRowOperation(i, m.generateCoefficients({i: entry.inverse()}), output)
                    if output:
                        print ("After: ")
                        print (m)
                    counter += 1
                else:
                    found = m.findARowXJSuchThatEntryAtXJisNonZero(i, j)
                    if found != -1:
                        if not m.consistsOfZeros(m.getRow(i)):
                            m.interchangeRows(i, found)
                            counter += 1
                            if output:
                                print (f"Step {counter}: ")
                                print (f"R_{i+1} <--> R_{found+1}")
                                print ("After: ")
                                print (m)
                            
                            entry = m.getEntry(i, j)
                            if not entry.equals(1):
                                if output:
                                    print (f"Step {counter}: ")
                                    print (f"R_{i+1} <--- R_{i+1}/{entry}")
                                    
                                m.elementaryRowOperation(i, m.generateCoefficients({i: entry.inverse()}), output)
                                if output:
                                    print ("After: ")
                                    print (m)
                                counter += 1
                                
            
            counter = m.makeZeroBottomOfThePosition(i, j, counter, output)
            i = i + 1
        return m, counter

    
    def makeZeroAboveOfThePosition(self, i, j, counter = 0, output = True):
        if j == 0:
            return counter
        if output and self.DEBUG:
            print (f"Making zero above of the position ({i}, {j}):")
        nonzero_indexes = [] # that are above the ij pos.
        col = self.getColumn(j)
        x = 0
        
        while x < j:
            if not col[x].equals(0):
                nonzero_indexes.append(x)
            x += 1
        
        for index in nonzero_indexes:
            m_ij = self.getEntry(index, j)
            coefficients = self.generateCoefficients({index: self.toRN(1), i: m_ij.mul(-1)})
            
            
            if output:
                print (f"Step {counter}: ")
                print (f"R_{index+1} <---- R_{index+1} - {m_ij}R_{i + 1}")
            
            self.elementaryRowOperation(index, coefficients, output)
            
            if output:
                print ("After: ")
                print (self)
            counter += 1
            #applying the elementary row operation e.g. R_2 <---- R_2 - cR_1
        
        if output and self.DEBUG:
            print (f"End of making zero above of the position ({i}, {j}):")
        return counter        
            
    def makeZeroBottomOfThePosition(self, i, j, counter = 0, output = True):
        if output and self.DEBUG:
            print (f"Making zero bottom of the position ({i}, {j}):")
        nonzero_indexes = [] # that are below the ij pos.
        col = self.getColumn(j)
        x = i+1
        if x == self.rowNumber: 
            return counter
            
        while x < len(col):
            if not col[x].equals(0):
                nonzero_indexes.append(x)
            x += 1
        
        for index in nonzero_indexes:
            m_ij = self.getEntry(index, j)
            coefficients = self.generateCoefficients({index: self.toRN(1), i: m_ij.mul(-1)})
            
            if output:
                print (f"Step {counter}: ")
                print (f"R_{index+1} <---- R_{index+1} - {m_ij}R_{i + 1}")
            
            self.elementaryRowOperation(index, coefficients, output)
            if output:
                print ("After: ")
                print (self)
            counter += 1
            #applying the elementary row operation e.g. R_2 <---- R_2 - cR_1
        if output and self.DEBUG:
            print (f"End of making zero below of the position ({i}, {j}):")
        return counter        
    
    def findARowXJSuchThatEntryAtXJisNonZero(self, i, j):
        x = i
        while x < self.rowNumber and self.getEntry(x, j).equals(0):
            x += 1
        
        if x >= self.rowNumber or j >= self.columnNumber:
            return -1
        
        if not self.getEntry(x, j).equals(0):
            return x
        else:
            return -1
        
    
    def generateCoefficients(self, d, rown = -1):
        if rown == -1:
            rown = self.rowNumber
        # d = {index1 : c1, index2 : c2, ...}
        r = [self.toRN(0) for i in range(rown)]
        
        for index, value in d.items():
            r[index] = value
        
        return r
    
            
    def firstNonzeroColumnAfter(self, j):
        x = j+1
        if x == self.columnNumber:
            return x
        while x < self.columnNumber and self.consistsOfZeros(self.getColumn(x)):
            x += 1
        return x
        
        
    def consistsOfZeros(self, l):
        #l is a column vector or a row vector and is of type list
        
        zeros = 0
        for i in l:
            if i.equals(0):
                zeros += 1
        
        return len(l) == zeros
    
    def __str__(self):
        r = ""
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                r += str(self.values[i][j]).center(self.maxLength) + " "
            r += "\n"
        
        return r