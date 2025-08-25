import json
import os
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

admission_bp = Blueprint('admission', __name__)

# Load admission data
def load_admission_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'admission_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@admission_bp.route('/search', methods=['GET'])
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

@admission_bp.route('/info', methods=['GET'])
@cross_origin()
def get_admission_info():
    data = load_admission_data()
    return jsonify({
        'college_info': data['college_info'],
        'admission_info': data['admission_info']
    })

@admission_bp.route('/stats', methods=['GET'])
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

