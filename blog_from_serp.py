import time
import os
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential
import google.generativeai as genai
from exa_py import Exa


def main():
    # Set page configuration
    st.set_page_config(page_title="Alwrity - AI Blog Writer", layout="wide")
    
    # Apply custom CSS for styling and scrollbar
    st.markdown("""
        <style>
            /* Use color palette reminiscent of your reference image */
            /* Shades of Blue: #0073B1, #00BCD4, #F1F8FF, etc. */
            
            /* Page Background */
            body {
                background-color: #F1F8FF;
            }

            /* Container (no functionality change) */
            .block-container {
                padding: 1rem 2rem;
                font-family: "Open Sans", sans-serif;
                max-width: 1100px;
                margin: auto;
            }

            /* Headings: use a bold, dark blue #0073B1 */
            h1, h2, h3, h4, h5, h6 {
                color: #0073B1 !important;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }

            /* Subtle text color for paragraphs */
            p, div, label {
                color: #444444;
            }

            /* Buttons: gradient with a slight hover effect */
            div.stButton > button:first-child {
                background: linear-gradient(135deg, #0073B1 0%, #00BCD4 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.3s ease;
            }
            div.stButton > button:first-child:hover {
                background: linear-gradient(135deg, #005A86 0%, #00A0B8 100%);
            }

            /* Panels or "card" style for key sections */
            .stExpander, .stTabs, .stTextInput, .stSelectbox {
                border: 1px solid #00BCD4 !important;
                background-color: #ffffff;
                border-radius: 6px;
            }

            /* Tooltip style (if you have tooltips) */
            .tooltip {
                position: relative;
                border-bottom: 1px dotted #333;
                cursor: help;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 200px;
                background-color: #333;
                color: #fff;
                text-align: center;
                border-radius: 4px;
                padding: 6px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }

            /* Scrollbar: a subtle custom style in line with your palette */
            ::-webkit-scrollbar {
                width: 12px;
            }
            ::-webkit-scrollbar-track {
                background: #E1EBF9;
            }
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #0073B1, #00BCD4);
                border-radius: 6px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ ALwrity - AI Blog Post Generator")
    st.markdown("Create high-quality blog content effortlessly with our AI-powered tool. Ideal for bloggers and content creators. 🚀")

    # API Key Input Section
    with st.expander("**API Configuration** 🔑", expanded=False):
        st.markdown("If the default API keys are unavailable or exceed their limits, you can provide your own API keys below.")

        # Input fields for Metaphor and Gemini API keys
        user_metaphor_api_key = st.text_input("**Metaphor API Key**", type="password", help="Provide your Metaphor API Key if the default key is unavailable.")
        user_gemini_api_key = st.text_input("**Gemini API Key**", type="password", help="Provide your Gemini API Key if the default key is unavailable.")

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below. 📝", expanded=True):
        input_blog_keywords = st.text_input('**Enter main keywords of your blog!** (Blog Title Or Content Topic)', 
                                            help="The main topic or title for your blog.")
        
        col1, col2, col3 = st.columns([5, 5, 5])
        
        with col1:
            blog_type = st.selectbox('**Choose Blog Post Type** 📄', 
                                     options=['General', 'How-to Guides', 'Listicles', 'Job Posts', 'Cheat Sheets', 'Customize'], 
                                     index=0)
            if blog_type == 'Customize':
                blog_type = st.text_input("**Enter your custom blog type**", help="Provide a custom blog type if you chose 'Customize'.")
        
        with col2:
            input_blog_tone = st.selectbox('**Choose Blog Tone** 🎨', 
                                           options=['General', 'Professional', 'Casual', 'Customize'], 
                                           index=0)
            if input_blog_tone == 'Customize':
                input_blog_tone = st.text_input("**Enter your custom blog tone**", help="Provide a custom blog tone if you chose 'Customize'.")
        
        with col3:
            input_blog_language = st.selectbox('**Choose Language** 🌐', 
                                               options=['English', 'Vietnamese', 'Chinese', 'Hindi', 'Spanish', 'Customize'], 
                                               index=0)
            if input_blog_language == 'Customize':
                input_blog_language = st.text_input("**Enter your custom language**", help="Provide a custom language if you chose 'Customize'.")

        # Generate Blog FAQ button
        if st.button('**Write Blog Post ✍️**'):
            with st.spinner('Generating your blog post...'):
                # Input validation
                if not input_blog_keywords:
                    st.error('**🫣 Provide Inputs to generate Blog Post. Keywords are required!**')
                else:
                    # Use user-provided API keys if available
                    metaphor_api_key = user_metaphor_api_key or os.getenv('METAPHOR_API_KEY')
                    gemini_api_key = user_gemini_api_key or os.getenv('GEMINI_API_KEY')

                    if not metaphor_api_key:
                        st.error("❌ **Metaphor API Key is not available! Please provide your API key in the API Configuration section.**")
                        return
                    if not gemini_api_key:
                        st.error("❌ **Gemini API Key is not available! Please provide your API key in the API Configuration section.**")
                        return

                    try:
                        blog_post = generate_blog_post(input_blog_keywords, blog_type, input_blog_tone, input_blog_language, metaphor_api_key, gemini_api_key)
                        if blog_post:
                            st.subheader('**🧕🔬👩 Your Final Blog Post!**')
                            st.write(blog_post)
                        else:
                            st.error("💥 **Failed to generate blog post. Please try again!**")
                    except Exception as e:
                        if "quota exceeded" in str(e).lower():
                            st.error("❌ **API limit exceeded! Please provide your own API key in the API Configuration section.**")
                        else:
                            st.error(f"💥 **An unexpected error occurred: {e}**")


# Function to generate the blog post using the LLM
def generate_blog_post(input_blog_keywords, input_type, input_tone, input_language, metaphor_api_key, gemini_api_key):
    serp_results = None
    try:
        serp_results = metaphor_search_articles(input_blog_keywords, metaphor_api_key)
    except Exception as err:
        st.error(f"❌ Failed to retrieve search results for {input_blog_keywords}: {err}")
    
    if serp_results:
        prompt = f"""
        You are ALwrity, an experienced SEO specialist and creative content writer who crafts blog posts with a personal, authentic voice. You write {input_type} blog posts in {input_language} that not only rank well in search results but also resonate with readers as if written by a human.
        Your task is to create a comprehensive, engaging, and SEO-optimized blog post on the topic below. The post should incorporate natural storytelling elements, personal insights, and relatable language that sounds genuine and warm. Use the research keywords and Google search results provided to shape your content, ensuring you capture the nuances of current trends and reader interests.

        Requirements:
        1. The content must compete effectively against existing blogs found in the search results.
        2. Include 5 FAQs derived from “People also ask” queries and related search suggestions, each with thoughtful, well-articulated answers.
        3. Format the blog in markdown, ensuring a clean and accessible layout.
        4. Write in a conversational yet informative style that reflects a {input_tone} tone, balancing professionalism with a personable touch.
        5. Use clear, natural language and include personal anecdotes or insights where appropriate to enhance readability and authenticity.
        6. Additionally, after the main blog content, append the following SEO metadata:
            - A **Blog Title**
            - A **Meta Description** that summarizes the blog post.
            - A **URL slug** that is short, easy to read, and formatted in lowercase with hyphens.
            - A list of **Hashtags** relevant to the content.
        7. The final blog post should clearly demonstrate experience, expertise, authoritativeness, and trustworthiness.

        Blog keywords: {input_blog_keywords}
        Google SERP results: {serp_results}
        """
        return generate_text_with_exception_handling(prompt, gemini_api_key)
    return None


# Metaphor search function
def metaphor_search_articles(query, api_key):
    if not api_key:
        raise ValueError("Metaphor API Key is missing!")

    metaphor = Exa(api_key)
    
    try:
        search_response = metaphor.search_and_contents(query, use_autoprompt=True, num_results=5)
        return search_response.results
    except Exception as err:
        st.error(f"Failed in metaphor.search_and_contents: {err}")
        return None


# Exception handling for text generation
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config={"max_output_tokens": 8192})
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text
    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()

