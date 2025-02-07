import streamlit as st

def footer():
    st.markdown(
        """
        <style>
        .footer {
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 0);  /* 투명한 배경 */
            text-align: left;
            padding: 10px;
            color: white;
        }
        </style>
        <div class="footer">
            <p>© Naver Boostcourse AI Tech 7th Team Medvision. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
