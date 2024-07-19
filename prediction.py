import cv2
import glob
import numpy as np
from itertools import combinations

IMAGE_SIZE = 224

class Predictor:
    def __init__(self, model_path, env="WINDOWS"):
        self.env = env

        if env == "WINDOWS":
            from tensorflow.keras.models import load_model  # type: ignore
            model_files = glob.glob(model_path + '/*.h5')  # Ensure .h5 extension
            self.models = [load_model(file) for file in model_files]

            if not self.models:
                raise ValueError("No models were loaded. Check the model path and file extensions.")

        elif env == "RASPBERRY":
            import tflite_runtime.interpreter as tflite  # type: ignore
            # Placeholder for Raspberry Pi model loading
            self.models = None  # Replace with actual model loading logic

        print("\033[91mmodel is loaded\033[0m")

        self.IMG_SIZE = 224

    def preprocess_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0
        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
        img = img.reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 3)
        return img

    def predict_image(self, face_images):
        all_age_predictions = {}
        all_gender_predictions = {}

        for face_id, images in face_images.items():
            age_predictions = []
            gender_predictions = []
            print(f"{face_id}:{len(images)}")
            for img in images:
                preprocessed_img = self.preprocess_image(img)

                if self.env == "WINDOWS":
                    prediction_results = []
                    for model in self.models:
                        pred = model.predict(preprocessed_img, verbose=0)
                        prediction_results.append(pred)

                    prediction_results = np.array(prediction_results)
                    mean_prediction = np.mean(prediction_results, axis=0).squeeze()
                    print(f"{face_id}:{mean_prediction}")
                    if mean_prediction.ndim == 1 and mean_prediction.size == 2:
                        age_predictions.append(mean_prediction[0])
                        gender_predictions.append(mean_prediction[1])
                    else:
                        raise ValueError("Unexpected shape of prediction results: ", mean_prediction.shape)

                elif self.env == "RASPBERRY":
                    # Placeholder for Raspberry Pi model predictions
                    pass

            if age_predictions and gender_predictions:
                avg_age = np.mean(age_predictions)
                avg_gender = np.mean(gender_predictions)
                all_age_predictions[face_id] = round(avg_age)
                all_gender_predictions[face_id] = round(avg_gender)

        # Sorting the predictions by face_id
        sorted_age_predictions = [all_age_predictions[face_id] for face_id in sorted(all_age_predictions.keys())]
        sorted_gender_predictions = [all_gender_predictions[face_id] for face_id in sorted(all_gender_predictions.keys())]

        return sorted_age_predictions, sorted_gender_predictions


class RelationPredictor:
    def __init__(self, model_path, env="WINDOWS"):
        self.env = env

        if env == "WINDOWS":
            from tensorflow.keras.models import load_model  # type: ignore
            self.models = load_model(model_path)

            if not self.models:
                raise ValueError("No models were loaded. Check the model path and file extensions.")

        elif env == "RASPBERRY":
            import tflite_runtime.interpreter as tflite  # type: ignore
            # Placeholder for Raspberry Pi model loading
            self.models = None  # Replace with actual model loading logic

        print("\033[91mmodel is loaded\033[0m")

        self.IMG_SIZE = 224

    def preprocess_image(self, img):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
        img = img.reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 3)
        return img

    def predict_image(self, face_images,ages,genders):
        if len(face_images.keys()) < 2:
            raise ValueError("Only One person in frame")
        
        face_id_combinations = list(combinations(face_images.keys(), 2))

        relation_proportion = np.array([0.0, 0.0, 0.0])

        for face_id1, face_id2 in face_id_combinations:
            face_image_1 = face_images[face_id1]
            face_image_2 = face_images[face_id2]
            face_image_1 = self.preprocess_image(face_image_1)
            face_image_2 = self.preprocess_image(face_image_2)

            metadata = [ages[face_id1], ages[face_id2], genders[face_id1],genders[face_id2]]
            
            if self.env == "WINDOWS":
                model_output = self.model.predict([face_image_1,face_image_2,metadata], verbose=0)
                model_output = np.squeeze(model_output)
                relation_proportion += model_output

            elif self.env == "RASPBERRY":
                # Placeholder for Raspberry Pi model predictions
                pass

        relation_proportion /= len(face_id_combinations)

        relation_prediction_result = {
                "friend": relation_proportion[0],
                "family": relation_proportion[1],
                "couple": relation_proportion[2],
            }

        return relation_prediction_result
