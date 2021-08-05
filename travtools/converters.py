def ext_hex(n):
    """Converts decimal into extended Hexadecimal"""
    
    result = ""
    if n < 16:
        result = "%X" % n
    elif n == 16:
        result = "G"
    elif n == 17:
        result = "H"
    elif n == 18:
        result = "J"
    elif n == 19:
        result = "K"
    elif n == 20:
        result = "L"
    return result


def ext_dec(n):
    """Converts an extended hex string back into integers."""

    result = 0
    try: 
        result = int(n, 16)
    except:
        if n == "G":
            result = 16
        elif n == "H":
            result = 17
        elif  n == "J":
            result = 18
        elif n == "K":
            result = 19
        elif n == "L":
            result = 20    
    return result

def neg_ehex(n, d):
    """Converts a negative number for qrebs into it's ehex number.

    n is the number/letter to convert.
    d is the direction of conversion: 
        F = Forwards number to letter
        B = Backwards letter to number
    """

    result = n
    
    if d == "F":
        if n == -1:
            result = "A"
        elif n == -2:
            result = "B"
        elif n == -3:
            result = "C"
        elif n == -4: 
            result = "D"
        elif n == -5:
            result = "X"
        return str(result)

    if d == "B": 
        if n == "A":
            result = -1
        elif n == "B":
            result = -2
        elif n == "C":
            result = -3
        elif n == "D":
            result = -4
        elif n == "X":
            result = -5
        return str(result)