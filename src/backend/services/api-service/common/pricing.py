from __future__ import annotations

from typing import Dict, List

from app.schemas import Currency, Event, TicketListing


def convert_currency(amount: float, source: Currency, target: Currency, rates: Dict[Currency, float]) -> float:
    """Convert amount using provided rate map (relative to 1 unit)."""
    if source == target:
        return amount
    source_rate = rates.get(source, 1.0)
    target_rate = rates.get(target, 1.0)
    return amount * (source_rate / target_rate)


def mark_best_prices(events: List[Event], target_currency: Currency = Currency.USD) -> List[Event]:
    """Flag best-priced listings per event after currency normalization."""
    for event in events:
        if not event.listings:
            continue

        rates = {
            Currency.USD: 1.0,
            Currency.EUR: 1.08,
            Currency.GBP: 1.28,
        }

        normalized_prices = [
            (
                idx,
                convert_currency(listing.price.amount, listing.price.currency, target_currency, rates),
            )
            for idx, listing in enumerate(event.listings)
        ]

        best_idx, _ = min(normalized_prices, key=lambda item: item[1])
        for listing in event.listings:
            listing.is_best_price = False
        event.listings[best_idx].is_best_price = True

    return events
