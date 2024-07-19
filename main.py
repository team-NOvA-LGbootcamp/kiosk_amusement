import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from prediction import Predictor, RelationPredictor

if __name__ == "__main__":
    model = Predictor('./models', env="WINDOWS")  # 모델 경로와 환경 설정
    relation_model = RelationPredictor('./relationship_model/relationship_prediction_model_v1.h5', env="WINDOWS")
    app = QApplication(sys.argv)
    main_window = MainWindow(model, relation_model)
    main_window.show()
    sys.exit(app.exec_())
