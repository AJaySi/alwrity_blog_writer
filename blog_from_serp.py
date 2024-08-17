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
            .block-container { padding-top: 0rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; }
            ::-webkit-scrollbar-track { background: #e1ebf9; }
            ::-webkit-scrollbar-thumb { background-color: #90CAF9; border-radius: 10px; border: 3px solid #e1ebf9; }
            ::-webkit-scrollbar-thumb:hover { background: #64B5F6; }
            ::-webkit-scrollbar { width: 16px; }
            div.stButton > button:first-child {
                background: #1565C0; color: white; border: none; padding: 12px 24px; 
                border-radius: 8px; text-align: center; display: inline-block; 
                font-size: 16px; margin: 10px 2px; cursor: pointer; 
                transition: background-color 0.3s ease; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI Blog Post Generator")
    st.markdown("Create high-quality blog content effortlessly with our AI-powered tool. Ideal for bloggers and content creators. 🚀")

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
                    blog_post = generate_blog_post(input_blog_keywords, blog_type, input_blog_tone, input_blog_language)
                    if blog_post:
                        st.subheader('**🧕🔬👩 Your Final Blog Post!**')
                        st.write(blog_post)
                    else:
                        st.error("💥 **Failed to generate blog post. Please try again!**")


# Function to generate the blog post using the LLM
def generate_blog_post(input_blog_keywords, input_type, input_tone, input_language):
    serp_results = None
    try:
        serp_results = metaphor_search_articles(input_blog_keywords)
    except Exception as err:
        st.error(f"❌ Failed to retrieve search results for {input_blog_keywords}: {err}")
    
    if serp_results:
        prompt = f"""
        You are Alwrity, an SEO expert & {input_language} Creative Content writer. 
        You specialize in writing {input_type} blog posts.
        Write a detailed, informative, and SEO-optimized blog post using the following web research keywords and Google search results.
        
        Ensure that:
        1. The blog content competes against existing blogs in the search results.
        2. You include 5 FAQs based on 'People also ask' and related queries from the search results, with answers.
        3. The blog is formatted in markdown and follows the {input_tone} tone.
        4. Include personal insights and make the content engaging.
        5. Your final response should be highly readable and demostrate Experience, Expertise, Authoritativeness, and Trustworthiness.
        6. Maintain blog tone of type {input_tone}, attitude and mood of your blog, conveyed through sentence formations, phrase types, and word choices.

        Blog keywords: {input_blog_keywords}
        Google SERP results: {serp_results}
        """
        return generate_text_with_exception_handling(prompt)
    return None


# Metaphor search function
def metaphor_search_articles(query):
    METAPHOR_API_KEY = os.getenv('METAPHOR_API_KEY')
    if not METAPHOR_API_KEY:
        raise ValueError("METAPHOR_API_KEY environment variable not set!")

    metaphor = Exa(METAPHOR_API_KEY)
    
    try:
        search_response = metaphor.search_and_contents(query, use_autoprompt=True, num_results=5)
        return search_response.results
    except Exception as err:
        st.error(f"Failed in metaphor.search_and_contents: {err}")
        return None


# Exception handling for text generation
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config={"max_output_tokens": 8192})
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text
    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()

