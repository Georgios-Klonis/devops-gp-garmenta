from __future__ import annotations

import logging


def configure_logging(level: str) -> None:
    """Configure basic structured logging for the service."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # Align uvicorn logs with application log level.
    logging.getLogger("uvicorn.access").setLevel(level)
    logging.getLogger("uvicorn.error").setLevel(level)
