from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

REPORT_DIR = Path("reports")


def _ensure_report_dir() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _build_html(
    run_id: str,
    host: str,
    users: int,
    spawn_rate: int,
    duration: str,
    avg_response_time: float,
    p95_response_time: float,
    total_requests: int,
    total_failures: int,
    failure_rate: float,
    rps: float,
    sla_status: str,
) -> str:
    status_color = "#2ecc71" if sla_status == "PASS" else "#e74c3c"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetPerf Report - {run_id}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f6fa; color: #2d3436; padding: 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ font-size: 24px; margin-bottom: 8px; }}
        .subtitle {{ color: #636e72; margin-bottom: 32px; font-size: 14px; }}
        .section {{ background: #fff; border-radius: 8px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .section h2 {{ font-size: 16px; margin-bottom: 16px; color: #636e72; text-transform: uppercase; letter-spacing: 1px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }}
        .metric {{ text-align: center; }}
        .metric .value {{ font-size: 28px; font-weight: 700; }}
        .metric .label {{ font-size: 12px; color: #636e72; margin-top: 4px; }}
        .status-badge {{ display: inline-block; padding: 6px 20px; border-radius: 4px; font-weight: 700; font-size: 18px; color: #fff; background: {status_color}; }}
        .meta-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
        .meta-item {{ font-size: 14px; }}
        .meta-item span {{ color: #636e72; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>PetPerf Performance Report</h1>
        <p class="subtitle">Run ID: {run_id}</p>

        <div class="section">
            <h2>SLA Status</h2>
            <div style="text-align:center; padding: 20px 0;">
                <span class="status-badge">{sla_status}</span>
            </div>
        </div>

        <div class="section">
            <h2>Performance Metrics</h2>
            <div class="grid">
                <div class="metric">
                    <div class="value">{avg_response_time:.0f}</div>
                    <div class="label">Avg Response (ms)</div>
                </div>
                <div class="metric">
                    <div class="value">{p95_response_time:.0f}</div>
                    <div class="label">P95 Response (ms)</div>
                </div>
                <div class="metric">
                    <div class="value">{rps:.1f}</div>
                    <div class="label">Requests/sec</div>
                </div>
                <div class="metric">
                    <div class="value">{total_requests}</div>
                    <div class="label">Total Requests</div>
                </div>
                <div class="metric">
                    <div class="value">{total_failures}</div>
                    <div class="label">Total Failures</div>
                </div>
                <div class="metric">
                    <div class="value">{failure_rate:.2f}%</div>
                    <div class="label">Failure Rate</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Execution Details</h2>
            <div class="meta-grid">
                <div class="meta-item"><span>Target Host:</span> {host}</div>
                <div class="meta-item"><span>Virtual Users:</span> {users}</div>
                <div class="meta-item"><span>Spawn Rate:</span> {spawn_rate}</div>
                <div class="meta-item"><span>Duration:</span> {duration}</div>
                <div class="meta-item"><span>Generated:</span> {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
            </div>
        </div>
    </div>
</body>
</html>"""


def generate_html_report(
    stats: dict[str, Any],
    run_metadata: dict[str, Any],
    sla_status: str = "UNKNOWN",
) -> str:
    _ensure_report_dir()

    run_id = run_metadata.get("run_id", "unknown")
    html = _build_html(
        run_id=run_id,
        host=run_metadata.get("target_host", "N/A"),
        users=run_metadata.get("user_count", 0),
        spawn_rate=run_metadata.get("spawn_rate", 0),
        duration=run_metadata.get("duration", "N/A"),
        avg_response_time=stats.get("avg_response_time", 0),
        p95_response_time=stats.get("p95_response_time", 0),
        total_requests=stats.get("total_requests", 0),
        total_failures=stats.get("total_failures", 0),
        failure_rate=stats.get("failure_rate", 0),
        rps=stats.get("requests_per_second", 0),
        sla_status=sla_status,
    )

    report_path = REPORT_DIR / "latest-report.html"
    report_path.write_text(html, encoding="utf-8")
    logger.info("HTML report generated: %s", report_path)
    return str(report_path)
