from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class ReportGenerator:
    """Generate investor-ready PDF reports"""
    
    def __init__(self, analysis, user):
        self.analysis = analysis
        self.user = user
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_pdf(self) -> str:
        """Generate complete PDF report"""
        
        # Create reports directory
        os.makedirs('reports', exist_ok=True)
        
        filename = f"reports/financial_report_{self.analysis.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        
        story = []
        
        # Title page
        story.extend(self._create_title_page())
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary())
        story.append(Spacer(1, 0.3*inch))
        
        # Financial health score
        story.extend(self._create_health_score_section())
        story.append(Spacer(1, 0.3*inch))
        
        # Key metrics
        story.extend(self._create_metrics_section())
        story.append(Spacer(1, 0.3*inch))
        
        # AI insights
        story.extend(self._create_insights_section())
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations_section())
        story.append(Spacer(1, 0.3*inch))
        
        # Industry comparison
        story.extend(self._create_industry_section())
        story.append(Spacer(1, 0.3*inch))
        
        # Credit readiness
        story.extend(self._create_credit_section())
        story.append(Spacer(1, 0.3*inch))
        
        # Cash flow forecast
        story.extend(self._create_forecast_section())
        
        # Build PDF
        doc.build(story)
        
        return filename
    
    def _create_title_page(self):
        """Create title page"""
        elements = []
        
        elements.append(Spacer(1, 2*inch))
        
        title = Paragraph("Financial Health Assessment Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        company = Paragraph(f"<b>{self.user.company_name}</b>", self.styles['Heading2'])
        elements.append(company)
        elements.append(Spacer(1, 0.3*inch))
        
        date = Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", self.styles['Normal'])
        elements.append(date)
        
        return elements
    
    def _create_executive_summary(self):
        """Create executive summary"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        summary_text = f"""
        This report provides a comprehensive analysis of {self.user.company_name}'s financial health 
        based on submitted financial data. The analysis includes liquidity assessment, profitability metrics, 
        cash flow analysis, debt health evaluation, and forward-looking projections.
        """
        
        elements.append(Paragraph(summary_text, self.styles['Normal']))
        
        return elements
    
    def _create_health_score_section(self):
        """Create health score section"""
        elements = []
        
        elements.append(Paragraph("Financial Health Score", self.styles['SectionHeader']))
        
        # Score table
        score_data = [
            ['Overall Health Score', f"{self.analysis.health_score}/100"],
            ['Risk Classification', self.analysis.risk_band],
            ['Assessment Date', self.analysis.created_at.strftime('%B %d, %Y')]
        ]
        
        score_table = Table(score_data, colWidths=[3*inch, 2*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Component scores
        component_data = [
            ['Component', 'Score'],
            ['Liquidity', f"{self.analysis.liquidity_score}/100"],
            ['Profitability', f"{self.analysis.profitability_score}/100"],
            ['Cash Flow', f"{self.analysis.cash_flow_score}/100"],
            ['Debt Health', f"{self.analysis.debt_health_score}/100"]
        ]
        
        component_table = Table(component_data, colWidths=[3*inch, 2*inch])
        component_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(component_table)
        
        return elements
    
    def _create_metrics_section(self):
        """Create key metrics section"""
        elements = []
        
        elements.append(Paragraph("Key Financial Metrics", self.styles['SectionHeader']))
        
        metrics = self.analysis.metrics
        
        metrics_data = [
            ['Metric', 'Value'],
            ['Current Ratio', f"{metrics.get('current_ratio', 0):.2f}"],
            ['Quick Ratio', f"{metrics.get('quick_ratio', 0):.2f}"],
            ['Gross Profit Margin', f"{metrics.get('gross_profit_margin', 0):.2f}%"],
            ['Net Profit Margin', f"{metrics.get('net_profit_margin', 0):.2f}%"],
            ['Operating Margin', f"{metrics.get('operating_margin', 0):.2f}%"],
            ['Debt-to-Equity', f"{metrics.get('debt_to_equity', 0):.2f}"],
            ['Interest Coverage', f"{metrics.get('interest_coverage', 0):.2f}"],
            ['Cash Conversion Cycle', f"{metrics.get('cash_conversion_cycle', 0):.0f} days"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3.5*inch, 1.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(metrics_table)
        
        return elements
    
    def _create_insights_section(self):
        """Create AI insights section"""
        elements = []
        
        elements.append(Paragraph("AI-Powered Insights", self.styles['SectionHeader']))
        
        insights = self.analysis.ai_insights.get('summary', 'No insights available')
        elements.append(Paragraph(insights, self.styles['Normal']))
        
        return elements
    
    def _create_recommendations_section(self):
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Actionable Recommendations", self.styles['SectionHeader']))
        
        for i, rec in enumerate(self.analysis.recommendations[:5], 1):
            rec_title = Paragraph(f"<b>{i}. {rec['title']}</b> (Priority: {rec['priority']})", 
                                 self.styles['Normal'])
            elements.append(rec_title)
            elements.append(Spacer(1, 0.1*inch))
            
            rec_desc = Paragraph(rec['description'], self.styles['Normal'])
            elements.append(rec_desc)
            elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def _create_industry_section(self):
        """Create industry comparison section"""
        elements = []
        
        elements.append(Paragraph("Industry Benchmarking", self.styles['SectionHeader']))
        
        industry_data = self.analysis.industry_comparison
        
        text = f"Industry: {industry_data.get('industry', 'N/A')}<br/>"
        text += f"Overall Performance: {industry_data.get('overall_performance', 'N/A')}"
        
        elements.append(Paragraph(text, self.styles['Normal']))
        
        return elements
    
    def _create_credit_section(self):
        """Create credit readiness section"""
        elements = []
        
        elements.append(Paragraph("Credit Readiness Assessment", self.styles['SectionHeader']))
        
        credit = self.analysis.credit_readiness.get('credit_readiness', {})
        
        text = f"Credit Readiness Score: {credit.get('credit_readiness_score', 0):.2f}/100<br/>"
        text += f"Readiness Level: {credit.get('readiness_level', 'N/A')}<br/>"
        text += f"{credit.get('description', '')}"
        
        elements.append(Paragraph(text, self.styles['Normal']))
        
        return elements
    
    def _create_forecast_section(self):
        """Create cash flow forecast section"""
        elements = []
        
        elements.append(Paragraph("6-Month Cash Flow Forecast", self.styles['SectionHeader']))
        
        forecast = self.analysis.cash_flow_forecast
        
        text = f"Trend: {forecast.get('trend', 'N/A')}<br/>"
        text += f"Average Projected Cash Flow: ₹{forecast.get('average_projected_cf', 0):,.2f}"
        
        elements.append(Paragraph(text, self.styles['Normal']))
        
        return elements
