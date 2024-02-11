import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

# Set your OpenAI API key here
openai.api_key = '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'

st.title('Your Own Ideas NoteBook')

# User input for the text prompt
user_prompt = st.text_area("Enter your business idea:", 'A futuristic cityscape')
mutual_instructions = "info graphic for an idea, and please be detailed with writing inside the image with no writing errors"

# Function to perform business idea analysis
def analyze_business_idea(prompt):
    messages = [
        {"role": "system", "content": "You are a Venture Capital Analyst analyze this idea"},
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  # Use an appropriate and available model
            messages=messages,
            max_tokens=1024
        )
        # Assuming the last message in the response is the assistant's analysis
        if response.choices:
            analysis = response.choices[0]['message']['content']
            return analysis
        else:
            return "Failed to generate analysis. Please try again."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Button to generate image and perform analysis
if st.button('Generate Image and Analyze Idea'):
    # Combine the user's prompt with the mutual instructions
    final_prompt = f"{user_prompt}, {mutual_instructions}"
    
    # Generate an image based on the final prompt
    try:
        response = openai.Image.create(
            model="dall-e-3",  # Adjust the model as needed
            prompt=final_prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Size of the generated image
        )
        
        # Check if the response is successful and display the image
        if response and 'data' in response and len(response['data']) > 0:
            image_url = response['data'][0]['url']
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            st.image(image, caption='Generated Image', use_column_width=True)
        else:
            st.error('Failed to generate image. Please try again.')
    except Exception as e:
        st.error(f"An error occurred during image generation: {str(e)}")
    
    # Business idea analysis with GPT-4 (or the most advanced version available)
    analysis_result = analyze_business_idea(user_prompt)
    st.subheader('Business Idea Analysis')
    st.write(analysis_result)
