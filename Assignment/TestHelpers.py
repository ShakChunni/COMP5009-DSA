def expectError(label, exception_type, operation):
    try:
        operation()
    except exception_type as error:
        print(f"PASS {label}: {error}")
        return
    raise AssertionError("Expected error was not raised: " + label)


def check(label, condition):
    if not condition:
        raise AssertionError("Failed: " + label)
    print("PASS", label)
