import subprocess
import pandas as pd
import re


def myping(host):
    command = ["ping", "-n", "3", host]
    response = subprocess.check_output(command).decode('utf-8')
    return response


def parse_to_csv(list_text):
    csv_skeleton = {
        "ServerName": [],
        "SentPackets": [],
        "ReceivedPackets": [],
        "LostPackets": [],
        "MinimumTime": [],
        "MaximumTime": [],
        "AverageTime": []
    }
    for text in list_text:
        lines = text.split("\n")

        for line in lines:
            line = line.strip()

            if line.startswith("Pinging"):
                csv_skeleton["ServerName"].append(line.split()[1])

            match_packets = re.search(r"Sent = (\d+), Received = (\d+), Lost = (\d+)", line)
            if match_packets:
                csv_skeleton["SentPackets"].append(int(match_packets.group(1)))
                csv_skeleton["ReceivedPackets"].append(int(match_packets.group(2)))
                csv_skeleton["LostPackets"].append(int(match_packets.group(3)))

            match_times = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", line)
            if match_times:
                csv_skeleton["MinimumTime"].append(int(match_times.group(1)))
                csv_skeleton["MaximumTime"].append(int(match_times.group(2)))
                csv_skeleton["AverageTime"].append(int(match_times.group(3)))


    df = pd.DataFrame(csv_skeleton)

    df.to_csv("ping_results.csv", index=False, encoding="utf-8")

    print("CSV файл создан: ping_results.csv")
    print(df)


servers_name = ["www.google.com", "yandex.com", "chatgpt.com", "youtube.com", "github.com"]
ping_result = []
for server in servers_name:
    ping_result.append(myping(server))
parse_to_csv(ping_result)
