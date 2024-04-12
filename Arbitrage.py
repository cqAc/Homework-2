# Liquidity data setup
o_liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def find_cycles(graph, start, end, path=[]):
    path = path + [start]
    if len(path) > 1 and start == end:
        yield path
        return
    for node in graph[start]:
        if node not in path or (node == end and len(path) > 1):
            yield from find_cycles(graph, node, end, path)

# Define the graph
graph = {
    'tokenA': ['tokenB', 'tokenC', 'tokenD', 'tokenE'],
    'tokenB': ['tokenA', 'tokenC', 'tokenD', 'tokenE'],
    'tokenC': ['tokenA', 'tokenB', 'tokenD', 'tokenE'],
    'tokenD': ['tokenA', 'tokenB', 'tokenC', 'tokenE'],
    'tokenE': ['tokenA', 'tokenB', 'tokenC', 'tokenD']
}

# Find all cycles starting and ending at 'tokenB'
cycles = list(find_cycles(graph, 'tokenB', 'tokenB'))

def swap(liquidity, input_token, output_token, input_amount, fee):
    if (input_token, output_token) in liquidity:
        x, y = liquidity[(input_token, output_token)]
    elif (output_token, input_token) in liquidity:
        y, x = liquidity[(output_token, input_token)]
    else:
        return 0  # No liquidity for this token pair

    # Calculate the fee
    fee_amount = input_amount * fee
    input_amount -= fee_amount

    # Calculate output amount using the constant product formula
    k = x * y  # Constant product
    new_x = x + input_amount
    new_y = k / new_x
    output_amount = y - new_y

    # Check if there is enough liquidity for the output token
    if output_amount <= 0:
        return 0

    # Update the liquidity pool
    if (input_token, output_token) in liquidity:
        liquidity[(input_token, output_token)] = (new_x, new_y)
    elif (output_token, input_token) in liquidity:
        liquidity[(output_token, input_token)] = (new_y, new_x)

    return output_amount

def arbitrage_cycles(cycles, o_liquidity, fee):
    results = []
    for cycle in cycles:
        amount = 5  # Start with 1 unit of tokenB
        liquidity = o_liquidity.copy()
        for i in range(len(cycle) - 1):
            input_token = cycle[i]
            output_token = cycle[i + 1]
            amount = swap(liquidity, input_token, output_token, amount, fee)
            if amount == 0:
                break  # Not enough liquidity, quit the current cycle
        if amount != 0:
            results.append((cycle, amount))
    return results

# Define the fee
fee = 0.003  # 0.3 percent

# Find all cycles starting and ending at 'tokenB'
cycles = list(find_cycles(graph, 'tokenB', 'tokenB'))

# Calculate the final amount of tokenB for each cycle
arbitrage_results = arbitrage_cycles(cycles, o_liquidity, fee)

# Print the results
maxa = 0
path = []
for result in arbitrage_results:
    if maxa < result[1]:
        maxa = result[1]
        path = result[0]

print(f"path: {path}, tokenB balance={maxa}")
