import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from main_window import MainWindow
from prediction import Predictor, RelationPredictor

folder_dir = os.path.dirname(os.path.realpath(__file__))
AGE_GENDER_MODEL_PATH = folder_dir+'/models/age_gender'
REALTIONSHIP_MODEL_PATH = folder_dir+'/models/relationship'

def load_fonts(dir):
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont(dir)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        print(f"Registered font family: {font_family}")

if __name__ == "__main__":
    try:
        _env = sys.argv[1] #ex)WINDOWS, RASPBERRY(default)
    except:
        _env = "RASPBERRY"
    model = Predictor(AGE_GENDER_MODEL_PATH, env=_env)  # 모델 경로와 환경 설정
    relation_model = RelationPredictor(REALTIONSHIP_MODEL_PATH, env=_env)
    app = QApplication(sys.argv)
    with open("style.qss", "r", encoding='utf-8') as f:
        stylesheet = f.read()
    load_fonts('fonts/HSSanTokki2.0(2024).ttf')
    app.setStyleSheet(stylesheet)
    main_window = MainWindow(model, relation_model, _env)
    main_window.show()
    sys.exit(app.exec_())
