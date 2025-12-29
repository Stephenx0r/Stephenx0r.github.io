# 🔒 Security Header Checker

**A practical pentesting tool for rapid web security assessment**

Built for the Binary Bandits Hackathon - A professional-grade security tool that helps identify missing security headers in web applications.

## 🎯 What It Does

This tool automatically analyzes any website and:
- ✅ Checks for 7 critical security headers
- 📊 Provides a security score (0-100)
- 🎨 Shows severity levels (HIGH/MEDIUM/LOW)
- 💡 Gives actionable recommendations
- 📄 Exports results to JSON

## 🚀 Quick Start

```bash
# Install requirements
pip install requests

# Basic usage
python3 security_header_checker.py example.com

# With JSON export
python3 security_header_checker.py example.com --export report.json

# Custom timeout
python3 security_header_checker.py example.com --timeout 20
```

## 🛡️ Security Headers Checked

| Header | Severity | Protection Against |
|--------|----------|-------------------|
| Strict-Transport-Security | HIGH | Man-in-the-middle attacks |
| Content-Security-Policy | HIGH | XSS and injection attacks |
| X-Frame-Options | HIGH | Clickjacking |
| X-Content-Type-Options | MEDIUM | MIME-type sniffing |
| Permissions-Policy | MEDIUM | Unauthorized feature access |
| X-XSS-Protection | MEDIUM | Legacy XSS attacks |
| Referrer-Policy | LOW | Information leakage |

## 📊 Example Output

```
╔═══════════════════════════════════════════════════════════════════╗
║           Security Header Checker v1.0                           ║
║           Pentesting Tool for Web Security Assessment            ║
╚═══════════════════════════════════════════════════════════════════╝

[*] Checking: https://example.com

======================================================================
SECURITY HEADER ANALYSIS REPORT
======================================================================
URL: https://example.com
Security Score: 42/100 🔴 D (Poor)
======================================================================

✓ PRESENT HEADERS (2):
----------------------------------------------------------------------
  🟡 X-Content-Type-Options
    Value: nosniff
    Info: Prevents MIME-type sniffing

  🟢 Referrer-Policy
    Value: no-referrer-when-downgrade
    Info: Controls referrer information

✗ MISSING HEADERS (5):
----------------------------------------------------------------------
  🔴 Strict-Transport-Security [HIGH]
    Risk: Forces HTTPS connections
    Fix: Add: Strict-Transport-Security: max-age=31536000; includeSubDomains

  🔴 X-Frame-Options [HIGH]
    Risk: Prevents clickjacking attacks
    Fix: Add: X-Frame-Options: DENY or SAMEORIGIN

  🔴 Content-Security-Policy [HIGH]
    Risk: Prevents XSS and injection attacks
    Fix: Add: Content-Security-Policy: default-src 'self'

======================================================================
ASSESSMENT:
  Poor security posture. Immediate action required!
  ⚠️  3 HIGH severity header(s) missing - address these first!
======================================================================
```

## 💡 Real-World Use Cases

1. **Security Audits**: Quickly assess client websites for basic security posture
2. **Pentesting**: First step in web application security testing
3. **DevOps/CI/CD**: Integrate into deployment pipelines to catch missing headers
4. **Compliance**: Verify security header requirements are met
5. **Education**: Learn about web security headers and their importance

## 🎓 Why This Tool Matters

**Problem**: Many websites lack basic security headers, leaving them vulnerable to:
- XSS attacks
- Clickjacking
- Man-in-the-middle attacks
- Data injection

**Solution**: This tool provides instant visibility into security header coverage, with clear recommendations for fixing issues.

**Impact**: 
- Saves hours of manual header checking
- Prevents common web vulnerabilities
- Helps developers understand security best practices
- Can be integrated into automated security workflows

## 🔧 Technical Details

- **Language**: Python 3
- **Dependencies**: `requests` (standard HTTP library)
- **Compatibility**: Cross-platform (Linux, macOS, Windows)
- **Performance**: < 5 seconds per scan
- **Output formats**: Terminal (colored) + JSON export

## 🏆 Features That Set This Apart

1. **Severity-based scoring**: Not all headers are equal - HIGH severity issues weighted more heavily
2. **Actionable recommendations**: Doesn't just identify problems, shows how to fix them
3. **Professional output**: Clean, readable reports suitable for client presentations
4. **Export capability**: JSON output for integration with other tools
5. **User-friendly**: Works with or without URL scheme (http/https)

## 📈 Potential Extensions

This tool could be expanded to:
- Scan multiple URLs from a file
- Check for insecure header values (not just presence/absence)
- Historical tracking of security scores
- Integration with vulnerability databases
- Automated fix suggestions for specific frameworks (Django, Flask, Express, etc.)

## 🎯 Hackathon Submission

**Category**: Most Useful Tool

**Why this deserves to win**:
1. ✅ **Solves a real problem**: Security headers are often overlooked but critical
2. ✅ **Production-ready**: Can be used immediately by security professionals
3. ✅ **Clear value**: Saves time and prevents vulnerabilities
4. ✅ **Well-executed**: Clean code, good UX, comprehensive coverage
5. ✅ **Extensible**: Strong foundation for future enhancements

## 📝 Requirements

- Python 3.6+
- `requests` library

```bash
pip install requests
```

## 🤝 Contributing

This tool was built during the Binary Bandits Hackathon. Future improvements welcome!

## 📄 License

MIT License - Free to use, modify, and distribute.

---

**Built with ☕ and 🔒 for the Binary Bandits Hackathon**

