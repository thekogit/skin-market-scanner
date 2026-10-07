import math

def steam_fees_cents(seller_cents: int, steam_rate: float = 0.05, game_rate: float = 0.10) -> int:
    """Steam fee + game publisher fee, each at least 1 cent, charged on top of the seller's amount."""
    return max(1, math.floor(seller_cents * steam_rate)) + max(1, math.floor(seller_cents * game_rate))

def steam_seller_receives(buyer_price: float) -> float:
    """Largest amount the seller can receive when the buyer pays buyer_price."""
    p = round(buyer_price * 100)
    s = int(p / 1.15)
    while s > 0 and s + steam_fees_cents(s) > p:
        s -= 1
    while s + 1 + steam_fees_cents(s + 1) <= p:
        s += 1
    return s / 100

def steam_price_needed(net: float) -> float:
    """Lowest buyer price at which the seller receives at least `net`."""
    target = round(net * 100)
    p = max(3, math.floor(target * 1.15) - 2) / 100
    while round(steam_seller_receives(p) * 100) < target:
        p = round(p + 0.01, 2)
    return p
