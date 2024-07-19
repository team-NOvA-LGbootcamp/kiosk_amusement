import cv2
import glob
import numpy as np

IMAGE_SIZE = 224

class Predictor:
    def __init__(self, model_path, env="WINDOWS"):
        self.env = env

        if env == "WINDOWS":
            from tensorflow.keras.models import load_model  # type: ignore
            model_files = glob.glob(model_path + '/*.h5')
            self.model = [load_model(file) for file in model_files]

        elif env == "RASPBERRY":
            import tflite_runtime.interpreter as tflite  # type: ignore
            # RASPBERRY 환경의 코드 생략

        print("\033[91mmodel is loaded\033[0m")

        self.IMG_SIZE = 224

    def predict_image(self, img_list):
        age_predictions = []
        gender_predictions = []

        for img in img_list:
            # Convert BGR to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_normalized = img_rgb / 255.0  # Normalize the image
            img_resized = cv2.resize(img_normalized, (self.IMG_SIZE, self.IMG_SIZE))
            img_reshaped = img_resized.reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 3)  # Reshape for model input

            if self.env == "WINDOWS":
                prediction_results = np.array([model.predict(img_reshaped, verbose=0) for model in self.model])
                print(prediction_results)
                result = np.round(np.squeeze(np.mean(prediction_results, axis=0)))

                age_predictions.append(round(result[0]))
                gender_predictions.append(round(result[1]))

            # elif self.env == "RASPBERRY":
            #     RASPBERRY 환경의 코드 생략

        return age_predictions, gender_predictions
