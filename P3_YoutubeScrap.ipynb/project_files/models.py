import pandas as pd
from googleapiclient.discovery import build
import requests

api_key = "AIzaSyCtzy6Tov5ZhVvcAs4EeYGPNdmAr03A6c4"

list_channel_name = ['collEge Wallah']

YOUTUBE=build('YOUTUBE','v3',developerKey=api_key)


def get_yt_df(list_channel_name):
    channel_id_list = find_channelID(list_channel_name)
    channel_details = get_channel_stats(YOUTUBE, channel_id_list)
    df = channels_overview(channel_details)
    video_ids = list(map(lambda x: get_video_id(YOUTUBE, x), df.playlist))
    list_all_video_details = list(map(lambda index: video_details(YOUTUBE, video_ids, index), range(len(video_ids))))
    df_collection = []
    for seprate_yt_details in list_all_video_details:
        df_dummy = pd.DataFrame(seprate_yt_details)
        df_dummy.Published_date = pd.to_datetime(df_dummy.Published_date)
        df_dummy.Views = pd.to_numeric(df_dummy.Views)
        df_dummy.Likes = pd.to_numeric(df_dummy.Likes)
        df_dummy.Comments = pd.to_numeric(df_dummy.Comments)
        df_collection.append(df_dummy)
    merged_df = pd.concat([x for x in df_collection], axis=0)
    return df,df_collection,merged_df.head(5)


def seprate_yt(df_collection): #[df1,df2]
    Views=[]
    Likes=[]
    Comments = []
    Published_date=[]
    for df in df_collection:
        Views.append(df.sort_values('Views', ascending=False).head(5))
        Likes.append(df.sort_values('Likes', ascending=False).head(5))
        Comments.append(df.sort_values('Comments', ascending=False).head(5))
        Published_date.append(df.sort_values('Published_date', ascending=False).head(5))
    return Views,Likes,Comments,Published_date #[][][][]


# def compare_channel(merged_df):
#     Views = []
#     Likes=[]
#     Comments = []
#     Published_date=[]
#     Views.append(merged_df.sort_values('Views', ascending=False).head(5))
#     Likes.append(merged_df.sort_values('Likes', ascending=False).head(5))
#     Comments.append(merged_df.sort_values('Comments', ascending=False).head(5))
#     Published_date.append(merged_df.sort_values('Published_date', ascending=False).head(5))
#     return Views,Likes,Comments,Published_date



def find_channelID(list_channel_name):
    channel_id_list=[]
    for channel_name in list_channel_name:
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_name}&key={api_key}&maxResults=1&type=channel'
        response = requests.get(url).json()
        channel_id = response['items'][0]['snippet']['channelId']
        channel_id_list.append(channel_id)
    
    return channel_id_list

def get_channel_stats(YOUTUBE, channel_id_list):

    channel_details=[]

    for channel_id in channel_id_list:
        request = YOUTUBE.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        response = request.execute()

        repeated_code = response['items'][0]

        data = dict(
            channel_name=repeated_code['snippet']['title'],
            subscribers=repeated_code['statistics']['subscriberCount'],
            views=repeated_code['statistics']['viewCount'],
            total_videos=repeated_code['statistics']['videoCount'],
            playlist=repeated_code['contentDetails']['relatedPlaylists']['uploads']
        )
        channel_details.append(data)

    return channel_details

def channels_overview(channel_details):
    df = pd.DataFrame(channel_details, index=range(1, len(channel_details)+1))
    df.subscribers = pd.to_numeric(df.subscribers)
    df.views = pd.to_numeric(df.views)
    df.total_videos = pd.to_numeric(df.total_videos)
    return df

def get_video_id(YOUTUBE, playlist_Id, pg_token=''):
    request = YOUTUBE.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_Id,
        maxResults=50,
        pageToken=pg_token
    )
    response = request.execute()

    list_video_id = list(
        map(lambda x: x['contentDetails']['videoId'], response['items']))
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        return list_video_id + get_video_id(YOUTUBE, playlist_Id, pg_token=nextPageToken)

    return list_video_id

def get_data(x):
    try: 
        channelTitle_ = x['snippet']['channelTitle']
    except:
        channelTitle_="NAN"

    try:
        Title_ = x['snippet']['title']
    except:
        Title_="NAN"

    try:
        Published_date_ = x['snippet']['publishedAt']
    except:
        Published_date_ = 0

    try:
        Views_ = x['statistics']['viewCount']
    except:
        Views_ = 0

    try:    
        Likes_ = x['statistics']['likeCount']
    except:
        Likes_ = 0


    try:
        Comments_ = x['statistics']['commentCount']
    except:
        Comments_= 0

    dicts = {
        'channelTitle': channelTitle_,
        'Title': Title_,
        'Published_date': Published_date_,
        'Views': Views_,
        'Likes': Likes_,
        'Comments': Comments_
    }
    return dicts

def video_details(YOUTUBE, video_id, list_num, start_point=0, end_point=50):
    request = YOUTUBE.videos().list(
        part="snippet,contentDetails,statistics",
        id=','.join(video_id[list_num][start_point:end_point])
    )
    response = request.execute()

    data = list(map(lambda x:  get_data(x), response['items']))
    while end_point < len(video_id[list_num]):
        return data + video_details(YOUTUBE, video_id, list_num, start_point=start_point+50, end_point=end_point+50)

    return data



# def cleaning_data(df, channel_name):
#     temp_df = pd.to_datetime(df.Published_date)
#     df['Date'] = temp_df.dt.date
#     df['Time'] = temp_df.dt.time
#     df.drop('Published_date', inplace=True, axis=1)
#     df[['Views', 'Likes', 'Comments']] = df[[
#         'Views', 'Likes', 'Comments']].apply(pd.to_numeric)
#     df.reset_index(drop=True, inplace=True)
#     df.index += 1
#     df.to_excel(f'{channel_name}.xlsx')


# # cleaning data of seprate dataframe
# for x in df_collection:
#     cleaning_data(x, x.iloc[0, 0])

# # cleaning the main common dataframe
# cleaning_data(merged_df, 'Comparing_all')
