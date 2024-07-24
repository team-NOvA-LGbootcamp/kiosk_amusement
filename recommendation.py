class RecommendationAlgorithm:
    def __init__(self):
        self.age = []
        self.gender = []
        self.scores = {
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

    def run_recommendation(self, ages, genders, relation):
        num_detected = len(ages)

        for i in range(num_detected):
            self.age.append(ages[i+1])
            self.gender.append(genders[i+1])

        if num_detected==1: 
            a = self.age[0]
            g = self.gender[0]

            if a in range(0,10):
                self.scores["bumper_cars"] += 4
                self.scores["ferris_wheel"] += 7
                self.scores["merry_go_round"] += 8
                self.scores["safari"] += 6
                self.scores["swing_ride"] += 5
                self.scores["themepark_train"] += 9
                if g==0:
                    self.scores["bumper_cars"] += 5
                    self.scores["safari"] += 5
                    self.scores["swing_ride"] += 5
            elif a in range(10,20):
                self.scores["bumper_cars"] += 4
                self.scores["merry_go_round"] += 9 
                self.scores["roller_coaster"] += 3
                self.scores["safari"] += 5
                self.scores["swing_ride"] += 8
                self.scores["themepark_train"] += 7
                self.scores["viking"] += 6
                if g==0:
                    self.scores["bumper_cars"] += 5
                    self.scores["haunted_house"] += 5
                    self.scores["roller_coaster"] += 5
                    self.scores["viking"] += 5
                if g==1:
                    self.scores["merry_go_round"] += 5
                    self.scores["ferris_wheel"] += 5
            elif a in range(20,30):
                self.scores["bumper_cars"] += 7
                self.scores["ferris_wheel"] += 6
                self.scores["haunted_house"] += 4
                self.scores["merry_go_round"] += 1
                self.scores["roller_coaster"] += 9
                self.scores["safari"] += 2
                self.scores["swing_ride"] += 5
                self.scores["themepark_train"] += 3
                self.scores["viking"] += 8 
                if g==0:
                    self.scores["bumper_cars"] += 5
                    self.scores["haunted_house"] += 5
                    self.scores["roller_coaster"] += 5
                    self.scores["viking"] += 5
                if g==1:
                    self.scores["ferris_wheel"] += 5
                    self.scores["merry_go_round"] += 5
                    self.scores["safari"] += 5
                    self.scores["swing_ride"] += 5
                    self.scores["themepark_train"] += 5
            elif a in range(30,40):
                self.scores["bumper_cars"] += 4
                self.scores["ferris_wheel"] += 5
                self.scores["haunted_house"] += 3
                self.scores["merry_go_round"] += 9
                self.scores["roller_coaster"] += 2
                self.scores["safari"] += 8
                self.scores["swing_ride"] += 6
                self.scores["themepark_train"] += 7
                self.scores["viking"] += 1
                if g==0:
                    self.scores["bumper_cars"] += 3
                    self.scores["haunted_house"] += 3
                    self.scores["roller_coaster"] += 3
                    self.scores["viking"] += 3
            elif a in range(40,50):
                self.scores["ferris_wheel"] += 9
                self.scores["merry_go_round"] += 5
                self.scores["safari"] += 8
                self.scores["swing_ride"] += 6
                self.scores["themepark_train"] += 7
                if g==0:
                    self.scores["bumper_cars"] += 5
                    self.scores["haunted_house"] += 5
                    self.scores["roller_coaster"] += 5
                    self.scores["viking"] += 5
            elif a in range(50,60):
                self.scores["ferris_wheel"] += 9
                self.scores["merry_go_round"] += 5
                self.scores["safari"] += 8
                self.scores["swing_ride"] += 6
                self.scores["themepark_train"] += 7
                if g==0:
                    self.scores["bumper_cars"] += 5
                    self.scores["haunted_house"] += 5
                    self.scores["roller_coaster"] += 5
                    self.scores["viking"] += 5
        
        if num_detected==2:
            a = self.age
            g = self.gender

            if relation in ["family", "friend"]:
                if a[0] in range(0,10):
                    if a[1] in range(0,10):
                        self.scores["safari"] += 2
                        self.scores["swing_ride"] += 5
                        self.scores["themepark_train"] += 3
                    elif a[1] in range(10,20):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    elif a[1] in range(20,30):
                        self.scores["bumper_cars"] += 3
                        self.scores["safari"] += 2
                        self.scores["themepark_train"] += 1
                    elif a[1] in range(30,40):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    else:
                        self.scores["merry_go_round"] += 1
                        self.scores["safari"] +=  2
                        self.scores["themepark_train"] += 3
                elif a[0] in range(10,20):
                    if a[1] in range(0,10):
                        self.scores["safari"] += 2
                        self.scores["swing_ride"] += 5
                        self.scores["themepark_train"] += 3
                    elif a[1] in range(10,20):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    elif a[1] in range(20,30):
                        self.scores["bumper_cars"] += 3
                        self.scores["safari"] += 2
                        self.scores["themepark_train"] += 1
                    elif a[1] in range(30,40):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    else:
                        self.scores["merry_go_round"] += 1
                        self.scores["safari"] +=  2
                        self.scores["themepark_train"] += 3
                elif a[0] in range(20,30):
                    if a[1] in range(0,10):
                        self.scores["safari"] += 2
                        self.scores["swing_ride"] += 5
                        self.scores["themepark_train"] += 3
                    elif a[1] in range(10,20):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    elif a[1] in range(20,30):
                        self.scores["bumper_cars"] += 3
                        self.scores["safari"] += 2
                        self.scores["themepark_train"] += 1
                    elif a[1] in range(30,40):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    else:
                        self.scores["merry_go_round"] += 1
                        self.scores["safari"] +=  2
                        self.scores["themepark_train"] += 3
                elif a[0] in range(30,40):
                    if a[1] in range(0,10):
                        self.scores["safari"] += 2
                        self.scores["swing_ride"] += 5
                        self.scores["themepark_train"] += 3
                    elif a[1] in range(10,20):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    elif a[1] in range(20,30):
                        self.scores["bumper_cars"] += 3
                        self.scores["safari"] += 2
                        self.scores["themepark_train"] += 1
                    elif a[1] in range(30,40):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    else:
                        self.scores["merry_go_round"] += 1
                        self.scores["safari"] +=  2
                        self.scores["themepark_train"] += 3
                elif a[0] in range(40,50):
                    if a[1] in range(0,10):
                        self.scores["safari"] += 2
                        self.scores["swing_ride"] += 5
                        self.scores["themepark_train"] += 3
                    elif a[1] in range(10,20):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    elif a[1] in range(20,30):
                        self.scores["bumper_cars"] += 3
                        self.scores["safari"] += 2
                        self.scores["themepark_train"] += 1
                    elif a[1] in range(30,40):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    else:
                        self.scores["merry_go_round"] += 1
                        self.scores["safari"] +=  2
                        self.scores["themepark_train"] += 3
                else:
                    if a[1] in range(0,10):
                        self.scores["safari"] += 2
                        self.scores["swing_ride"] += 5
                        self.scores["themepark_train"] += 3
                    elif a[1] in range(10,20):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    elif a[1] in range(20,30):
                        self.scores["bumper_cars"] += 3
                        self.scores["safari"] += 2
                        self.scores["themepark_train"] += 1
                    elif a[1] in range(30,40):
                        self.scores["ferris_wheel"] += 1
                        self.scores["merry_go_round"] += 2
                        self.scores["safari"] += 3
                    else:
                        self.scores["merry_go_round"] += 1
                        self.scores["safari"] +=  2
                        self.scores["themepark_train"] += 3
            if relation=="couple":
                self.scores["safari"] += 8
                self.scores["ferris_wheel"] += 6
                self.scores["haunted_house"] += 7

        if num_detected==3:
            a = self.age
            g = self.gender
            if relation =="family":
                self.scores["safari"] += 3
                self.scores["merry_go_round"] += 2
                self.scores["themepark_train"] += 1
            if relation =="friend" or relation =="couple":
                self.scores["bumper_cars"] += 3
                self.scores["roller_coaster"] += 2
                self.scores["safari"] += 1

        if num_detected==4:
            a = self.age
            g = self.gender

            if relation =="family":
                self.scores["safari"] += 3
                self.scores["merry_go_round"] += 2
                self.scores["themepark_train"] += 1
            if relation =="friend" or relation =="couple":
                self.scores["bumper_cars"] += 3
                self.scores["roller_coaster"] += 2
                self.scores["safari"] += 1
        
        if num_detected>4:
            if relation =="family":
                self.scores["safari"] += 3
                self.scores["merry_go_round"] += 2
                self.scores["themepark_train"] += 1
            if relation =="friend" or relation =="couple":
                self.scores["bumper_cars"] += 3
                self.scores["roller_coaster"] += 2
                self.scores["safari"] += 1

      
        top3 = sorted(self.scores, key=lambda x: self.scores[x], reverse=True)[:3]
        return top3