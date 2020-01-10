# RetinaViewer
## 1. Goals & Objectives
### 1.1. Goals
  * Help doctor diagnose diabetic retinopathy quickly and accurately
### 1.2. Objectives
  * Build a retina image viewer app
  * Build a machine learning model to speed up disease detection
  * Integrate disease detection model in retina image viewer app
## 2. Tools & Technologies
### 2.1 Tools
  * PycharmIDE
  * PhpMyAdmin
  * MySQLServer
### 2.2. Technologies
  * Python
  * Tensorflow
  * OpenCV
  * Flask
## 3.Installation & Features
### 3.1 Installation
#### Supported Systems
* Windows 8/10
* Ubuntu
#### Requirements
  * Python 3.5+
  * MySQL Server
  * Tensorflow 1.9+
#### To install retina-viewer application:
```bat
git clone https://github.com/quandapro/SE03-group06
cd SE03-group06
```
Install external libraries and dependencies:
```bat
python -m pip install -r requirements.txt
```
Navigate to src/Flask, start the application by the following commands:
```bat
cd src/Flask
python main.py
```
Application is now live on port 5000.

Start MySQL Server or Xampp and create database retinadb. Then import retinadb.sql, which contains admin account and a dummy doctor account. 
### 3.2 Features
#### Admin
* Admin creates or deletes doctor's account. 
* Admin's username is "admin".
#### Doctor
* Doctor views patient's images, uses the viewer and gives diagnosis. 
* Doctor's username should be his/her fullname in lowercase without spaces.
#### Auto Diagnosis 
Auto diagnosis shows how likely a patient has diabetic retinopathy based on patient's retina image. With accuracy of over 91% on thousands test images, we hope this feature will help doctor make decision easier and more accurate!
#### Image Processing
Great variety of image processing methods to help doctor extract retina's features and easily detect herrmorhages, cotton wools spot, hard exudates present in retina. 
## Team members
* Dương Anh Quân (Team leader)
* Đào Quang Minh Hiếu
* Phạm Nhật Hiếu
* Trương Hoàng Giang

