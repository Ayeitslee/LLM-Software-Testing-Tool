def generate_tests(code_snippet, function_name):

    base_tests = {
        "whitebox": [],
        "blackbox": [],
        "bva": [],
        "ecp": [],
        "mutation": [],
        "path_coverage": [],
        "block_coverage": []
    }

    # -------------------------
    # ADD FUNCTION
    # -------------------------
    if function_name == "add":
        base_tests.update({
            "whitebox": ["add(2,3)=5", "add(-1,1)=0"],
            "blackbox": ["valid integers", "negative inputs"],
            "bva": ["0 boundary", "large numbers"],
            "ecp": ["positive class", "negative class"]
        })

    # -------------------------
    # DIVIDE FUNCTION
    # -------------------------
    elif function_name == "divide":
        base_tests.update({
            "whitebox": ["divide(10,2)=5", "divide(10,0)=error"],
            "blackbox": ["normal division", "zero division"],
            "bva": ["denominator=1", "denominator=0"],
            "ecp": ["valid numbers", "invalid zero case"]
        })

    # -------------------------
    # DISCOUNT FUNCTION
    # -------------------------
    elif function_name == "calculate_discount":
        base_tests.update({
            "whitebox": ["100,10=10", "100,0=0"],
            "blackbox": ["valid range 0-100", "invalid range"],
            "bva": ["0%,100%,101%"],
            "ecp": ["valid class", "invalid class"]
        })

    # -------------------------
    # BONUS FEATURES (SIMULATED)
    # -------------------------

    # Block Coverage Simulation
    blocks = code_snippet.count("if") + code_snippet.count("for")
    base_tests["block_coverage"] = [
        f"Detected {blocks} decision blocks",
        "Each branch executed at least once (simulated)"
    ]

    # Path Coverage Simulation
    paths = 2 ** max(blocks, 1)
    base_tests["path_coverage"] = [
        f"Estimated paths: {paths}",
        "All major execution paths approximated"
    ]

    # Mutation Testing Simulation
    base_tests["mutation"] = [
        "Replaced > with <",
        "Replaced + with -",
        "Replaced == with !="
    ]

    return base_tests
