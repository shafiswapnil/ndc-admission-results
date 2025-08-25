import os
import sys
import json
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS, cross_origin

# Get the root directory (parent of api folder)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(ROOT_DIR, 'src', 'static')
DATA_PATH = os.path.join(ROOT_DIR, 'src', 'admission_data.json')

app = Flask(__name__, static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Cache admission data to avoid reading file multiple times
_admission_data = None

def load_admission_data():
    global _admission_data
    if _admission_data is None:
        try:
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                _admission_data = json.load(f)
        except Exception as e:
            print(f"Error loading admission data: {e}")
            # Return default data structure if file not found
            _admission_data = {
                'college_info': {},
                'admission_info': {'fee_structure': {}},
                'selected_students': {
                    'science_bengali': [],
                    'science_english': [],
                    'humanities': [],
                    'business_studies': []
                }
            }
    return _admission_data

# Admission routes
@app.route('/api/admission/search', methods=['GET'])
@cross_origin()
def search_roll():
    roll_number = request.args.get('roll')
    if not roll_number:
        return jsonify({'error': 'Roll number is required'}), 400
    
    try:
        roll_number = int(roll_number)
    except ValueError:
        return jsonify({'error': 'Invalid roll number format'}), 400
    
    data = load_admission_data()
    
    # Search in all departments
    result = {
        'roll_number': roll_number,
        'selected': False,
        'department': None,
        'department_bengali': None,
        'fee_info': None
    }
    
    # Check Science Bengali
    if roll_number in data['selected_students']['science_bengali']:
        result['selected'] = True
        result['department'] = 'Science (Bengali Medium)'
        result['department_bengali'] = 'বিজ্ঞান বিভাগ (বাংলা মাধ্যম)'
        result['fee_info'] = data['admission_info']['fee_structure']['science_bengali']
    
    # Check Science English
    elif roll_number in data['selected_students']['science_english']:
        result['selected'] = True
        result['department'] = 'Science (English Version)'
        result['department_bengali'] = 'বিজ্ঞান বিভাগ (ইংরেজি ভার্সন)'
        result['fee_info'] = data['admission_info']['fee_structure']['science_english']
    
    # Check Humanities
    elif roll_number in data['selected_students']['humanities']:
        result['selected'] = True
        result['department'] = 'Humanities'
        result['department_bengali'] = 'মানবিক বিভাগ'
        result['fee_info'] = data['admission_info']['fee_structure']['humanities']
    
    # Check Business Studies
    elif roll_number in data['selected_students']['business_studies']:
        result['selected'] = True
        result['department'] = 'Business Studies'
        result['department_bengali'] = 'ব্যবসায় শিক্ষা বিভাগ'
        result['fee_info'] = data['admission_info']['fee_structure']['business_studies']
    
    return jsonify(result)

@app.route('/api/admission/info', methods=['GET'])
@cross_origin()
def get_admission_info():
    data = load_admission_data()
    return jsonify({
        'college_info': data['college_info'],
        'admission_info': data['admission_info']
    })

@app.route('/api/admission/stats', methods=['GET'])
@cross_origin()
def get_stats():
    data = load_admission_data()
    stats = {
        'total_selected': 0,
        'departments': {}
    }
    
    for dept, students in data['selected_students'].items():
        count = len(students)
        stats['departments'][dept] = count
        stats['total_selected'] += count
    
    return jsonify(stats)

# Serve static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    try:
        if path and path != "":
            # Try to serve the requested file
            file_path = os.path.join(STATIC_DIR, path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return send_from_directory(STATIC_DIR, path)
        
        # Default to index.html
        index_path = os.path.join(STATIC_DIR, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(STATIC_DIR, 'index.html')
        else:
            return jsonify({'error': 'Application not found', 'static_dir': STATIC_DIR}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'path': path}), 500

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'root_dir': ROOT_DIR,
        'static_dir': STATIC_DIR,
        'data_path': DATA_PATH,
        'data_exists': os.path.exists(DATA_PATH),
        'static_exists': os.path.exists(STATIC_DIR)
    })

if __name__ == '__main__':
    app.run(debug=True)