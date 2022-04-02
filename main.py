import pandas as pd
from src.scraper import ElteMathThesisParser


def run():
    # initialize object
    elte_ttk_math = ElteMathThesisParser()
    # print the link to homepage
    print(elte_ttk_math.home)

    # parse all thesis info to single dataframe
    data = elte_ttk_math.parse_all()

    # save parsed info to excel
    elte_ttk_math.to_excel(data=data, save_to='elte-ttk-thesis-list.xlsx')


if __name__ == '__main__':
    run()
