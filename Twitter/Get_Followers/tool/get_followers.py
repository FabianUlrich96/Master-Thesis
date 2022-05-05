import pandas as pd
import tweepy

follower_df_list = []


def get_followers(dataframe):
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAOR%2BbwEAAAAASwiLtwOgXt%2FtG0EJIrLdaph2Xsw%3DspW7CHN0I6KBcjdy4BVvj75LpMAdgQ5l3DIkrcVWMFz8FLIHlz"

    client = tweepy.Client(bearer_token, wait_on_rate_limit=True)
    username = dataframe["user_name"]
    user_id = dataframe["user_id"]
    follower_ids = []
    follower_username = []
    next_token = ""
    try:
        response = client.get_users_followers(user_id, max_results=1000, pagination_token=None)
    except:
        return

    try:
        for user in response.data:
            username = user["username"]
            user_id = user["id"]
            follower_ids.append(user_id)
            follower_username.append(username)
    except:
        username = None
        user_id = None
        follower_ids.append(user_id)
        follower_username.append(username)
    try:
        next_token = response.meta["next_token"]
    except:
        next_token = None
    iterations = 0
    while (next_token != None) and (iterations <= 9):
        print(next_token)
        response = client.get_users_followers(user_id, max_results=1000, pagination_token=next_token)

        try:
            for user in response.data:
                username = user["username"]
                user_id = user["id"]
                follower_ids.append(user_id)
                follower_username.append(username)
        except:
            username = None
            user_id = None
            follower_ids.append(user_id)
            follower_username.append(username)

        try:
            next_token = response.meta["next_token"]
        except:
            next_token = None
        iterations = iterations + 1

    current_follower_df = pd.DataFrame({'follower_id': follower_ids, 'follower_username': follower_username})
    current_follower_df['username'] = username
    current_follower_df['user_id'] = user_id
    follower_df_list.append(current_follower_df)
    print("test")
    df = pd.concat(follower_df_list)
    df["follower_id"] = df["follower_id"].astype('Int64')

    print(df)
    df.to_csv("users_with_followers-process.csv", index=False)


def main():
    merged_user_df = pd.read_csv("merged_user.csv")
    merged_user_df["user_id"] = merged_user_df["user_id"].astype('Int64')

    merged_user_df.apply(lambda x: get_followers(x), axis=1)

    complete_df = pd.concat(follower_df_list)
    print(complete_df)
    complete_df["follower_id"] = complete_df["follower_id"].astype('Int64')
    complete_df.to_csv("users_with_followers.csv", index=False)


if __name__ == "__main__":
    main()
