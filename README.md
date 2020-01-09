# RetinaViewer
## 1. Goals & Objectives
### 1.1. Goals
  * Có demo tốt để thi vấn đáp cuối kỳ môn CNPM
  * Nâng cao kỹ năng làm việc nhóm
  * Nâng cao kỹ năng lập trình và xây dựng phần mềm
  * Nâng cao hiểu biết về các quá trính làm việc và cấu trúc chung cỏ tổ chức
### 1.2. Objectives
  * Phát triển phần mềm để ứng dụng vào thực tế tại các bệnh viện</li>
  * Tạo ra một phần mềm xem ảnh võng mạc, đưa ra tỉ lệ mắt có bị bệnh hay không</li>
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
## 3.Installation & Usages
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
### 3.2 Usages
#### Admin
* Admin creates or deletes doctor's account.
* Admin has no permission to view and diagnose patient. 
* Admin's username is "admin".
#### Doctor
* Doctor views patient's images, uses the viewer and gives diagnosis. 
* Doctor does not have admin's priviledges.
* Doctor's username should be his/her fullname in lowercase without spaces.
#### Special Feature
Auto diagnosis shows how likely a patient has diabetic retinopathy based on patient's retina image. With accuracy of over 91% on thousands test images, we hope this feature will help doctor make decision easier and more accurate!

