import re
import time
from hyperloglog import HyperLogLog


class IPAnalyzer:
    def __init__(self):
        self.data = []

    def load_data(self):
        file_path = "../data/lms-stage-access.log"
        self.data = []
        ip_pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

        with open(file_path, "r") as file:
            for line in file:
                match = ip_pattern.search(line)
                if match:
                    self.data.append(match.group(1))
        print(f"\nЗавантажено {len(self.data)} IP-адрес.\n")

    def count_unique_ips_exact(self):
        unique_ips = set(self.data)
        return len(unique_ips)

    def count_unique_ips_approximate(self):
        hll = HyperLogLog(0.1)
        _ = [hll.add(ip) for ip in self.data]
        return len(hll)

    def compare_methods(self):
        results = {}

        start = time.time()
        exact_count = self.count_unique_ips_exact()
        exact_time = time.time() - start

        start = time.time()
        approximate_count = self.count_unique_ips_approximate()
        approximate_time = time.time() - start

        results["Exact"] = {"Count": exact_count, "Time (s)": exact_time}
        results["Approximate"] = {
            "Count": approximate_count, "Time (s)": approximate_time}

        return results


if __name__ == "__main__":
    analyzer = IPAnalyzer()
    log_file_path = "lms-stage-access.log"
    analyzer.load_data()

    comparison_results = analyzer.compare_methods()

    print("Результати порівняння:")
    print(f"{'':<25}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
    print(
        f"{'Унікальні елементи':<25}{comparison_results['Exact']['Count']:<20}{comparison_results['Approximate']['Count']:<20}")
    print(
        f"{'Час виконання (сек.)':<25}{comparison_results['Exact']['Time (s)']:<20.6f}{comparison_results['Approximate']['Time (s)']:<20.6f}")
