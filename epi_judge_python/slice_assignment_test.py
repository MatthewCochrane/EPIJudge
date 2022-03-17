import os
import psutil

ARR_SIZE = 100000


def get_usage_kb() -> int:
    return int(psutil.Process(os.getpid()).memory_info().rss / 1024)


if __name__ == "__main__":
    arr = [0] * ARR_SIZE
    initial_usage = get_usage_kb()
    # O(1) extra space
    for i in range(len(arr)):
        arr[i] *= 2
    print(f"Loop assignment extra space used {get_usage_kb() - initial_usage}KB")
    initial_usage = get_usage_kb()
    # O(n) extra space
    arr[:] = (x * 2 for x in arr)
    print(f"Slice assignment extra space used {get_usage_kb() - initial_usage}KB")

    exit(0)
