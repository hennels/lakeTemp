import argparse
import sh
import misc_func

sensors = {"aux_short1":"28-00000544fce0",
           "aux_long":"28-000005454e97",
           "aux_short2":"28-0000054589c1",
           "std_inside":"28-000004fc7931",
           "std_outside":"28-000004fc8ae5"}

filenames = {"STD.md":["std_outside", "std_inside"],
             "AUX.md":["aux_short1", "aux_short2", "aux_long"]}

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="File to update.")
parser.add_argument("password", help="Sudo password in plaintext.")
args = parser.parse_args()

# validate filename
if args.filename not in filenames:
    raise ValueError("Invalid filename")

# intialize probes
with sh.contrib.sudo(password=args.password, _with=True):
        sh.modprobe("w1-gpio")
        sh.modprobe("w1-therm")

# take temperature readings
temperatures = tuple([misc_func.get_temp(sensors[probe]) for probe in filenames[args.filename]])

# log it
timestamp, line = misc_func.make_line(*temperatures)
misc_func.add_line_to_file_after(args.filename, line)

# commit
sh.git.add(args.filename)
sh.git.commit("-m", timestamp)

# update repo
sh.git.pull()
sh.git.push()

