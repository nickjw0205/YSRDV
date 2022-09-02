import argparse
from utils.download_videos import *
from utils.parse_csv import *
from utils.utils import *
import sys

original_columns = ['Link', 'status', 'author', 'videoId', 'channel_id', 'title', 'length', 'width', 'height','fps']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_path', type=str, default='download_list.csv', help='csv path')
    parser.add_argument('--keyword', type=str, help='search terms on youtube')
    parser.add_argument('--cc_license', type=bool, default=False, help='download only creative commons license videos')
    parser.add_argument('--scroll', type=int, default=200, help='# of scrolls')
    parser.add_argument('--download', type=bool, default=False, help='download videos in csv')
    parser.add_argument('--save_path', default="videos/", help="save path of downloaded videos")
    args = parser.parse_args()
        
    csv_data, download_start_index = parse_csv(args.csv_path)
    
    if args.keyword:
        csv_data = get_search_list(csv_data, args)
    
    if args.download:
        download_videos(args, csv_data)
        
    