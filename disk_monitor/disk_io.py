"""
Author: Geferson Lucatelli

Simple total I/O read/write linux monitor per disk.
I use this to monitor my daily total I/O during data processing,
specially in SSDs.
"""
import time
import matplotlib.pyplot as plt

INTERVAL = 2  # seconds
OUTPUT_FILE = 'disk_io_stats.txt'
SECTOR_SIZE = 512  # bytes
BYTES_IN_GB = 1e9

# For plotting
plt.ion()
fig, ax = plt.subplots()

def read_diskstats():
    with open('/proc/diskstats', 'r') as f:
        return f.readlines()

def is_disk(device_name):
    # Check if the device_name is a SATA disk or an NVMe disk
    if device_name.startswith("nvme"):
        return "p" not in device_name
    else:
        return device_name[-1].isalpha()

def parse_diskstats(lines):
    io_data = {}
    for line in lines:
        parts = line.split()
        device_name = parts[2]
        if not is_disk(device_name):
            continue
        read_sectors = int(parts[5]) * SECTOR_SIZE / BYTES_IN_GB
        write_sectors = int(parts[9]) * SECTOR_SIZE / BYTES_IN_GB
        io_data[device_name] = (read_sectors, write_sectors)
    return io_data

def store_to_file(data):
    with open(OUTPUT_FILE, 'a') as f:
        for disk, (read, write) in data.items():
            f.write(f"{time.time()} {disk} read {read} write {write}\n")

def plot_io(data):
    disk_names = list(data.keys())
    read_values = [data[disk][0] for disk in disk_names]
    write_values = [data[disk][1] for disk in disk_names]

    ax.clear()
    bar_width = 0.35
    r1 = range(len(disk_names))
    r2 = [x + bar_width for x in r1]

    ax.bar(r1, read_values, width=bar_width, label='Reads (GB)', color='blue')
    ax.bar(r2, write_values, width=bar_width, label='Writes (GB)', color='red')

    ax.set_xlabel('Disks')
    ax.set_ylabel('I/O (GB)')
    ax.set_xticks([r + bar_width for r in range(len(disk_names))])
    ax.set_xticklabels(disk_names)
    ax.legend()
    fig.tight_layout()
    fig.canvas.flush_events()

def main():
    while True:
        disk_data = parse_diskstats(read_diskstats())
        store_to_file(disk_data)
        plot_io(disk_data)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        plt.ioff()
        plt.show()