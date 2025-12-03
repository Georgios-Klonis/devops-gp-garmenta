from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

# Helpers for building the LLM prompt used by TicketFinderService.

DEFAULT_VENDORS: List[str] = [
    "Ticketmaster",
    "SeeTickets",
    "AXS",
    "StubHub",
    "SeatGeek",
    "Viagogo",
    "official club site",
]


def render_prompt(
    team_1: str,
    team_2: str = "",
    date_from: str | None = None,
    date_to: str | None = None,
    price_from: str = "",
    price_to: str = "",
    preferred_vendors: str | List[str] | None = None,
) -> str:
    """Render the ticket search prompt using the shared template."""
    today = datetime.now(timezone.utc).date()
    default_date_from = today.isoformat()
    default_date_to = (today + timedelta(days=60)).isoformat()

    date_from = date_from if date_from is not None else default_date_from
    date_to = date_to if date_to is not None else default_date_to

    if preferred_vendors:
        if isinstance(preferred_vendors, str):
            vendors_list = [v.strip() for v in preferred_vendors.split(",") if v.strip()]
        else:
            vendors_list = [v for v in preferred_vendors if v]
    else:
        vendors_list = DEFAULT_VENDORS

    prompt_path = Path(__file__).resolve().parent.parent / "resources" / "prompt.txt"
    prompt_template = prompt_path.read_text()
    prompt_filled = prompt_template.replace("<VENDOR_LIST>", ", ".join(vendors_list))

    input_block = "\n".join([
        f"{team_1}, {team_2 or ''}",
        f"{date_from} - {date_to}",
        f"{price_from} - {price_to}",
    ])

    return f"{input_block}\n\n{prompt_filled}"
