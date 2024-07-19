import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from main_window import MainWindow
from prediction import Predictor, RelationPredictor


def load_fonts(dir):
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont(dir)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        print(f"Registered font family: {font_family}")

if __name__ == "__main__":
    model = Predictor('./models', env="WINDOWS")  # 모델 경로와 환경 설정
    relation_model = RelationPredictor('./relationship_model/relationship_prediction_model_v1.h5', env="WINDOWS")
    app = QApplication(sys.argv)
    with open("style.qss", "r", encoding='utf-8') as f:
        stylesheet = f.read()
    load_fonts('fonts/HSSanTokki2.0(2024).ttf')
    
    app.setStyleSheet(stylesheet)
    main_window = MainWindow(model, relation_model)
    main_window.show()
    sys.exit(app.exec_())
