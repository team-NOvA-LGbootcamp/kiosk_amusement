import cv2
import glob
import numpy as np
from itertools import combinations

IMAGE_SIZE = 224

class Predictor:
    def __init__(self, model_path, env="WINDOWS"):
        
        # tmp
        model_path = "./models/age_gender"
        # env = "RASPBERRY"

        self.env = env
        if env == "WINDOWS":

            from tensorflow.keras.models import load_model  # type: ignore
            model_files = glob.glob(model_path + '/*.h5')  # Ensure .h5 extension
            self.models = [load_model(file) for file in model_files]

            if not self.models:
                raise ValueError("No models were loaded. Check the model path and file extensions.")

        elif env == "RASPBERRY":
            import tflite_runtime.interpreter as tflite  # type: ignore
            model_files = glob.glob(model_path + '/*.tflite')
            self.interpreters = [tflite.Interpreter(model_path=file) for file in model_files]
            self.input_details_list = []
            self.output_details_list = []
            self.input_dtype_list = []

            for i,intp in enumerate(self.interpreters):
                intp.allocate_tensors()
                self.input_details_list.append(intp.get_input_details())
                self.output_details_list.append(intp.get_output_details())
                self.input_dtype_list.append(intp.get_input_details()[0]['dtype'])

            if not self.interpreters:
                raise ValueError("No interpreters were loaded. Check the model path and file extensions.")

        print("\033[91mmodel is loaded\033[0m")

        self.IMG_SIZE = 224

    def preprocess_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0
        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
        img = img.reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 3)
        return img

    def predict_image(self, face_image):
        dict_age_predictions = {}
        dict_gender_predictions = {}
        for face_id, img in face_image.items():
            age_predictions = []
            gender_predictions = []
            preprocessed_img = self.preprocess_image(img)
            if self.env == "WINDOWS":
                prediction_results = []
                for model in self.models:
                    pred = model.predict(preprocessed_img, verbose=0)
                    prediction_results.append(pred)
                prediction_results = np.array(prediction_results)
                mean_prediction = np.mean(prediction_results, axis=0).squeeze()
                if mean_prediction.ndim == 1 and mean_prediction.size == 2:
                    age_predictions.append(mean_prediction[0])
                    gender_predictions.append(mean_prediction[1])
                else:
                    raise ValueError("Unexpected shape of prediction results: ", mean_prediction.shape)

            elif self.env == "RASPBERRY":
                prediction_results = []
                for intp,ind,outd,indty in zip(self.interpreters,
                                                self.input_details_list,
                                                self.output_details_list,
                                                self.input_dtype_list):

                    intp.set_tensor(ind[0]['index'], preprocessed_img.astype(indty))
                    intp.invoke()
                    age_output_data = intp.get_tensor(outd[0]['index'])[0]
                    gender_output_data = intp.get_tensor(outd[1]['index'])[0]
                    prediction_results.append([age_output_data,gender_output_data])

                prediction_results = np.array(prediction_results)
                mean_prediction = np.mean(prediction_results, axis=0).squeeze()
                print(f"{face_id}:{mean_prediction}")
                if mean_prediction.ndim == 1 and mean_prediction.size == 2:
                    age_predictions.append(mean_prediction[0])
                    gender_predictions.append(mean_prediction[1])
                else:
                    raise ValueError("Unexpected shape of prediction results: ", mean_prediction.shape)

            if age_predictions and gender_predictions:
                avg_age = np.mean(age_predictions)
                avg_gender = np.mean(gender_predictions)
                dict_age_predictions[face_id] = round(avg_age)
                dict_gender_predictions[face_id] = round(avg_gender)

        return dict_age_predictions, dict_gender_predictions


class RelationPredictor:
    def __init__(self, model_path, env="WINDOWS"):
        # tmp
        model_path = "./models/relationship"
        # env = "RASPBERRY"

        self.env = env

        if env == "WINDOWS":
            from tensorflow.keras.models import load_model  # type: ignore
            self.model = load_model(glob.glob(model_path + '/*.h5')[0])

            if not self.model:
                raise ValueError("No models were loaded. Check the model path and file extensions.")

        elif env == "RASPBERRY":
            import tflite_runtime.interpreter as tflite  # type: ignore
            file = glob.glob(model_path + '/*.tflite')[0]
            self.interpreter = tflite.Interpreter(model_path=file)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()


            if not self.interpreter:
                raise ValueError("No interpreter were loaded. Check the model path and file extensions.")

        print("\033[91mmodel is loaded\033[0m")

        self.IMG_SIZE = 224

    def preprocess_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
        return np.array([img])

    def map_age(self,age):
        if age <= 4: return 0
        elif age <= 19: return 1
        elif age <= 44: return 2
        elif age <= 59: return 3
        else: return 4

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

            age1, age2 = ages[face_id1], ages[face_id2]
            age1_mapped = self.map_age(age1)
            age2_mapped = self.map_age(age2)

            gender1, gender2 = genders[face_id1], genders[face_id2]

            metadata = np.array([[age1_mapped, gender1, age2_mapped, gender2]], dtype='float32')

            

            if self.env == "WINDOWS":
                input_data =[face_image_1, face_image_2, metadata]

                model_output = self.model.predict(input_data, verbose=0)
                model_output = np.squeeze(model_output)
                relation_proportion += model_output

            elif self.env == "RASPBERRY":
                self.interpreter.set_tensor(self.input_details[0]['index'], np.array(face_image_1).astype(self.input_details[0]['dtype']))
                self.interpreter.set_tensor(self.input_details[1]['index'], metadata.astype(self.input_details[1]['dtype']))
                self.interpreter.set_tensor(self.input_details[2]['index'], np.array(face_image_2).astype(self.input_details[2]['dtype']))
                
                self.interpreter.invoke()
                model_output = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
                model_output = np.squeeze(model_output)
                relation_proportion += model_output

        relation_proportion /= len(face_id_combinations)

        relation_prediction_result = {
                "friend": relation_proportion[0],
                "family": relation_proportion[1],
                "couple": relation_proportion[2],
            }

        return relation_prediction_result
