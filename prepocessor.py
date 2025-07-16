import re
import pandas as pd

def preprocessor(data):
    data = re.sub(r'[\u202f\u00A0\u2009\u200d]', ' ', data)
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[AaPp][Mm]\s\-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'dates': dates})
    df['date'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %I:%M %p - ')
    # Now what we will be ding is we will bw seprating the Users and MEssages in diffferent Lists

    users = []
    messages = []

    for i in df['user_message']:

        entry = re.split(r'([\w\W]+?):\s', i, maxsplit=1)  # use r in the regrex
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group_Notification')
            messages.append(entry[0])

    # Creating the table in the DATA FRAME

    df['user'] = users
    messages = [msg.rstrip('\n') for msg in
                messages]  # i have used these to remove the \n from the last of the messsages
    df['message'] = messages

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['month_time'] = df['date'].dt.strftime('%I:%M %p')

    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()



    df['day'] = df['date'].dt.day
    df['Hour'] = df['date'].dt.hour
    df['Minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df









