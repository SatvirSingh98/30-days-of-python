import os
import sys
from datetime import datetime

import pandas as pd
import requests
from requests_html import HTML

BASE_DIR = os.path.dirname(__file__)
now = datetime.now()
current_year = now.year


def url_to_file(url: str, year: int = current_year, save: bool = False):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            FILE_PATH = os.path.join(BASE_DIR, f"world-{year}.html")
            with open(FILE_PATH, "w") as f:
                f.write(html_text)
        return html_text
    return ""


def parse_and_extract(url: str, year: int = current_year):
    html_txt = url_to_file(url)

    r_html = HTML(html=html_txt)
    table_class = ".imdb-scroll-table"
    r_table = r_html.find(table_class)
    # print(r_table)

    table_data = []
    # table_dict_data = {}
    headers = []

    if len(r_table) == 1:
        # print(r_table[0].text)
        parsed_table = r_table[0]
        rows = parsed_table.find('tr')
        header_row = rows[0]
        header_col = header_row.find('th')
        headers = [head.text for head in header_col]

        for row in rows[1:]:
            # print(row.text)
            cols = row.find('td')
            row_data = []
            # row_dict_data = {}
            for i, col in enumerate(cols):
                # print(i, col.text, '\n\n')

                # header_name = header_names[i]
                # row_dict_data[header_name] = col.text

                row_data.append(col.text)
            table_data.append(row_data)
            # table_dict_data.append(row_dict_data)

    # print(headers)
    # print(table_data[0])

    path = os.path.join(BASE_DIR, 'data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, f'{year}.csv')

    df = pd.DataFrame(table_data, columns=headers)
    # df = pd.DataFrame(table_dict_data)
    df.to_csv(filepath, index=False)


def run(start_year: int = None, years_ago: int = None):
    if start_year is None:
        now = datetime.now()
        start_year = now.year

    assert isinstance(start_year, int)

    if (1977 <= start_year <= current_year):
        if years_ago is not None:
            assert isinstance(years_ago, int)
            for year in range(years_ago):
                url = f"https://www.boxofficemojo.com/year/world/{start_year}/"
                parse_and_extract(url, year=start_year)

                print(f'Finished parsing {start_year}')
                start_year -= 1
        else:
            url = f"https://www.boxofficemojo.com/year/world/{start_year}/"
            parse_and_extract(url, year=start_year)
            print(f'Finished parsing {start_year}')
    else:
        print('The Requested Page Not Found...( INVALID YEAR )')
        print(('data is available from 1977 to {}.'.upper())
              .format(current_year))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            start = int(sys.argv[1])
        except Exception:
            start = None
        try:
            count = int(sys.argv[2])
        except Exception:
            count = None
        run(start_year=start, years_ago=count)
    else:
        run()
