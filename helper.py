from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        # 1.number of messages/sentences
        num_messages = df.shape[0] # if whole dataset is selected then return all messages number

        # 2.number of words
        words = []
        for message in df['user_message']:
            words.extend(message.split())


        # 3.number of media files shared
        num_media_files = df[df['user_message'] == '<Media omitted>'].shape[0]

        # 4.number of links shared
        extract = URLExtract()
        links = []
        for message in df['user_message']:
            links.extend(extract.find_urls(message))  #adding the link to the links list if it is found



        return num_messages, len(words), num_media_files, len(links)


    else:
        new_df = df[df['user'] == selected_user]

        # 1.number of messages/sentences
        num_messages = new_df.shape[0] # if a specific user is selected then return the number of mssgs made by the user

        # 2.number of words
        words = []
        for message in new_df['user_message']:
            words.extend(message.split())

        # 3.number of media files shared
        num_media_files = new_df[new_df['user_message'] == '<Media omitted>'].shape[0]

        # 4.number of links shared
        extract = URLExtract() # creating an object of the URLExtract class used to extract URLs
        links = []
        for message in new_df['user_message']:
            links.extend(extract.find_urls(message)) # adding the link to the links list if it is found


        return num_messages, len(words), num_media_files, len(links)

def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()

    # finding the percentage of messages by each user and round it off till 2 decimal places
    df = round((df['user'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns = {'index': 'name', 'user': 'percent'})

    return x, df

def create_wordcloud(selected_user, df):
    # Load stop words
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    if selected_user == 'Overall':
        temp = df.copy()
    else:
        temp = df[df['user'] == selected_user]

    # Removing messages sent by user - group notification
    temp = temp[temp['user'] != 'group_notification']

    # Removing the message - Media Omitted
    temp = temp[temp['user_message'] != '<Media omitted>']

    # Filtering out stop words
    def filter_stop_words(message):
        return ' '.join([word for word in message.lower().split() if word not in stop_words])

    temp['filtered_message'] = temp['user_message'].apply(filter_stop_words)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    # Generate the word cloud from the filtered messages
    df_wc = wc.generate(temp['filtered_message'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user == 'Overall':

        f = open('stop_hinglish.txt', 'r')
        stop_words = f.read()

        # removing messages sent by user - group notification
        temp = df[df['user'] != 'group_notification']

        # removing the message - Media Omitted
        temp = temp[temp['user_message'] != '<Media omitted>\n']

        # including only the words which are present in out hinglish txt file
        words = []
        for message in temp['user_message']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)
        return_df = pd.DataFrame(Counter(words).most_common(20))
        return_df = return_df.rename(columns={0: 'word', 1: 'count'})
        # Counter(words) counts the frequency of all words and most_common gives the mentioned no of top values
        return return_df


    else:
        df = df[df['user'] == selected_user]

        f = open('stop_hinglish.txt', 'r')
        stop_words = f.read()

        # removing messages sent by user - group notification
        temp = df[df['user'] != 'group_notification']

        # removing the message - Media Omitted
        temp = temp[temp['user_message'] != '<Media omitted>\n']

        # including only the words which are present in out hinglish txt file
        words = []
        for message in temp['user_message']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)
        return_df = pd.DataFrame(Counter(words).most_common(20))
        return_df = return_df.rename(columns={0: 'word', 1: 'count'})
        # Counter(words) counts the frequency of all words and most_common gives the mentioned no of top values
        return return_df

# most common emojis
def most_common_emoji(selected_user, df):
    emojis = []
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

        # Function to check if a character is an emoji
        def is_emoji(c):
            return c in emoji.EMOJI_DATA

        # Extract emojis from messages
        for message in df['user_message']:
            emojis.extend([c for c in message if is_emoji(c)])

        emoji_list = pd.DataFrame(Counter(emojis).most_common())
        return emoji_list

    if selected_user == 'Overall':
        # Function to check if a character is an emoji
        def is_emoji(c):
            return c in emoji.EMOJI_DATA

        # Extract emojis from messages
        for message in df['user_message']:
            emojis.extend([c for c in message if is_emoji(c)])

        emoji_list = pd.DataFrame(Counter(emojis).most_common())
        return emoji_list

# analysing timeline - in which month of which year how many mssgs were sent

# monthly timeline
def timeline_function(selected_user, df):
    if selected_user == 'Overall':
        temp = df.copy()
    else:
        temp = df[df['user'] == selected_user]

    # extracting the month number from the data
    temp['month_number'] = temp['date'].dt.month

    # finding the number of messages in all the months of each year
    timeline = temp.groupby(['year', 'month_number', 'month']).count()['user_message']

    #converting timeline to a dataframe
    timeline = temp.groupby(['year', 'month_number', 'month']).count()['user_message'].reset_index()

    #merging the month and year column
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

# daily timeline
def timeline_function1(selected_user, df):
    if selected_user == 'Overall':
        temp = df.copy()
    else:
        temp = df[df['user'] == selected_user]

    # extracting the month number from the data
    temp['date_number'] = temp['date'].dt.date

    # finding the number of messages in all the months of each year
    timeline1 = temp.groupby(['date_number']).count()['user_message']

    #converting timeline to a dataframe
    timeline1 = temp.groupby(['date_number']).count()['user_message'].reset_index()

    return timeline1

def most_active_day(selected_user, df):
    if selected_user == 'Overall':
        temp = df.copy()
    else:
        temp = df[df['user'] == selected_user]

    #extracting the day
    temp['day_name'] = temp['date'].dt.day_name()

    #finding the max number of messages were sent on which day
    return temp['day_name'].value_counts()

def most_active_month(selected_user, df):
    if selected_user == 'Overall':
        temp = df.copy()
    else:
        temp = df[df['user'] == selected_user]

    #finding the max number of messages were sent on which day
    return temp['month'].value_counts()

def activity_map(selected_user, df):
    if selected_user == 'Overall':
        temp = df.copy()
    else:
        temp = df[df['user'] == selected_user]

    period = []

    for hour in temp['hour']:
        if hour == 23:
            period.append(str(hour) + "-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    temp['time_period'] = period

    temp['day_name'] = temp['date'].dt.day_name()
    activity_heatmap = temp.pivot_table(index = 'day_name', columns = 'time_period', values = 'user_message', aggfunc = 'count').fillna(0)
    return activity_heatmap














