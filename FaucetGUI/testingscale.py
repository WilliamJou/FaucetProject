def scale(value, low, high, newlow, newhigh):
    newVal = newlow + (value-low)*(newhigh - newlow)/(high-low)
    return newVal
def main():
    val = 300
    low = 250
    high = 650
    newlow = 10
    newhigh = 32
    print(scale(val, low, high, newlow, newhigh))
    
main()