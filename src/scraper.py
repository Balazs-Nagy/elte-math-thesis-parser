import requests
from bs4 import BeautifulSoup
import pandas as pd


class ElteMathThesisParser:
    """ Parse all available thesis information for all programs run by
    the Institute of Mathematics of Faculty of Science, Eötvös Loránd University."""

    def __init__(self):
        # link to homepage
        self.home = 'https://www.math.elte.hu/kepzesek/diplomamunkak/'

    @property
    def programs(self) -> dict:
        # name of available programs and links to thesis submissions per program
        response = requests.get(self.home)
        soup = BeautifulSoup(response.content, "html.parser")
        programs = {tag.text: tag.a.get('href') for tag in soup.find('div', class_='dobozban').find_all('p')}
        return programs

    def parse_one(self, program) -> pd.DataFrame:
        """ Parse thesis entries found on the webpage of a single program."""
        try:
            url = self.programs[program]
        except KeyError:
            print(f'No program "{program}" is available.')
            return None

        # download page
        response = requests.get(url)
        # parse html
        soup = BeautifulSoup(response.content, "html.parser")
        # the information is found in a div tag with class "main"
        main = soup.find('div', class_='main')
        # the pages are not really well-structured, so following code can become obsolete
        # -- current pattern is:
        # --- h3 tag contains the year of dissertation
        # --- after that p tags contain the author, title of thesis and supervisor and also href to thesis
        tags = main.find_all(['h3', 'p'])

        # list container to store rows of the dataframe
        dfs = []
        year = None
        for item in tags:
            # tag name
            name = item.name
            if name == 'h3':
                # should contain the year in integer format
                year = int(item.text.strip())
            if name == 'p':
                # text attribute of the p tag contains author, title, supervisor info
                text = item.text.strip()
                # author of thesis
                author = text.split('Témavezető:')[0].split(':')[0].strip()
                # title of thesis
                title = text.split('Témavezető:')[0].split(':')[-1].strip()
                # supervisor of the thesis
                supervisor = text.split('Témavezető:')[-1].strip()
                # create link from href to thesis
                href = item.a.get('href')
                link = f'https://web.cs.elte.hu{href}'
                # store results in a list that will correspond to a single row of the resulting dataframe
                dfs.append([program, year, author, title, supervisor, link])

        # create single dataframe from rows
        df = pd.DataFrame(dfs, columns=['program', 'year', 'author', 'title', 'supervisor', 'url'])
        return df

    def parse_all(self, programs: list = None) -> pd.DataFrame:
        """ Run the parse_one() method for all available programs based on the homepage of the mathematical faculty
        of ELTE. """
        if not programs:
            # if not specified use all available programs
            programs = self.programs.keys()
        dfs = []
        for program in programs:
            df = self.parse_one(program)
            dfs.append(df)
            print(f'Finished parsing for {program}.')
        data = pd.concat(dfs)
        # clean unwanted characters
        for col in ['author', 'title', 'supervisor']:
            data[col] = data[col].replace(r'[\t\n"]', '', regex=True)
        return data

    def to_excel(self, data: pd.DataFrame, save_to: str = 'elte-ttk-thesis-list.xlsx'):
        # available programs as dataframe
        programs = pd.DataFrame.from_dict(self.programs,
                                          orient='index',
                                          columns=['link']).reset_index().rename({'index': 'program'}, axis=1)
        results = {'programs': programs,
                   'data': data}

        # save programs and thesis data to Excel
        with pd.ExcelWriter(save_to, engine='xlsxwriter') as writer:
            for sheet_name, df in results.items():
                # write data to sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                # apply auto-filter
                writer.sheets[sheet_name].autofilter(0, 0, df.shape[0], df.shape[1] - 1)
        print(f'Saved results to {save_to}.')