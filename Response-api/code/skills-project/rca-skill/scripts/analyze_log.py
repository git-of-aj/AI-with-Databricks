import re
import sys
from collections import Counter


HTTP_PATTERN = re.compile(r"\bHTTP[ /]*(\d{3})\b|\bstatus[=: ]+(\d{3})\b", re.I)

ERROR_PATTERN = re.compile(
    r"\b(ERROR|ERR|FATAL|CRITICAL)\b",
    re.I
)

WARNING_PATTERN = re.compile(
    r"\b(WARN|WARNING)\b",
    re.I
)

EXCEPTION_PATTERN = re.compile(
    r"\b([A-Za-z_][A-Za-z0-9_]*(?:Exception|Error))\b"
)


def analyze_log(path):
    errors = []
    warnings = []
    exceptions = []
    http_codes = Counter()

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line_number, line in enumerate(f, start=1):

            line = line.rstrip()

            # HTTP status codes
            match = HTTP_PATTERN.search(line)

            if match:
                code = match.group(1) or match.group(2)
                http_codes[code] += 1

            # Errors
            if ERROR_PATTERN.search(line):
                errors.append({
                    "line": line_number,
                    "text": line
                })

            # Warnings
            if WARNING_PATTERN.search(line):
                warnings.append({
                    "line": line_number,
                    "text": line
                })

            # Exceptions
            for exception in EXCEPTION_PATTERN.findall(line):
                exceptions.append({
                    "line": line_number,
                    "type": exception,
                    "text": line
                })

    print("\n=== LOG SUMMARY ===")

    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Exceptions: {len(exceptions)}")

    print("\n=== HTTP STATUS CODES ===")

    if http_codes:
        for code, count in http_codes.most_common():
            print(f"HTTP {code}: {count}")
    else:
        print("No HTTP status codes detected.")

    print("\n=== ERROR LINES ===")

    for item in errors[:50]:
        print(f"[line {item['line']}] {item['text']}")

    print("\n=== WARNING LINES ===")

    for item in warnings[:30]:
        print(f"[line {item['line']}] {item['text']}")

    print("\n=== EXCEPTIONS ===")

    exception_counts = Counter(
        item["type"] for item in exceptions
    )

    for exception, count in exception_counts.most_common():
        print(f"{exception}: {count}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python analyze_log.py <log-file>")
        sys.exit(1)

    analyze_log(sys.argv[1])
