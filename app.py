import streamlit as st
import google.generativeai as genai

# ---------------- CONFIG ----------------
genai.configure(api_key = "API_KEY_VALUE")
genai.configure(api_key = API_KEY_VALUE)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- UI HEADER ----------------
st.title("Social Engineering & Phishing Detector")
st.write("Analyze suspicious messages and URLs to detect phishing and manipulation.")

# ---------------- USER INPUT ----------------
name = st.text_input("Enter your name:")

content = st.text_area(
    "Paste the content of the message/email you received:",
    height=180
)

# ---------------- SURVEY ----------------
st.header("Context Survey")

howRecieved = st.text_input("How did you receive this message? (e.g., email, SMS, Instagram)")

youKnow = st.radio("Is the sender someone you know?", ("No", "Yes"), horizontal=True)
youKnowDetails = st.text_input("Who is the sender?") if youKnow == "Yes" else ""

claimedAcc = st.radio("Do you have an account with the claimed sender?", ("No", "Yes"), horizontal=True)
claimedAccDetails = st.text_input("Which company or service?") if claimedAcc == "Yes" else ""

actionTaken = st.radio("Did you take any action because of this message?", ("No", "Yes"), horizontal=True)
actionTakenDetails = st.text_input("What action did you take?") if actionTaken == "Yes" else ""

previousCom = st.radio("Have you communicated with this sender before?", ("No", "Yes"), horizontal=True)
previousComDetails = st.text_input("Describe prior communication") if previousCom == "Yes" else ""

deviceUsed = st.text_input("What device did you use?")
region = st.text_input("Your region/country?")

concernLevel = st.slider("How concerned are you? (1–10)", 1, 10, 5)

messageType = st.radio(
    "Type of message received:",
    ("Email", "SMS/Text Message", "Social Media", "Instant Message", "Other")
)

# ---------------- SIDEBAR: URL CHECK ----------------
st.sidebar.header("Phishing URL Checker")
phishingUrl = st.sidebar.text_input("Enter a URL:")

if st.sidebar.button("Check URL"):
    if not phishingUrl.strip():
        st.sidebar.error("Please enter a URL.")
    else:
        with st.spinner("Analyzing URL..."):
            try:
                url_prompt = f"""
                You are an AI cybersecurity analyst.

                Analyze the following URL for phishing risks:
                {phishingUrl}

                Provide:
                - Risk level (Low / Medium / High)
                - Why it may be dangerous
                - What the user should do next
                """
                url_result = model.generate_content(url_prompt)
                st.sidebar.write(url_result.text)
            except Exception:
                st.sidebar.error("URL analysis failed. Try again.")

# ---------------- MESSAGE ANALYSIS ----------------
st.divider()

if st.button("Analyze Message"):
    if not content.strip():
        st.error("Please paste a message to analyze.")
    else:
        with st.spinner("Analyzing message..."):
            try:
                prompt = f"""
                You are an AI cybersecurity analyst analyzing a potentially malicious message.

                Message content:
                {content}

                Context:
                - Message type: {messageType}
                - How received: {howRecieved}
                - Know sender: {youKnow} ({youKnowDetails})
                - Claimed account: {claimedAcc} ({claimedAccDetails})
                - Action taken: {actionTaken} ({actionTakenDetails})
                - Previous communication: {previousCom} ({previousComDetails})
                - Device used: {deviceUsed}
                - Region: {region}
                - User concern level: {concernLevel}/10

                Tasks:
                1. Identify social engineering tactics.
                2. Identify phishing indicators.
                3. Give Social Engineering Risk (Low/Medium/High).
                4. Give Phishing Risk (Low/Medium/High).
                5. Highlight suspicious phrases or links.
                6. Provide clear next steps.
                """

                result = model.generate_content(prompt)

                st.subheader("Analysis Results")
                st.write(result.text)

            except Exception:
                st.error("Analysis failed. Please try again.")

# ---------------- FOOTER ----------------
st.caption("⚠️ This tool provides guidance only. Always verify messages independently.")








