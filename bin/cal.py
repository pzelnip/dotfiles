#!/usr/bin/env python3

import sys
import calendar
from datetime import datetime


def main():
    cur_year = datetime.now().year
    query = sys.argv[1] if len(sys.argv) > 1 else str(cur_year)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    month_mapping = {month: i + 1 for i, month in enumerate(months)}
    for month, idx in month_mapping.items():
        if query.lower() in month:
            print(calendar.month(cur_year, idx))
            return
    if query.lower() == "year":
        print(calendar.calendar(cur_year))
        return
    if len(query) == 4 and query.isdigit():
        print(calendar.calendar(int(query)))
        return

if __name__ == "__main__":
    exit(main())
