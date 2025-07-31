#!/usr/bin/env python3
"""
Create YouTube URLs Template Excel File
"""

import pandas as pd
from datetime import datetime

def create_template():
    """Create template Excel file for YouTube URLs"""
    
    # Sample YouTube URLs data
    template_data = {
        'youtube_url': [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtu.be/9bZkp7q19f0',
            'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
            'https://www.youtube.com/watch?v=ScMzIvxBSi4',
            'https://youtu.be/oHg5SJYRHA0',
            '',  # Empty rows for user input
            '',
            '',
            '',
            ''
        ],
        'description': [
            'Rick Astley - Never Gonna Give You Up (Sample)',
            'PSY - GANGNAM STYLE (Sample)',
            'Luis Fonsi - Despacito (Sample)',
            'Queen - Bohemian Rhapsody (Sample)',
            'Wiz Khalifa - See You Again (Sample)',
            '',
            '',
            '',
            '',
            ''
        ],
        'notes': [
            'This is a sample URL - replace with your own',
            'Another sample URL',
            'You can add your video URLs here',
            'Remove sample URLs and add your own',
            'Keep this format: one URL per row',
            'Add your YouTube URLs below',
            '',
            '',
            '',
            ''
        ]
    }
    
    try:
        # Create DataFrame
        df = pd.DataFrame(template_data)
        
        # Save to Excel
        filename = 'youtube_urls_template.xlsx'
        df.to_excel(filename, index=False, engine='openpyxl')
        
        print(f"✅ Template Excel berhasil dibuat: {filename}")
        print(f"📊 Template berisi {len(df)} baris")
        print("💡 Gunakan file ini sebagai template untuk input URL YouTube")
        
        return True
        
    except Exception as e:
        print(f"❌ Error membuat template: {e}")
        return False

if __name__ == "__main__":
    create_template()
