import os
import sys
import json
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS, cross_origin

# Add the parent directory to the path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Load admission data
def load_admission_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'admission_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

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
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Vercel handler
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=True)