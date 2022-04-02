from src.scraper import ElteMathThesisParser


def run():
    # initialize object
    elte_ttk_math = ElteMathThesisParser()
    # print the link to homepage
    print(elte_ttk_math.home)
    # parse thesis info to single dataframe for the given programs
    data = elte_ttk_math.parse_all(programs=None)
    # save parsed info to excel
    elte_ttk_math.to_excel(data=data, save_to='elte-ttk-thesis-list.xlsx')
    # download theses corresponding to selected programs
    programs = ['BSc Matematikus diplomamunkák', 'MSc Biztosítási és pénzügyi matematikus']
    # download theses (pdf files)
    elte_ttk_math.download(data[data.program.isin(programs)], download_delay=3)


if __name__ == '__main__':
    run()
