import streamlit as st
import helper
import matplotlib.pyplot as plt
import prepocessor
import plotly.express as px
import numpy as np
import pandas as pd
import seaborn as sns

from helper import daily_time

st.sidebar.title("Whatsapp Chat")
#CODE to add the feature for the uploading of the files
# Show helpful instructions
with st.sidebar.expander("🛠️ How to Export WhatsApp Chat (.txt)", expanded=True):
    st.markdown("""
**Follow these steps carefully before uploading your chat file:**

1. 📱 Open **WhatsApp** and go to the group or chat.
2. Tap on **three dots → More → Export chat**.
3. Choose **“Without media”** (⚠️ Required).
4. A `.zip` file will be downloaded (contains `.txt` file).
5. **Extract** the `.txt` file from the `.zip`.
6. Finally, upload the `.txt` file using the uploader below. ✅
    """)
uploaded_file=st.sidebar.file_uploader("Choose a Exported Chat File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
#Once a file is uploaded, the app reads its raw content as bytes and stores it in bytes_data for further processing
    # Now we have to conbert these into the string
    data = bytes_data.decode("utf-8")

    df= prepocessor.preprocessor(data)

    # st.dataframe(df)

    #fetch the unique names of the user

    user_list = df['user'].unique().tolist()
    #to remove the Group Notification
    if 'Group_Notification' in user_list:
        user_list.remove('Group_Notification')
    #TO SORT THE USER_NAMES In the Ascending order
    user_list.sort()
    #inserting at the position to show that analyssis has been selected to the overall rather than individual

    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Showing Analysis w.r.t",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words, count, unique_links= helper.fetch_stats(selected_user,df)
        col1, col2, col3 , col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Transfered")
            st.title(count)
        with col4:
            st.header("Shared Links")
            st.title(unique_links)

            # time line
        st.title("________________________________")

        st.title("Most Active Months")


        # timeline = helper.monthly_timeline(selected_user,df)
        # fig, ax = plt.subplots(dpi=200)
        # ax.plot(timeline['time'], timeline['message'])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        import plotly.graph_objects as go

        # Prepare timeline
        timeline = helper.monthly_timeline(selected_user, df)

        # Ensure 'time' is in datetime format
        timeline['time'] = pd.to_datetime(timeline['time'])

        # Create a new column for hover text
        timeline['Month_Year'] = timeline['time'].dt.strftime('%b %Y')  # e.g., "Jul 2025"

        # Build figure manually with custom hover
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=timeline['time'],
            y=timeline['message'],
            mode='lines+markers',
            line=dict(color='#FF1E56', width=2),
            marker=dict(size=6),
            hovertemplate="%{customdata} : %{y}",  # 🟢 Custom format: Month Year : Count
            customdata=timeline['Month_Year'],  # This feeds %{customdata}
            name=''
        ))

        fig.update_layout(

            xaxis_title='Time',
            yaxis_title='No. of Messages',
            xaxis_tickangle=90,
            xaxis_title_font=dict(size=20, color='#900C3F'),
            yaxis_title_font=dict(size=20, color='#C70039'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(bgcolor="black", font_size=14)
        )

        # Show in Streamlit
        st.plotly_chart(fig, use_container_width=True)

#Hourly Time line
        st.title("Most Active Hours")

        message_time = helper.hourly_timeline(selected_user, df)

        # Reset index if needed (to treat hours as a column)
        message_time = message_time.reset_index()
        message_time.columns = ['Hour', 'Messages']

        # Create interactive Plotly line chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=message_time['Hour'],
            y=message_time['Messages'],
            mode='lines+markers',
            line=dict(color='#FF1E56', width=2),
            marker=dict(size=6),
            hovertemplate="%{x} : %{y} messages",  # Custom hover: "13 : 212 messages"
            name=''
        ))

        # Style the layout
        fig.update_layout(

            xaxis_title='Hour of Day',
            yaxis_title='Number of Messages',
            xaxis_tickangle=90,
            xaxis_title_font=dict(size=20, color='#900C3F'),
            yaxis_title_font=dict(size=20, color='#C70039'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(bgcolor="black", font_size=14)
        )

        # Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)


        # message_time = helper.hourly_timeline(selected_user,df)
        # fig, ax = plt.subplots(dpi=200)
        # ax.plot(message_time.index, message_time.values)
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        # fig, ax = plt.subplots(dpi=200)
        # ax.plot(timeline['time'], timeline['message'])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)
#Daily Time line

        st.title("Daily Active TimeLine")

        import plotly.graph_objects as go

        # Get daily message data
        daily_timeline = helper.daily_time(selected_user, df)

        # Ensure date column is datetime
        daily_timeline['only_date'] = pd.to_datetime(daily_timeline['only_date'])

        # Format for custom hover: e.g., "2025-07-15 : 832"
        daily_timeline['formatted_date'] = daily_timeline['only_date'].dt.strftime('%Y-%m-%d')

        # Create interactive Plotly line chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_timeline['only_date'],
            y=daily_timeline['message'],
            mode='lines+markers',
            line=dict(color='#FF1E56', width=2),
            marker=dict(size=6),
            hovertemplate="%{customdata} : %{y} messages",
            customdata=daily_timeline['formatted_date'],
            name=''
        ))

        # Update layout styling
        fig.update_layout(

            xaxis_title='Date',
            yaxis_title='Number of Messages',
            xaxis_tickangle=45,
            xaxis_title_font=dict(size=20, color='#900C3F'),
            yaxis_title_font=dict(size=20, color='#C70039'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(bgcolor="black", font_size=14)
        )

        # Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # daily_timeline=helper.daily_time(selected_user, df)
        #
        #
        #
        # ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)
#actively days
        # map_data=helper.activity_heat_map(selected_user, df)
        # fig, ax = plt.subplots(dpi=200)
        # # plt.figure(figsize=(8, 4))
        # ax=sns.heatmap(map_data)
        # # plt.yticks(rotation='horizontal')
        # st.pyplot(fig)

        st.title("Weekly Active TimeLine")

        # Dark mode style
        plt.style.use("dark_background")

        # Get heatmap data
        map_data = helper.activity_heat_map(selected_user, df)

        # Set larger figure size and higher DPI
        fig, ax = plt.subplots(figsize=(14, 6), dpi=200)

        # Draw heatmap
        sns.heatmap(
            map_data,
            ax=ax,
            cmap="coolwarm",  # Or try: "rocket_r", "magma", "viridis"
            cbar=True,
            square=False,  # Allow rectangular cells
            xticklabels=True,
            yticklabels=True,
            linewidths=0,  # No gridlines
            linecolor=None,
            cbar_kws={
                'label': 'Message Count',
                'orientation': 'vertical',
                'shrink': 0.7,  # Shrink colorbar size
                'format': '%d'
            }
        )

        # Axis labels
        ax.set_xlabel("Hour Period", fontsize=12, color='white')
        ax.set_ylabel("Day of Week", fontsize=12, color='white')

        # Tick styling
        ax.tick_params(axis='x', colors='white', labelsize=9)
        ax.tick_params(axis='y', colors='white', labelsize=9)

        # Rotation
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)

        # Tight layout to avoid cutoff
        plt.tight_layout()

        # Display in Streamlit
        st.pyplot(fig)





        import plotly.graph_objects as go
        st.title("Messages by Day of the Week")

        # Get the daily message breakdown by weekday
        daily_days = helper.days_timeline(selected_user, df)

        # Ensure correct day order (optional but recommended)
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_days['day_name'] = pd.Categorical(daily_days['day_name'], categories=day_order, ordered=True)
        daily_days = daily_days.sort_values('day_name')

        # Create the interactive line chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_days['day_name'],
            y=daily_days['count'],
            mode='lines+markers',
            line=dict(color='#FF1E56', width=2),
            marker=dict(size=6),
            hovertemplate="%{x} : %{y} messages",
            name=''
        ))

        # Style the layout
        fig.update_layout(

            xaxis_title='Day',
            yaxis_title='Number of Messages',
            xaxis_tickangle=45,
            xaxis_title_font=dict(size=20, color='#900C3F'),
            yaxis_title_font=dict(size=20, color='#C70039'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(bgcolor="black", font_size=14)
        )

        # Show the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        #Most Active Hours
        #Finding the Busiest Users in the Groups(Group Level){By using the Interactive plotly}
        if selected_user =="Overall":
            st.title("Most Busy Users")
            x= helper.most_busy(df)

            df_plot = x.reset_index()
            df_plot.columns = ['User','Messages']


            # Plotly Interaction bar chart

            fig = px.bar(
                df_plot,
                x='User',
                y='Messages',

                color_discrete_sequence=['#FF1E56'],
                labels={'Messages':'No. of Messages', 'User':'Users'},
                hover_data={'User':True,'Messages':True},
            )
            fig.update_layout(
                xaxis_title_font=dict(size=20,color='#900C3F'),
                yaxis_title_font=dict(size=20,color='#C70039'),
                xaxis_tickangle=90,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )

            st.plotly_chart(fig, use_container_width=True)







        # Finding the Busiest Users in the Groups(Group Level){By using the matplotlib}
        # if selected_user == "Overall":
        #     st.title("Most Busy Users")
        #     x=helper.most_busy(df)
        #     fig, ax = plt.subplots()
        #
        #
        #     col1,col2  = st.columns(2)
        #     with col1:
        #         # font1 = {'family' : 'sans-serif','color':'Blue','size': 20}
        #         # font2 = {'family' : 'sans-serif','color':'red','size': 20}
        #
        #         font1 = {'family': 'sans-serif', 'color': '#900C3F', 'size': 20}  # Deep Maroon for X-axis
        #         font2 = {'family': 'sans-serif', 'color': '#C70039', 'size': 20}  # Crimson Red for Y-axis
        #
        #         # ax.bar(x.index, x.values,color='red')
        #         ax.bar(x.index, x.values,color='#FF1E56' )
        #
        #         plt.xlabel("Users",fontdict=font1)
        #         plt.ylabel("No.of Messages",fontdict=font2)
        #         plt.xticks(rotation='vertical')
        #         st.pyplot(fig)

#Working with the wordcloud
        st.title("Most Spoken Words")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots(dpi=200)


        plt.imshow(df_wc)
        st.pyplot(fig)
#most Common Words
        # dfa=helper.most_common_words(selected_user,df)
        # st.dataframe(dfa)

        st.title("Most Common Words")



        #graphs
        import plotly.graph_objects as go
        
        dfa = helper.most_common_words(selected_user, df)
        
        # Check if there are any words to plot
        if not dfa.empty:
        
            # Compute angles safely
            angles_deg = np.linspace(0, 360, len(dfa), endpoint=False)
        
            # Create polar bar chart
            fig = go.Figure()
        
            fig.add_trace(go.Barpolar(
                r=dfa['freq'],
                theta=angles_deg,
                width=[360 / len(dfa)] * len(dfa),
                marker_color=dfa['freq'],
                marker_colorscale='Turbo',
                marker_line_color='white',
                marker_line_width=2,
                opacity=0.85,
                text=dfa["word"],
                hoverinfo="text+r"
            ))
        
            fig.update_layout(
                polar=dict(
                    bgcolor='#0e1117',
                    radialaxis=dict(visible=False),
                    angularaxis=dict(
                        tickmode='array',
                        tickvals=angles_deg,
                        ticktext=dfa["word"],
                        direction="clockwise",
                        rotation=90
                    ),
                ),
                showlegend=False,
                paper_bgcolor='#0e1117',
                font=dict(size=12, color='white')
            )
        
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.warning("Not enough data to display the most common words chart.")


        #emoji Ananlysis

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Frequency Analysis")

        import pandas as pd
        import plotly.graph_objects as go

        # Emoji frequency data

        emoji_df.columns = ['emoji', 'count']
        #to sort the frequency of the emojis
        emoji_df = emoji_df.sort_values(by='count', ascending=False).reset_index(drop=True)

        # Create base frame (all zeros)
        base_counts = [0] * len(df)

        # Create initial figure with zeroed bars
        fig = go.Figure(
            data=[go.Bar(
                y=emoji_df['emoji'],
                x=base_counts,
                orientation='h',
                text=emoji_df['emoji'],
                textposition='inside',
                insidetextanchor='middle',
                marker=dict(
                    color='rgba(100,149,237,0.8)',
                    line=dict(color='rgba(100,149,237,1)', width=3),
                ),
                hovertemplate='<b>%{y}</b><br>Frequency: %{x}<extra></extra>',
                width=0.6,
            )]
        )

        # Define animation frames — one by one, but keeping all shown
        frames = []
        for i in range(len(emoji_df)):
            frame_counts = emoji_df['count'].copy()
            for j in range(i + 1, len(emoji_df)):
                frame_counts.iloc[j] = 0  # Hide only future ones
            frames.append(go.Frame(
                data=[go.Bar(x=frame_counts)],
                name=f"frame{i}"
            ))

        # Attach frames
        fig.frames = frames

        # Layout with autoplaying animation
        fig.update_layout(

            xaxis=dict(range=[0, max(emoji_df['count']) * 1.2], showgrid=False),
            yaxis=dict(tickfont=dict(size=20)),
            bargap=0.3,
            height=600,
            plot_bgcolor='#0e1117',
            margin=dict(l=100, r=40, t=80, b=40),
            showlegend=False,
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [{
                    "label": "Play",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 500, "redraw": True},
                        "mode": "immediate",
                        "fromcurrent": True,
                        "transition": {"duration": 300}
                    }]
                }]
            }],
        )

        # Start animation automatically
        fig.update_layout(
            sliders=[],
            transition={"duration": 300, "easing": "cubic-in-out"},
        )

        # Automatically play when loaded
        # figa=fig.show(config={'scrollZoom': False, 'displayModeBar': False})
        st.plotly_chart(fig, use_container_width=True)






