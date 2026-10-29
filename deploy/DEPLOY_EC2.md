# Deploy Vyasa Reader on Amazon Linux EC2 (Phase 06; not run / not verified)

Nginx (HTTPS, public) → Gunicorn (`127.0.0.1:8000`, private) → Flask `app:app`, run by systemd as a non-root user. You run every command yourself. Nothing here has been executed or tested.

Placeholders: `YOUR_DOMAIN` (e.g. `reader.example.com`), `YOUR_IP` (your home/office public IP), `REPO_URL` (where this code lives), `KEY.pem` (your SSH key).

Files: `deploy/vyasa-reader.service` (systemd unit) and `deploy/nginx-vyasa-reader.conf` (Nginx site).

## 1. Check the instance (read-only)

```
ssh -i KEY.pem ec2-user@<ELASTIC_IP>
cat /etc/os-release      # expect: Amazon Linux 2023
uname -m                 # x86_64 or aarch64; both work, nothing here is arch-specific
python3 --version        # must be 3.9 or newer (app uses Path.is_relative_to; Flask 3.1 needs 3.9+)
getenforce 2>/dev/null   # SELinux mode, see step 6
```

- **Amazon Linux 2023** (`dnf`): follow this runbook.
- **Amazon Linux 2** (`yum`): stop. Its default `python3` is 3.7, which is too old for this app, and AL2 has reached end of standard support. Launch an AL2023 instance instead of patching Python on AL2.
- Anything else: these commands do not apply; do not adapt them blindly.

## 2. AWS setup (console; your action)

1. **Elastic IP:** allocate one and associate it with the instance so the address survives stop/start.
2. **DNS** at your domain registrar/DNS host: `A` record `YOUR_DOMAIN` → Elastic IP. Add an `AAAA` record only if the instance has an IPv6 address and the Security Group allows IPv6. Wait until `nslookup YOUR_DOMAIN` returns the Elastic IP.
3. **Security Group inbound rules** (remove anything else, including any 5000/8000 rule):

| Type | Port | Source | Why |
|---|---|---|---|
| HTTPS | 443 | `0.0.0.0/0` (and `::/0` if IPv6) | The app |
| HTTP | 80 | `0.0.0.0/0` (and `::/0` if IPv6) | Redirect to HTTPS and certificate challenge |
| SSH | 22 | `YOUR_IP/32` only | Admin access |

Port 8000 must **never** be open; Gunicorn listens on loopback only. Outbound: default (allow all) is fine.

## 3. Install packages and the app

```
sudo dnf install -y python3 python3-pip git nginx
sudo useradd --system --no-create-home --home-dir /opt/vyasa-reader --shell /sbin/nologin vyasa
sudo mkdir /opt/vyasa-reader && sudo chown vyasa:vyasa /opt/vyasa-reader
sudo -u vyasa git clone REPO_URL /opt/vyasa-reader
sudo -u vyasa python3 -m venv /opt/vyasa-reader/.venv
sudo -u vyasa /opt/vyasa-reader/.venv/bin/pip install -r /opt/vyasa-reader/requirements.txt
```

Private repo: use a read-only deploy key for the `vyasa` user, or copy the files from your PC with `scp -r`. Never commit keys, tokens, or passwords to the repo.

## 4. Gunicorn under systemd

```
sudo cp /opt/vyasa-reader/deploy/vyasa-reader.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now vyasa-reader
systemctl status vyasa-reader
curl -s http://127.0.0.1:8000/health      # expect {"status":"ok"}
```

Flask debug is never enabled: Gunicorn imports `app:app` directly, and `app.py` sets `debug=False`.

## 5. HTTPS certificate (Let's Encrypt, free)

Check whether AL2023 packages Certbot: `dnf info certbot`.

- If available: `sudo dnf install -y certbot`
- If not, use Certbot's official pip method:
  ```
  sudo python3 -m venv /opt/certbot
  sudo /opt/certbot/bin/pip install certbot
  sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot
  ```

Issue the certificate with Nginx stopped (standalone mode uses port 80; the hooks are saved for renewals):

```
sudo systemctl stop nginx
sudo certbot certonly --standalone -d YOUR_DOMAIN --agree-tos -m you@example.com \
  --pre-hook "systemctl stop nginx" --post-hook "systemctl start nginx"
```

Renewal: `systemctl list-timers | grep -i certbot`. If no timer exists (typical for the pip method), create one:

```
sudo tee /etc/systemd/system/certbot-renew.service >/dev/null <<'EOF'
[Service]
Type=oneshot
ExecStart=/usr/bin/certbot renew -q
EOF
sudo tee /etc/systemd/system/certbot-renew.timer >/dev/null <<'EOF'
[Timer]
OnCalendar=*-*-* 03:30
RandomizedDelaySec=1h
Persistent=true
[Install]
WantedBy=timers.target
EOF
sudo systemctl daemon-reload && sudo systemctl enable --now certbot-renew.timer
sudo certbot renew --dry-run
```

Renewal stops Nginx for a few seconds only when a certificate is actually renewed.

## 6. Nginx reverse proxy

```
sudo sed "s/YOUR_DOMAIN/your.real.domain/g" /opt/vyasa-reader/deploy/nginx-vyasa-reader.conf | sudo tee /etc/nginx/conf.d/vyasa-reader.conf
sudo nginx -t
sudo systemctl enable --now nginx
```

If `getenforce` printed `Enforcing`, allow Nginx to reach Gunicorn: `sudo setsebool -P httpd_can_network_connect 1`.

The app must stay at the site root (`/`): the PWA `scope`, `start_url`, and `/sw.js` assume it. Nginx passes Flask's `Cache-Control: no-cache` on `/sw.js` through unchanged; do not add long cache headers for it.

## 7. Operate

| Task | Command |
|---|---|
| Restart app | `sudo systemctl restart vyasa-reader` |
| Reload Nginx after config edit | `sudo nginx -t && sudo systemctl reload nginx` |
| App logs | `journalctl -u vyasa-reader -n 100 --no-pager` (add `-f` to follow) |
| Nginx logs | `sudo tail -n 100 /var/log/nginx/access.log /var/log/nginx/error.log` |
| Disk space | `df -h /` and `journalctl --disk-usage` |

**Update:**

```
cd /opt/vyasa-reader
sudo -u vyasa git rev-parse HEAD | sudo tee /opt/vyasa-reader/.last-good
sudo -u vyasa git pull --ff-only
sudo -u vyasa .venv/bin/pip install -r requirements.txt
sudo systemctl restart vyasa-reader && curl -s http://127.0.0.1:8000/health
```

If shell files changed (CSS/JS/icons), bump `CACHE` in `static/sw.js` in that release so phones pick up the update.

**Rollback:**

```
cd /opt/vyasa-reader
sudo -u vyasa git checkout "$(cat .last-good)"
sudo -u vyasa .venv/bin/pip install -r requirements.txt
sudo systemctl restart vyasa-reader
```

Return to the branch later with `sudo -u vyasa git checkout main`.

## 8. Manual verification (you run; not performed by Claude)

From your PC:
1. `curl -I http://YOUR_DOMAIN/` → `301` to `https://`.
2. `curl -I https://YOUR_DOMAIN/health` → `200`; the browser shows a valid lock and the certificate is issued for `YOUR_DOMAIN`.
3. `curl -m 5 http://YOUR_DOMAIN:8000/` → times out or is refused (port 8000 not public).

On the server:
4. `sudo ss -tlnp | grep 8000` shows `127.0.0.1:8000` only, never `0.0.0.0` or `*`.
5. `sudo reboot`; after reconnecting, `systemctl is-active vyasa-reader nginx` → `active active`, and `/health` works over HTTPS.
6. `journalctl -u vyasa-reader -b --no-pager` shows no errors; `df -h /` has free space.

On Android Chrome (see `docs/PWA.md`):
7. Open `https://YOUR_DOMAIN/`, reload once, Menu > **Install app**. The icon appears; opening it shows no address bar.
8. Open the demo story, scroll halfway, close the app from Recents, reopen: it returns near the same paragraph.
9. Run `sudo systemctl restart vyasa-reader`, then reboot the server; reopen the app each time: resume still works (state is in the phone's browser storage, not the server).
10. Airplane mode: navigating shows the "You are offline" page. Chrome > Settings > Site settings > YOUR_DOMAIN shows stored data; only the app shell is cached, no source text.

## Costs (check current AWS and registrar pricing; no amounts given here)

- **EC2:** instance hours (by instance type and region), EBS volume storage, and outbound data transfer.
- **Public IPv4:** AWS bills public IPv4 addresses, including an Elastic IP, by the hour.
- **Domain:** yearly registration/renewal fee at your registrar; DNS hosting may cost extra (for example Route 53 hosted zones).
- **Certificate:** Let's Encrypt is free. Use AWS Billing > Budgets to get an alert before costs exceed your limit.
