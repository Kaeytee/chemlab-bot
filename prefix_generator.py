# Function to generate the prefix based on the number of carbons
def generate_prefix(n):
    base_prefixes = [
        "meth", "eth", "prop", "but", "pent", "hex", "hept", "oct", "non", "dec"
    ]

    tens_prefixes = [
        "dec", "icos", "tricos", "tetracos", "pentacos", "hexacos", "heptacos", "octacos", "nonacos"
    ]

    if n <= 10:
        return base_prefixes[n - 1]
    elif n < 100:
        tens = n // 10
        ones = n % 10
        return tens_prefixes[tens - 1] + (ones > 0 and base_prefixes[ones - 1] or "")
    else:
        hundreds = n // 100
        remainder = n % 100
        hundreds_prefix = base_prefixes[hundreds - 1] + "cent"
        return hundreds_prefix + (remainder > 0 and generate_prefix(remainder) or "")
