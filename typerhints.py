from typing import List, Union, Tuple
import pandas as pd

CountryList = List[Tuple[str, str]]
HistoryFrame = Union[pd.DataFrame, pd.Series]
HistoryFrameBlocks = List[Tuple[str, HistoryFrame]]
Countries = Union[int, List[str]]
SearchTerm = List[str]
StringList = List[str]