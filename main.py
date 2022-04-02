from src.scraper import ElteMathThesisParser


def run():
    # initialize object
    elte_ttk_math = ElteMathThesisParser()
    # print the link to homepage
    print(elte_ttk_math.home)
    # parse thesis info to single dataframe for the given programs
    data = elte_ttk_math.parse_all(programs=['MSc Biztosítási és pénzügyi matematikus'])
    # save parsed info to excel
    elte_ttk_math.to_excel(data=data, save_to='elte-ttk-thesis-list.xlsx')
    # download theses (pdf files)
    elte_ttk_math.download(data, download_delay=5)


if __name__ == '__main__':
    run()
