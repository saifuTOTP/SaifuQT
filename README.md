# SaifuQT

A desktop TOTP authenticator app built with PySide6 (Qt), created as part of a personal privacy stack to replace proprietary authenticator apps (Google Authenticator, Authy, etc.) with a self-hosted, open-source alternative.

---

## What it does

- Manages multiple TOTP (Time-based One-Time Password) accounts
- Generates live 2FA codes via `pyotp`
- Qt-based GUI with per-account add/remove controls
- Optional API integration for cross-device update checking

Built to give full control over 2FA secrets without trusting a closed-source app or a third-party cloud service with authentication credentials.

---

## Part of a broader privacy stack

SaifuQT sits alongside:
- **GrapheneOS** — phone OS with app isolation
- **nix_dots** — declarative NixOS config managing the full system
- **Self-hosted OwnCloud, Matrix, Jabber** — replacements for Google Suite and messaging
- Custom find-my integration, finance app, and resume tooling

The goal across all of these: equivalent security to big-tech platforms, without the privacy trade-off.

---

## Setup

Requires Python 3.10+ and PySide6.

```bash
pip install pyotp PySide6 requests
python main.py
```
