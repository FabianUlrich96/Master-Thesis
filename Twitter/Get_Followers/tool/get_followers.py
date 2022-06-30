import pandas as pd
import tweepy

follower_df_list = []
next_token = ''


def get_followers(dataframe):
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAOR%2BbwEAAAAASwiLtwOgXt%2FtG0EJIrLdaph2Xsw%3DspW7CHN0I6KBcjdy4BVvj75LpMAdgQ5l3DIkrcVWMFz8FLIHlz"

    client = tweepy.Client(bearer_token, wait_on_rate_limit=True)
    username = dataframe["user_name"]
    user_id = dataframe["user_id"]
    follower_ids = []
    follower_usernames = []
    global next_token
    print(user_id)
    try:
        response = client.get_users_followers(user_id, max_results=1000, pagination_token=None)
        print(response)
    except:
        return

    try:
        for user in response.data:
            follower_username = user["username"]
            follower_user_id = user["id"]
            follower_ids.append(follower_user_id)
            follower_usernames.append(follower_username)
    except:
        follower_username = None
        follower_user_id = None
        follower_ids.append(follower_user_id)
        follower_usernames.append(follower_username)
    try:
        next_token = response.meta["next_token"]
    except:
        next_token = None
    iterations = 0
    while (next_token != None):
        print(next_token)
        response = client.get_users_followers(user_id, max_results=1000, pagination_token=next_token)

        try:
            for user in response.data:
                follower_username = user["username"]
                follower_user_id = user["id"]
                follower_ids.append(follower_user_id)
                follower_usernames.append(follower_username)
        except:
            follower_username = None
            follower_user_id = None
            follower_ids.append(follower_user_id)
            follower_usernames.append(follower_username)

        try:
            next_token = response.meta["next_token"]
        except:
            next_token = None
        iterations = iterations + 1

    current_follower_df = pd.DataFrame({'follower_id': follower_ids, 'follower_username': follower_usernames})
    current_follower_df['username'] = username
    current_follower_df['user_id'] = user_id
    follower_df_list.append(current_follower_df)
    df = pd.concat(follower_df_list)
    df["follower_id"] = df["follower_id"].astype('Int64')

    df.to_csv("users_with_followers-process.csv", index=False)


def main():
    merged_user_df = pd.read_csv("merged_user-current.csv")
    merged_user_df["user_id"] = merged_user_df["user_id"].astype('Int64')

    merged_user_df.apply(lambda x: get_followers(x), axis=1)

    complete_df = pd.concat(follower_df_list)
    #print(complete_df)
    complete_df["follower_id"] = complete_df["follower_id"].astype('Int64')
    complete_df.to_csv("users_with_followers.csv", index=False)


if __name__ == "__main__":
    main()
