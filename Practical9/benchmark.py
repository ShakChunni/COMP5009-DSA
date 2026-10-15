from SortsTestHarness import runTest


def main():
    print("| Size | Input | Bubble | Insertion | Selection | Merge | Quick left | Quick median3 | Quick random |")
    print("|---:|---|---:|---:|---:|---:|---:|---:|---:|")
    size = 250
    while size <= 2000:
        for array_type in "adr":
            row = "| " + str(size) + " | " + array_type + " |"
            for sort_type in "bismqtu":
                seconds = runTest(size, sort_type, array_type, False)
                row += " " + format(seconds * 1000, ".3f") + " |"
            print(row, flush=True)
        size *= 2


if __name__ == "__main__":
    main()
