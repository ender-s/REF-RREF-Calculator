class RationalNumber(object):
    def __init__(self, numerator, denominator):
        assert (denominator != 0)
        if numerator*denominator >= 0:
            numerator = abs(numerator)
            denominator = abs(denominator)
        else:
            numerator = -1*abs(numerator)
            denominator = abs(denominator)
        
        self.numerator = numerator
        self.denominator = denominator
        self.reduce()
    
    def reduce(self):
        gcd = self.gcd()
        self.numerator = int(self.numerator / gcd)
        self.denominator = int(self.denominator / gcd)
    
    def gcd(self):
        num = abs(self.numerator)
        den = self.denominator
        
        if num >= den:
            max = num
            min = den
        else:
            max = den
            min = num
        
        while min != 0:
            r = max % min
            max = min
            min = r
        
        return max
    
    def add(self, r):
        r = self.toRN(r)
        num = self.numerator*r.denominator + r.numerator*self.denominator
        den = self.denominator * r.denominator
        return RationalNumber(num, den)
     
    def sub(self, r):
        r = self.toRN(r)
        num = self.numerator*r.denominator - r.numerator*self.denominator
        den = self.denominator * r.denominator
        return RationalNumber(num, den)
        
    def mul(self, r):
        r = self.toRN(r)
        num = self.numerator*r.numerator
        den = self.denominator*r.denominator
        return RationalNumber(num, den)
    
    def copy(self):
        return RationalNumber(self.numerator, self.denominator)
    
    def div(self, r):
        return self.mul(self.toRN(r).inverse())
    
    def inverse(self):
        return RationalNumber(self.denominator, self.numerator)
    
    def equals(self, r):
        r = self.toRN(r)

        if self.numerator == 0 and r.numerator == 0:
            return True
        else:
            if self.numerator == r.numerator and self.denominator == r.denominator:
                return True
            else:
                return False

    def toRN(self, n):
        # possible inputs: integer
        #                   floating number
        #                   string of form "a/b"
        #                   tuple of form (a,b)
        #                   list of form [a,b]
        
    
    
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
    
    def __str__(self):
        if self.numerator == 0:
            return "0"
        elif self.denominator == 1:
            return f"{self.numerator}"
        else:
            return f"{self.numerator}/{self.denominator}"
    
    def floatingNumberForm(self):
        return self.numerator/self.denominator