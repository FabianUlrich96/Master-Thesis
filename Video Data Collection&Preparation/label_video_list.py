import asyncio
import pandas as pd
from pyppeteer import launch
from PyInquirer import prompt, print_json, Separator


def load_dataframe():
    filename = input("File name in folder: ")
    filename = f'{filename}.csv'
    csv_file = pd.read_csv(filename)

    return csv_file, filename


def save_dataframe(result_df, filename):
    new_filename = f'{filename}_labeled.csv'
    try:
        result_df.to_csv(new_filename)
    except:
        result_df.to_csv("in_save_mode.csv")


async def query_videos(dataframe, videos, filename, to_code):
    browser = await launch(headless=False)
    page = await browser.newPage()
    valid_video = [
        {
            'type': 'list',
            'name': 'valid',
            'message': 'Is this a valid video?',
            'choices': [
                'yes',
                'no']}
    ]

    not_valid_video = [
        {
            'type': 'list',
            'name': 'not_valid',
            'message': 'Why is this video not valid?',
            'choices': [
                'Topic',
                'Language',
                'Video not available',
                'Comments disabled',
                'Other']}
    ]
    for video in videos:
        answer_not_valid = None
        video_url = f'https://www.youtube.com/watch?v={video}'
        await page.goto(video_url)

        answer_valid = prompt(valid_video)
        answer_valid = answer_valid["valid"]

        if answer_valid == "yes":
            valid = 'valid'
        else:
            answer_not_valid = prompt(not_valid_video)
            answer_not_valid = answer_not_valid["not_valid"]

            if answer_not_valid == "Other":
                answer_not_valid = input("Please specify: ")

            valid = answer_not_valid

        dataframe.loc[dataframe['video_id'] == video, ['valid']] = valid

        save_dataframe(dataframe, filename)
        to_code = to_code - 1
        print(f'{to_code} still to code')


async def main():
    dataframe, filename = load_dataframe()
    threshold = 51
    dataframe.loc[dataframe['comment_count'] < threshold, 'valid'] = 'comment threshold'

    print(dataframe)
    selected = dataframe.loc[dataframe['comment_count'] > threshold]["video_id"]
    video_list = selected.values.tolist()
    print(video_list)
    to_code = len(video_list)
    await query_videos(dataframe, video_list, filename, to_code)


asyncio.get_event_loop().run_until_complete(main())
