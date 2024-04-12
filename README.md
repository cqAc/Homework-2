# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution
> 
> B -> A -> D -> C -> B. The final reward is around 20.129888944077446732. The in and out of the swaps are
> 
> 5 -> 5.6496666 -> 2.45497711020355453679639703627177194143569710568370756590098306665 -> 5.0797981073492201638512003494222239110161976735075475226496268007 -> 20.129888944077446732.

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution
> 
> Slippage in AMMs like Uniswap occurs when the actual price of a trade is different from the expected price at the time the transaction is submitted. This is due to the time delay in executing the trade and the price change caused by the trade itself.
> 
> Uniswap V2 allows users to set a maximum slippage tolerance to prevent trades from executing at prices that are too far from their expectations. If the actual price exceeds this tolerance, the trade will not go through.
```
    def swap_tokens(input_amount, reserve_in, reserve_out, max_slippage):
    # Calculate the output amount using the constant product formula
    output_amount = reserve_out - (reserve_in * reserve_out) / (reserve_in + input_amount)
    
    # Calculate the minimum amount the user is willing to accept (based on max slippage)
    min_output_amount = output_amount * (1 - max_slippage)
    
    # Check if the actual output amount is above the minimum acceptable amount
    if output_amount >= min_output_amount:
        # Update reserves to reflect the trade
        reserve_in += input_amount
        reserve_out -= output_amount
        return output_amount
    else:
        # Slippage too high, trade not executed
        return "Trade failed due to high slippage"

  # Example usage with 1% max slippage tolerance
  result = swap_tokens(100, 5000, 5000, 0.01)
```

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution
>
> The rationale behind subtracting a minimum liquidity in the UniswapV2Pair contract upon initial liquidity minting is to prevent division by zero errors in the contract's calculations. This is necessary because the Uniswap protocol uses a constant product formula to maintain liquidity and determine prices, which involves division operations. By ensuring that there is always a minimum amount of liquidity in the pool, the contract avoids situations where a division by zero could occur.
>
> The minimum liquidity is set to a small amount (1000 liquidity tokens) and is permanently locked in the pool by sending it to the zero address. This means that the first liquidity provider does not receive liquidity tokens equivalent to the full amount of liquidity they provide; instead, the amount corresponding to the minimum liquidity is deducted and locked away. This is a one-time event that only occurs when the pool is first created.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution
>
> The intention behind this formula is to maintain the constant product formula (x * y = k), which is the core of the Automated Market Maker (AMM) model used by Uniswap. This formula ensures that the relative value of each liquidity token remains constant with respect to the pool's reserves. It prevents the dilution of value for existing liquidity providers by ensuring that new liquidity providers can only add liquidity at the current price ratio of the pool.
> 
> By using this formula, Uniswap enforces that the price of the assets in the pool does not change due to the addition of new liquidity. This protects the interests of existing liquidity providers and maintains the integrity of the market pricing mechanism inherent in the AMM model. It also ensures that the liquidity provider receives a fair share of the pool's total liquidity proportional to the amount of assets they deposit, relative to the current pool size.


## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution
>
> A sandwich attack is a type of front-running attack in decentralized finance (DeFi) where a malicious actor places orders before and after a victim's transaction. When a user initiates a swap on a decentralized exchange (DEX), the attacker sees the pending transaction and quickly places an order with a higher gas fee to get their transaction executed first, thus increasing the price of the asset. After the victim's transaction is executed at this inflated price, the attacker completes the attack by selling the asset at the higher price, profiting from the price slippage caused by the victim's transaction. This can lead to financial loss for the victim as they receive less of the swapped asset than expected.

