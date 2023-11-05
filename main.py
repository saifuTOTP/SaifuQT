import sys, pyotp, time, re
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from functools import partial
import requests
import threading

widgets = {
    "button": [],
    "buttonTwo": [],
    "QuestionOne": [],
    "QuestionTwo": [],
    "SubmitBox": [],
    "CancelBox": [],
    "Imputs": [],
    "RemoveButtons": [],
    "QuestionAccount": []
}

data = {}

AccNum = ""
update = ""
APIWebsite = "flask.benmac.xyz"
boolLock1 = False
boolLock4 = False
ApiCheck = False

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Who wants to be a programmer???")
window.setFixedWidth(1080)
window.setFixedHeight(2400)
window.move(3700, 100)
window.setStyleSheet("background: #1e1e2e;")

grid = QGridLayout()


def updateLoop():
    global update
    global boolLock4

    while True:
        if (AccNum != "") & (boolLock4 == False):

            try:

                print(f'http://{APIWebsite}/checkAccountUpdates/{AccNum}')
                update = requests.get(f'http://{APIWebsite}/checkAccountUpdates/{AccNum}').text
                print(update)
                if update != 'no updates':
                    global ApiCheck
                    if update in data:
                        ApiCheck=True
                    else:
                        requests.get(f'http://{APIWebsite}/replyToUpdate/{AccNum}/invalidDomain')
                else:
                    ApiCheck = False
                    pass
            except:
                pass
        time.sleep(0.75)



refresh_timer = QtCore.QTimer()
api_timer = QtCore.QTimer()

update_timer = QtCore.QTimer()

update_thread = threading.Thread(target=updateLoop, daemon=True)

def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

    while grid.count():
        child = grid.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

def newOTP():
    global boolLock1
    boolLock1 = False
    global boolLock4
    boolLock4 = False
    clear_widgets()
    frame2()

def newAcc():
    global boolLock1
    boolLock1 = False
    global boolLock4
    boolLock4 = False
    clear_widgets()
    frame3()

def newCode():
    global boolLock1
    boolLock1 = False
    clear_widgets()
    frame4()

def CancelEvent():
    global boolLock4
    boolLock4 = False
    clear_widgets()
    frame1()

def YesEvent():
    global boolLock4
    boolLock4 = False
    requests.get(f'http://{APIWebsite}/replyToUpdate/{AccNum}/{str(pyotp.TOTP(data[update]).now())}')
    clear_widgets()
    frame1()

def NoEvent():
    global boolLock4
    boolLock4 = False
    requests.get(f'http://{APIWebsite}/replyToUpdate/{AccNum}/denied')
    clear_widgets()
    frame1()

def SubmitClicked():
    global boolLock4
    boolLock4 = False
    x = widgets["QuestionOne"][-1].text().lower()
    y = re.sub(r'[^A-Z2-7]', '', widgets["QuestionTwo"][-1].text())
    data[x] = y
    clear_widgets()
    frame1()

def AccSubmitClicked():
    global boolLock4
    boolLock4 = False
    x = widgets["QuestionAccount"][-1].text()
    global AccNum
    AccNum = x
    clear_widgets()
    frame1()

def removeEntry(key):
    global boolLock4
    boolLock4 = False
    if key in data:
        del data[key]
        clear_widgets()
        frame1()

def frame1():
    global boolLock1
    boolLock1 = True
    i = 0
    grid.addWidget(QPushButton(""), 40, 2)
    grid.addWidget(QPushButton(""), 40, 1)
    for key in data:
        x = QtWidgets.QLabel(key + ":" + " " + str(pyotp.TOTP(data[key]).now()))
        remove_button = QPushButton()
        remove_button.setIcon(QIcon("plus-circle-lavender.svg"))
        remove_button.setIconSize(QtCore.QSize(60, 60))
        remove_button.clicked.connect(partial(removeEntry, key))

        widgets["Imputs"].append(x)
        widgets["RemoveButtons"].append(remove_button)

        grid.addWidget(widgets["Imputs"][i], i + 1, 0)
        grid.addWidget(widgets["RemoveButtons"][i], i + 1, 1)

        x.setStyleSheet(
            "font-family: Shanti;" +
            "font-size: 50px;" +
            "color: '#f5c2e7';" +
            "padding: 10px;" +
            "margin-right: 15px;" +
            "margin-left: 75px;" +
            "border: 4px solid '#8e95b3';" +
            "border-radius: 15px;"
        )

        i = i + 1

    button = QPushButton()
    button.setIcon(QIcon("plus-circle-lavender.svg"))
    button.setIconSize(QtCore.QSize(200, 200))
    margin = 2000 - 100 * i
    button.setGeometry(QtCore.QRect(550, margin, 200, 200))
    button.setStyleSheet(
        f"margin-top: {margin}px;" +
        "margin-right: 155px;" +
        "margin-left: 845px;"
        "margin-bottom: 250px;"
    )

    buttonTwo = QPushButton()
    buttonTwo.setIcon(QIcon("plus-circle-skyblue.svg"))
    buttonTwo.setIconSize(QtCore.QSize(100, 100))
    buttonTwo.setStyleSheet(
        "margin-right: 865px;" +
        "margin-left: 85px;" +
        "margin-bottom: 25px;"
        "margin-top: 25px;"
    )

    widgets["button"].append(button)
    grid.addWidget(widgets["button"][-1], 40, 0)
    grid.addWidget(buttonTwo, 0, 0)
    button.clicked.connect(newOTP)
    buttonTwo.clicked.connect(newAcc)

def frame2():
    QuestionOne = QtWidgets.QLineEdit()
    QuestionOne.setPlaceholderText("Domain")
    QuestionOne.maxLength = 64

    QuestionOne.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 150px;" +
        "margin-top: 950px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )
    QuestionOne.setAlignment(QtCore.Qt.AlignCenter)

    QuestionTwo = QtWidgets.QLineEdit()
    QuestionTwo.setPlaceholderText("Character Key")
    QuestionTwo.maxLength = 64

    QuestionTwo.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 150px;" +
        "margin-bottom: 50px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )
    QuestionTwo.setAlignment(QtCore.Qt.AlignCenter)

    SubmitBox = QtWidgets.QPushButton("Submit")

    SubmitBox.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 350px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )

    CancelBox = QtWidgets.QPushButton("Cancel")

    CancelBox.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 350px;" +
        "margin-bottom: 950px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )

    widgets["CancelBox"].append(CancelBox)
    widgets["SubmitBox"].append(SubmitBox)
    widgets["QuestionOne"].append(QuestionOne)
    widgets["QuestionTwo"].append(QuestionTwo)
    grid.addWidget(widgets["QuestionOne"][-1], 0, 0)
    grid.addWidget(widgets["QuestionTwo"][-1], 1, 0)

    grid.addWidget(widgets["CancelBox"][-1], 3, 0)
    grid.addWidget(widgets["SubmitBox"][-1], 2, 0)
    CancelBox.clicked.connect(CancelEvent)
    SubmitBox.clicked.connect(SubmitClicked)

def frame3():
    QuestionAccount = QtWidgets.QLineEdit()
    QuestionAccount.setPlaceholderText("Account Number")
    QuestionAccount.maxLength = 64

    QuestionAccount.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 150px;" +
        "margin-top: 950px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )
    QuestionAccount.setAlignment(QtCore.Qt.AlignCenter)

    CancelBoxTwo = QtWidgets.QPushButton("Cancel")

    CancelBoxTwo.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 350px;" +
        "margin-bottom: 950px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )

    SubmitBoxTwo = QtWidgets.QPushButton("Submit")

    SubmitBoxTwo.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 350px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )

    widgets["QuestionAccount"].append(QuestionAccount)
    grid.addWidget(QuestionAccount, 0, 0)
    grid.addWidget(CancelBoxTwo, 3, 0)
    grid.addWidget(SubmitBoxTwo, 2, 0)
    CancelBoxTwo.clicked.connect(CancelEvent)
    SubmitBoxTwo.clicked.connect(AccSubmitClicked)

def frame4():
    global boolLock4
    boolLock4 = True

    YesBox = QtWidgets.QPushButton("Yes")

    YesBox.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 350px;" +
        "margin-top: 950px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )

    NoBox = QtWidgets.QPushButton("No")

    NoBox.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 50px;" +
        "color: '#f5c2e7';" +
        "padding: 10px;" +
        "margin: 0px 350px;" +
        "margin-bottom: 1000px;" +
        "border: 4px solid '#8e95b3';" +
        "border-radius: 15px;"
    )

    grid.addWidget(YesBox, 0, 0)
    grid.addWidget(NoBox, 1, 0)
    YesBox.clicked.connect(YesEvent)
    NoBox.clicked.connect(NoEvent)

def refresh_frame1():
    global boolLock1

    if boolLock1 == True:
        clear_widgets()
        frame1()

def ApiCheckUpdate():
    global ApiCheck
    if ApiCheck == True:
        newCode()

refresh_timer.timeout.connect(refresh_frame1)
refresh_timer.start(30000)

api_timer.timeout.connect(ApiCheckUpdate)
api_timer.start(2000)

update_thread.start()

frame1()
#newCode()
window.setLayout(grid)
window.show()
sys.exit(app.exec())
