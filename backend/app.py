from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
import cv2
from skimage import measure, filters, morphology
from skimage.feature import graycomatrix, graycoprops
import shutil
import os
import uuid

# ======================
# Load model (robust path)
# ======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "voting_classifier_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# ======================
# FastAPI App
# ======================
app = FastAPI(
    title="Breast Cancer Prediction API",
    version="1.0"
)

# ======================
# CORS Middleware
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Input Schema
# ======================
class CancerInput(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float

    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float

    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float


FEATURE_ORDER = list(CancerInput.model_fields.keys())

# ======================
# Image Processing Utils
# ======================
def fractal_dimension(Z):
    """Estimate fractal dimension using box-counting"""
    Z = (Z > 0).astype(int)
    sizes = 2 ** np.arange(1, int(np.log2(min(Z.shape))))
    counts = []

    for size in sizes:
        S = np.add.reduceat(
            np.add.reduceat(Z, np.arange(0, Z.shape[0], size), axis=0),
            np.arange(0, Z.shape[1], size),
            axis=1,
        )
        counts.append(np.sum(S > 0))

    if len(counts) < 2:
        return 0.0

    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return -coeffs[0]


def extract_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Could not read image")

    try:
        thresh_val = filters.threshold_otsu(img)
    except Exception:
        thresh_val = 128

    binary = img > thresh_val
    binary = morphology.remove_small_objects(binary, 50)

    labeled_img = measure.label(binary)
    regions = measure.regionprops(labeled_img, intensity_image=img)

    if not regions:
        return {f: 0.0 for f in FEATURE_ORDER}

    region = max(regions, key=lambda r: r.area)

    area = region.area
    perimeter = region.perimeter
    radius = np.sqrt(area / np.pi)
    compactness = perimeter**2 / (4 * np.pi * area) if area > 0 else 0
    concavity = region.eccentricity
    concave_points = region.extent
    symmetry = region.major_axis_length / (region.minor_axis_length + 1e-5)
    fractal = fractal_dimension(binary)

    glcm = graycomatrix(
        img, distances=[1], angles=[0], levels=256, symmetric=True, normed=True
    )
    texture = graycoprops(glcm, "contrast")[0, 0]
    smoothness = region.mean_intensity

    raw_features = [
        radius,
        texture,
        perimeter,
        area,
        smoothness,
        compactness,
        concavity,
        concave_points,
        symmetry,
        fractal,
    ]

    feature_names = [
        "radius",
        "texture",
        "perimeter",
        "area",
        "smoothness",
        "compactness",
        "concavity",
        "concave_points",
        "symmetry",
        "fractal_dimension",
    ]

    features = {}
    for i, name in enumerate(feature_names):
        mean_val = float(raw_features[i])
        se_val = float(raw_features[i] / np.sqrt(region.area)) if region.area > 0 else 0.0
        worst_val = mean_val

        features[f"{name}_mean"] = mean_val
        features[f"{name}_se"] = se_val
        features[f"{name}_worst"] = worst_val

    return features

# ======================
# Health Check
# ======================
@app.get("/")
def health():
    return {"status": "FastAPI is running"}

# ======================
# Prediction Endpoint (Numeric)
# ======================
@app.post("/predict")
def predict(data: CancerInput):
    X = np.array([[getattr(data, f) for f in FEATURE_ORDER]])

    prediction = model.predict(X)[0]

    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(model.predict_proba(X)[0].max())

    return {
        "prediction": "Malignant" if prediction == 1 else "Benign",
        "confidence": confidence,
    }

# ======================
# Prediction Endpoint (Image)
# ======================
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    temp_file = f"temp_{uuid.uuid4().hex}.png"

    try:
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        features_dict = extract_features(temp_file)
        input_data = CancerInput(**features_dict)

        result = predict(input_data)
        result["features"] = features_dict

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
