import odf
import odf.opendocument
from odf.table import Table, TableCell, TableRow
from odf.text import P


class Spreadsheet(object):
    def __init__(self, inputFileOrName):
        self.doc = odf.opendocument.load(inputFileOrName)
        self.SHEETS = {}
        for sheet in self.doc.spreadsheet.getElementsByType(Table):
            self.readSheet(sheet)

    def readSheet(self, sheet):
        '''reads a sheet in the sheet dictionary, storing each sheet as an array (rows) of arrays (columns)
        '''
        name = sheet.getAttribute("name")
        rows = sheet.getElementsByType(TableRow)
        arrRows = []

        # for each row
        for row in rows:
            row_comment = ""
            arrCells = []
            cells = row.getElementsByType(TableCell)

            # for each cell
            for cell in cells:
                # repeated value?
                repeat = cell.getAttribute("numbercolumnsrepeated")
                if(not repeat):
                    repeat = 1

                ps = cell.getElementsByType(P)
                textContent = ""

                # for each text node
                for p in ps:
                    for n in p.childNodes:
                        if (n.nodeType == 3):
                            textContent = textContent + unicode(n.data)

                if(textContent):
                    if(textContent[0] != "#"): # ignore comments cells
                        for rr in range(int(repeat)): # repeated?
                            arrCells.append(textContent)

                    else:
                        row_comment = row_comment + textContent + " ";

            # if row contained something
            if(len(arrCells)):
                arrRows.append(arrCells)

            #else:
            #    print "Empty or commented row (", row_comment, ")"

        self.SHEETS[name] = arrRows
    
    def getSheet(self, name):
        '''returns a sheet as an array (rows) of arrays (columns)
        '''
        return self.SHEETS[name]
