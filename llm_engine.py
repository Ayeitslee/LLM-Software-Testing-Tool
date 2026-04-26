def generate_tests(code_snippet, function_name):

    tests = {
        "whitebox": [],
        "blackbox": [],
        "bva": [],
        "ecp": [],
        "mutation": [],
        "block_coverage": [],
        "path_coverage": []
    }

    # -------------------------
    # ADD
    # -------------------------
    if function_name == "add":
        tests["whitebox"] = [
            "add(2,3)=5",
            "add(-1,1)=0"
        ]
        tests["blackbox"] = [
            "add(10,5)=15",
            "add(0,0)=0"
        ]
        tests["bva"] = [
            "add(0,1)=1",
            "add(999,1)=1000"
        ]
        tests["ecp"] = [
            "add(5,5)=10",
            "add(-5,-5)=-10"
        ]

    # -------------------------
    # DIVIDE
    # -------------------------
    elif function_name == "divide":
        tests["whitebox"] = [
            "divide(10,2)=5",
            "divide(10,0)=error"
        ]
        tests["blackbox"] = [
            "divide(9,3)=3",
            "divide(5,0)=error"
        ]
        tests["bva"] = [
            "divide(1,1)=1",
            "divide(10,1)=10"
        ]
        tests["ecp"] = [
            "divide(8,2)=4",
            "divide(7,0)=error"
        ]

    # -------------------------
    # DISCOUNT
    # -------------------------
    elif function_name == "calculate_discount":
        tests["whitebox"] = [
            "calculate_discount(100,10)=10",
            "calculate_discount(100,0)=0"
        ]
        tests["blackbox"] = [
            "calculate_discount(50,50)=25",
            "calculate_discount(100,110)=error"
        ]
        tests["bva"] = [
            "calculate_discount(100,0)=0",
            "calculate_discount(100,100)=100"
        ]
        tests["ecp"] = [
            "calculate_discount(200,10)=20",
            "calculate_discount(200,-5)=error"
        ]

    # -------------------------
    # METADATA (NOT EXECUTED TESTS)
    # -------------------------
    blocks = code_snippet.count("if") + code_snippet.count("for")
    tests["block_coverage"] = [
        f"blocks={blocks}"
    ]

    paths = 2 ** max(blocks, 1)
    tests["path_coverage"] = [
        f"paths={paths}"
    ]

    tests["mutation"] = [
        "mutant: > -> <",
        "mutant: + -> -",
        "mutant: == -> !="
    ]

    return tests