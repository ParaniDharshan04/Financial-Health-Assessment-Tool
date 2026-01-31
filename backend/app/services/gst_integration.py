import json
import xmltodict
from typing import Dict, List, Optional
from datetime import datetime

class GSTIntegration:
    """GST Returns Integration and Compliance Service"""
    
    def __init__(self):
        self.gst_rates = [0, 5, 12, 18, 28]
    
    def parse_gstr1(self, file_data: bytes, file_type: str = "json") -> Dict:
        """Parse GSTR-1 return (Outward Supplies)"""
        try:
            if file_type == "json":
                data = json.loads(file_data.decode('utf-8'))
            elif file_type == "xml":
                data = xmltodict.parse(file_data.decode('utf-8'))
            else:
                raise ValueError("Unsupported file type. Use 'json' or 'xml'")
            
            # Extract summary if provided in file
            file_summary = data.get('summary', {})
            
            parsed_data = {
                "return_type": "GSTR-1",
                "return_period": data.get('return_period', ''),
                "filing_date": data.get('filing_date', ''),
                "gstin": data.get('gstin', ''),
                "legal_name": data.get('legal_name', ''),
                "trade_name": data.get('trade_name', ''),
                "outward_supplies": self._extract_outward_supplies(data),
                "summary": file_summary if file_summary else {}
            }
            
            # Calculate summary if not provided
            if not parsed_data["summary"]:
                parsed_data["summary"] = self._calculate_gstr1_summary(
                    parsed_data["outward_supplies"]
                )
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"Error parsing GSTR-1: {str(e)}")
    
    def parse_gstr3b(self, file_data: bytes, file_type: str = "json") -> Dict:
        """Parse GSTR-3B return (Summary Return)"""
        try:
            if file_type == "json":
                data = json.loads(file_data.decode('utf-8'))
            elif file_type == "xml":
                data = xmltodict.parse(file_data.decode('utf-8'))
            else:
                raise ValueError("Unsupported file type. Use 'json' or 'xml'")
            
            parsed_data = {
                "return_type": "GSTR-3B",
                "return_period": data.get('return_period', ''),
                "filing_date": data.get('filing_date', ''),
                "gstin": data.get('gstin', ''),
                "legal_name": data.get('legal_name', ''),
                "outward_supplies": self._extract_3b_outward(data),
                "inward_supplies": self._extract_3b_inward(data),
                "itc_claimed": self._extract_3b_itc(data),
                "tax_liability": self._extract_3b_tax_liability(data),
                "tax_paid": data.get('tax_paid', {}),
                "summary": {}
            }
            
            # Calculate summary
            parsed_data["summary"] = self._calculate_gstr3b_summary(parsed_data)
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"Error parsing GSTR-3B: {str(e)}")
    
    def _extract_outward_supplies(self, data: Dict) -> Dict:
        """Extract outward supplies from GSTR-1"""
        # Handle both standard keys and our test file keys
        b2b = data.get('b2b_invoices', data.get('b2b', []))
        b2c_large = data.get('b2c_large', data.get('b2cl', []))
        b2c_small = data.get('b2c_small', data.get('b2cs', []))
        exports = data.get('exports', data.get('exp', []))
        
        return {
            "b2b": b2b,  # Business to Business
            "b2c_large": b2c_large,  # B2C Large (>2.5L)
            "b2c_small": b2c_small,  # B2C Small
            "exports": exports,
            "nil_rated": data.get('nil', []),
            "total_taxable_value": 0,
            "total_tax": 0
        }
    
    def _extract_3b_outward(self, data: Dict) -> Dict:
        """Extract outward supplies from GSTR-3B"""
        outward = data.get('outward_supplies', {})
        
        # Handle nested structure
        taxable_supplies = outward.get('taxable_supplies', outward)
        
        return {
            "taxable_value": taxable_supplies.get('taxable_value', outward.get('taxable_value', 0)),
            "integrated_tax": taxable_supplies.get('igst', outward.get('igst', 0)),
            "central_tax": taxable_supplies.get('cgst', outward.get('cgst', 0)),
            "state_tax": taxable_supplies.get('sgst', outward.get('sgst', 0)),
            "cess": taxable_supplies.get('cess', outward.get('cess', 0))
        }
    
    def _extract_3b_inward(self, data: Dict) -> Dict:
        """Extract inward supplies from GSTR-3B"""
        inward = data.get('inward_supplies', {})
        return {
            "reverse_charge": inward.get('reverse_charge', 0),
            "imports": inward.get('imports', 0)
        }
    
    def _extract_3b_itc(self, data: Dict) -> Dict:
        """Extract Input Tax Credit from GSTR-3B"""
        # Handle both 'itc' and 'itc_claimed' keys
        itc = data.get('itc_claimed', data.get('itc', {}))
        
        # Calculate totals from components if available
        total_itc = itc.get('total', 0)
        if total_itc == 0:
            total_itc = itc.get('igst', 0) + itc.get('cgst', 0) + itc.get('sgst', 0)
        
        # Get net ITC
        net_itc_data = data.get('net_itc', {})
        net_itc = net_itc_data.get('total', itc.get('net', total_itc))
        
        return {
            "itc_available": total_itc,
            "itc_reversed": data.get('itc_reversed', {}).get('total', itc.get('reversed', 0)),
            "itc_ineligible": itc.get('ineligible', 0),
            "net_itc": net_itc
        }
    
    def _extract_3b_tax_liability(self, data: Dict) -> Dict:
        """Extract tax liability from GSTR-3B"""
        # Handle both 'tax_liability' and 'tax_payable' keys
        liability = data.get('tax_payable', data.get('tax_liability', {}))
        
        return {
            "integrated_tax": liability.get('igst', 0),
            "central_tax": liability.get('cgst', 0),
            "state_tax": liability.get('sgst', 0),
            "cess": liability.get('cess', 0),
            "interest": liability.get('interest', 0),
            "late_fee": liability.get('late_fee', 0),
            "total": liability.get('total', 0)
        }
    
    def _calculate_gstr1_summary(self, outward_supplies: Dict) -> Dict:
        """Calculate summary for GSTR-1"""
        # In production, this would sum up all invoices
        b2b_count = len(outward_supplies.get('b2b', []))
        b2c_large_count = len(outward_supplies.get('b2c_large', []))
        b2c_small_count = len(outward_supplies.get('b2c_small', []))
        export_count = len(outward_supplies.get('exports', []))
        
        return {
            "total_invoices": b2b_count + b2c_large_count + b2c_small_count + export_count,
            "total_taxable_value": 0,
            "total_tax_amount": 0,
            "b2b_count": b2b_count,
            "b2c_count": b2c_large_count + b2c_small_count,
            "export_count": export_count
        }
    
    def _calculate_gstr3b_summary(self, data: Dict) -> Dict:
        """Calculate summary for GSTR-3B"""
        outward = data.get('outward_supplies', {})
        itc = data.get('itc_claimed', {})
        liability = data.get('tax_liability', {})
        
        total_tax = (
            outward.get('integrated_tax', 0) +
            outward.get('central_tax', 0) +
            outward.get('state_tax', 0) +
            outward.get('cess', 0)
        )
        
        net_tax_payable = total_tax - itc.get('net_itc', 0)
        
        return {
            "total_turnover": outward.get('taxable_value', 0),
            "total_tax_liability": total_tax,
            "total_itc_claimed": itc.get('net_itc', 0),
            "net_tax_payable": max(0, net_tax_payable),
            "interest_payable": liability.get('interest', 0),
            "late_fee": liability.get('late_fee', 0)
        }
    
    def validate_compliance(self, gst_data: Dict, financial_data: Dict) -> Dict:
        """Validate GST compliance"""
        compliance_result = {
            "is_compliant": True,
            "issues": [],
            "warnings": [],
            "score": 100
        }
        
        # Check if GST registration is required
        revenue = financial_data.get('revenue', 0)
        gst_threshold = 4000000  # ₹40 lakhs
        
        if revenue > gst_threshold:
            if not gst_data.get('gstin'):
                compliance_result["is_compliant"] = False
                compliance_result["score"] -= 30
                compliance_result["issues"].append({
                    "severity": "High",
                    "issue": "GST Registration Required",
                    "description": f"Revenue of ₹{revenue:,.0f} exceeds threshold of ₹{gst_threshold:,.0f}",
                    "action": "Register for GST immediately"
                })
        
        # Check return filing
        if gst_data.get('gstin') and not gst_data.get('returns_filed'):
            compliance_result["warnings"].append({
                "severity": "Medium",
                "issue": "GST Returns Not Filed",
                "description": "No GST returns found for recent periods",
                "action": "File pending GST returns (GSTR-1 and GSTR-3B)"
            })
            compliance_result["score"] -= 20
        
        # Check tax payment
        summary = gst_data.get('summary', {})
        net_tax_payable = summary.get('net_tax_payable', 0)
        
        if net_tax_payable > 0:
            compliance_result["warnings"].append({
                "severity": "High",
                "issue": "GST Payment Pending",
                "description": f"Net GST payable: ₹{net_tax_payable:,.2f}",
                "action": "Pay GST before due date to avoid interest and penalty"
            })
            compliance_result["score"] -= 15
        
        # Determine compliance status
        if compliance_result["score"] >= 80:
            compliance_result["status"] = "Compliant"
        elif compliance_result["score"] >= 60:
            compliance_result["status"] = "Partially Compliant"
        else:
            compliance_result["status"] = "Non-Compliant"
            compliance_result["is_compliant"] = False
        
        return compliance_result
    
    def calculate_gst_liability(self, financial_data: Dict, gst_rate: float = 0.18) -> Dict:
        """Calculate GST liability from financial data"""
        revenue = financial_data.get('revenue', 0)
        
        # Calculate GST components
        taxable_value = revenue / (1 + gst_rate)  # Reverse calculate if GST included
        gst_amount = taxable_value * gst_rate
        
        # Split into CGST and SGST (for intra-state) or IGST (for inter-state)
        # Assuming intra-state for simplicity
        cgst = gst_amount / 2
        sgst = gst_amount / 2
        
        return {
            "taxable_value": round(taxable_value, 2),
            "gst_rate": gst_rate * 100,
            "total_gst": round(gst_amount, 2),
            "cgst": round(cgst, 2),
            "sgst": round(sgst, 2),
            "igst": 0,  # Assuming intra-state
            "total_value_with_gst": round(revenue, 2)
        }
    
    def generate_gst_summary_report(self, gst_data: Dict) -> Dict:
        """Generate comprehensive GST summary report"""
        return {
            "gstin": gst_data.get('gstin', 'Not Registered'),
            "legal_name": gst_data.get('legal_name', ''),
            "return_period": gst_data.get('return_period', ''),
            "summary": gst_data.get('summary', {}),
            "compliance_status": self.validate_compliance(gst_data, {}),
            "recommendations": self._generate_gst_recommendations(gst_data)
        }
    
    def _generate_gst_recommendations(self, gst_data: Dict) -> List[Dict]:
        """Generate GST-specific recommendations"""
        recommendations = []
        
        summary = gst_data.get('summary', {})
        
        # ITC optimization
        itc_claimed = summary.get('total_itc_claimed', 0)
        if itc_claimed == 0:
            recommendations.append({
                "title": "Claim Input Tax Credit",
                "description": "You haven't claimed any ITC. Ensure you're claiming ITC on eligible purchases.",
                "priority": "Medium",
                "potential_saving": "Variable"
            })
        
        # Timely filing
        recommendations.append({
            "title": "File Returns on Time",
            "description": "File GSTR-1 by 11th and GSTR-3B by 20th of every month to avoid late fees.",
            "priority": "High",
            "potential_saving": "₹200-5,000 per return"
        })
        
        # Reconciliation
        recommendations.append({
            "title": "Reconcile GSTR-2A with Books",
            "description": "Regularly reconcile GSTR-2A with your purchase records to claim maximum ITC.",
            "priority": "Medium",
            "potential_saving": "Variable"
        })
        
        return recommendations
    
    def get_mock_gst_data(self, gstin: str = "29ABCDE1234F1Z5") -> Dict:
        """Get mock GST data for demo purposes"""
        return {
            "gstin": gstin,
            "legal_name": "Demo Business Pvt Ltd",
            "trade_name": "Demo Business",
            "return_period": "012025",  # January 2025
            "return_type": "GSTR-3B",
            "outward_supplies": {
                "taxable_value": 1000000,
                "integrated_tax": 0,
                "central_tax": 90000,
                "state_tax": 90000,
                "cess": 0
            },
            "inward_supplies": {
                "reverse_charge": 0,
                "imports": 0
            },
            "itc_claimed": {
                "itc_available": 50000,
                "itc_reversed": 0,
                "itc_ineligible": 0,
                "net_itc": 50000
            },
            "tax_liability": {
                "integrated_tax": 0,
                "central_tax": 90000,
                "state_tax": 90000,
                "cess": 0,
                "interest": 0,
                "late_fee": 0
            },
            "summary": {
                "total_turnover": 1000000,
                "total_tax_liability": 180000,
                "total_itc_claimed": 50000,
                "net_tax_payable": 130000,
                "interest_payable": 0,
                "late_fee": 0
            },
            "returns_filed": True,
            "filing_date": "2025-01-18",
            "is_demo": True
        }
