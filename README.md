# Network Performance Monitor

A lightweight Python tool for measuring network performance (RTT, jitter, and packet loss) to different targets, with time-series visualization.

## Features
- Periodically probes a target host (IP address or domain) using ICMP.
- Computes Round-Trip Time (RTT), jitter, and packet loss rate.
- Handles ICMP timeouts gracefully (skips `None` values in plots).
- Exports raw data to CSV and generates a time-series plot.
- Supports command-line arguments for custom target, count, and interval.

## Requirements
- Python 3.x
- `ping3`, `matplotlib`

## Usage
Run the tool with default settings (probes 8.8.8.8 10 times):
```bash
python monitor.py
