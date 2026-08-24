from file_manager.read_csv import read_hostnames
import os


def write_sample_csv(path: str):
    with open(path, "w", newline="") as fh:
        fh.write("hostname\n")
        fh.write("host-a\n")
        fh.write("host-b\n")
        fh.write("host-a\n")


def dedupe(ids: list) -> list:
    seen = set()
    out = []
    for h in ids:
        if h and h not in seen:
            seen.add(h)
            out.append(h)
    return out


def main():
    sample = "hosts_sample.csv"
    write_sample_csv(sample)
    names = read_hostnames(sample)
    print("Parsed hostnames:", names)

    sample_ids = ["id-1", "id-2", "id-1", "id-3"]
    print("Original ids:", sample_ids)
    print("Dedupe ->", dedupe(sample_ids))


if __name__ == '__main__':
    main()
