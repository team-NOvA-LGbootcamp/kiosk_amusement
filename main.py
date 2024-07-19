import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from prediction import Predictor

if __name__ == "__main__":
    model = Predictor('./models', env="WINDOWS")
    app = QApplication(sys.argv)
    main_window = MainWindow(model)
    main_window.show()
    sys.exit(app.exec_())