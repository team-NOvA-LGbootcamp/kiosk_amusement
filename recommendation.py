import time

rides_table = {
    "bumper_cars",
    "ferris_wheel",
    "haunted_house",
    "merry_go_round",
    "roller_coaster",
    "safari",
    "swing_ride",
    "themepark_train",
    "viking"
    }
        

class RecommendationAlgorithm:
    def __init__(self):
        self.model = None
        self.prediction_results = []
        self.age = []
        self.gender = []
        self.recommendation = ""
    
    def run_recommendation(self, ages, genders, relation):
        
        num_detected = len(ages)
        for i in range(num_detected):
            self.age.append(ages[i+1])
            self.gender.append(genders[i+1])
        print(self.age, self.gender)
        
        # if age<10:
        #     self.age = 0
        # elif 10<=age and age<20:
        #     self.age = 10
        # elif 20<=age and age<30:
        #     self.age = 20
        # elif 30<=age and age<40:
        #     self.age = 30
        # elif 40<=age and age<50:
        #     self.age = 40
        # elif 50<=age and age<60:
        #     self.age = 50
        # else:
        #     self.age = 60

        # self.gender = gender
        time.sleep(1)

        return ["viking", "ferris_wheel", "safari"]
    
    def get_recommendation_res(self):
        return self.recommendation
