# TuReward
**Your Loyalty, Rewarded.**

TuReward is a digital loyalty system designed to help businesses such as restaurants, bars, and pharmacies enhance customer retention. Using QR codes, customers can easily collect points and redeem exclusive rewards, while businesses can efficiently manage their loyalty programs.

---

## Features
- **Custom User Management**: Separate user types (admins and customers) with a custom Django user model.
- **QR Code Integration**: Streamlined point collection and redemption.
- **Admin Dashboard**: Manage rewards, add points, and view transaction history.
- **User Dashboard**: Track points, view rewards, and link to businesses.
- **Comprehensive Backend**: Business creation, reward management, and user linking via Django Admin.

---

## Tech Stack
- **Backend**: Django, Django REST Framework, MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Design**: Adobe Illustrator (for logos and illustrations)

---

## Installation
1. Clone the repository: `git clone https://github.com/OscarFa28/TuReward.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the database and migrate:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
