import json
import pathlib
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def solve_lab1():
    notebook_path = pathlib.Path("Day1/Lab1.ipynb")
    if not notebook_path.exists():
        print("Error: Day1/Lab1.ipynb not found.")
        return False

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    
    # Solve Factorial
    notebook["cells"][1]["source"] = [
        "def factorial(n):\n",
        "    \"\"\"Compute the factorial of a number.\"\"\"\n",
        "    result = 1\n",
        "    for i in range(1, n + 1):  # <-- Filled: n + 1\n",
        "        result *= i  # <-- Filled: i\n",
        "    return result\n",
        "\n",
        "# ✅ Test Case\n",
        "def test_factorial():\n",
        "    assert factorial(5) == 120, \"Test case failed!\"\n",
        "    assert factorial(3) == 6, \"Test case failed!\"\n",
        "    assert factorial(1) == 1, \"Test case failed!\"\n",
        "    print(\"✅ All test cases passed!\")\n",
        "\n",
        "test_factorial()"
    ]

    # Solve Reverse String
    notebook["cells"][3]["source"] = [
        "def reverse_string(s):\n",
        "    \"\"\"Reverse a string.\"\"\"\n",
        "    return s[::-1]  # <-- Filled: s[::-1]\n",
        "\n",
        "# ✅ Test Case\n",
        "def test_reverse_string():\n",
        "    assert reverse_string(\"Python\") == \"nohtyP\", \"Test case failed!\"\n",
        "    assert reverse_string(\"Data\") == \"ataD\", \"Test case failed!\"\n",
        "    print(\"✅ All test cases passed!\")\n",
        "\n",
        "test_reverse_string()"
    ]

    # Solve Even Numbers
    notebook["cells"][5]["source"] = [
        "def find_even_numbers(lst):\n",
        "    \"\"\"Return a list of even numbers.\"\"\"\n",
        "    return [num for num in lst if num % 2 == 0]  # <-- Filled: num and num % 2 == 0\n",
        "\n",
        "# ✅ Test Case\n",
        "def test_find_even_numbers():\n",
        "    assert find_even_numbers([1, 2, 3, 4, 5, 6]) == [2, 4, 6], \"Test case failed!\"\n",
        "    assert find_even_numbers([10, 15, 20, 25]) == [10, 20], \"Test case failed!\"\n",
        "    print(\"✅ All test cases passed!\")\n",
        "\n",
        "test_find_even_numbers()"
    ]

    # Solve File Handling
    notebook["cells"][7]["source"] = [
        "# Writing to a file\n",
        "def write_to_file(filename, data):\n",
        "    with open(filename, 'w') as file:  # <-- Filled: 'w'\n",
        "        for name in data:\n",
        "            file.write(name + '\\n')  # <-- Filled: write(name + '\\n')\n",
        "\n",
        "# Reading from a file\n",
        "def read_from_file(filename):\n",
        "    with open(filename, 'r') as file:  # <-- Filled: 'r'\n",
        "        return file.readlines()  # <-- Filled: readlines()\n",
        "\n",
        "# ✅ Test Case\n",
        "def test_file_handling():\n",
        "    filename = \"names.txt\"\n",
        "    names = [\"Alice\", \"Bob\", \"Charlie\"]\n",
        "    \n",
        "    write_to_file(filename, names)\n",
        "    content = read_from_file(filename)\n",
        "    \n",
        "    assert content == [\"Alice\\n\", \"Bob\\n\", \"Charlie\\n\"], \"Test case failed!\"\n",
        "    print(\"✅ All test cases passed!\")\n",
        "\n",
        "test_file_handling()"
    ]

    # Solve JSON Handling
    notebook["cells"][9]["source"] = [
        "import json\n",
        "\n",
        "# Writing to a JSON file\n",
        "def write_json(filename, data):\n",
        "    with open(filename, 'w') as file:  # <-- Filled: 'w'\n",
        "        json.dump(data, file, indent=4)  # <-- Filled: data\n",
        "\n",
        "# Reading from a JSON file\n",
        "def read_json(filename):\n",
        "    with open(filename, 'r') as file:  # <-- Filled: 'r'\n",
        "        return json.load(file)  # <-- Filled: load(file)\n",
        "\n",
        "# ✅ Test Case\n",
        "def test_json_handling():\n",
        "    filename = \"data.json\"\n",
        "    data = {\"name\": \"Alice\", \"age\": 25, \"city\": \"Paris\"}\n",
        "    \n",
        "    write_json(filename, data)\n",
        "    loaded_data = read_json(filename)\n",
        "    \n",
        "    assert loaded_data == data, \"Test case failed!\"\n",
        "    print(\"✅ All test cases passed!\")\n",
        "\n",
        "test_json_handling()"
    ]

    notebook_path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    print("✅ Day1/Lab1.ipynb updated with solutions.")
    return True

def solve_lab1_server():
    notebook_path = pathlib.Path("Day1/Lab1_Server_Health.ipynb")
    if not notebook_path.exists():
        print("Error: Day1/Lab1_Server_Health.ipynb not found.")
        return False

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    # Task 1: load_servers
    notebook["cells"][4]["source"] = [
        "import json\n",
        "import pathlib\n",
        "import sys\n",
        "\n",
        "# ✏️ YOUR TURN\n",
        "# Write a function load_servers(path: str) -> list[dict] that:\n",
        "#   1. Reads the JSON file at the given path\n",
        "#   2. Returns the parsed list of server dicts\n",
        "#   3. Prints a clear error and exits if the file is not found or invalid JSON\n",
        "\n",
        "def load_servers(path: str) -> list[dict]:\n",
        "    \"\"\"Load and return the list of servers from a JSON file.\"\"\"\n",
        "    try:\n",
        "        raw = pathlib.Path(path).read_text(encoding='utf-8')\n",
        "        return json.loads(raw)\n",
        "    except FileNotFoundError:\n",
        "        print(f\"Error: The file '{path}' does not exist.\", file=sys.stderr)\n",
        "        sys.exit(1)\n",
        "    except json.JSONDecodeError:\n",
        "        print(f\"Error: The file '{path}' is not valid JSON.\", file=sys.stderr)\n",
        "        sys.exit(1)\n",
        "\n",
        "\n",
        "# Test your function\n",
        "servers = load_servers('servers.json')\n",
        "print(f'Loaded {len(servers)} servers')\n",
        "print('First server:', servers[0])"
    ]

    # Task 2: check_server
    notebook["cells"][6]["source"] = [
        "import requests\n",
        "import time\n",
        "\n",
        "# ✏️ YOUR TURN\n",
        "# Write check_server(server: dict) -> dict\n",
        "# It should return a dict with keys:\n",
        "#   name, url, status, response_time_ms, status_code\n",
        "# For DOWN servers: response_time_ms=None, status_code=None, add an 'error' key\n",
        "\n",
        "def check_server(server: dict) -> dict:\n",
        "    \"\"\"Check the health of a single server and return a result dict.\"\"\"\n",
        "    url = f\"{server['protocol']}://{server['host']}:{server['port']}{server['health_path']}\"\n",
        "    start = time.time()\n",
        "    try:\n",
        "        # Perform GET request with a 5-second timeout\n",
        "        resp = requests.get(url, timeout=5)\n",
        "        elapsed_ms = (time.time() - start) * 1000\n",
        "        \n",
        "        status_code = resp.status_code\n",
        "        # Status rules:\n",
        "        # - UP — HTTP 200 and response time <= 500 ms\n",
        "        # - DEGRADED — HTTP 200 but slow, OR a non-200 HTTP response\n",
        "        # - DOWN — connection error or timeout\n",
        "        if status_code == 200:\n",
        "            if elapsed_ms <= 500:\n",
        "                status = \"UP\"\n",
        "            else:\n",
        "                status = \"DEGRADED\"\n",
        "        else:\n",
        "            status = \"DEGRADED\"\n",
        "            \n",
        "        return {\n",
        "            \"name\": server[\"name\"],\n",
        "            \"url\": url,\n",
        "            \"status\": status,\n",
        "            \"response_time_ms\": elapsed_ms,\n",
        "            \"status_code\": status_code\n",
        "        }\n",
        "    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:\n",
        "        return {\n",
        "            \"name\": server[\"name\"],\n",
        "            \"url\": url,\n",
        "            \"status\": \"DOWN\",\n",
        "            \"response_time_ms\": None,\n",
        "            \"status_code\": None,\n",
        "            \"error\": str(e)\n",
        "        }\n",
        "\n",
        "\n",
        "# Quick test with the first (healthy) server\n",
        "result = check_server(servers[0])\n",
        "print(result)"
    ]

    # Task 3: run_health_check
    notebook["cells"][8]["source"] = [
        "from datetime import datetime\n",
        "\n",
        "# ✏️ YOUR TURN\n",
        "# Write run_health_check(servers: list[dict]) -> dict\n",
        "# It should:\n",
        "#   1. Call check_server() for each server\n",
        "#   2. Print a one-line status per server as it runs\n",
        "#   3. Return a report dict with: checked_at, total, up, degraded, down, results\n",
        "\n",
        "def run_health_check(servers: list[dict]) -> dict:\n",
        "    \"\"\"Check all servers and return a summary report.\"\"\"\n",
        "    results = []\n",
        "    up = 0\n",
        "    degraded = 0\n",
        "    down = 0\n",
        "    \n",
        "    for server in servers:\n",
        "        res = check_server(server)\n",
        "        results.append(res)\n",
        "        \n",
        "        # Print a one-line status per server as it runs\n",
        "        if res[\"status\"] == \"DOWN\":\n",
        "            print(f\"[-_ -] {res['name']}: {res['status']} (Error: {res.get('error')})\")\n",
        "            down += 1\n",
        "        else:\n",
        "            print(f\"[o_o] {res['name']}: {res['status']} (HTTP {res['status_code']}, {res['response_time_ms']:.1f}ms)\")\n",
        "            if res[\"status\"] == \"UP\":\n",
        "                up += 1\n",
        "            else:\n",
        "                degraded += 1\n",
        "                \n",
        "    return {\n",
        "        \"checked_at\": datetime.now().isoformat(timespec='seconds'),\n",
        "        \"total\": len(servers),\n",
        "        \"up\": up,\n",
        "        \"degraded\": degraded,\n",
        "        \"down\": down,\n",
        "        \"results\": results\n",
        "    }\n",
        "\n",
        "\n",
        "report = run_health_check(servers)\n",
        "print('\\nReport keys:', list(report.keys()))"
    ]

    notebook_path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    print("✅ Day1/Lab1_Server_Health.ipynb updated with solutions.")
    return True

if __name__ == "__main__":
    s1 = solve_lab1()
    s2 = solve_lab1_server()
    if s1 and s2:
        print("🎉 All labs solved successfully!")
    else:
        sys.exit(1)
