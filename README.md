# YOLO Object Detection Streamlit App

This is an object detection web application built with Ultralytics YOLO and Streamlit for polyp detection.

## Features

- 🎯 Custom YOLO model (best.pt) for polyp detection
- 📤 Image upload and real-time detection
- 🎨 Visualized detection results with original colors preserved
- 📊 Detection statistics
- 🔧 Adjustable confidence threshold

## Installation

```bash
pip install -r requirements.txt
```

## Running the App Locally

```bash
streamlit run app.py
```

Or use the provided script:
```bash
bash run.sh
```

The app will automatically open in your browser at `http://localhost:8501`

## Usage

1. Upload an image
2. Adjust confidence threshold in the sidebar (optional)
3. Click the "Start Detection" button
4. View detection results and statistics

## Deployment to Streamlit Cloud

### Step 1: Push to GitHub

1. Initialize git repository (if not already done):
```bash
cd /root/autodl-tmp/demo
git init
git add .
git commit -m "Initial commit: YOLO Polyp Detection App"
```

2. Create a new repository on GitHub (https://github.com/new)

3. Add remote and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to: `app.py`
6. Click "Deploy"

### Important Notes for Streamlit Cloud

- The app uses a custom model file (`ultralytics-8.1.0/best.pt`) - make sure this file is included in your repository
- If the model file is too large (>100MB), consider using Git LFS or hosting the model file elsewhere
- Streamlit Cloud provides free CPU resources, so detection may be slower than with GPU

## File Structure

```
demo/
├── app.py                 # Streamlit main application file
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── run.sh                # Run script
├── .gitignore           # Git ignore file
├── .streamlit/          # Streamlit configuration
│   └── config.toml
└── ultralytics-8.1.0/   # Ultralytics YOLO library
    └── best.pt          # Custom trained model
```

## Notes

- Model file (`best.pt`) must be present in the repository for the app to work
- Supported image formats: JPG, PNG, BMP, WEBP
- The app preserves original image colors in detection results
