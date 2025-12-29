#!/usr/bin/env python3
"""
Security Header Checker - A practical pentesting tool for web security assessment
Author: Binary Bandits Hackathon Submission
"""

import requests
import sys
import argparse
from urllib.parse import urlparse
from typing import Dict, List, Tuple
import json

class SecurityHeaderChecker:
    """Check websites for security headers and provide actionable recommendations"""
    
    # Security headers with their importance and descriptions
    SECURITY_HEADERS = {
        'Strict-Transport-Security': {
            'severity': 'HIGH',
            'description': 'Forces HTTPS connections',
            'recommendation': 'Add: Strict-Transport-Security: max-age=31536000; includeSubDomains'
        },
        'X-Frame-Options': {
            'severity': 'HIGH',
            'description': 'Prevents clickjacking attacks',
            'recommendation': 'Add: X-Frame-Options: DENY or SAMEORIGIN'
        },
        'X-Content-Type-Options': {
            'severity': 'MEDIUM',
            'description': 'Prevents MIME-type sniffing',
            'recommendation': 'Add: X-Content-Type-Options: nosniff'
        },
        'Content-Security-Policy': {
            'severity': 'HIGH',
            'description': 'Prevents XSS and injection attacks',
            'recommendation': 'Add: Content-Security-Policy: default-src \'self\''
        },
        'X-XSS-Protection': {
            'severity': 'MEDIUM',
            'description': 'Enables XSS filtering (legacy browsers)',
            'recommendation': 'Add: X-XSS-Protection: 1; mode=block'
        },
        'Referrer-Policy': {
            'severity': 'LOW',
            'description': 'Controls referrer information',
            'recommendation': 'Add: Referrer-Policy: no-referrer-when-downgrade'
        },
        'Permissions-Policy': {
            'severity': 'MEDIUM',
            'description': 'Controls browser features and APIs',
            'recommendation': 'Add: Permissions-Policy: geolocation=(), microphone=()'
        }
    }
    
    def __init__(self, url: str, timeout: int = 10):
        self.url = self._normalize_url(url)
        self.timeout = timeout
        self.headers = {}
        self.missing_headers = []
        self.present_headers = []
        self.score = 0
        
    def _normalize_url(self, url: str) -> str:
        """Ensure URL has a scheme"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    def check_headers(self) -> bool:
        """Fetch and analyze security headers"""
        try:
            print(f"[*] Checking: {self.url}")
            response = requests.get(self.url, timeout=self.timeout, allow_redirects=True)
            self.headers = response.headers
            
            # Check each security header
            for header, info in self.SECURITY_HEADERS.items():
                if header in self.headers:
                    self.present_headers.append({
                        'header': header,
                        'value': self.headers[header],
                        'info': info
                    })
                else:
                    self.missing_headers.append({
                        'header': header,
                        'info': info
                    })
            
            self._calculate_score()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Error: {e}")
            return False
    
    def _calculate_score(self):
        """Calculate security score (0-100)"""
        total_headers = len(self.SECURITY_HEADERS)
        present_count = len(self.present_headers)
        
        # Weight by severity
        max_score = 0
        current_score = 0
        
        for header, info in self.SECURITY_HEADERS.items():
            severity_weight = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
            weight = severity_weight[info['severity']]
            max_score += weight
            
            if any(h['header'] == header for h in self.present_headers):
                current_score += weight
        
        self.score = int((current_score / max_score) * 100)
    
    def print_report(self):
        """Print a detailed security report"""
        print("\n" + "="*70)
        print(f"SECURITY HEADER ANALYSIS REPORT")
        print("="*70)
        print(f"URL: {self.url}")
        print(f"Security Score: {self.score}/100 {self._get_grade()}")
        print("="*70)
        
        # Present headers
        if self.present_headers:
            print(f"\n✓ PRESENT HEADERS ({len(self.present_headers)}):")
            print("-"*70)
            for h in self.present_headers:
                severity_color = self._get_severity_symbol(h['info']['severity'])
                print(f"  {severity_color} {h['header']}")
                print(f"    Value: {h['value'][:80]}")
                print(f"    Info: {h['info']['description']}")
                print()
        
        # Missing headers
        if self.missing_headers:
            print(f"\n✗ MISSING HEADERS ({len(self.missing_headers)}):")
            print("-"*70)
            for h in self.missing_headers:
                severity_color = self._get_severity_symbol(h['info']['severity'])
                print(f"  {severity_color} {h['header']} [{h['info']['severity']}]")
                print(f"    Risk: {h['info']['description']}")
                print(f"    Fix: {h['info']['recommendation']}")
                print()
        
        # Overall assessment
        print("="*70)
        print("ASSESSMENT:")
        self._print_assessment()
        print("="*70)
    
    def _get_grade(self) -> str:
        """Convert score to letter grade"""
        if self.score >= 90:
            return "🟢 A (Excellent)"
        elif self.score >= 70:
            return "🟡 B (Good)"
        elif self.score >= 50:
            return "🟠 C (Fair)"
        else:
            return "🔴 D (Poor)"
    
    def _get_severity_symbol(self, severity: str) -> str:
        """Get symbol for severity level"""
        symbols = {
            'HIGH': '🔴',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        return symbols.get(severity, '⚪')
    
    def _print_assessment(self):
        """Print overall security assessment"""
        high_missing = sum(1 for h in self.missing_headers if h['info']['severity'] == 'HIGH')
        
        if self.score >= 90:
            print("  Excellent security posture! Minor improvements possible.")
        elif self.score >= 70:
            print("  Good security, but some important headers are missing.")
        elif self.score >= 50:
            print("  Fair security. Several improvements needed.")
        else:
            print("  Poor security posture. Immediate action required!")
        
        if high_missing > 0:
            print(f"  ⚠️  {high_missing} HIGH severity header(s) missing - address these first!")
    
    def export_json(self, filename: str = None):
        """Export results to JSON"""
        data = {
            'url': self.url,
            'score': self.score,
            'present_headers': self.present_headers,
            'missing_headers': self.missing_headers
        }
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n[+] Results exported to {filename}")
        
        return data


def main():
    parser = argparse.ArgumentParser(
        description='Security Header Checker - Analyze websites for security headers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s example.com
  %(prog)s https://example.com
  %(prog)s example.com --export report.json
  %(prog)s example.com --timeout 20
        """
    )
    parser.add_argument('url', help='Target URL to check')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('--export', metavar='FILE', help='Export results to JSON file')
    
    args = parser.parse_args()
    
    # Banner
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║           Security Header Checker v1.0                           ║
║           Pentesting Tool for Web Security Assessment            ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Run checker
    checker = SecurityHeaderChecker(args.url, timeout=args.timeout)
    
    if checker.check_headers():
        checker.print_report()
        
        if args.export:
            checker.export_json(args.export)
        
        # Exit code based on score
        sys.exit(0 if checker.score >= 70 else 1)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()

