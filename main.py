import configparser
import sys

from PyQt5.QtGui import QIcon
from SendEmail import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
# Press the green button in the gutter to run the script.
class main():
  def load_config(self):
    print(self.lineEdit.text())
    config = configparser.ConfigParser()
    file = config.read('user.ini')

    if file:
      config_dict = config.defaults()
      if len(config_dict)!=0:
        user_name = config_dict['user']
        self.lineEdit.setText(user_name.format())
        password = config_dict['passt']
        self.lineEdit_2.setText(password)
        receiver = config_dict['receiver']
        self.lineEdit_3.setText(receiver)
        if config_dict['checkbox'] == 'True':
          self.checkBox_2.setChecked(True)
        else:
          self.checkBox_2.setChecked(False)
        if config_dict['emailtype']=='QQ邮箱':
          self.comboBox.setCurrentIndex(1)
        elif config_dict['emailtype']=='新浪邮箱':
          self.comboBox.setCurrentIndex(2)
        elif config_dict['emailtype']=='163邮箱':
          self.comboBox.setCurrentIndex(3)
        else:
          self.comboBox.setCurrentIndex(0)


if __name__ == '__main__':

  app=QApplication(sys.argv)
  app.setWindowIcon(QIcon('Emali.png'))
  mainwind=QMainWindow()
  mainview=Ui_MainWindow()
  mainview.setupUi(mainwind)
  main.load_config(mainview)
  mainwind.show()
  app.exit(app.exec_())




