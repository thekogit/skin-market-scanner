from data_analysis import compute_fee_aware_arbitrage_opportunity

def test_no_steam_data():
    label, profit, breakdown = compute_fee_aware_arbitrage_opportunity(10.0, None, 50)
    assert label == "NO_STEAM_DATA"
    assert profit == 0.0

def test_classifier_bands():
    # EXCELLENT_BUY: profit >= 20%, volume >= 50
    label, profit, _ = compute_fee_aware_arbitrage_opportunity(10.0, 15.0, 50)
    assert label == "EXCELLENT_BUY"
    assert profit >= 20.0

    # GOOD_BUY: 10% <= profit < 20%, volume >= 50
    label, profit, _ = compute_fee_aware_arbitrage_opportunity(10.0, 13.0, 50)
    assert label == "GOOD_BUY"
    assert 10.0 <= profit < 20.0

    # GOOD_BUY_LOW_VOL: profit >= 10%, volume < 50
    label, profit, _ = compute_fee_aware_arbitrage_opportunity(10.0, 13.0, 10)
    assert label == "GOOD_BUY_LOW_VOL"
    assert profit >= 10.0

    # MARGINAL_PROFIT: 5% <= profit < 10%
    label, profit, _ = compute_fee_aware_arbitrage_opportunity(10.0, 12.30, 50)
    assert label == "MARGINAL_PROFIT"
    assert 5.0 <= profit < 10.0

    # BREAKEVEN: 0% <= profit < 5%
    label, profit, _ = compute_fee_aware_arbitrage_opportunity(10.0, 11.60, 50)
    assert label == "BREAKEVEN"
    assert 0.0 <= profit < 5.0

    # SMALL_LOSS: -10% <= profit < 0%
    label, profit, _ = compute_fee_aware_arbitrage_opportunity(10.0, 11.0, 50)
    assert label == "SMALL_LOSS"
    assert -10.0 <= profit < 0.0

    # OVERPRICED: profit < -10%
    label, profit, _ = compute_fee_aware_arbitrage_opportunity(10.0, 8.0, 50)
    assert label == "OVERPRICED"
    assert profit < -10.0
