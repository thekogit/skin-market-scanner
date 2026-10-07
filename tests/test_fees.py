from fees import steam_seller_receives, steam_price_needed

def test_minimum_fees():
    assert steam_seller_receives(0.03) == 0.01

def test_round_prices():
    assert steam_seller_receives(1.15) == 1.00
    assert steam_seller_receives(10.00) == 8.70

def test_price_needed_round_trips():
    assert steam_price_needed(8.70) == 10.00
    for net in (0.50, 1.00, 8.70, 123.45):
        assert steam_seller_receives(steam_price_needed(net)) >= net
