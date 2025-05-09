# Alwrity - AI Blog Post Generator

Alwrity is an AI-powered blog post generator built with Streamlit, leveraging the capabilities of a large language model (LLM). It streamlines the process of creating SEO-optimized and engaging blog posts.

## Features

- **Keyword-driven Content Generation**: Input your main blog keywords to generate a comprehensive blog post.
- **Blog Post Type Selection**: Choose from various blog post formats such as 'General', 'How-to Guides', 'Listicles', and more.
- **Tone and Language Customization**: Select the desired tone (e.g., Professional, Casual) and language (e.g., English, Vietnamese) for your blog post.
- **SEO Optimization**: Automatically optimized for search engines, considering relevant keywords and search intent.
- **FAQ Generation**: Generates FAQs based on "People Also Ask" results from Google searches.
- **Human-like Writing Style**: Produces content in a natural and engaging style, incorporating personal insights and anecdotes.

## Dependencies

The application requires the following dependencies:

- **Streamlit**
- **OpenAI API** (or another LLM provider)
- **Serper API** (for Google search results)
- **requests**

## Installation

This installation process was tested on Windows PowerShell by the author.

1. Clone the repository:
    ```powershell
    git clone https://github.com/AJaySi/alwrity_blog_writer.git
    ```
2. Navigate to the project directory:
    ```powershell
    cd alwrity_blog_writer
    ```
3. Run the application:
    ```powershell
    streamlit run blog_from_serp.py
    ```
4. When the app opens in your browser, enter your API keys in the UI under the "API Configuration" section.

No need to set environment variables or edit code—just provide your API keys in the app interface after launch.

## Usage

1. Open the Alwrity application in your web browser.
2. Enter the main keywords for your blog post.
3. Select the desired blog post type, tone, and language.
4. Click the **"Write Blog Post"** button.
5. View the generated blog post, which includes SEO-optimized content and relevant FAQs.

## Limitations

- The quality of the generated content depends on the input keywords and the capabilities of the LLM.
- FAQs are based on Google search results and may not always be comprehensive or accurate.
- API keys for OpenAI and Serper may have usage limits or associated costs.

## Future Improvements

- Integration with additional LLM providers for diverse content generation.
- User feedback mechanisms to enhance the quality and relevance of generated content.
- A user interface for customizing SEO parameters and content structure.

---

We welcome contributions and feedback! Feel free to open issues or submit pull requests to help improve Alwrity.
