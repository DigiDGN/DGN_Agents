# save_csv/load_csv for Thread (lossy)
import csv

def save_csv(thread, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["role", "content"])
        for msg in thread.messages:
            writer.writerow([msg.role, msg.content])

def load_csv(path):
    from DGN_Agents.models import Thread, Turn
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        messages = [Turn(role=row["role"], content=row["content"]) for row in reader]
    return Thread(messages=messages)
