def generate_tests(code_snippet, function_name):

    if function_name == "add":
        return {
            "whitebox": ["add(2,3)=5", "add(-1,1)=0"],
            "blackbox": ["valid integers", "negative inputs"],
            "bva": ["0 boundary", "large numbers"],
            "ecp": ["positive class", "negative class"]
        }

    elif function_name == "divide":
        return {
            "whitebox": ["divide(10,2)=5", "divide(10,0)=error"],
            "blackbox": ["normal division", "zero division"],
            "bva": ["denominator=1", "denominator=0"],
            "ecp": ["valid numbers", "invalid zero case"]
        }

    elif function_name == "calculate_discount":
        return {
            "whitebox": ["100,10=10", "100,0=0"],
            "blackbox": ["valid range 0-100", "invalid range"],
            "bva": ["0%,100%,101%"],
            "ecp": ["valid class", "invalid class"]
        }

    return {
        "whitebox": ["generic test"],
        "blackbox": ["generic case"],
        "bva": ["boundary test"],
        "ecp": ["equivalence class test"]
    }
