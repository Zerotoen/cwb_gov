import os,csv,time,urllib,pandas,pandas_bokeh 
from mainwindow import Ui_MainWindow
from PyQt6 import QtWidgets, QtGui, QtCore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class MainWindow_controller(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__() 
        self.cwb_gov = cwb_gov()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.comboBox = self.ui.comboBox
        self.lineEdit = self.ui.lineEdit
        self.tableWidget = self.ui.tableWidget
        self.ui.search_Button.clicked.connect(self.search_weather)
        self.ui.drawing_Button.clicked.connect(self.drawing_check)
        self.check_point = None
    def search_weather(self):
        country={
          '苗栗縣':'10005','連江縣':'09007','彰化縣':'10007',
          '雲林縣':'10009','金門縣':'09020','澎湖縣':'10016',
          '嘉義縣':'10010','南投縣':'10008','臺東縣':'10014',
          '屏東縣':'10013','花蓮縣':'10015','宜蘭縣':'10002',
          '新竹縣':'10004','基隆市':'10017','新竹市':'10018',
          '新北市':'65','桃園市':'68','臺北市':'63',
          '臺中市':'66','臺南市':'67','高雄市':'64',
          '台中市':'66','台南市':'67','台北市':'63',
          '台東縣':'10014','嘉義市':'10020'
          }
        
        if self.lineEdit.text() == '':
           edit_text = self.comboBox.currentText()
        else:
            edit_text = self.lineEdit.text()   
            
        if edit_text in country:
            self.check_point = True
            self.cwb_gov.scrape_weather_data(country[edit_text])
            datelist, daytimelist, nightlist, lo_templist, uvi_wraplist = self.cwb_gov.scrape_weather_data(edit_text)
            self.tableWidget.setRowCount(4)
            self.tableWidget.setColumnCount(len(datelist))
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            vitems = ['白天(°C)', '晚上(°C)', '體感溫度(°C)', '紫外線（UVI）']
            for i in range(len(vitems)):
                item = QtWidgets.QTableWidgetItem(vitems[i])
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setVerticalHeaderItem(i, item)
            
            for i in range(len(datelist)):
                item = QtWidgets.QTableWidgetItem(datelist[i])
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setHorizontalHeaderItem(i, item)   
                
            for i in range(len(daytimelist)):
                item = QtWidgets.QTableWidgetItem(daytimelist[i])
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(0, i, item)
                
            for i in range(len(nightlist)):
                item = QtWidgets.QTableWidgetItem(nightlist[i])
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(1, i, item)
                
            for i in range(len(lo_templist)):
                item = QtWidgets.QTableWidgetItem(lo_templist[i])
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(2, i, item)
                
            for i in range(len(uvi_wraplist)):
                item = QtWidgets.QTableWidgetItem(uvi_wraplist[i])
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(3, i, item)
        else:
              self.tableWidget.setRowCount(1)
              self.tableWidget.setColumnCount(1)
              self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
              self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
              item = QtWidgets.QTableWidgetItem('目前無此資料')
              item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
              self.tableWidget.setItem(0, 0, item)  
              
    def drawing_check(self):
        if self.check_point == True:
            if self.lineEdit.text() == '':
               edit_text = self.comboBox.currentText()
            else:
                edit_text = self.lineEdit.text()   
            self.cwb_gov.csv_drawing(edit_text)

        else:
            self.tableWidget.setRowCount(1)
            self.tableWidget.setColumnCount(1)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            item = QtWidgets.QTableWidgetItem('目前尚未讀取資料')
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(0, 0, item)  
            
class cwb_gov():
    def __init__(self):
        super().__init__() 
        
        op=webdriver.ChromeOptions()
        op.add_argument("headless")
        self.web=webdriver.Chrome(options=op)
        WebDriverWait(self.web, 10)
        self.datelist=[]
        self.daytimelist=[]
        self.nightlist=[]
        self.lo_templist=[]
        self.uvi_wraplist=[]
        
    def scrape_weather_data(self, edit_text):
        url='https://www.cwb.gov.tw/V8/C/W/County/County.html?CID={}'.format(edit_text)
        self.web.get(url)
        self.datelist=[]
        self.daytimelist=[]
        self.nightlist=[]
        self.lo_templist=[]
        self.uvi_wraplist=[]
        
        main = self.web.find_element(By.CLASS_NAME , 'panel-group')
    
        for date in main.find_elements(By.CLASS_NAME , 'date'):
            self.datelist.append(date.text)
        
        for daytime in main.find_elements(By.CLASS_NAME , 'Day'):
            self.daytimelist.append(daytime.text)
        
        for night in main.find_elements(By.CLASS_NAME , 'Night'):
            self.nightlist.append(night.text)
        
        openslider = main.find_element(By.XPATH , '//*[@id="heading-1"]/h4/a')
        self.web.execute_script("arguments[0].setAttribute('aria-expanded' , 'true')" , openslider)
        inside = main.find_element(By.XPATH , '//*[@id="collapse-1"]')
        lo_temp = inside.find_element(By.XPATH , '//*[@id="collapse-1"]/div/ul[1]/li[2]/span[1]')
        uvi_wrap = inside.find_element(By.XPATH , '//*[@id="collapse-1"]/div/ul[2]/li[2]/span')
        self.lo_templist.append(lo_temp.text)
        self.uvi_wraplist.append(uvi_wrap.text)
        
        for i in range(2, 8):
            self.web.find_element(By.XPATH , f'//*[@id="heading-{i}"]/h4/a').click()
            time.sleep(1)
            lo_temp = main.find_element(By.XPATH , f'//*[@id="collapse-{i}"]/div/ul[1]/li[2]/span[1]')
            uvi_wrap = main.find_element(By.XPATH , f'//*[@id="collapse-{i}"]/div/ul[2]/li[2]/span')
            self.lo_templist.append(lo_temp.text)
            self.uvi_wraplist.append(uvi_wrap.text)
            
        return self.datelist, self.daytimelist, self.nightlist, self.lo_templist, self.uvi_wraplist
        
    def csv_drawing(self, edit_text):

        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        os.chdir(script_dir)
        folder_path = os.path.join(script_dir, 'file')
        os.makedirs(folder_path, exist_ok=True)
        os.chdir('file')
        filename = '{}{}-{}.csv'.format(edit_text,self.datelist[0].split('\n')[1].replace('/', ''), self.datelist[-1].split('\n')[1].replace('/', ''))
        if not os.path.isfile(filename):
            with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile)
                colname = ['日期', '白天', '晚上', '白天體感', '晚上體感', '紫外線']
                writer.writerow(colname)
                
                for i in range(len(self.datelist)):
                    data1 = self.datelist[i].split('\n')[1] 
                    data2 = self.daytimelist[i].split('\n')[1][-2:]
                    data3 = self.nightlist[i].split('\n')[1][:3]
                    data4 = self.lo_templist[i].split(' ')[-1]
                    data5 = self.lo_templist[i].split(' ')[0]
                    data6 = self.uvi_wraplist[i][0]
                    writer.writerow([data1, data2, data3, data4, data5, data6])
                
        pandas_bokeh.output_file(f"{filename}.html")
        dF=pandas.read_csv(filename)
        dF.plot_bokeh(kind="line",x="日期",line_width=5,title="一周預報",line_alpha=0.3,figsize=(1200,800),ylabel="溫度(攝氏C)/紫外線（UVI）") 
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), '..')))
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())    












