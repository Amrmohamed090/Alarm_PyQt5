import sys
from PyQt5.QtCore import Qt, QUrl, QTimer, QTime,QRect,QSize

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent,QMediaPlaylist
from datetime import datetime
from qtwidgets import AnimatedToggle

styleSheet = """
QWidget {
    background-color: #fff;
} 
QLabel{
    color: #464d55;
    font-weight: 600;
    font-size: 18px;} 
    
QLabel#heading {
  color: #0f1925;
  font-size: 18px;
  margin-bottom: 10px;
}
QLabel#subheading {
  color: #0f1925;
  font-size: 12px;
  font-weight: normal;
  margin-bottom: 10px;
}
QLineEdit {
  border-radius: 8px;
  border: 1px solid #e0e4e7;
  padding: 5px 15px;
}
QLineEdit:focus {
  border: 1px solid #d0e3ff;
}
QLineEdit::placeholder {
  color: #767e89;
}
QPushButton {
  background-color: #38598b;
  
  color: #fff;
  font-weight: 600;
  border-radius: 8px;
  border: 1px solid #113f67;
  padding: 5px 15px;
  margin-top: 10px;
  outline: 0px;
}
QPushButton:hover{
  background-color: #113f67;
  border: 2px solid #113f67;
}

"""
clock_styleSheet = """QLabel{
    color: #464d55;
    font-weight: 600;
    font-size: 36px;} 
}"""


second_color = "#a2a8d3"
third_color= "#38598b"
fourth_color = "#113f67"


    


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.width=400
        self.height=600
        
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)
        self.setStyleSheet(styleSheet)
        
        #timer 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkTime)
        self.timer.start(50)
        
        # Create Alarm layout
        
        layout = QVBoxLayout()
        layout.addStretch()
        layout.setSpacing(5)
        
        #clock
        self.timer_label = QLabel(QTime.currentTime().toString("hh:mm:ss"))
        self.timer_label.setStyleSheet(clock_styleSheet)
        self.timer_label.setAlignment(Qt.AlignCenter)
        
        self.next_alarm_label = QLabel("All Alarms are off")
        self.next_alarm_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.timer_label)
        layout.addWidget(self.next_alarm_label)
      
        #add set Time layout to main layout
        self.hold_timer_up_1 = QTimer(self)
        self.hold_timer_up_2 = QTimer(self)
        self.hold_timer_down_1 = QTimer(self)
        self.hold_timer_down_2 = QTimer(self)
  
        self.pushButton_up_1 = QPushButton("+")  
        self.pushButton_up_1.pressed.connect(self.on_press_increase_hour)
        self.pushButton_up_1.released.connect(self.on_release_increase_hour)
        self.hold_timer_up_1.timeout.connect(self.increase_hour)
        
        
        self.pushButton_down_1 = QPushButton("-")
        self.pushButton_down_1.pressed.connect(self.on_press_decrease_hour)
        self.pushButton_down_1.released.connect(self.on_release_decrease_hour)
        self.hold_timer_down_1.timeout.connect(self.decrease_hour)
        
        self.pushButton_up_2 = QPushButton("+")
        self.pushButton_up_2.pressed.connect(self.on_press_increase_minute)
        self.pushButton_up_2.released.connect(self.on_release_increase_minute)
        self.hold_timer_up_2.timeout.connect(self.increase_minute)
        
        self.pushButton_down_2 = QPushButton("-")
        self.pushButton_down_2.pressed.connect(self.on_press_decrease_minute)
        self.pushButton_down_2.released.connect(self.on_release_decrease_minute)
        self.hold_timer_down_2.timeout.connect(self.decrease_minute)
        
        self.set_clock_hour = int(QTime.currentTime().hour())
        if self.set_clock_hour <10:
            self.set_clock_hour_label = QLabel("0"+str(self.set_clock_hour))
        else:
            self.set_clock_hour_label = QLabel(str(self.set_clock_hour))
        
        self.set_clock_minute = int(QTime.currentTime().minute())
        if self.set_clock_minute <10:
            self.set_clock_minute_label = QLabel("0"+str(self.set_clock_minute))
        else:
            self.set_clock_minute_label = QLabel(str(self.set_clock_minute))
        
        
        
        self.add_alarm_button = QPushButton("Add")
        self.add_alarm_button.clicked.connect(self.addAlarm)
        
       
        self.set_time_layout = QGridLayout()
        self.set_time_layout.addWidget(self.pushButton_up_1,1,0)
        self.set_time_layout.addWidget(self.set_clock_hour_label,2,0,alignment=Qt.AlignCenter)
        self.set_time_layout.addWidget(self.pushButton_down_1,3,0)
        self.set_time_layout.addWidget(self.add_alarm_button,2,5)
 
        
        self.set_time_layout.addWidget( QLabel(':'),2,2)
        
        self.set_time_layout.addWidget(self.pushButton_up_2,1,2)
        self.set_time_layout.addWidget(self.set_clock_minute_label,2,2,alignment=Qt.AlignCenter)
        self.set_time_layout.addWidget(self.pushButton_down_2,3,2)
        
         #repeate once row
        self.repeat_once_layout = QHBoxLayout()
        
        self.active_checkbox = AnimatedToggle(
            checked_color=fourth_color,
            pulse_checked_color=second_color
        )
        self.active_checkbox.setChecked(True)
        self.active_checkbox.setMaximumWidth(60)
        self.active_checkbox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.repeat_once_layout.addWidget(QLabel('repeat only once'))
        self.repeat_once_layout.addWidget(self.active_checkbox)
        
        self.repeat_once_layout.addStretch()
        self.repeat_once_layout.setSpacing(10)
        
        
        layout.addLayout(self.set_time_layout)
        layout.addLayout(self.repeat_once_layout)
        # add line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        #Create alarms layout
        self.alarms_layout = QVBoxLayout()
        widget = QWidget()
        self.alarms_layout = QVBoxLayout(widget)


        # create a scroll area and set the widget as its child
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        scroll_area.setMinimumWidth(300)
        scroll_area.setMinimumHeight(200)
      
        # add the scroll area to the layout
        layout.addWidget(scroll_area)
        
        layout.addLayout(self.alarms_layout)
    
        #add set alarm layout to main layout
        self.alarms_list = []
        
        layout.setAlignment(Qt.AlignTop)
        spacer = QSpacerItem(1, 4, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addItem(spacer)
        self.setLayout(layout)
        self.setWindowTitle('Alarm')
        self.show()
    
    
    def addAlarm(self):
        self.alarms_list.append(new_row(self.set_clock_hour, self.set_clock_minute, self.active_checkbox.isChecked()))
        self.alarms_layout.addLayout(self.alarms_list[-1])
        
    def checkTime(self):

        # getting current time
        current_time = QTime.currentTime()
        self.timer_label.setText(current_time.toString("hh:mm:ss"))
        min_delta = 999999999

        for alarm in self.alarms_list:
            should_be_triggered =  (alarm.hour == current_time.hour() and alarm.minute == current_time.minute())or(alarm.snoozeHour == current_time.hour() and alarm.snoozeMinute == current_time.minute())
            if should_be_triggered and alarm.triggered == False and alarm.active_checkbox.isChecked()==True:
                alarm.triggered = True
                dlg = CustomDialog(alarm)
                dlg.exec()
            elif should_be_triggered and alarm.triggered == True and alarm.active_checkbox.isChecked()==True:
                continue
            elif not (should_be_triggered and alarm.active_checkbox.isChecked()==True) and alarm.triggered == True:
                alarm.triggered = False
                
            # calculating the time left for the lable
            if  (not should_be_triggered)  and alarm.active_checkbox.isChecked()==True:
                alarm_time = datetime.strptime(f"{alarm.hour}:{alarm.minute}:00", "%H:%M:%S")
                c_time = datetime.strptime(f"{current_time.hour()}:{current_time.minute()}:{current_time.second()}", "%H:%M:%S")
                delta_seconds = (alarm_time-c_time).seconds
                if delta_seconds < min_delta:
                    min_delta = delta_seconds
            
        if not min_delta == 999999999:
            hour_left = int(min_delta/60/60)
            if hour_left == 0:
                hour_left = ""
            elif hour_left == 1:
                hour_left = f"{hour_left} hour "
            else:
                hour_left = f"{hour_left} hours "
                
            minute_left = int(((min_delta/3600)%1)*60)
            
            if minute_left == 0:
                minute_left = ""
            elif minute_left == 1:
                minute_left = f"{minute_left} minute "
            else:
                minute_left = f"{minute_left} minutes "
            
            seconds_left = ""
            if hour_left == "" :
                seconds_left = int(((((min_delta/3600)%1)*60)%1)*60)
                if seconds_left > 1:
                    seconds_left = f"{seconds_left} seconds "
                else:
                    seconds_left = f"{seconds_left} second "

            final_label = "Alarm in "+hour_left+minute_left+seconds_left
            self.next_alarm_label.setText(final_label)
        else:
            self.next_alarm_label.setText("All Alarms are off")
   
    ############### START hold Buttons methods ###############
    def increase_minute(self):
        self.set_clock_minute +=1
        if self.set_clock_minute > 59:
            self.set_clock_minute = 0
        if self.set_clock_minute < 10: 
            self.set_clock_minute_label.setText("0"+str(self.set_clock_minute))
        else:
            self.set_clock_minute_label.setText(str(self.set_clock_minute))
        
    def increase_hour(self):
        print("increase_hour")
        self.set_clock_hour +=1
        if self.set_clock_hour > 23:
            self.set_clock_hour = 0
        
        if self.set_clock_hour< 10:
            self.set_clock_hour_label.setText('0'+str(self.set_clock_hour))
        else:
            self.set_clock_hour_label.setText(str(self.set_clock_hour))
        
    def decrease_minute(self):
        self.set_clock_minute -=1
        if self.set_clock_minute < 0:
            self.set_clock_minute = 59
        if self.set_clock_minute< 10:
            self.set_clock_minute_label.setText("0"+str(self.set_clock_minute))
        else:
            self.set_clock_minute_label.setText(str(self.set_clock_minute))
            
    def decrease_hour(self):
        self.set_clock_hour -=1
        if self.set_clock_hour < 0:
            self.set_clock_hour = 23
        if self.set_clock_hour< 10:
            self.set_clock_hour_label.setText('0'+str(self.set_clock_hour))
        else:
            self.set_clock_hour_label.setText(str(self.set_clock_hour))
    

    def on_press_increase_hour(self):
        self.increase_hour()
        self.hold_timer_up_1.start(200)
    def on_release_increase_hour(self):
        self.hold_timer_up_1.stop()
        
    def on_press_increase_minute(self):
        self.increase_minute()
        self.hold_timer_up_2.start(100)
    def on_release_increase_minute(self):
        self.hold_timer_up_2.stop()
        
    def on_press_decrease_hour(self):
        self.decrease_hour()
        self.hold_timer_down_1.start(200)
    def on_release_decrease_hour(self):
        self.decrease_hour()
        self.hold_timer_down_1.stop()
        
    def on_press_decrease_minute(self):
        self.decrease_minute()
        self.hold_timer_down_2.start(100)
    def on_release_decrease_minute(self):
        self.hold_timer_down_2.stop()
        
        
    ############### END hold Buttons methods ###############
    
class new_row(QHBoxLayout):
    def __init__(self,hour : int ,minute: int, onlyOnce=True):
        super().__init__()
        hour_label= hour
        minute_label= minute
        if hour < 10:
            hour_label = f"0{hour}"
        if minute < 10:
            minute_label = f"0{minute}"
            
        self.time_label = QLabel(f'{hour_label} : {minute_label}')
        
        self.hour = hour
        self.minute = minute
        self.snoozeHour = hour
        self.snoozeMinute = minute
        self.snoozed = False
        self.onlyOnce = onlyOnce
        self.triggered = False
        
        self.ringtone = "./ringtone/morning_glory.mp3"
        
        self.active_checkbox = AnimatedToggle(
            checked_color=fourth_color,
            pulse_checked_color=second_color
        )
        self.active_checkbox.setChecked(True)
        self.active_checkbox.setMaximumWidth(60)
        
        
        
        
      
    

        style = QApplication.style()
       
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon("./icon/delete.png"))
        self.delete_button.clicked.connect(self.delete_mySelf)
        self.delete_button.setMaximumWidth(40)
        
        self.addWidget(self.time_label)
        self.addWidget(self.active_checkbox)
        self.addWidget(self.delete_button)
        
    def delete_mySelf(self):
        self.time_label.setParent(None)
        self.active_checkbox.setParent(None)
        self.delete_button.setParent(None)
        self.setParent(None)
        for i,_ in enumerate(window.alarms_list):
            if window.alarms_list[i].hour == self.hour and window.alarms_list[i].minute == self.minute and window.alarms_list[i].active_checkbox.isChecked() == self.active_checkbox.isChecked():
                window.alarms_list.remove(_)

class CustomDialog(QDialog):
    def __init__(self,alarm):
        super().__init__()
        self.current_time = QTime.currentTime()
        self.setWindowTitle("Alarm")
        self.setStyleSheet(styleSheet)
        self.alarm=alarm
        self.setFixedSize(300, 150)
        #ringtone play
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        url = QUrl.fromLocalFile(alarm.ringtone)
        content = QMediaContent(url)
        self.playlist.addMedia(content)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playlist)
        self.player.play()
                
        #layout
        self.layout = QVBoxLayout()
        message = QLabel("Alarm")
        message.setAlignment(Qt.AlignCenter)
        time_label = QLabel(self.current_time.toString("hh:mm"))
        time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(time_label)
        
        hbox = QHBoxLayout()
        self.ok_pushbutton = QPushButton("Ok")
        
        self.snooze_pushButton = QPushButton("Snooze")
        hbox.addWidget(self.ok_pushbutton)
        self.ok_pushbutton.clicked.connect(self.ok)
        hbox.addWidget(self.snooze_pushButton)
        self.snooze_pushButton.clicked.connect(self.snooze)
        
        self.layout.addLayout(hbox)
        self.setLayout(self.layout)             
        
    def ok(self):
        self.alarm.snoozed = False
        self.alarm.snoozeHour = self.alarm.hour
        self.alarm.snoozeMinute =  self.alarm.minute
        if self.alarm.onlyOnce:
            self.alarm.active_checkbox.setChecked(False)
        self.close()
                
    def snooze(self):
        self.alarm.snoozed = True
        hour = self.alarm.snoozeHour
        minute = self.alarm.snoozeMinute
        snooze_minute = 2
        if snooze_minute+minute > 59:
            self.alarm.snoozeHour = hour +1
            self.alarm.snoozeMinute = snooze_minute+minute - 60
        else:
            self.alarm.snoozeMinute = snooze_minute+minute
        self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())