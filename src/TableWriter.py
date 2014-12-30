import os
from Table import Table
import errno

class TableWriter:
    def __init__(self, table, outputdir, rowsPerPage = 20, pgListBreak = 20, makeChart = False, desc=''):
        self.outputdir = outputdir
        self.rowsPerPage = rowsPerPage
        self.table = table
        self.pgListBreak = pgListBreak
        self.makeChart = makeChart
        self.desc = desc
    def write(self):
        self.mkdir_p(self.outputdir)
        nRows = self.table.countRows()
        pgCounter = 1
        for i in range(0, nRows, self.rowsPerPage):
            rowsSubset = self.table.rows[i : i + self.rowsPerPage]
            t = Table(self.table.headerRows + rowsSubset)
            f = open(os.path.join(self.outputdir, str(pgCounter) + '.html'), 'w')
            pgLinks = self.getPageLinks(nRows / self.rowsPerPage + 1, 
                    pgCounter, self.pgListBreak)
            
            f.write(pgLinks)
            f.write('<p>' + self.desc + '</p>')
            f.write(t.getHTML(makeChart = self.makeChart))
            f.write(pgLinks)
            
            f.close()
            pgCounter += 1
    @staticmethod
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
    @staticmethod
    def getPageLinks(nPages, curPage, pgListBreak):
        if nPages < 2:
            return ''
        links = ''
        for i in range(1, nPages + 1):
            if not i == curPage:
                links += '<a href="' + str(i) + '.html">' + str(i) + '</a>&nbsp'
            else:
                links += str(i) + '&nbsp'
            if (i % pgListBreak == 0):
                links += '<br />'
        return '\n' + links + '\n'

