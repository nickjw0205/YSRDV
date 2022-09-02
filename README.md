# YSRDV
get Youtube Search Result and Download Videos

## Installation
```
pip3 install -r requirements.txt
```

## Usage
Get search result(links) to csv
```
python main.py --csv_path "path_for_csv" --keyword "search_words" --scroll num_of_scroll_you_want"
```
- Chrome will turn on automatically and it will scroll to get more video links.  

Download searched videos
```
python main.py --download True
```

Get search result to csv and download videos
```
python main.py --csv_path "path_for_csv" --keyword "search_words" --scroll num_of_scroll_you_want" --download True
```