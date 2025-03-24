# AgriTrack Backend

AgriTrack is a farm management system that helps farmers and cooperatives manage their crops, track resources, and log farming activities. This is the backend repository built using Django.

## Features

- **Crop Management:** CRUD operations for crop profiles.
- **Resource Management:** CRUD operations for farming resources like seeds, fertilizers, etc.
- **Activity Tracking:** Log farming activities (planting, irrigation, harvesting) linked to crops.
- **Dashboard:** Displays crop stats, upcoming tasks, and growth progress.


## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/mcgarretronald/AgriTrack-Backend.git
cd AgriTrack-Backend
```
### 2. Set up a virtual environment:
```bash

python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  
   # For Windows
   ```
### 3. Install dependencies:
```bash
pip install -r requirements.txt
```
### 4. Apply migrations:
```bash
python manage.py migrate
```
### 5. Start the development server:
```bash
python manage.py runserver
```
Now you can access the API at http://127.0.0.1:8000.


