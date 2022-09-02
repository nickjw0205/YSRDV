import pandas as pd
import sys

original_columns = ['Link', 'status', 'author', 'videoId', 'channel_id', 'title', 'length', 'width', 'height','fps']

def check_cloumns(csv_path):
    try:
        data_list = pd.read_csv(csv_path)
        print(data_list.shape)
    except PermissionError:
        print("csv file is opened. Please close file and retry...")
        sys.exit(0)
    print(data_list.columns.tolist())
    assert data_list.columns.tolist() == original_columns, "csv file seems to be corrupted!! check columns!"
    return pd.read_csv(csv_path)

def parse_csv(csv_path):
    data_list = check_cloumns(csv_path)
    download_start_row = -1
    for index, row in data_list.iterrows():
        # print(index, row)
        if row['status'] == "X":
            download_start_row = index
    
    return data_list, download_start_row