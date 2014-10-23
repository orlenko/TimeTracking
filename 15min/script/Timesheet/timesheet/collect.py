import os
import re
import datetime
from spreadsheet import Spreadsheet

DEFAULT_SPAN_DAYS = 30

p = lambda path: os.path.abspath(os.path.realpath(path))

CWD = p(os.path.dirname(__file__))
PROJECT_ROOT = p(os.path.join(CWD, '..', '..', '..'))

RE_TIMESHEET_DIR = re.compile(r'^(\d\d\d\d)-(\d\d)$')
RE_TIMESHEET_FILE = re.compile(r'^(\d\d\d\d)-(\d\d)-(\d\d)\.')


def _filterout_in_place(the_list, the_re):
    total = len(the_list)
    for index, entry in enumerate(reversed(the_list)):
        if not the_re.match(entry):
            del the_list[total - index - 1]
    return the_list


def get_filenames(maxdays=DEFAULT_SPAN_DAYS):
    all_filenames = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Make sure only timesheet directories are included in the walk

        if root == PROJECT_ROOT:
            _filterout_in_place(dirs, RE_TIMESHEET_DIR)
        else:
            files = _filterout_in_place(files, RE_TIMESHEET_FILE)
            for f in files:
                all_filenames.append(p(os.path.join(root, f)))

    return sorted(all_filenames)[-maxdays:]


def get_data(maxdays=DEFAULT_SPAN_DAYS):
    for f in get_filenames(maxdays):
        basename = os.path.basename(f)
        parts = RE_TIMESHEET_FILE.search(basename)
        year = int(parts.group(1))
        month = int(parts.group(2))
        day = int(parts.group(3))
        date = datetime.date(year, month, day)
        spreadsheet = Spreadsheet(f)
        sheet = spreadsheet.SHEETS.values()[0]
        for index, row in enumerate(sheet):
            if row[0] == 'Day Summary:':
                billable_true = row[2]
                billable_report = row[4]
                lost = sheet[index+1][1]
                optimizable = sheet[index+2][1]
                yield {
                    'date': date,
                    'billable_true': float(billable_true),
                    'billable_report': float(billable_report),
                    'lost': float(lost),
                    'optimizable': float(optimizable)
                }
                break




if __name__ == '__main__':
    print 'Test run'
    #print 'PROJECT ROOT:', PROJECT_ROOT
    #print 'FILENAMES:'
    #for f in get_filenames():
    #    print ' ', f
    for d in get_data():
        print d