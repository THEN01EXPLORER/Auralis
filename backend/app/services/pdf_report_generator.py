"""
PDF Report Generator for Auralis Security Audits
Generates professional audit reports with DREAD scores
"""

from datetime import datetime
from typing import Dict, List
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class PDFReportGenerator:
    """Generate PDF audit reports"""
    
    def __init__(self):
        self.available = REPORTLAB_AVAILABLE
    
    def generate_report(self, analysis_result: Dict, dread_scores: Dict) -> bytes:
        """
        Generate a PDF audit report
        
        Args:
            analysis_result: Analysis results from Auralis
            dread_scores: DREAD scoring results
            
        Returns:
            PDF file as bytes
        """
        if not self.available:
            raise RuntimeError("reportlab is not installed. Install with: pip install reportlab")
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("🛡️ Auralis Security Audit Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        
        summary_data = [
            ['Analysis Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis Method:', analysis_result.get('analysis_method', 'hybrid').upper()],
            ['Risk Score:', f"{analysis_result.get('risk_score', 0)}/100"],
            ['Vulnerabilities Found:', str(len(analysis_result.get('vulnerabilities', [])))],
            ['Max Risk Level:', dread_scores.get('max_risk_level', 'Unknown')],
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # DREAD Matrix
        story.append(Paragraph("DREAD Risk Assessment", heading_style))
        
        dread_data = [
            ['Metric', 'Score (0-10)', 'Description'],
            ['Damage', f"{dread_scores.get('average_damage', 0):.1f}", 'Potential impact of exploit'],
            ['Reproducibility', f"{dread_scores.get('average_reproducibility', 0):.1f}", 'Ease of reproduction'],
            ['Exploitability', f"{dread_scores.get('average_exploitability', 0):.1f}", 'Effort to exploit'],
            ['Affected Users', f"{dread_scores.get('average_affected_users', 0):.1f}", 'Number of users impacted'],
            ['Discoverability', f"{dread_scores.get('average_discoverability', 0):.1f}", 'Ease of discovery'],
        ]
        
        dread_table = Table(dread_data, colWidths=[1.5*inch, 1.2*inch, 3.3*inch])
        dread_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        story.append(dread_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Vulnerabilities
        vulnerabilities = analysis_result.get('vulnerabilities', [])
        
        if vulnerabilities:
            story.append(Paragraph(f"Detailed Findings ({len(vulnerabilities)} Issues)", heading_style))
            story.append(Spacer(1, 0.1*inch))
            
            for i, vuln in enumerate(vulnerabilities, 1):
                # Vulnerability header
                severity = vuln.get('severity', 'Unknown')
                severity_color = self._get_severity_color(severity)
                
                vuln_title = f"{i}. {vuln.get('type', 'Unknown')} (Line {vuln.get('line', 'N/A')})"
                story.append(Paragraph(vuln_title, styles['Heading3']))
                
                # Vulnerability details
                vuln_details = [
                    ['Severity:', severity],
                    ['Confidence:', f"{vuln.get('confidence', 0)}%"],
                    ['Description:', vuln.get('description', 'No description')],
                    ['Recommendation:', vuln.get('recommendation', 'No recommendation')],
                ]
                
                vuln_table = Table(vuln_details, colWidths=[1.2*inch, 4.8*inch])
                vuln_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                    ('BACKGROUND', (1, 0), (1, 0), severity_color),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                ]))
                
                story.append(vuln_table)
                story.append(Spacer(1, 0.2*inch))
        else:
            story.append(Paragraph("✅ No vulnerabilities detected!", styles['Normal']))
        
        # Footer
        story.append(PageBreak())
        story.append(Spacer(1, 0.5*inch))
        footer_text = """
        <para align=center>
        <b>Auralis Security Auditor</b><br/>
        AI-Powered Smart Contract Security Analysis<br/>
        <i>This report was generated automatically. Please review findings with a security expert.</i>
        </para>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _get_severity_color(self, severity: str):
        """Get color for severity level"""
        colors_map = {
            'Critical': colors.HexColor('#e74c3c'),
            'High': colors.HexColor('#e67e22'),
            'Medium': colors.HexColor('#f39c12'),
            'Low': colors.HexColor('#3498db'),
        }
        return colors_map.get(severity, colors.grey)
