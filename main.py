import pandas as pd
from src.scraper import ElteMathThesisParser


# initialize object
elte_ttk_math = ElteMathThesisParser()
# link to homepage
print(elte_ttk_math.home)

# available programs as dataframe
programs = pd.DataFrame.from_dict(elte_ttk_math.programs,
                                  orient='index',
                                  columns=['link']).reset_index().rename({'index': 'program'}, axis=1)
# parse all thesis info to single dataframe
data = elte_ttk_math.parse_all()

# save programs and thesis data to Excel
with pd.ExcelWriter('elte-ttk-thesis-list.xlsx') as writer:
    programs.to_excel(writer, sheet_name='programs', index=False)
    data.to_excel(writer, sheet_name='data', index=False)
