#!/usr/bin/env python3
"""
Health Checker Web Dashboard
Author: Joshua
Description: Simple Flask dashboard to view health check reports
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

REPORTS_DIR = Path('/app/reports')


def get_latest_report():
    """Get the most recent health report"""
    report_files = list(REPORTS_DIR.glob('*.json'))

    if not report_files:
        return None

    # Sort by modification time, most recent first
    latest_report = max(report_files, key=lambda p: p.stat().st_mtime)

    try:
        with open(latest_report, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error reading report: {e}")
        return None


def get_all_reports():
    """Get all health reports sorted by timestamp"""
    report_files = list(REPORTS_DIR.glob('*.json'))
    reports = []

    for report_file in report_files:
        try:
            with open(report_file, 'r') as f:
                data = json.load(f)
                data['filename'] = report_file.name
                reports.append(data)
        except Exception:
            continue

    # Sort by timestamp, newest first
    reports.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return reports


@app.route('/')
def index():
    """Main dashboard page"""
    report = get_latest_report()

    if report is None:
        return render_template('no_data.html')

    return render_template('dashboard.html', report=report)


@app.route('/api/latest')
def api_latest():
    """API endpoint for latest report"""
    report = get_latest_report()

    if report is None:
        return jsonify({'error': 'No reports available'}), 404

    return jsonify(report)


@app.route('/api/history')
def api_history():
    """API endpoint for historical reports"""
    reports = get_all_reports()
    return jsonify({
        'count': len(reports),
        'reports': reports[:50]  # Limit to 50 most recent
    })


@app.route('/history')
def history():
    """Historical reports page"""
    reports = get_all_reports()
    return render_template('history.html', reports=reports[:50])


@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    # Ensure reports directory exists
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Health Checker Dashboard Starting")
    print("=" * 60)
    print(f"Reports directory: {REPORTS_DIR}")
    print("Dashboard URL: http://localhost:5000")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=False)
