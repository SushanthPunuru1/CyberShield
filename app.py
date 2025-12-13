import streamlit as st
import google.generativeai as genai


genai.configure(api_key = "AIzaSyBZnlIWxjCWCtq0MUxmigAGyprZLf-9tiQ")


model = genai.GenerativeModel("gemini-2.5-flash")


import streamlit as st


st.title("Social Engineering & Phishing Detector")
st.write("Welcome to the Social Engineering & Phishing Detector app.")


name = st.text_input("Enter your name:")


content = st.text_area("Paste the content of the message/email you received:")


st.header("Survey")
howRecieved = st.text_input("How did you receive this message?")
youKnow = st.text_input("Is the sender someone you know?")
claimedAcc = st.text_input("Do you have an account with the claimed sender?")
actionTaken = st.text_input("Was any action already taken?")
previousCom = st.text_input("Previous communication with this sender?")
deviceUsed = st.text_input("Device used to receive/open the message?")
region = st.text_input("Your region/country?")


concernLevel = st.slider("How concerned are you (1–10)?", 1, 10, 5)


messageType = st.radio(
    "Message type:",
    ('Email', 'SMS/Text Message', 'Social Media Message', 'Instant Message', 'Other')
)


st.sidebar.header("Phishing URL Checker")
phishingUrl = st.sidebar.text_input("Enter URL:")


if st.sidebar.button("Check URL"):
    prompt = f"""
    You are an AI cybersecurity analyst.
    Analyze the following URL for phishing risks:


    URL: {phishingUrl}


    Provide a simple explanation of:
    - Risk level
    - Why it may be dangerous
    - What the user should do next
    """
    urlAnalysis = model.generate_content(prompt)
    st.write(urlAnalysis.text)


if st.button("Analyze Message"):
    prompt = f"""
    You are an AI cybersecurity analyst analyzing a potentially malicious message.


    Message content:
    {content}


    Context:
    - Message type: {messageType}
    - How received: {howRecieved}
    - Know sender: {youKnow}
    - Claimed account: {claimedAcc}
    - Action taken: {actionTaken}
    - Previous communication: {previousCom}
    - Device used: {deviceUsed}
    - Region: {region}
    - User concern level: {concernLevel}/10


    Tasks:
    1. Identify social engineering tactics.
    2. Identify phishing indicators.
    3. Give Social Engineering Risk (Low/Medium/High).
    4. Give Phishing Risk (Low/Medium/High).
    5. Highlight suspicious phrases or links.
    6. Provide simple next steps.
    """


    result = model.generate_content(prompt)
    st.write(result.text)