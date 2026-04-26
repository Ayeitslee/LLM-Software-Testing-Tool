def generate_tests(code_snippet, function_name):

    tests = {
        "whitebox": [],
        "blackbox": [],
        "bva": [],
        "ecp": [],
        "mutation": [],
        "path_coverage": [],
        "block_coverage": []
    }

    if function_name == "add":
        tests["whitebox"] = [
            "add(2,3)=5",
            "add(-1,1)=0"
        ]
        tests["ecp"] = [
            "add(5,5)=10",
            "add(0,1)=1"
        ]

    elif function_name == "divide":
        tests["whitebox"] = [
            "divide(10,2)=5",
            "divide(10,0)=error"
        ]
        tests["ecp"] = [
            "divide(9,3)=3",
            "divide(5,0)=error"
        ]

    elif function_name == "calculate_discount":
        tests["whitebox"] = [
            "calculate_discount(100,10)=10",
            "calculate_discount(100,0)=0"
        ]
        tests["ecp"] = [
            "calculate_discount(50,10)=5",
            "calculate_discount(100,110)=error"
        ]

    # metadata ONLY (NOT EXECUTED)
    tests["mutation"] = [
        "mutant: > -> <",
        "mutant: + -> -"
    ]

    tests["block_coverage"] = [f"blocks={code_snippet.count('if')}"]
    tests["path_coverage"] = [f"paths={2 ** max(1, code_snippet.count('if'))}"]

    return tests
