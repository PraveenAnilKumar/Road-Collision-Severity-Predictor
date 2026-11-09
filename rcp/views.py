from pathlib import Path
import pickle
from datetime import datetime

import pandas as pd
from django.conf import settings
from django.shortcuts import render
from .models import PredictionRecord


MODEL_DIR = Path(settings.BASE_DIR) / "models"
MODEL_PATHS = {
    "macro_f1": MODEL_DIR / "best_macro_f1_model.pkl",
    "accuracy": MODEL_DIR / "bagging_model.pkl",
}
MODELS = {}
for model_key, model_path in MODEL_PATHS.items():
    with model_path.open("rb") as model_file:
        MODELS[model_key] = pickle.load(model_file)

MODEL_LABELS = {
    "macro_f1": "Best macro F1 model",
    "accuracy": "Best accuracy model",
}
SEVERITY_LABELS = {
    1: "Fatal",
    2: "Serious",
    3: "Slight",
}


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def predictor(request):
    prediction = None
    selected_model = request.POST.get("model", "macro_f1") if request.method == "POST" else "macro_f1"

    if request.method == "POST":
        try:
            if selected_model not in MODELS:
                raise ValueError("Unknown model selection")
            collision_date = datetime.strptime(request.POST["collision_date"], "%Y-%m-%d").date()
            collision_time = datetime.strptime(request.POST["collision_time"], "%H:%M").time()
            hour = collision_time.hour
            youngest_driver = int(request.POST["youngest_driver"])
            oldest_driver = int(request.POST["oldest_driver"])
            # The notebook treats missing driver ages as -1. The form asks users
            # to enter 0 when unknown, so normalize that sentinel here.
            youngest_driver = -1 if youngest_driver == 0 else youngest_driver
            oldest_driver = -1 if oldest_driver == 0 else oldest_driver
            features = {
                "number_of_vehicles": int(request.POST["number_of_vehicles"]),
                "day_of_week": collision_date.isoweekday() % 7 + 1,  # DfT: Sunday=1 ... Saturday=7
                "first_road_class": int(request.POST["first_road_class"]),
                "road_type": int(request.POST["road_type"]),
                "speed_limit": int(request.POST["speed_limit"]),
                "junction_detail": int(request.POST["junction_detail"]),
                "junction_control": int(request.POST["junction_control"]),
                "pedestrian_crossing": int(request.POST["pedestrian_crossing"]),
                "light_conditions": int(request.POST["light_conditions"]),
                "weather_conditions": int(request.POST["weather"]),
                "road_surface_conditions": int(request.POST["road_surface"]),
                "urban_or_rural_area": int(request.POST["urban_or_rural_area"]),
                "trunk_road_flag": int(request.POST["trunk_road_flag"]),
                "n_motorcycles": int(request.POST["n_motorcycles"]),
                "n_cars": int(request.POST["n_cars"]),
                "n_vans": int(request.POST["n_vans"]),
                "n_hgv": int(request.POST["n_hgv"]),
                "n_buses": int(request.POST["n_buses"]),
                "n_cyclists": int(request.POST["n_cyclists"]),
                "youngest_driver": youngest_driver,
                "oldest_driver": oldest_driver,
                "hour": hour,
                "month": collision_date.month,
                "is_weekend": int(collision_date.isoweekday() in (6, 7)),
                "is_rush_hour": int(hour in (7, 8, 9, 16, 17, 18)),
            }
            model = MODELS[selected_model]
            input_df = pd.DataFrame([features], columns=list(model.feature_names_in_))
            fatal_threshold = getattr(model, "fatal_threshold_", None)
            if selected_model == "macro_f1" and fatal_threshold is not None:
                probabilities = model.predict_proba(input_df)[0]
                classes = list(model.classes_)
                fatal_index = classes.index(1)
                if probabilities[fatal_index] >= fatal_threshold:
                    predicted_class = 1
                else:
                    nonfatal = [(probabilities[i], cls) for i, cls in enumerate(classes) if cls != 1]
                    predicted_class = max(nonfatal)[1]
            else:
                predicted_class = int(model.predict(input_df)[0])
            prediction = SEVERITY_LABELS.get(predicted_class, str(predicted_class))
            PredictionRecord.objects.create(
                model_key=selected_model,
                inputs={key: value for key, value in request.POST.items()
                        if key not in {"csrfmiddlewaretoken", "model"}},
                predicted_class=int(predicted_class),
                predicted_severity=prediction,
            )
        except (KeyError, ValueError):
            prediction = None

    return render(request, "predictor.html", {
        "prediction": prediction,
        "prediction_error": request.method == "POST" and prediction is None,
        "selected_model": selected_model,
        "selected_model_label": MODEL_LABELS.get(selected_model, MODEL_LABELS["macro_f1"]),
    })
