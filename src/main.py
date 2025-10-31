import streamlit as st
import asyncio
import re
from langchain_core.messages import HumanMessage
from agent import make_agent  # Assuming this is the correct import

@st.cache_resource
def load_agent():
    return make_agent()

def setup_page():
    """Setup Streamlit page configuration and styles"""
    st.set_page_config(page_title="Project Samarth", layout="centered")
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
        
        html {
            font-size: 16px;
        }

        body {
            font-family: 'Google Sans', sans-serif;
        }
        
        .multicolor-title {
            font-family: 'Google Sans', sans-serif;
            font-size: 3.0rem; 
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #4285F4, #EA4335);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 2.0rem; 
            letter-spacing: -0.03125rem;
        }
        
        .question-label {
            font-family: 'Google Sans', sans-serif;
            font-size: 1.1rem;
            font-weight: 500;
            color: #5f6368;
            margin-bottom: 0.5rem;
            text-align: center;
            display: block;
        }
        
        .stTextArea textarea {
            font-family: 'Google Sans', sans-serif !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            min-height: 8rem; 
        }
        
        /* --- Gradient CSS for the submit button has been REMOVED --- */
        
        [data-testid="stForm"] > div {
            gap: 1rem;
        }
        
        </style>
        """, unsafe_allow_html=True)

def clean_response(response: str) -> str:
    """
    Cleans the agent's final string response.
    - Removes any stray SQL code blocks.
    - Leaves the citation block (which is plain markdown) intact.
    """
    print("CLEANING RESPONSE:", type(response))
    
    # Ensure we are working with a string
    if not isinstance(response, str):
        response = str(response)

    # This regex ONLY removes markdown blocks specifically tagged with "sql"
    # It will NOT remove your citation block, which doesn't have "sql".
    cleaned = re.sub(r'```sql.*?```', '', response, flags=re.DOTALL)
    
    cleaned = cleaned.strip()
    
    # If cleaning results in an empty string, return a user-friendly message.
    if not cleaned:
        # This is the line you were seeing. It's a fallback.
        return "Analysis completed. Please check the data sources for detailed information."
    
    return cleaned
def main():
    setup_page()
    
    st.markdown('<div class="multicolor-title">Project Samarth</div>', unsafe_allow_html=True)
    st.markdown('<span class="question-label">Ask questions about Indian crop production or rainfall trends</span>', unsafe_allow_html=True)

    agent = load_agent()

    SAMPLE_PROMPT = "Compare average rainfall and wheat production in Rajasthan for 2010."

    # --- STATE LOGIC ---
    
    if "text_value" not in st.session_state:
        st.session_state.text_value = ""
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = None
    if "last_response" not in st.session_state:
        st.session_state.last_response = None

    if st.session_state.last_prompt:
        with st.chat_message("user"):
            st.markdown(st.session_state.last_prompt)
        with st.chat_message("assistant"):
            if "Sorry," in st.session_state.last_response:
                st.error(st.session_state.last_response)
            else:
                st.markdown(st.session_state.last_response)
    
    prompt_to_submit = None
    
    # --- FORM ---
    with st.form(key="query_form"):
        question = st.text_area(
            "Question",
            placeholder=SAMPLE_PROMPT,
            label_visibility="collapsed",
            value=st.session_state.text_value 
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            sample_clicked = st.form_submit_button(
                "Ask a sample prompt",
                use_container_width=True,
                type="secondary" # This is the default grey button
            )
            
        with col2:
            submitted = st.form_submit_button(
                "Submit",
                use_container_width=True
                # This is now the default primary (blue) button
            )
    
    # --- FORM LOGIC ---
    
    if sample_clicked:
        prompt_to_submit = SAMPLE_PROMPT
        st.session_state.text_value = ""

    elif submitted:
        if question:
            prompt_to_submit = question
            st.session_state.text_value = ""
        else:
            st.warning("Please enter a question.")
            st.session_state.last_prompt = None 
            st.session_state.last_response = None
    
    else:
        st.session_state.text_value = question

    # --- AGENT LOGIC ---
    if prompt_to_submit:
        st.session_state.last_prompt = prompt_to_submit
        
        with st.chat_message("user"):
            st.markdown(prompt_to_submit)
        
        with st.chat_message("assistant"):
            with st.spinner("Finding out the answer for you!"):
                try:
                    config = {"recursion_limit": 50}
                    result = agent.invoke(
                        {"messages": [HumanMessage(content=prompt_to_submit)]},
                        config=config
                    )
                    final_response = result["messages"][-1].content
                    
                    # Debug: Print raw response to understand the structure
                    print("RAW RESPONSE TYPE:", type(final_response))
                    print("RAW RESPONSE CONTENT:", final_response)
                    
                    # Clean the response using our improved function
                    cleaned_response = clean_response(final_response)
                    print("CLEANED RESPONSE:", cleaned_response)
                    
                    st.session_state.last_response = cleaned_response
                    
                except Exception as e:
                    error_msg = f"Sorry, I couldn't get the answer for you :( {str(e)}"
                    st.session_state.last_response = error_msg
        
        st.rerun()

if __name__ == "__main__":
    main()