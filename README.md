# skin-market-scanner

Asynchronous market data scanner identifying price spreads between Skinport listings and Steam Community Market prices with exact fee modeling.

![Skin Market Scanner Report](docs/report.png)

## Why
Finding pricing discrepancies between third-party gaming marketplaces and the Steam Community Market requires modeling exact platform fee structures and handling restrictive endpoint rate limits. Simple percentage subtractions fail to account for Steam's additive buyer-side fee formula and per-item minimums, while unthrottled requests trigger immediate HTTP 429 lockouts.

## How it works
- Ingests public marketplace listings and sales history from Skinport's REST API.
- Fetches Steam Community Market pricing asynchronously via `aiohttp` bounded by an adaptive semaphore.
- Handles HTTP 429 rate limits through exponential backoff with request jitter.
- Persists market data snapshots in a SQLite cache with configurable time-to-live expiration.
- Calculates exact Steam proceeds using integer cents to model Valve's 5% Steam + 10% publisher fee split (1-cent minimums).
- Generates an interactive, dark-themed HTML report with sortable tables, fee breakdowns, and price charts.

## Results
Summary from a live scan (Counter-Strike 2, USD, $10–$100, volume ≥ 50 sales/week):

```bash
python main.py
```

```text
Processed 23 items across 1 game(s)

--- Classification Summary ---
  NO_STEAM_DATA: 1
  BREAKEVEN: 2
  MARGINAL_PROFIT: 3
  SMALL_LOSS: 17

Items with positive spread: 5
Median positive spread: 6.20%
```

| Classification | Spread Range | Count |
|---|---|---|
| EXCELLENT_BUY | ≥ +20%, 7d volume ≥ 50 | 0 |
| GOOD_BUY | ≥ +10%, 7d volume ≥ 50 | 0 |
| GOOD_BUY_LOW_VOL | ≥ +10%, 7d volume < 50 | 0 |
| MARGINAL_PROFIT | +5% to +10% | 3 |
| BREAKEVEN | 0% to +5% | 2 |
| SMALL_LOSS | -10% to 0% | 17 |
| NO_STEAM_DATA | Missing / unlisted | 1 |
| **Total** | | **23** |

## Quickstart
Compatible with Python 3.10–3.12:

```bash
git clone https://github.com/thekogit/skin-market-scanner.git
cd skin-market-scanner
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Tests
Run the test suite:

```bash
pytest -q
```

## Limitations
- Steam proceeds are credited as Steam Wallet funds and cannot be withdrawn directly to fiat currency.
- Valve trade holds (7-day or 14-day hold periods) expose inventory to price fluctuations before items can be liquidated.
- Relies on unauthenticated Steam Community Market price overview endpoints subject to dynamic rate throttling.
- Prices fluctuate continuously; spreads observed during a scan may diverge prior to trade execution.

## How I used AI
I used Antigravity to draft parts of the code. I chose the design, reviewed every change, replaced the inaccurate fee calculation with an exact integer-cent fee algorithm matching Valve's fee mechanics, cleaned the repository of untracked build artifacts, and wrote the test suite in `tests/` to verify fee maths and classifications. Developed through feature branches and 7 merged PRs; agent-made commits are visible in the git history.

## License
MIT License. See [LICENSE](LICENSE) for details.
