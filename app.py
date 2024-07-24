# to run the application through terminal - streamlit run app.py
import matplotlib.pyplot as plt
import streamlit as st
import preprocessor, helper
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyser")

# uploading whatsapp chat into streamlit into the form of bytes data.
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)
    # converting the bytes data into a string
    data = bytes_data.decode("utf-8")
    # st.text(data)

    df = preprocessor.preprocess_data(data)
    # display the dataframe on streamlit
    # st.dataframe(df)

    # fetch unique users so that we can decide for whome among the grp or the personal chat the analysis has to be done
    user_list = df['user'].unique().tolist()

    # removing unnecessary users from the list
    user_list.remove("System")

    # sort the user list
    user_list.sort()

    # inserting a user - Overall at the 0th position/index for overall analysis of the grp or personal chat
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    # only if someone presses the below button only then the analysis will start
    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_files, num_links = helper.fetch_stats(selected_user, df)

        st.title("Statistics of the Whatsapp Chat")



        col1, col2, col3, col4 = st.columns(4) # In Streamlit, the columns method is used to create multiple columns in your layout. T
        # his allows you to place elements side-by-side rather than stacking them vertically.
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total number of words")
            st.title(words)
        with col3:
            st.header("Number of media files shared")
            st.title(num_media_files)
        with col4:
            st.header("Number of media links shared")
            st.title(num_links)

        # finding the busiest user in the group
        # works only if selected user is overall
        if selected_user == 'Overall':
            st.title("Most Busy Users")

            # to find most active memebers we look for who has sent the most messages.
            # value_counts in the user column will give no of unique values/messages that particular user has sent
            x, new_df = helper.fetch_most_busy_users(df)

            # plotting the graph
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='gold')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # wordcloud makes the image consisting of words used
        st.header("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_words = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_words['word'], most_common_words['count'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # most emoji used analysis
        st.title("Most Common Emojis")
        most_common_emoji = helper.most_common_emoji(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_emoji)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(most_common_emoji[1].head(), labels = most_common_emoji[0].head(),autopct = "%.2f")
            st.pyplot(fig)

        # analysing the timeline
        st.title("Timeline Analysis - Monthly Timeline")
        timeline = helper.timeline_function(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['user_message'], color = 'teal')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        st.title("Timeline Analysis - Daily Timeline")
        timeline1 = helper.timeline_function1(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline1['date_number'], timeline1['user_message'], color = 'purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Activity Map - Most Active Day")
        active_day = helper.most_active_day(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(active_day.index, active_day.values, color = 'coral')
        st.pyplot(fig)

        st.title("Activity Map - Most Active Month")
        active_month = helper.most_active_month(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(active_month.index, active_month.values, color = 'orange')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        st.title("Weekly Activity Heat Map - The lighter the color the more active the time period is")
        heat_map = helper.activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heat_map)
        st.pyplot(fig)



















