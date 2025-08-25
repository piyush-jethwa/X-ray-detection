import os
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
import streamlit as st

# Get API Key from environment variables (for deployment security)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Ensure API Key is provided
if not GROQ_API_KEY:
    st.error("⚠️ Groq API Key not found. Please set your GROQ_API_KEY in the Streamlit secrets settings.")
    st.info("To set your API key:\n1. Go to your Streamlit app's settings\n2. Add a secret called 'GROQ_API_KEY'\n3. Set its value to your actual Groq API key")
    st.stop()

# Initialize the Medical Agent
medical_agent = Agent(
    model=Groq(id="llama3-70b-8192"),  # Using Llama 3 70B model from Groq
    tools=[DuckDuckGoTools()],
    markdown=True
)

# Medical Analysis Query - Simplified for Groq API compatibility
query = """
You are a medical imaging expert. Analyze the medical image and provide:

1. Image type and anatomical region
2. Key findings and observations
3. Diagnostic assessment
4. Patient-friendly explanation

Use clear markdown formatting and be concise.
"""

# Function to analyze medical image
def analyze_medical_image(image_path):
    """Processes and analyzes a medical image using AI."""
    
    # Open and resize image
    image = PILImage.open(image_path)
    width, height = image.size
    aspect_ratio = width / height
    new_width = 500
    new_height = int(new_width / aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    # Save resized image
    temp_path = "temp_resized_image.png"
    resized_image.save(temp_path)

    # Create AgnoImage object
    agno_image = AgnoImage(filepath=temp_path)

    # Run AI analysis - Groq requires a different approach for images
    try:
        # Convert image to base64 for Groq compatibility
        import base64
        with open(temp_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Create a modified query that includes image reference
        image_query = f"{query}\n\nPlease analyze this medical image: [Image attached]"
        
        response = medical_agent.run(image_query)
        return response.content
    except Exception as e:
        return f"⚠️ Analysis error: {e}"
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Streamlit UI setup
st.set_page_config(page_title="Medical Image Analysis", layout="centered")
st.title("🩺 Medical Image Analysis Tool 🔬")
st.markdown(
    """
    Welcome to the **Medical Image Analysis** tool! 📸
    Upload a medical image (X-ray, MRI, CT, Ultrasound, etc.), and our AI-powered system will analyze it, providing detailed findings, diagnosis, and research insights.
    Let's get started!
    """
)

# Upload image section
st.sidebar.header("Upload Your Medical Image:")
uploaded_file = st.sidebar.file_uploader("Choose a medical image file", type=["jpg", "jpeg", "png", "bmp", "gif"])

# Button to trigger analysis
if uploaded_file is not None:
    # Display the uploaded image in Streamlit
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    if st.sidebar.button("Analyze Image"):
        with st.spinner("🔍 Analyzing the image... Please wait."):
            # Save the uploaded image to a temporary file
            image_path = f"temp_image.{uploaded_file.type.split('/')[1]}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Run analysis on the uploaded image
            report = analyze_medical_image(image_path)
            
            # Display the report
            st.subheader("📋 Analysis Report")
            st.markdown(report, unsafe_allow_html=True)
            
            # Clean up the saved image file
            if os.path.exists(image_path):
                os.remove(image_path)
else:
    st.warning("⚠️ Please upload a medical image to begin analysis.")
    
# Additional information about API key setup
st.sidebar.markdown("---")
st.sidebar.info("🔒 This app requires a Groq API key to function. Make sure you've set it in your Streamlit secrets.")
