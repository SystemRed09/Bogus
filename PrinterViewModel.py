from logging import warning

from Printer import Printer


class FormattedCodes:
    OK = "\033[92m Ok \033[0m"
    FAILED = "\033[91m Failed \033[0m"


class PrinterViewModel:
    printers: list[Printer]

    def __init__(self, printers=None):
        if printers is None:
            printers = []
            warning("No printers provided")
        self.printers = printers

    def add(self, p: Printer) -> None:
        self.printers.append(p)

    @staticmethod
    def connectionInfo(printer: Printer) -> str:
        cStatus = FormattedCodes.FAILED if printer.hasError() else FormattedCodes.OK
        return f"Printer: {printer.name} with connection status {cStatus}\n"

    @staticmethod
    def warningsInfo(printer: Printer) -> str:
        w = []
        for sc in printer.getWarnings():
            w.append(sc.title)
        return f"With warnings: {"| ".join(w)}\n" if w.__len__() > 0 else "With no warnings\n"

    def Info(self, index=0) -> str:
        infoBody = self.connectionInfo(self.printers[index])
        if not self.printers[index].hasError():
            infoBody += self.warningsInfo(self.printers[index])
        return infoBody

    def AllPrinterInfo(self) -> str:
        c = ""
        for i in range(self.printers.__len__()):
            c += self.Info(index=i) + '\n'
        return c