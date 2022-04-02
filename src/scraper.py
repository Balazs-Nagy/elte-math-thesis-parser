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

    def parse_all(self) -> pd.DataFrame:
        """ Run the parse_one() method for all available programs based on the homepage of the mathematical faculty
        of ELTE. """
        dfs = []
        for program in self.programs.keys():
            df = self.parse_one(program)
            dfs.append(df)
        data = pd.concat(dfs)
        return data