# Data Collection & Preparation

## video_collection.xlsx
* Overview of the data collection process.
## translation.py
* Translates given dataframe column to English.

## merge_files.ipynb
* File to merge different unlabeled video keyword csv files of one month to one file.

## get_video_metadata.py
* Preprocessing for semi-automatic labeling. 
* Gets metadata of videos.
* Removes videos with no comments.
* Removes videos with a language other than German.

## label_video_list.py
* Tool to label videos by opening them and giving the user the option to select a label.

## delete_unvalid.ipynb
* Takes a labeled video file and deletes the videos labeled "unvalid".

