import openai
import streamlit as st

st.title("Customer simulator")

openai.api_key = st.secrets["openai"]

#context of the discussion
context= "Evaluate this discussion between a sales person and a customer." 
context+="evaluate if a sales person arguments for a sell are convincing or not."
context+="please evaluate as regard following factors: "
context+="Clarity and Relevance,Credibility,Benefits and Value,Objection Handling,Emotional Appeal,Call to Action,Listening Skills,Comparison and Differentiation,Customer Feedback"

context+="Please provide a rating for the sales person per factor and a global rating"
                
messages = [{"role": "system", "content": context}]

with st.form("input form"):
    st.write("<h3>Enter the discussion between sales and customer ✨</h3>", unsafe_allow_html=True)
    discussion = st.text_input("Enter the discussion text:")

    if st.form_submit_button("Evaluate"):
        if discussion is not None:
            if "openai_model" not in st.session_state:
                st.session_state["openai_model"] = "gpt-3.5-turbo"
            
            if "messages" not in st.session_state:
                st.session_state.messages = messages
            
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            st.session_state.messages.append({"role": "user", "content": discussion})

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
        
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")

            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
