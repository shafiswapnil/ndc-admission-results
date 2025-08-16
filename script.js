// Global variables
let admissionInfo = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadAdmissionInfo();
    loadStats();
    
    // Add enter key support for search
    document.getElementById('rollInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchRoll();
        }
    });
});

// Load admission information
async function loadAdmissionInfo() {
    try {
        const response = await fetch('/api/admission/info');
        if (!response.ok) throw new Error('Failed to load admission info');
        admissionInfo = await response.json();
    } catch (error) {
        console.error('Error loading admission info:', error);
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/admission/stats');
        if (!response.ok) throw new Error('Failed to load stats');
        const stats = await response.json();
        
        displayStats(stats);
    } catch (error) {
        console.error('Error loading stats:', error);
        document.getElementById('statsContent').innerHTML = '<p>Failed to load statistics</p>';
    }
}

// Display statistics
function displayStats(stats) {
    const statsContent = document.getElementById('statsContent');
    
    const statsHTML = `
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-number">${stats.total_selected}</div>
                <div class="stat-label">Total Selected</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${stats.departments.science_bengali || 0}</div>
                <div class="stat-label">Science (Bengali)</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${stats.departments.science_english || 0}</div>
                <div class="stat-label">Science (English)</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${stats.departments.humanities || 0}</div>
                <div class="stat-label">Humanities</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${stats.departments.business_studies || 0}</div>
                <div class="stat-label">Business Studies</div>
            </div>
        </div>
    `;
    
    statsContent.innerHTML = statsHTML;
}

// Search roll number
async function searchRoll() {
    const rollInput = document.getElementById('rollInput');
    const searchBtn = document.getElementById('searchBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultContent = document.getElementById('resultContent');
    
    const rollNumber = rollInput.value.trim();
    
    if (!rollNumber) {
        alert('Please enter a roll number');
        return;
    }
    
    // Show loading state
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
    searchBtn.disabled = true;
    
    try {
        const response = await fetch(`/api/admission/search?roll=${rollNumber}`);
        if (!response.ok) throw new Error('Search failed');
        
        const result = await response.json();
        
        // Display results
        displayResult(result);
        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error searching roll:', error);
        alert('Error occurred while searching. Please try again.');
    } finally {
        // Reset button state
        searchBtn.innerHTML = '<i class="fas fa-search"></i> Search';
        searchBtn.disabled = false;
    }
}

// Display search result
function displayResult(result) {
    const resultContent = document.getElementById('resultContent');
    
    if (result.selected) {
        // Student is selected
        const feeDetailsHTML = result.fee_info ? `
            <div class="fee-details">
                <h4>Fee Information</h4>
                <div class="fee-item">
                    <span>Admission Fee:</span>
                    <span>৳${result.fee_info.admission_fee.toLocaleString()}</span>
                </div>
                <div class="fee-item">
                    <span>Tuition Fee:</span>
                    <span>৳${result.fee_info.tuition_fee.toLocaleString()}</span>
                </div>
                <div class="fee-item">
                    <span>Board Registration:</span>
                    <span>৳${result.fee_info.july_board_registration.toLocaleString()}</span>
                </div>
                <div class="fee-item">
                    <span>Other Charges:</span>
                    <span>৳${result.fee_info.hostel_bag_online_charge.toLocaleString()}</span>
                </div>
                <div class="fee-item">
                    <span>Online Charge (1%):</span>
                    <span>৳${result.fee_info.online_charge_1_percent.toLocaleString()}</span>
                </div>
                <div class="fee-item">
                    <span><strong>Total Amount:</strong></span>
                    <span><strong>৳${result.fee_info.grand_total.toLocaleString()}</strong></span>
                </div>
            </div>
        ` : '';
        
        resultContent.innerHTML = `
            <div class="result-success">
                <div class="success-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h3>Congratulations! 🎉</h3>
                <div class="roll-number">Roll Number: ${result.roll_number}</div>
                <div class="department">
                    <strong>${result.department}</strong><br>
                    <span style="color: #667eea;">${result.department_bengali}</span>
                </div>
                <p style="color: #48bb78; font-weight: 600; margin-bottom: 20px;">
                    You have been selected for admission to Notre Dame College!
                </p>
                <p style="color: #4a5568; margin-bottom: 20px;">
                    Please complete your admission process by August 17, 2025 at 12:00 PM through the college website.
                </p>
                ${feeDetailsHTML}
            </div>
        `;
    } else {
        // Student is not selected
        resultContent.innerHTML = `
            <div class="result-failure">
                <div class="failure-icon">
                    <i class="fas fa-times-circle"></i>
                </div>
                <h3>Not Selected</h3>
                <div class="roll-number">Roll Number: ${result.roll_number}</div>
                <p>Unfortunately, this roll number was not selected for admission to Notre Dame College for the 2025-2026 academic session.</p>
                <p style="margin-top: 15px; color: #667eea;">
                    We encourage you to explore other educational opportunities. Best of luck with your future endeavors!
                </p>
            </div>
        `;
    }
}

// Show fee structure modal
function showFeeStructure() {
    if (!admissionInfo) {
        alert('Fee information is not available at the moment.');
        return;
    }
    
    const modal = document.getElementById('feeModal');
    const feeContent = document.getElementById('feeContent');
    
    const feeStructure = admissionInfo.admission_info.fee_structure;
    
    const feeHTML = `
        <table class="fee-table">
            <thead>
                <tr>
                    <th>Department</th>
                    <th>Admission Fee</th>
                    <th>Tuition Fee</th>
                    <th>Board Registration</th>
                    <th>Other Charges</th>
                    <th>Total Amount</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Science (Bengali Medium)</strong><br><small>বিজ্ঞান বিভাগ (বাংলা মাধ্যম)</small></td>
                    <td>৳${feeStructure.science_bengali.admission_fee.toLocaleString()}</td>
                    <td>৳${feeStructure.science_bengali.tuition_fee.toLocaleString()}</td>
                    <td>৳${feeStructure.science_bengali.july_board_registration.toLocaleString()}</td>
                    <td>৳${feeStructure.science_bengali.hostel_bag_online_charge.toLocaleString()}</td>
                    <td><strong>৳${feeStructure.science_bengali.grand_total.toLocaleString()}</strong></td>
                </tr>
                <tr>
                    <td><strong>Science (English Version)</strong><br><small>বিজ্ঞান বিভাগ (ইংরেজি ভার্সন)</small></td>
                    <td>৳${feeStructure.science_english.admission_fee.toLocaleString()}</td>
                    <td>৳${feeStructure.science_english.tuition_fee.toLocaleString()}</td>
                    <td>৳${feeStructure.science_english.july_board_registration.toLocaleString()}</td>
                    <td>৳${feeStructure.science_english.hostel_bag_online_charge.toLocaleString()}</td>
                    <td><strong>৳${feeStructure.science_english.grand_total.toLocaleString()}</strong></td>
                </tr>
                <tr>
                    <td><strong>Business Studies</strong><br><small>ব্যবসায় শিক্ষা বিভাগ</small></td>
                    <td>৳${feeStructure.business_studies.admission_fee.toLocaleString()}</td>
                    <td>৳${feeStructure.business_studies.tuition_fee.toLocaleString()}</td>
                    <td>৳${feeStructure.business_studies.july_board_registration.toLocaleString()}</td>
                    <td>৳${feeStructure.business_studies.hostel_bag_online_charge.toLocaleString()}</td>
                    <td><strong>৳${feeStructure.business_studies.grand_total.toLocaleString()}</strong></td>
                </tr>
                <tr>
                    <td><strong>Humanities</strong><br><small>মানবিক বিভাগ</small></td>
                    <td>৳${feeStructure.humanities.admission_fee.toLocaleString()}</td>
                    <td>৳${feeStructure.humanities.tuition_fee.toLocaleString()}</td>
                    <td>৳${feeStructure.humanities.july_board_registration.toLocaleString()}</td>
                    <td>৳${feeStructure.humanities.hostel_bag_online_charge.toLocaleString()}</td>
                    <td><strong>৳${feeStructure.humanities.grand_total.toLocaleString()}</strong></td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 20px; padding: 15px; background: #f7fafc; border-radius: 10px;">
            <p><strong>Note:</strong> All fees include a 1% online processing charge. Payment must be made through bKash Apps as specified in the admission notice.</p>
            <p style="margin-top: 10px;"><strong>Contact for queries:</strong> 01847601600</p>
        </div>
    `;
    
    feeContent.innerHTML = feeHTML;
    modal.style.display = 'block';
}

// Close fee structure modal
function closeFeeModal() {
    document.getElementById('feeModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('feeModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}