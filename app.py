import streamlit as st
import sys
import os
import warnings
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Suppress FutureWarning from timm library
warnings.filterwarnings("ignore", category=FutureWarning, module="timm.models.layers")

# Try to import ultralytics - first try pip installed version, then local version
try:
    from ultralytics import YOLO
except ImportError:
    # If pip version fails, try local ultralytics directory
    ultralytics_local_path = Path(__file__).parent / "ultralytics-8.1.0"
    if ultralytics_local_path.exists():
        sys.path.insert(0, str(ultralytics_local_path))
        try:
            from ultralytics import YOLO
        except ImportError:
            st.error("Unable to import ultralytics library. Please ensure it is properly installed.")
            st.error(f"Checked loca

# Page configuration
st.set_page_config(
    page_title="YOLO Object Detection App",
    page_icon="🎯",
    layout="wide"
)

# Title
st.title(" Demo:TB Polyp Detection ")
st.markdown("---")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Use custom best.pt model
model_path = str(Path(__file__).parent / "ultralytics-8.1.0" / "best.pt")

# Confidence threshold
confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.25,
    step=0.05
)

# File upload
st.header("📤 Upload Image")
uploaded_file = st.file_uploader(
    "Select an image for detection",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    help="Supports JPG, PNG, BMP, WEBP formats"
)

# Initialize model
@st.cache_resource
def load_model(model_path):
    """Load YOLO model"""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        return None

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Original Image")
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", width='stretch')
        
        # Save uploaded image
        image_path = f"/tmp/uploaded_image_{uploaded_file.name}"
        image.save(image_path)
        
        # Execute detection
        if st.button("Start Detection", type="primary"):
            with st.spinner("Loading model and executing detection..."):
                try:
                    # Load model
                    model = load_model(model_path)
                    
                    if model is None:
                        st.error("Model loading failed. Please check the model file.")
                    else:
                        # Execute detection task
                        results = model.predict(
                            source=image_path,
                            conf=confidence,
                            task="detect",
                            save=False
                        )
                        
                        # Display results
                        with col2:
                            st.subheader("Detection Results")
                            
                            # Draw detection boxes on original image to preserve colors
                            result_image = image.copy()
                            draw = ImageDraw.Draw(result_image)
                            
                            # Try to load a font, fallback to default if not available
                            try:
                                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
                            except:
                                try:
                                    font = ImageFont.truetype("arial.ttf", 20)
                                except:
                                    font = ImageFont.load_default()
                            
                            if hasattr(results[0], 'boxes') and results[0].boxes is not None:
                                class_names = model.names
                                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
                                
                                for i, box in enumerate(results[0].boxes):
                                    # Get box coordinates
                                    xyxy = box.xyxy[0].cpu().numpy()
                                    x1, y1, x2, y2 = map(int, xyxy)
                                    
                                    # Get class and confidence
                                    cls = int(box.cls[0])
                                    conf = float(box.conf[0])
                                    class_name = class_names[cls]
                                    
                                    # Choose color based on class
                                    color = colors[cls % len(colors)]
                                    
                                    # Draw bounding box
                                    draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
                                    
                                    # Draw label background
                                    label = f"{class_name} {conf:.2f}"
                                    bbox = draw.textbbox((0, 0), label, font=font)
                                    text_width = bbox[2] - bbox[0]
                                    text_height = bbox[3] - bbox[1]
                                    
                                    # Draw label background rectangle
                                    draw.rectangle([x1, y1 - text_height - 4, x1 + text_width + 4, y1], fill=color)
                                    
                                    # Draw label text
                                    draw.text((x1 + 2, y1 - text_height - 2), label, fill=(255, 255, 255), font=font)
                            
                            st.image(result_image, caption="Detection Results", width='stretch')
                            
                            # Display detection information
                            st.markdown("### 📊 Detection Statistics")
                            
                            if hasattr(results[0], 'boxes') and results[0].boxes is not None:
                                num_detections = len(results[0].boxes)
                                st.metric("Number of Detected Objects", num_detections)
                                
                                # Display detected classes
                                if num_detections > 0:
                                    st.markdown("#### Detected Classes:")
                                    class_names = model.names
                                    detected_classes = {}
                                    
                                    for box in results[0].boxes:
                                        cls = int(box.cls[0])
                                        conf = float(box.conf[0])
                                        class_name = class_names[cls]
                                        
                                        if class_name not in detected_classes:
                                            detected_classes[class_name] = []
                                        detected_classes[class_name].append(conf)
                                    
                                    for class_name, confidences in detected_classes.items():
                                        avg_conf = np.mean(confidences)
                                        count = len(confidences)
                                        st.write(f"- **{class_name}**: {count} objects (average confidence: {avg_conf:.2%})")
                            else:
                                st.info("No objects detected")
                                
                            # Display original result data
                            with st.expander("Detailed Result Data"):
                                st.json({
                                    "Model": "best.pt",
                                    "Confidence Threshold": confidence,
                                    "Task Type": "detect",
                                    "Image Size": image.size
                                })
                                
                except Exception as e:
                    st.error(f"Error occurred during detection: {str(e)}")
                    st.exception(e)
    else:
        st.info("👆 Please upload an image to start detection")

with col2:
    if uploaded_file is None:
        st.subheader("🎯 Detection Results")
        st.info("Detection results will be displayed here after uploading an image")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Built with Ultralytics YOLO | Streamlit App</p>
    </div>
    """,
    unsafe_allow_html=True
)

