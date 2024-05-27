from typing import List, Any, Optional
from texttable import Texttable
from latextable import draw_latex

def get_latex_table(rows: List[List[Any]],
                    caption: Optional[str] = None,
                    label: Optional[str] = None,
                    position: str = "htbp",
                    caption_above: bool = True,
                    list_of_cols: bool = True):

    # Init table
    table = Texttable()
    table.set_cols_align(["c"] * 4)
    table.set_deco(Texttable.HEADER | Texttable.VLINES)

    # Make 'list of cols' into 'list of rows'
    if list_of_cols:
        process_rows = [[row[i] for row in row_cols] for i in range(len(row_cols[0]))]
    else:
        process_rows = rows

    # Add rows and return latex table
    table.add_rows(process_rows)

    return draw_latex(table, caption=caption, caption_above=caption_above, label="tab:"+label, position=position)

##################################################################################################################

# LIST OF ROWS
rows = [['Rocket', 'Organisation', 'LEO Payload (Tonnes)', 'Maiden Flight'],
        ['Saturn V', 'NASA', '140', '1967'],
        ['Space Shuttle', 'NASA', '24.4', '1981'],
        ['Falcon 9 FT-Expended', 'SpaceX', '22.8', '2017'],
        ['Ariane 5 ECA', 'ESA', '21', '2002']]

# LIST OF COLS
row_cols = [
    ['col1', '11', '12', '13'],
    ['col2', '21', '22', '23'],
    ['col3', '31', '32', '33'],
    ['col4', '41', '42', '43'],
]

if __name__ == "__main__":
    # print(get_latex_table(rows, caption="Rocket Launches", caption_above=True, list_of_cols=False))
    print(get_latex_table(row_cols, caption="listofcols", label="ciaociao", caption_above=True, list_of_cols=True))