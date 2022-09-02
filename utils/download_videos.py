from pytube import YouTube # => to download video from youtube
from pytube.cli import on_progress
import time
import cv2
import sys
import pandas as pd

def change_title(title):
    special_char = '.\/:*?"<>|() '
    for char in special_char:
        if char in title:
            title = title.replace(char, '_')
    return title

def get_download_list(data_list, index):
    row = 3
    download_list = []

    # check if video is already downloaded
    for index, row in data_list.iterrows():
        # print(index, row)
        if row['status'] == "X":
            download_start_row = index
            
    return download_list

def get_video_info(title):
    cap = cv2.VideoCapture(title)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return width, height, fps

def update_csv(args, data_list, index, link, info, width, height, fps):
    # data_list.loc[index, 'status'] = 'O'
    # data_list.loc[index, 'author'] = info["author"]
    # data_list.loc[index, 'videoId'] = info["videoId"]
    # data_list.loc[index, 'channel_id'] = info["channelId"]
    # data_list.loc[index, 'title'] = info["title"]
    # data_list.loc[index, 'length'] = info["lengthSeconds"]
    # data_list.loc[index, 'status'] = width
    # data_list.loc[index, 'status'] = height
    # data_list.loc[index, 'status'] = fps
    data_list.loc[index] = [link, "O", info["author"], info["videoId"], info["channelId"], info["title"], info["lengthSeconds"], width, height, fps]
    data_list.to_csv(args.csv_path, mode='w', index=False)
    
def download_videos(args, data_list):
    
    try:
        data_list = pd.read_csv(args.csv_path, encoding="utf-8")
        print(data_list.shape)
    except PermissionError:
        print("csv file is opened. Please close file and retry...")
        sys.exit(0)
    
    download_list = []
    for index, row in data_list.iterrows():
        if row['status'] == "X":
            download_list.append([index, row['Link']])
    
    for i, (index, link) in enumerate(download_list):
        yt = YouTube(link, on_progress_callback=on_progress)
        info = yt.vid_info['videoDetails']
        title = info['title']
        title = change_title(title)
        print(title, "is downloading")
        start_time = time.time()
        yt.streams.filter(progressive=True).get_highest_resolution().download(filename=title+".mp4", output_path=args.save_path)
        width, height, fps = get_video_info(args.save_path+"\\"+title+".mp4")
        update_csv(args, data_list, index, link, info, width, height, fps)
        print("\nSaved in folder : ", args.save_path)
        print(title, "downloading completed - {0}sec elapsed\n".format(time.time() - start_time))
        print("{0} videos are left...".format(len(download_list) - (i+1)))