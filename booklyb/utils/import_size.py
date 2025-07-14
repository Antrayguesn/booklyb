
def metrics_size_to_mm(measure):
    size_and_unit = measure.split(" ")
    size = float(size_and_unit[0])
    unit = size_and_unit[1]
    if unit == "cm":
        return size * 10
    elif unit == "m":
        return size * 100
    elif unit == "mm":
        return size
