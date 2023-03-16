import streamlit as st
import gspread
import streamlit.components.v1 as components
import random
import pandas as pd
from datetime import datetime




def get_youtube_html(video_id, t_start, t_end, height=360, width=640):
    html = """<div id="ytplayer"></div>
        <script>
        // Load the IFrame Player API code asynchronously.
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/player_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        // Replace the 'ytplayer' element with an <iframe> and
        // YouTube player after the API code downloads.
        var player;
        function onYouTubePlayerAPIReady() {
            player = new YT.Player('ytplayer', {
                height: '%s',
                width: '%s',
                videoId: '%s',
                rel: '0',
    
                playerVars: {
                    'controls': 0,
                    'disablekb': 0  ,
                    'start': '%s',
                    'end': '%s',
                    'rel': 0,
                    'modestbranding': 1,
                    'showinfo': 0,
                    'autoplay': 0,
                    'title': ''
                }
            });
        }
        </script>""" % (height, width, video_id, t_start, t_end)
    return html

def get_youtube_html2(video_id, t_start, t_end, height=360, width=640):
    html = f"""
        <style>
            #playerWrap {{
                display: inline-block;
                position: relative;
            }}
            #playerWrap.shown::after {{
                content:"";
                position: absolute;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                cursor: pointer;
                background-color: black;
                background-repeat: no-repeat;
                background-position: center; 
                background-size: 64px 64px;
                background-image: url(data:image/svg+xml;utf8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiB2aWV3Qm94PSIwIDAgNTEwIDUxMCI+PHBhdGggZD0iTTI1NSAxMDJWMEwxMjcuNSAxMjcuNSAyNTUgMjU1VjE1M2M4NC4xNSAwIDE1MyA2OC44NSAxNTMgMTUzcy02OC44NSAxNTMtMTUzIDE1My0xNTMtNjguODUtMTUzLTE1M0g1MWMwIDExMi4yIDkxLjggMjA0IDIwNCAyMDRzMjA0LTkxLjggMjA0LTIwNC05MS44LTIwNC0yMDQtMjA0eiIgZmlsbD0iI0ZGRiIvPjwvc3ZnPg==);
            }}
        </style>
        <div id="playerWrap">
            <div id="ytplayer"></div>
        </div>
        <script>
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/player_api";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

            var player;
            function onYouTubePlayerAPIReady() {{
                player = new YT.Player('ytplayer', {{
                    height: '{height}',
                    width: '{width}',
                    videoId: '{video_id}',
                    playerVars: {{
                        'controls': 0,
                        'disablekb': 0,
                        'start': '{t_start}',
                        'end': '{t_end}',
                        'rel': 0,
                        'modestbranding': 1,
                        'showinfo': 0,
                        'autoplay': 0,
                        'title': ''
                    }},
                    events: {{
                        'onStateChange': onPlayerStateChange
                    }}
                }});
            }}

            function onPlayerStateChange(event) {{
                if (event.data == YT.PlayerState.ENDED) {{
                    document.getElementById("playerWrap").classList.add("shown");
                }}
            }}

            document.getElementById("playerWrap").addEventListener("click", function() {{
                player.seekTo({t_start});
                player.playVideo();
                document.getElementById("playerWrap").classList.remove("shown");
            }});
        </script>
    """
    return html

def submit_vote_to_sheet(sheet_name, row):
    # if streamlit app tested locally, use the following line
    # gc = gspread.service_account_from_dict(st.secrets)
    gc = gspread.service_account_from_dict(st.secrets) # when testing locally
    sh = gc.open(sheet_name)
    sh.sheet1.append_row(row, 2)

def get_covered_chunks_from_sheets(sheet_name):
    gc = gspread.service_account_from_dict(st.secrets) # when testing locally
    sh = gc.open(sheet_name)
    df = pd.DataFrame(sh.sheet1.get_all_records())
    covered_indexes = df.iloc[:,0].tolist()
    return covered_indexes
  

# Initialize the session state for video ID
if 'video_id' not in st.session_state:
    
    df = pd.read_csv("data.csv")
    st.session_state.df = df
    st.session_state.total_chunks = len(df)
    st.session_state.video_ids = df["video_id"].unique().tolist()
    st.session_state.start_times = df["t_first_line"].tolist()
    st.session_state.end_times = df["t_last_line"].tolist()
    st.session_state.chunks_covered = get_covered_chunks_from_sheets("Form-app")
    st.session_state.next_chunk_ix = st.session_state.chunks_covered[-1] + 1
    st.session_state.video_id = st.session_state.video_ids[st.session_state.next_chunk_ix]


ix = st.session_state.next_chunk_ix
id = st.session_state.df.loc[ix, 'video_id']
t_start = int(st.session_state.start_times[ix])
t_end = int(st.session_state.end_times[ix])
if t_start - t_end == 0:
    t_end = t_start + 3
video_height = 360
video_width = 640


user_name = st.text_input("Name")



# page contents
st.title("Tagging Examiner Comments")
components.html(get_youtube_html2(id, t_start, t_end, video_height, video_width), width=video_width, height=video_height)

genre = st.radio(
    "The described situation happens...",
    ("before the fragment.", "during the fragment.", "after the fragment.", "unclear (default)"), index=3)

criticality = st.slider("How critical is the described situation?", 0, 10, 0)
# checkboxes: The situation that's described is "taking place during the fragment", "taking place before the fragment", "taking place after the fragment"




sentiment = st.slider("Overall sentiment", 0, 10, 0)

happiness = st.select_slider(
    'How happy is the examiner?',
    options=['very unhappy', 'unhappy', 'neutral', 'happy', 'very happy'], value='neutral')

comment = st.text_area("Comment")

if st.button("Next"):
    # if user_name is empty, ask user to enter name
    if not user_name:
        st.error("Please enter your name.")
    else:
        # create timestamp in str format
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        submit_vote_to_sheet("Form-app", [st.session_state.next_chunk_ix, user_name, criticality, sentiment, happiness, comment, timestamp])
        
        st.session_state.next_chunk_ix += 1
        st.experimental_rerun()

with st.expander("More info about the video"):
    st.write("GPT-enhanced transcript:")
    st.write(st.session_state.df.loc[ix, 'response_2'])
    st.write("Chunk index", ix)
    st.write("Video ID", id)
    st.write("Start time", t_start)
    st.write("End time", t_end)
    st.write("Duration", t_end - t_start)
    st.write("Original transcript:")
    st.write(st.session_state.df.loc[ix, 'text'])
    
    







