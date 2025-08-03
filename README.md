# Medical Image Analysis App

A Streamlit application that uses Google's Gemini AI to analyze medical images and provide detailed findings, diagnosis, and research insights.

## Features
- Upload medical images (X-ray, MRI, CT, Ultrasound, etc.)
- AI-powered analysis with detailed findings
- Diagnostic assessments with confidence levels
- Patient-friendly explanations
- Research context with recent medical literature

## Deployment Instructions

### Step 1: Set up GitHub Repository
1. Create a new GitHub repository
2. Upload the following files to the repository:
   - `medical_deploy.py` (main application file)
   - `requirements.txt` (dependencies)

### Step 2: Deploy to Streamlit Community Cloud
1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app" and select your repository
4. Set the main file path to `medical_deploy.py`
5. Click "Deploy!"

### Step 3: Configure Google API Key
1. After deployment, go to your app's settings in Streamlit Community Cloud
2. Navigate to "Secrets" settings
3. Add a new secret:
   - Name: `GOOGLE_API_KEY`
   - Value: Your actual Google API key (get it from Google AI Studio)

### Step 4: Access Your App
Once deployed and configured, your app will be available at a URL like:
`https://your-username-streamlit-medical-deploy-medical-deploy-xyz123.streamlit.app`

## Local Development
To run locally:
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variable: `export GOOGLE_API_KEY=your_actual_key`
3. Run the app: `streamlit run medical_deploy.py`

## Dependencies
- agno==1.7.7
- google-genai==1.28.0
- duckduckgo-search==8.1.1
- streamlit==1.47.1
- Pillow==10.4.0

## Note
This application is for educational and informational purposes only. It is not intended to provide medical advice or diagnosis. Always consult with a qualified healthcare professional for medical concerns.
