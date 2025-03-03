import io
import tkinter as tk
from datetime import datetime

class JVMList:
    input_file_path = None
    fields =[]
    field_dict = {}
    dropdown_options = []
    output_options = []
    read_rows = 0
    successful_rows = 0
    error_rows = 0
    overwrite_input_file = False

    # tkinter
    root = None
    row_count = None
    row_count_str = None
    success_count = None
    successful_rows_str = None
    error_count = None
    error_count_str = None
    list_date_value = None
    list_type_value = None
    list_date_value_default = datetime.today().strftime('%m/%d/%y')
    list_type_options = ['SPCP', 'FTHB', 'Homerun', 'Stale', 'Ratebreak']