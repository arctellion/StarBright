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
