from Printer import Printer
from sys import argv
from os import listdir, name
from json import loads
from pyperclip import copy

from PrinterViewModel import PrinterViewModel

SYS_ARGS = argv[2:]
Dpath =  argv[1]

def helpInfo():
    f = listdir(Dpath)
    savedDefaultJSONs = ""
    for file in f:
        savedDefaultJSONs += file + ' | '
    savedDefaultJSONs = savedDefaultJSONs[:-2]
    print(f"""Tech classroom printer checker
        -d <ip> or --default <file> -> Load printer route file
        \tSaved Files: {savedDefaultJSONs}
        
        -i <ip> or --ip <ip>        -> Single IP4
        -h or --help                -> Help Screen (this)
        -o or --output              -> Output to file (output.txt)""")

def default(fileName="") -> str:
    if fileName == "" or fileName not in listdir(Dpath + "/Defaults/"): raise RuntimeError("File does not exist.")

    with open(f"{Dpath}/Defaults/{fileName}", 'r') as file:
        content = loads(file.read())

    printers = []
    for p in content["printers"]:
        printers.append(Printer(p["ip"], name=p["name"]))

    return PrinterViewModel(printers).AllPrinterInfo()

def single(ip="") -> str:
    if ip == "": raise RuntimeError("No ip provided")

    pVM = PrinterViewModel([Printer(ip, f"@{ip}")])
    return pVM.Info()

def output(out: str) -> None:
    for r in [r"\033", "[92m", "[91m", "[0m"]:
        out = out.replace(r, "")

    with open("output.txt", 'w') as f:
        f.write(out)

    copy(out)
    print("Copied to Clipboard")

def main(args) -> None:
    out: str | None = None
    if args.__len__() < 2:
        helpInfo()
        return
    print(Dpath)
    match args[0]:
        case '-h' | "--help":
            helpInfo()
        case '-d' | "--default":
            out = default(fileName=args[1])
        case '-i' | "--ip":
            out = single(ip=args[1])
        case _:
            helpInfo()

    print(out)
    if ('-o' in args or "--output" in args) and out is not None:
        output(out)

    _ =input("Press any key to exit.")

if __name__ == '__main__':
    main(SYS_ARGS)
    
