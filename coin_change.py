def coin_change_dp_verbose(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    last = [-1] * (amount + 1)

    logs = []

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0 and dp[i - coin] + 1 < dp[i]:
                old = dp[i]
                dp[i] = dp[i - coin] + 1
                last[i] = coin
                logs.append(f"dp[{i}] diperbarui dari {old} -> {dp[i]} (pakai koin {coin})")

    if dp[amount] == float('inf'):
        return -1, [], logs

    result = []
    curr = amount
    while curr > 0:
        result.append(last[curr])
        curr -= last[curr]

    return dp[amount], result, logs

def coin_change_greedy_verbose(coins, amount):
    coins.sort(reverse=True)
    result = []
    logs = []
    original_amount = amount

    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)
            logs.append(f"Ambil koin {coin}, sisa: {amount}")

    if amount != 0:
        logs.append("Tidak bisa membentuk jumlah target dengan greedy.")
        return -1, [], logs

    return len(result), result, logs
