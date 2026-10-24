import time
from ping3 import ping
import csv
import matplotlib.pyplot as plt
import argparse

# 解析命令行参数
parser = argparse.ArgumentParser(description="Network Performance Monitor")
parser.add_argument("--target", default="8.8.8.8", help="目标 IP 或域名")
parser.add_argument("--count", type=int, default=10, help="探测次数")
parser.add_argument("--interval", type=float, default=1.0, help="探测间隔（秒）")

args = parser.parse_args()

TARGET = args.target
COUNT = args.count
INTERVAL = args.interval

results = []  # 用来存每次的结果

for i in range(COUNT):
    rtt = ping(TARGET)

    if rtt is None:
        print(f"[{i+1}/{COUNT}] 超时")
        results.append(None)
    else:
        rtt_ms = rtt * 1000
        print(f"[{i+1}/{COUNT}] RTT: {rtt_ms:.2f} ms")
        results.append(rtt_ms)

    if i < COUNT - 1:      # 最后一次不用等
        time.sleep(INTERVAL)

print("原始结果：", results)

# ===== 阶段3：计算指标 =====

# 1. 丢包率：数列表里有多少个 None
loss_count = results.count(None)
loss_rate = loss_count / COUNT * 100

# 2. 成功 RTT 列表：过滤掉 None
success_rtts = [r for r in results if r is not None]

# 3. 平均 RTT
if success_rtts:
    avg_rtt = sum(success_rtts) / len(success_rtts)
else:
    avg_rtt = None

# 4. 抖动：相邻两次成功 RTT 差值的绝对值的平均
jitter = None
if len(success_rtts) >= 2:
    diffs = []
    for i in range(1, len(success_rtts)):
        diffs.append(abs(success_rtts[i] - success_rtts[i-1]))
    jitter = sum(diffs) / len(diffs)

# 5. 打印结果
print("\n===== 测量汇总 =====")
print(f"总探测次数: {COUNT}")
print(f"成功次数:   {len(success_rtts)}")
print(f"超时次数:   {loss_count}")
print(f"丢包率:     {loss_rate:.1f}%")
if avg_rtt is not None:
    print(f"平均 RTT:   {avg_rtt:.2f} ms")
if jitter is not None:
    print(f"抖动:       {jitter:.2f} ms")



# 1. 写CSV
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["index", "rtt_ms"])
    for i, r in enumerate(results, start=1):
        writer.writerow([i, "" if r is None else r])

print("\n已保存 results.csv")

# 2. 画图
x = list(range(1, COUNT + 1))
y = [float("nan") if r is None else r for r in results]

plt.figure(figsize=(8, 4))
plt.plot(x, y, marker="o", linestyle="-")
plt.xlabel("Probe index")
plt.ylabel("RTT (ms)")
plt.title(f"RTT to {TARGET} over {COUNT} probes")
plt.grid(True)
plt.savefig("rtt_plot.png", dpi=150)
plt.show()

print("已保存 rtt_plot.png")