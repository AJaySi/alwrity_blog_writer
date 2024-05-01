import time #Iwish
import os
import json
import requests
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import google.generativeai as genai


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity - AI Blog Writer",
        layout="wide",
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"""
      <style>
      [class="st-emotion-cache-7ym5gk ef3psqc12"]{{
            display: inline-block;
            padding: 5px 20px;
            background-color: #4681f4;
            color: #FBFFFF;
            width: 300px;
            height: 35px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 8px;’
      }}
      </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI Blog Post Generator")

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        input_blog_keywords = st.text_input('**Enter main keywords of your blog!** (Blog Title Or Content Topic)')
        col1, col2, space, col3 = st.columns([5, 5, 0.5, 5])
        with col1:
            blog_type = st.selectbox('Choose Blog Post Type', ('General', 'How-to Guides', 'Polls', 'Listicles', 
                'Reality check posts', 'Job Posts', 'FAQs', 'Checklists/Cheat Sheets'), index=0)
        with col2:
            input_blog_tone = st.selectbox('Choose Blog Tone', ('General', 'Professional', 'Casual'), index=0)
        with col3:
            input_blog_language = st.selectbox('Choose Language', ('English', 'Vietnamese',
                'Chinese', 'Hindi', 'Spanish'), index=0)
        # Generate Blog FAQ button
        if st.button('**Write Blog Post**'):
            with st.spinner():
                # Clicking without providing data, really ?
                if not input_blog_keywords:
                    st.error('** 🫣Provide Inputs to generate Blog Post. Keywords, Required!**')
                elif input_blog_keywords:
                    blog_post = generate_blog_post(input_blog_keywords, blog_type, 
                            input_blog_tone, input_blog_language)
                    if blog_post:
                        st.subheader('**🧕🔬👩 Your Final Blog Post!**')
                        st.write(blog_post)
                    else:
                        st.error("💥**Failed to generate blog Post. Please try again!**")


# Function to generate blog metadesc
def generate_blog_post(input_blog_keywords, input_type, input_tone, input_language):
    """ Function to call upon LLM to get the work done. """

    # Fetch SERP results & PAA questions for FAQ.
    try:
        serp_results, people_also_ask = get_serp_results(input_blog_keywords)
    except Exception as err:
        st.error(f"Failed to do Google search for {input_blog_keywords}")

    # If keywords and content both are given.
    if serp_results:
        prompt = f"""
        You are Alwrity, SEO expert & {input_language} Creative Content writer. 
        You are an expert content writer for {input_type} of blog posts.
        You excels at creating a introductions that attract users, to read more.

        I will provide you with my 'web research keywords' and its 'google search result'.
        Your goal is to create detailed SEO-optimized content and also include 5 FAQs.
        

        Follow below guidelines:
        1). Your blog content should compete against all blogs from search results.
        2). Your FAQ should be based on 'People also ask' and 'Related Queries' from given search result. 
            Always include answers for each FAQ, use your knowledge and confirm with snippets given in search result.
        3). Act as subject matter expert for given research keywords: {input_blog_keywords}.
        4). Your blog should be highly formatted in markdown style and highly readable.
        5). Always write in the first person, adopting {input_tone} voice of tone.
        6). Inject Your Unique Voice and Style: Add personal insights, anecdotes, or experiences to infuse authenticity and humanize the content, making it engaging and authentic.
        6). Important to provide your response in {input_language} language.\n

        blog keywords: '{input_blog_keywords}'\n
        google serp results: '{serp_results}'
        people_also_ask: '{people_also_ask}'
        """
        blog_post = generate_text_with_exception_handling(prompt)
        return blog_post


def get_serp_results(search_keywords):
    """ """
    serp_results = perform_serperdev_google_search(search_keywords)
    people_also_ask = [item.get("question") for item in serp_results.get("peopleAlsoAsk", [])]
    return serp_results, people_also_ask


def perform_serperdev_google_search(query):
    """
    Perform a Google search using the Serper API.

    Args:
        query (str): The search query.

    Returns:
        dict: The JSON response from the Serper API.
    """
    # Get the Serper API key from environment variables
    serper_api_key = os.getenv('SERPER_API_KEY')

    # Check if the API key is available
    if not serper_api_key:
        st.error("SERPER_API_KEY is missing. Set it in the .env file.")

    # Serper API endpoint URL
    url = "https://google.serper.dev/search"
    # FIXME: Expose options to end user. Request payload
    payload = json.dumps({
        "q": query,
        "gl": "in",
        "hl": "en",
        "num": 10,
        "autocorrect": True,
        "page": 1,
        "type": "search",
        "engine": "google"
    })

    # Request headers with API key
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    # Send a POST request to the Serper API with progress bar
    with st.spinner("Searching Google..."):
        response = requests.post(url, headers=headers, data=payload, stream=True)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code}, {response.text}")



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()
