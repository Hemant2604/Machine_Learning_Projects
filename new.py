import streamlit as st

st.set_page_config(page_title="💌 A Letter for Someone Special", layout="centered")

if "card_step" not in st.session_state:
    st.session_state.card_step = 1
if "accepted" not in st.session_state:
    st.session_state.accepted = False

def next_card():
    st.session_state.card_step += 1

st.markdown("""
<style>
body { background: #fefcf9; }
.letter-drop {
    animation: fadeInUp 1s ease forwards;
}
@keyframes fadeInUp {
    0% { transform: translateY(50px) rotate(-2deg); opacity: 0; }
    100% { transform: translateY(0) rotate(0); opacity: 1; }
}
.love-letter {
    background: #fdf6e3;
    padding: 30px;
    border: 2px solid #c0a080;
    border-radius: 12px;
    font-family: 'Georgia', serif;
    color: #4e342e;
    line-height: 1.8;
    box-shadow: 0 8px 12px rgba(0,0,0,0.08);
    transition: all 0.6s ease-in-out;
    max-width: 500px;
    margin: 0 auto;
}
h2 { 
    font-family: 'Lucida Handwriting', cursive; 
    text-align: center; 
    color: #5d4037; 
    font-weight: normal; 
}
p { text-align: center; font-size: 16px; }
.button-area { text-align: center; margin-top: 20px; }
.custom-btn {
    background: #6d4c41;
    color: #fff;
    padding: 10px 24px;
    border: none;
    border-radius: 10px;
    margin: 10px;
    font-size: 16px;
    cursor: pointer;
    transition: 0.3s ease;
}
.custom-btn:hover { background: #3e2723; }
</style>
""", unsafe_allow_html=True)

st.title("💌 A Letter for Someone Special")

messages = [
    "Hi Nehal 👋",
    "How are you?",
    "Yeah... I know you don't know me, but I knew you for a while now.",
    "I think we met in my dreams, right? 🌙",
    "Hehe... nothing serious, but I wish we could chat.✨",
    "Nehal, can you chat with me?"
]

if st.session_state.card_step <= len(messages):
    st.markdown(f"""
    <div class="love-letter letter-drop">
        <h2>{messages[st.session_state.card_step - 1]}</h2>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Next ➡"):
        next_card()

elif st.session_state.card_step > len(messages) and not st.session_state.accepted:
    st.markdown("""
    <div class="love-letter letter-drop">
        <h2>Nehal, would you like to talk to me? 💌</h2>
        <p>I promise it will be worth your while ☕</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("YES 💖"):
            st.session_state.accepted = True
    with col2:
        if st.button("NO 🙅‍♀"):
            st.warning("Please Nehal... 🥺 just once, say YES? 💌")

if st.session_state.accepted:
    st.markdown("""
    <div class="love-letter letter-drop">
        <h2>Thank you, Nehal! 🌸</h2>
        <p>
        waiting for your message like a letter waits for a reader... 💕
        </p>
    </div>
    """, unsafe_allow_html=True)