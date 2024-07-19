import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from prediction import Predictor

if __name__ == "__main__":
    model = Predictor('./models', env="WINDOWS")  # 모델 경로와 환경 설정
    app = QApplication(sys.argv)
    main_window = MainWindow(model)
    main_window.show()
    sys.exit(app.exec_())
