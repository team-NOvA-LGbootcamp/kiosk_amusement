import time

rides_score = {
    "bumper_cars": 0,
    "ferris_wheel": 0,
    "haunted_house": 0,
    "merry_go_round": 0,
    "roller_coaster": 0,
    "safari": 0,
    "swing_ride": 0,
    "themepark_train": 0,
    "viking": 0
}
        

class RecommendationAlgorithm:
    def __init__(self):
        self.model = None
        self.prediction_results = []
        self.age = []
        self.gender = []
    
    def run_recommendation(self, ages, genders, relation):
        num_detected = len(ages)

        for i in range(num_detected):
            self.age.append(ages[i+1])
            self.gender.append(genders[i+1])
        print(self.age, self.gender, num_detected)
        if num_detected==1: # 혼자왔어요
            a = self.age[0]
            g = self.gender[0]
            if a in range(0,10):
                rides_score["bumper_cars"] += 1
                rides_score["ferris_wheel"] += 1
                rides_score["merry_go_round"] += 3
                rides_score["safari"] += 2
                rides_score["swing_ride"] += 1
                rides_score["themepark_train"] += 3
            elif a in range(10,20):
                rides_score["bumper_cars"] += 3
                rides_score["ferris_wheel"] += 3
                rides_score["haunted_house"] += 1
                rides_score["merry_go_round"] += 3
                rides_score["roller_coaster"] += 1
                rides_score["safari"] += 3
                rides_score["swing_ride"] += 2
                rides_score["themepark_train"] += 3
                rides_score["viking"] += 1
            elif a in range(20,30):
                rides_score["bumper_cars"] += 2
                rides_score["ferris_wheel"] += 1
                rides_score["haunted_house"] += 3
                if g==0: rides_score["haunted_house"] += 2 
                rides_score["merry_go_round"] += 1
                rides_score["roller_coaster"] += 2
                rides_score["safari"] += 1
                rides_score["swing_ride"] += 2
                rides_score["themepark_train"] += 1
                rides_score["viking"] += 3
                if g==0: rides_score["viking"] += 2 
            elif a in range(30,40):
                rides_score["bumper_cars"] += 3
                rides_score["ferris_wheel"] += 3
                rides_score["haunted_house"] += 1
                rides_score["merry_go_round"] += 3
                rides_score["roller_coaster"] += 1
                rides_score["safari"] += 3
                rides_score["swing_ride"] += 2
                rides_score["themepark_train"] += 3
                rides_score["viking"] += 1
            elif a in range(40,50):
                rides_score["bumper_cars"] += 1
                rides_score["ferris_wheel"] += 3
                rides_score["merry_go_round"] += 3
                rides_score["safari"] += 3
                rides_score["swing_ride"] += 2
                rides_score["themepark_train"] += 3
                rides_score["viking"] += 1
            elif a in range(40,50):
                rides_score["ferris_wheel"] += 4
                rides_score["merry_go_round"] += 5
                rides_score["safari"] += 2
                rides_score["themepark_train"] += 3
        
        else:
            a = self.age[0]
            g = self.gender[0]
            if a in range(0,10):
                rides_score["bumper_cars"] += 1
                rides_score["ferris_wheel"] += 1
                rides_score["merry_go_round"] += 3
                rides_score["safari"] += 2
                rides_score["swing_ride"] += 1
                rides_score["themepark_train"] += 3
            elif a in range(10,20):
                rides_score["bumper_cars"] += 3
                rides_score["ferris_wheel"] += 3
                rides_score["haunted_house"] += 1
                rides_score["merry_go_round"] += 3
                rides_score["roller_coaster"] += 1
                rides_score["safari"] += 3
                rides_score["swing_ride"] += 2
                rides_score["themepark_train"] += 3
                rides_score["viking"] += 1
            elif a in range(20,30):
                rides_score["bumper_cars"] += 2
                rides_score["ferris_wheel"] += 1
                rides_score["haunted_house"] += 3
                if g==0: rides_score["haunted_house"] += 2 
                rides_score["merry_go_round"] += 1
                rides_score["roller_coaster"] += 2
                rides_score["safari"] += 1
                rides_score["swing_ride"] += 2
                rides_score["themepark_train"] += 1
                rides_score["viking"] += 3
                if g==0: rides_score["viking"] += 2 
            elif a in range(30,40):
                rides_score["bumper_cars"] += 3
                rides_score["ferris_wheel"] += 3
                rides_score["haunted_house"] += 1
                rides_score["merry_go_round"] += 3
                rides_score["roller_coaster"] += 1
                rides_score["safari"] += 3
                rides_score["swing_ride"] += 2
                rides_score["themepark_train"] += 3
                rides_score["viking"] += 1
            elif a in range(40,50):
                rides_score["bumper_cars"] += 1
                rides_score["ferris_wheel"] += 3
                rides_score["merry_go_round"] += 3
                rides_score["safari"] += 3
                rides_score["swing_ride"] += 2
                rides_score["themepark_train"] += 3
                rides_score["viking"] += 1
            elif a in range(40,50):
                rides_score["ferris_wheel"] += 4
                rides_score["merry_go_round"] += 5
                rides_score["safari"] += 2
                rides_score["themepark_train"] += 3
        
        top3 = sorted(rides_score, key=lambda x: rides_score[x], reverse=True)[:3]
        return top3
