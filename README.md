# Notre Dame College Admission Results Portal

![Flask](https://img.shields.io/badge/Flask-3.1.1-green?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A modern, responsive web application for Notre Dame College admission results checking system**

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Configuration](#️-configuration)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

## 🎯 Overview

The Notre Dame College Admission Results Portal is a comprehensive web application designed to streamline the admission results checking process for the 2025-2026 academic session. Built with Flask and modern web technologies, it provides students with an intuitive interface to check their admission status, view fee structures, and access important college information.

### Key Highlights

- **Real-time Results**: Instant admission status checking by roll number
- **Multi-department Support**: Science (Bengali/English), Humanities, and Business Studies
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Bilingual Interface**: English and Bengali language support
- **Modern UI/UX**: Glassmorphism design with smooth animations
- **RESTful API**: Well-structured backend API for data access

## ✨ Features

### 🔍 Core Functionality

- **Roll Number Search**: Students can search their admission status using application serial numbers
- **Department-wise Results**: Displays admitted department with Bengali translations
- **Fee Calculator**: Detailed fee breakdown including online charges and board registration
- **Admission Statistics**: Real-time statistics showing admission numbers by department
- **College Information**: Contact details, deadlines, and important notices

### 🎨 User Experience

- **Responsive Design**: Mobile-first approach with cross-device compatibility
- **Modern UI**: Glassmorphism effects with gradient backgrounds
- **Smooth Animations**: CSS transitions and loading states
- **Accessibility**: WCAG compliant design principles
- **Fast Loading**: Optimized static assets and efficient API calls

### 🔧 Technical Features

- **RESTful API**: Clean, documented API endpoints
- **Database Integration**: SQLAlchemy ORM with SQLite
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error management
- **Development Tools**: Debug mode and hot reloading

## 🛠 Technology Stack

### Backend

- **Framework**: Flask 3.1.1
- **Database**: SQLAlchemy 2.0.41 with SQLite
- **API**: RESTful architecture with Flask-CORS
- **Language**: Python 3.8+

### Frontend

- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome 6.0.0
- **Fonts**: Google Fonts (Inter)
- **Architecture**: Single Page Application (SPA)

### Development

- **Environment**: Virtual environment (venv)
- **Package Manager**: pip
- **Version Control**: Git
- **License**: MIT

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ndc-admission-results.git
   cd ndc-admission-results
   ```

2. **Create virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create database directory**

   ```bash
   mkdir -p src/database
   ```

5. **Run the application**

   ```bash
   python src/main.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`

### Docker Installation (Optional)

```bash
# Build Docker image
docker build -t ndc-admission-portal .

# Run container
docker run -p 8000:8000 ndc-admission-portal
```

## 📖 Usage

### For Students

1. **Check Admission Status**

   - Visit the portal homepage
   - Enter your application roll number
   - Click "Search" to view results

2. **View Fee Structure**

   - Click "View Fee Details" in the information section
   - Review department-wise fee breakdown
   - Note payment deadlines and methods

3. **Access College Information**
   - View contact details and important dates
   - Check admission statistics
   - Access college website and phone numbers

### For Administrators

1. **Update Admission Data**

   - Modify `src/admission_data.json`
   - Restart the application to reflect changes

2. **Monitor Usage**
   - Check application logs for search queries
   - Monitor API endpoint usage

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api
```

### Endpoints

#### Admission Endpoints

##### Search Roll Number

```http
GET /admission/search?roll={roll_number}
```

**Parameters:**

- `roll` (required): Student roll number (integer)

**Response:**

```json
{
  "roll_number": 12345,
  "selected": true,
  "department": "Science (Bengali Medium)",
  "department_bengali": "বিজ্ঞান বিভাগ (বাংলা মাধ্যম)",
  "fee_info": {
    "admission_fee": 7500,
    "tuition_fee": 9600,
    "july_board_registration": 3000,
    "hostel_bag_online_charge": 335,
    "total": 20435,
    "online_charge_1_percent": 204.35,
    "grand_total": 20639.35
  }
}
```

##### Get Admission Information

```http
GET /admission/info
```

**Response:**

```json
{
  "college_info": {
    "name": "Notre Dame College",
    "address": "P.O. Box No. 5, Motijheel, Dhaka-1000, Bangladesh",
    "phone": "7192325/7192598",
    "website": "ndc.edu.bd",
    "date": "August 14, 2025"
  },
  "admission_info": {
    "session": "2025-2026",
    "class": "Class XI (Ekadash)",
    "deadline": "August 17, 2025 at 12:00 PM",
    "contact_number": "01847601600",
    "fee_structure": { ... }
  }
}
```

##### Get Statistics

```http
GET /admission/stats
```

**Response:**

```json
{
  "total_selected": 2500,
  "departments": {
    "science_bengali": 2000,
    "science_english": 400,
    "humanities": 100,
    "business_studies": 0
  }
}
```

#### User Management Endpoints

##### Get All Users

```http
GET /users
```

##### Create User

```http
POST /users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com"
}
```

##### Get User by ID

```http
GET /users/{user_id}
```

##### Update User

```http
PUT /users/{user_id}
Content-Type: application/json

{
  "username": "updated_username",
  "email": "updated@example.com"
}
```

##### Delete User

```http
DELETE /users/{user_id}
```

## 📁 Project Structure

```
ndc-admission-results/
├── src/
│   ├── static/
│   │   ├── index.html          # Main HTML file
│   │   ├── styles.css          # CSS styles
│   │   └── script.js           # JavaScript functionality
│   ├── routes/
│   │   ├── admission.py        # Admission API routes
│   │   └── user.py            # User management routes
│   ├── models/
│   │   └── user.py            # User database model
│   ├── database/              # SQLite database directory
│   ├── admission_data.json    # Admission data storage
│   └── main.py               # Flask application entry point
├── venv/                     # Virtual environment
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT license
└── README.md                # Project documentation
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///src/database/app.db
```

### Application Settings

Key configuration options in `src/main.py`:

```python
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### Admission Data

Update `src/admission_data.json` to modify:

- College information
- Fee structures
- Selected student lists
- Department details

## 🤝 Contributing

We welcome contributions to improve the Notre Dame College Admission Portal!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful commit messages
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

### Code Style

```python
# Python code formatting
def search_roll_number(roll_number):
    """Search for student admission status by roll number."""
    # Implementation here
    pass
```

```javascript
// JavaScript code formatting
function searchRoll() {
  // Implementation here
}
```

## 🐛 Bug Reports

If you find a bug, please create an issue with:

- Bug description
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)
- Environment details

## 🔒 Security

- Input validation and sanitization
- CORS protection
- SQL injection prevention
- XSS protection
- Secure session management

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

- **Shafi Swapnil** - [GitHub Profile](https://github.com/shafiswapnil)
- **Email**: [swapnil.env@gmail.com](mailto:swapnil.env@gmail.com)
