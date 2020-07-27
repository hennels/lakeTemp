import datetime

def C2F(c):
    return 9.0*c/5 + 32.0

def make_line(*temperatures):
    dt = datetime.datetime.now()
    out = "| {} | {} ".format(dt.strftime("%m/%d/%Y"), dt.strftime("%H:%M"))
    timestamp = dt.strftime("%Y-%m-%d_%H:%M:%S")
    for temp in temperatures:
        out = out + "| {:.2f} ".format(C2F(temp))
    return timestamp, out + "|\n"

def add_line_to_file_after(filename, add_line):
    with open(filename, "r") as f:
        contents = f.readlines()
    index = None
    for i, line in enumerate(contents):
        if line.startswith("| ---- | ---- |"):
            index = i + 1
            break
    if index is None:
        raise ValueError("No table sep line found")
    else:
        contents.insert(index, add_line)
        with open(filename, "w") as f:
            f.writelines(contents)
    return None

def get_temp(probe):
    with open("/sys/bus/w1/devices/{}/w1_slave".format(probe)) as f:
        out = f.readlines()[1][29:]
    return int(out)/1000.0
