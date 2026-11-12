import os
import sys
import json
import io
from flask import Flask, jsonify, request, send_from_directory, send_file, Response
import pandas as pd

# Define absolute base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
DATA_DIR = os.path.join(BACKEND_DIR, 'data')
CHARTS_DIR = os.path.join(BACKEND_DIR, 'static', 'charts')

# Ensure backend folder is on Python path
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Data file paths
DATA_PATH = os.path.join(DATA_DIR, 'lakes_master.json')
STORIES_PATH = os.path.join(DATA_DIR, 'before_after_stories.json')

# Check if data or charts need to be generated automatically on startup
if not os.path.exists(DATA_PATH) or not os.path.exists(STORIES_PATH):
    print("Master datasets not found. Running data pipeline...")
    import data_pipeline

from chart_generator import (
    generate_chart_status_by_zone,
    generate_chart_area_distribution,
    generate_chart_wqi_density,
    generate_chart_before_after_metrics,
    generate_chart_encroachment_correlation,
    generate_chart_custodian_breakdown,
    generate_all_charts
)

# Ensure all 6 charts are generated
if not os.path.exists(CHARTS_DIR) or len(os.listdir(CHARTS_DIR)) < 6:
    print("Generating Matplotlib and Seaborn charts...")
    generate_all_charts()

# Initialize Flask application with frontend static directory
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

# Global CORS Headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

def get_master_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_stories_data():
    with open(STORIES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# ------------------------------------------------------------------------------
# 1. FRONTEND WEB APPLICATION SERVING
# ------------------------------------------------------------------------------
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return jsonify({'error': f'Path /{path} not found'}), 404

# ------------------------------------------------------------------------------
# 2. REST API: LAKES DATA WITH ADVANCED MULTI-CRITERIA FILTERS
# ------------------------------------------------------------------------------
@app.route('/api/lakes', methods=['GET'])
def get_lakes():
    lakes = get_master_data()
    
    # Query parameters
    zone = request.args.get('zone', '').strip()
    status = request.args.get('status', '').strip()
    search = request.args.get('search', '').strip().lower()
    min_acres = request.args.get('min_acres', type=float)
    max_acres = request.args.get('max_acres', type=float)
    min_wqi = request.args.get('min_wqi', type=float)
    has_track = request.args.get('has_track', '').strip().lower()
    
    filtered = []
    for l in lakes:
        if zone and l['zone'].lower() != zone.lower() and zone.lower() != 'all':
            continue
        if status and l['status'].lower() != status.lower() and status.lower() != 'all':
            continue
        if search and (search not in l['name'].lower() and search not in l['village_survey'].lower()):
            continue
        if min_acres is not None and l['acres'] < min_acres:
            continue
        if max_acres is not None and l['acres'] > max_acres:
            continue
        if min_wqi is not None and l['wqi'] < min_wqi:
            continue
        if has_track == 'true' and not l['has_walking_track']:
            continue
        filtered.append(l)
        
    return jsonify({
        'total': len(filtered),
        'total_unfiltered': len(lakes),
        'lakes': filtered
    })

@app.route('/api/lakes/<int:lake_id>', methods=['GET'])
def get_lake_by_id(lake_id):
    lakes = get_master_data()
    for l in lakes:
        if l['id'] == lake_id:
            return jsonify(l)
    return jsonify({'error': 'Lake not found'}), 404

# ------------------------------------------------------------------------------
# 3. REST API: AGGREGATED METRICS & KPIS
# ------------------------------------------------------------------------------
@app.route('/api/stats', methods=['GET'])
def get_stats():
    lakes = get_master_data()
    df = pd.DataFrame(lakes)
    
    total_lakes = len(df)
    total_acres = round(float(df['acres'].sum()), 1)
    developed_count = int((df['status'] == 'Developed / Rejuvenated').sum())
    wip_count = int((df['status'] == 'Work in Progress').sum())
    tbd_count = int((df['status'] == 'To Be Developed').sum())
    encroached_count = int((df['status'] == 'Degraded / Encroached').sum())
    
    rejuvenation_rate = round((developed_count / total_lakes) * 100, 1)
    avg_wqi = round(float(df['wqi'].mean()), 1)
    total_encroached_acres = round(float((df['acres'] * (df['encroachment_pct'] / 100.0)).sum()), 1)
    
    zone_distribution = df['zone'].value_counts().to_dict()
    status_distribution = df['status'].value_counts().to_dict()
    
    return jsonify({
        'total_lakes': total_lakes,
        'total_acres': total_acres,
        'developed_count': developed_count,
        'wip_count': wip_count,
        'tbd_count': tbd_count,
        'encroached_count': encroached_count,
        'rejuvenation_rate_pct': rejuvenation_rate,
        'avg_wqi': avg_wqi,
        'total_encroached_acres': total_encroached_acres,
        'zone_distribution': zone_distribution,
        'status_distribution': status_distribution,
        'largest_lake': {
            'name': df.loc[df['acres'].idxmax(), 'name'],
            'acres': float(df['acres'].max()),
            'zone': df.loc[df['acres'].idxmax(), 'zone']
        },
        'cleanest_lake': {
            'name': df.loc[df['wqi'].idxmax(), 'name'],
            'wqi': float(df['wqi'].max()),
            'status': df.loc[df['wqi'].idxmax(), 'status']
        }
    })

# ------------------------------------------------------------------------------
# 4. REST API: BEFORE / AFTER REJUVENATION STORIES
# ------------------------------------------------------------------------------
@app.route('/api/story', methods=['GET'])
def get_stories():
    stories = get_stories_data()
    story_id = request.args.get('id', '').strip().lower()
    if story_id:
        for s in stories:
            if s['id'] == story_id:
                return jsonify(s)
        return jsonify({'error': 'Story not found'}), 404
    return jsonify({'total': len(stories), 'stories': stories})

# ------------------------------------------------------------------------------
# 5. REST API: PYTHON CHARTS (MATPLOTLIB & SEABORN)
# ------------------------------------------------------------------------------
@app.route('/api/charts/<chart_id>', methods=['GET'])
def serve_chart(chart_id):
    zone = request.args.get('zone', '').strip()
    
    filename_map = {
        'status_by_zone': 'chart1_status_by_zone.png',
        'area_distribution': 'chart2_area_distribution.png',
        'wqi_density': 'chart3_wqi_density.png',
        'before_after_metrics': 'chart4_before_after_metrics.png',
        'encroachment_correlation': 'chart5_encroachment_correlation.png',
        'custodian_breakdown': 'chart6_custodian_breakdown.png'
    }
    
    if chart_id not in filename_map:
        return jsonify({'error': f'Invalid chart ID. Available: {list(filename_map.keys())}'}), 400
        
    # If dynamic zone filtering is applied
    if zone and zone.lower() != 'all':
        df = pd.DataFrame(get_master_data())
        df_sub = df[df['zone'].str.lower() == zone.lower()]
        if len(df_sub) >= 2:
            if chart_id == 'wqi_density':
                buf = generate_chart_wqi_density(df_sub)
                return Response(buf.getvalue(), mimetype='image/png')
            elif chart_id == 'area_distribution':
                buf = generate_chart_area_distribution(df_sub)
                return Response(buf.getvalue(), mimetype='image/png')
            elif chart_id == 'encroachment_correlation':
                buf = generate_chart_encroachment_correlation(df_sub)
                return Response(buf.getvalue(), mimetype='image/png')
                
    chart_file = os.path.join(CHARTS_DIR, filename_map[chart_id])
    if not os.path.exists(chart_file):
        generate_all_charts()
    return send_file(chart_file, mimetype='image/png')

@app.route('/api/charts/metadata', methods=['GET'])
def get_charts_metadata():
    return jsonify({
        'charts': [
            {
                'id': 'status_by_zone',
                'title': 'Lake Rejuvenation Status Breakdown by Civic Zone',
                'module': 'Matplotlib (Horizontal Stacked Bar)',
                'takeaway': 'Mahadevapura and Bommanahalli host 48% of total lakes, with highest ongoing active rejuvenation works.',
                'endpoint': '/api/charts/status_by_zone'
            },
            {
                'id': 'area_distribution',
                'title': 'Distribution of Lake Surface Extent (Acres) by Zone',
                'module': 'Seaborn (Boxplot with Mean Points)',
                'takeaway': 'Bellandur Lake (913 Acres) is Bengaluru’s massive outlier drainage sink; typical urban lakes median at 24 acres.',
                'endpoint': '/api/charts/area_distribution'
            },
            {
                'id': 'wqi_density',
                'title': 'Water Quality Index (WQI) Probability Density Matrix',
                'module': 'Seaborn (KDE Multi-Distribution Plot)',
                'takeaway': 'Clear bimodal separation: Rejuvenated lakes score 72–92 (Class B/C), while untreated water bodies stagnate under 45.',
                'endpoint': '/api/charts/wqi_density'
            },
            {
                'id': 'before_after_metrics',
                'title': 'Chemical & Biological Impact: Before vs After Rejuvenation',
                'module': 'Matplotlib (Two-Panel Aligned Horizontal Comparisons)',
                'takeaway': 'Constructed wetlands and STPs collapsed organic BOD load by 78%–94% while lifting Dissolved Oxygen up to 7.4 mg/L.',
                'endpoint': '/api/charts/before_after_metrics'
            },
            {
                'id': 'encroachment_correlation',
                'title': 'Perimeter Encroachment Rate vs Avian & Floral Biodiversity',
                'module': 'Seaborn (Linear Regression with 95% Confidence Band)',
                'takeaway': 'Statistically significant negative correlation (r = -0.84): lakes with >30% encroachment suffer catastrophic biodiversity collapse.',
                'endpoint': '/api/charts/encroachment_correlation'
            },
            {
                'id': 'custodian_breakdown',
                'title': 'Institutional Custodianship of Bengaluru Water Bodies',
                'module': 'Matplotlib (Bar Chart with Direct Proportions)',
                'takeaway': 'BBMP Lakes Division stewards 74% of civic water bodies, transitioning toward citizen co-management models.',
                'endpoint': '/api/charts/custodian_breakdown'
            }
        ]
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" LAKES OF BENGALURU — DATA VISUALISATION PLATFORM")
    print("="*70)
    print(" Server running at: http://localhost:5000")
    print(" Static Frontend:   c:\\Users\\admin\\Documents\\internship\\frontend")
    print(" Backend Analytics: c:\\Users\\admin\\Documents\\internship\\backend")
    print(" UI Design Specs:   c:\\Users\\admin\\Documents\\internship\\UI")
    print(" Open http://localhost:5000 in your browser to explore the website.")
    print("="*70 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
