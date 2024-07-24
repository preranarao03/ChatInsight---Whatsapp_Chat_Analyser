# gets text data and converts it into dataframe and returns the dataframe

import regex as re
import pandas as pd

import regex as re
import pandas as pd

# Function to parse the chat data from a string
def parse_chat(data):
    lines = data.split('\n')

    dates = []
    users = []
    messages = []

    for line in lines:
        date_time_match = re.match(r'^(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2})\s([apAP][mM]) - ', line)
        if date_time_match:
            date = date_time_match.group(1)
            time = date_time_match.group(2)
            period = date_time_match.group(3).upper()
            message = line[date_time_match.end():].strip()

            # Split user and message
            user_message_split = message.split(": ", 1)
            if len(user_message_split) > 1:
                user = user_message_split[0]
                message = user_message_split[1]
            else:
                user = "System"
                message = user_message_split[0]

            dates.append(f"{date} {time} {period}")
            users.append(user)
            messages.append(message)

    df1 = pd.DataFrame({'message_date': dates, 'user': users, 'user_message': messages})
    return df1

# Function to preprocess data and return a DataFrame
def preprocess_data(data):
    # Parse the chat data
    df = parse_chat(data)

    # Convert 'message_date' to datetime type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y %I:%M %p')

    # Rename 'message_date' to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract additional time-related columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df



