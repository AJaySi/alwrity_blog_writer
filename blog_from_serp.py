import time
import os
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential
from google import genai
from exa_py import Exa


def main():
    # Set page configuration
    st.set_page_config(page_title="Alwrity - AI Blog Writer", layout="wide")
    
    # --- ALwrity Theme: Only use proven working CSS selectors ---
    st.markdown("""
        <style>
        ::-webkit-scrollbar-track {
            background: #e1ebf9;
        }
        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }
        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hide Streamlit header and footer for a clean look
    st.markdown('<style>header {visibility: hidden;}</style>', unsafe_allow_html=True)
    st.markdown('<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>', unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI Blog Post Generator")
    st.markdown("Create high-quality blog content effortlessly with our AI-powered tool. Ideal for bloggers and content creators. 🚀")

    # API Key Input Section
    with st.expander("API Configuration 🔑", expanded=False):
        st.markdown('''If the default API keys are unavailable or exceed their limits, you can provide your own API keys below.<br>
        <a href="https://metaphor.systems/" target="_blank">Get Metaphor API Key</a><br>
        <a href="https://aistudio.google.com/app/apikey" target="_blank">Get Gemini API Key</a>
        ''', unsafe_allow_html=True)
        user_metaphor_api_key = st.text_input("Metaphor API Key", type="password", help="Paste your Metaphor API Key here if you have one.")
        user_gemini_api_key = st.text_input("Gemini API Key", type="password", help="Paste your Gemini API Key here if you have one.")

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below. 📝", expanded=True):
        # Full-width prompt/keywords input to match API key input width
        input_blog_keywords = st.text_area(
            "**🔑 Enter main keywords of your blog!** (Blog Title Or Content Topic)",
            height=80,
            placeholder="You can write a complete sentence or multiple keywords, e.g., 'How to start a vegetable garden in small spaces'.",
            help="Write a full sentence or provide multiple keywords for better results."
        )

        col1, col2, col3 = st.columns([5, 5, 5])
        with col1:
            blog_type = st.selectbox('📝 Blog Post Type', options=['General', 'How-to Guides', 'Listicles', 'Job Posts', 'Cheat Sheets', 'Customize'], index=0)
            if blog_type == 'Customize':
                blog_type = st.text_input("Enter your custom blog type", help="Provide a custom blog type if you chose 'Customize'.")
        with col2:
            input_blog_tone = st.selectbox('🎨 Blog Tone', options=['General', 'Professional', 'Casual', 'Customize'], index=0)
            if input_blog_tone == 'Customize':
                input_blog_tone = st.text_input("Enter your custom blog tone", help="Provide a custom blog tone if you chose 'Customize'.")
        with col3:
            input_blog_language = st.selectbox('🌐 Language', options=['English', 'Vietnamese', 'Chinese', 'Hindi', 'Spanish', 'Customize'], index=0)
            if input_blog_language == 'Customize':
                input_blog_language = st.text_input("Enter your custom language", help="Provide a custom language if you chose 'Customize'.")

        # Generate Blog Button
        if st.button('**Write Blog Post ✍️**'):
            with st.spinner('Generating your blog post...'):
                if not input_blog_keywords:
                    st.error('**🫣 Provide Inputs to generate Blog Post. Keywords are required!**')
                else:
                    metaphor_api_key = user_metaphor_api_key or os.getenv('METAPHOR_API_KEY')
                    gemini_api_key = user_gemini_api_key or os.getenv('GEMINI_API_KEY')
                    if not metaphor_api_key:
                        st.error("❌ Metaphor API Key is not available! Please provide your API key in the API Configuration section.")
                        return
                    if not gemini_api_key:
                        st.error("❌ Gemini API Key is not available! Please provide your API key in the API Configuration section.")
                        return
                    try:
                        blog_post = generate_blog_post(input_blog_keywords, blog_type, input_blog_tone, input_blog_language, metaphor_api_key, gemini_api_key)
                        if blog_post:
                            st.subheader('**👩🧕🔬 Your Final Blog Post!**')
                            st.write(blog_post)
                        else:
                            st.error("💥 Failed to generate blog post. Please try again!")
                    except Exception as e:
                        if "quota exceeded" in str(e).lower():
                            st.error("❌ API limit exceeded! Please provide your own API key in the API Configuration section.")
                        else:
                            st.error(f"💥 An unexpected error occurred: {e}")


# Function to generate the blog post using the LLM
def generate_blog_post(input_blog_keywords, input_type, input_tone, input_language, metaphor_api_key, gemini_api_key):
    serp_results = None
    try:
        serp_results = metaphor_search_articles(input_blog_keywords, metaphor_api_key)
    except Exception as err:
        st.error(f"❌ Failed to retrieve search results for {input_blog_keywords}: {err}")
    
    if serp_results:
        prompt = f"""
        You are ALwrity, an experienced SEO strategist and creative content writer who specializes in crafting {input_type} blog posts in {input_language}. Your blog posts are designed to rank highly in search results while deeply engaging readers with a professional yet personable tone.

        ### Task:
        Write a comprehensive, engaging, and SEO-optimized blog post on the topic below. The blog should:
        - Be structured for readability with clear headings, subheadings, and bullet points.
        - Include actionable insights, real-world examples, and personal anecdotes to make the content relatable and practical.
        - Be written in a {input_tone} tone that balances professionalism with a conversational style.

        ### Requirements:
        1. **SEO Optimization**:
           - Use the provided keywords naturally and strategically throughout the content.
           - Incorporate semantic keywords and related terms to enhance search engine visibility.
           - Align the content with Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) guidelines.

        2. **Content Structure**:
           - Start with a compelling introduction that hooks the reader and outlines the blog's value.
           - Organize the content with logical headings and subheadings.
           - Breakup text with clear headlines and bullet points for easier reading.
           - Write in active voice and avoid using passive voice.
           - Write in a simple and easy to understand human language.
           - Use words that people would use to look at your blog content and place those words in the blog post.
           - Include a clear CTAs at the end of the blog post.
           - Do not repeate the same words or phrases in the blog post.
           - Do not use fluff words or phrases.
           - Write in a way that is easy to understand and read.
           - Avoid using complex words or phrases.
           - Avoid using jargon words or phrases.
           - Avoid using words that are not related to the topic.
           - Avoid using AI sounding words like realm, evolving, etc.

        3. **Engagement and Value**:
           - Provide actionable tips, real-world examples, and personal anecdotes.
           - Include at least one engaging call-to-action (CTA) to encourage reader interaction.

        4. **FAQs Section**:
           - Include 5 FAQs derived from “People also ask” queries and related search suggestions.
           - Provide thoughtful, well-researched answers to each question.

        5. **Visual and Multimedia Suggestions**:
           - Recommend where to include images, infographics, or videos to enhance the content's appeal.

        6. **References Section**:
           - Include a "References" section after the conclusion but before SEO metadata
           - List all sources used for research with proper citations
           - Use the actual URLs from the search results provided
           - Format as numbered list: [Article Title] - [URL]
           - Include only the article title and clickable link
           
        7. **SEO Metadata**:
           - Append the following metadata after the main blog content:
             - A **Blog Title** that is catchy and includes the primary keyword.
             - A **Meta Description** summarizing the blog post in under 160 characters.
             - A **URL Slug** that is short, descriptive, and formatted in lowercase with hyphens.
             - A list of **Hashtags** relevant to the content.

        ### Blog Details:
        - **Title**: {input_blog_keywords}
        - **Keywords**: {input_blog_keywords}
        - **Google SERP Results**: {serp_results}

        Now, craft an exceptional blog post that stands out in search results and delivers maximum value to readers.
        """
        return generate_text_with_exception_handling(prompt, gemini_api_key)
    return None


# Metaphor search function
def metaphor_search_articles(query, api_key):
    if not api_key:
        raise ValueError("Metaphor API Key is missing!")

    metaphor = Exa(api_key)
    
    try:
        search_response = metaphor.search_and_contents(query, num_results=5)
        return search_response.results
    except Exception as err:
        st.error(f"Failed in metaphor.search_and_contents: {err}")
        return None


# Exception handling for text generation
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt, api_key):
    try:
        # The client automatically picks up the API key from the parameter
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()

