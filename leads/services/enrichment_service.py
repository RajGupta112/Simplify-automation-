"""
Company Enrichment Service
Production-grade enrichment pipeline
"""

import logging
import random

from urllib.parse import urlparse

import requests

from bs4 import BeautifulSoup

from playwright.sync_api import (
    sync_playwright,
)


logger = logging.getLogger(__name__)


REQUEST_TIMEOUT = 15

MAX_CONTENT_LENGTH = 5000


USER_AGENTS = [
    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
]


class EnrichmentService:

    def __init__(self):

        self.session = (
            requests.Session()
        )

        self.session.headers.update(
            {
                "User-Agent": (
                    random.choice(
                        USER_AGENTS
                    )
                )
            }
        )

    # -------------------------
    # URL HELPERS
    # -------------------------

    def normalize_url(
        self,
        url: str
    ) -> str:

        if not url.startswith(
            (
                "http://",
                "https://"
            )
        ):

            return (
                f"https://{url}"
            )

        return url

    def get_domain(
        self,
        url: str
    ) -> str:

        return urlparse(
            url
        ).netloc

    # -------------------------
    # VALIDATION
    # -------------------------

    def validate_website(
        self,
        url: str
    ) -> bool:

        try:

            response = (
                self.session.get(
                    url,
                    timeout=REQUEST_TIMEOUT
                )
            )

            return (
                response.status_code
                < 500
            )

        except Exception:

            return False

    # -------------------------
    # FETCH RAW HTML
    # -------------------------

    def fetch_html(
        self,
        url: str
    ) -> str:

        response = (
            self.session.get(
                url,
                timeout=REQUEST_TIMEOUT
            )
        )

        response.raise_for_status()

        return response.text

    # -------------------------
    # PLAYWRIGHT RENDER
    # -------------------------

    def fetch_rendered_data(
        self,
        url: str
    ) -> dict:

        logger.info(
            f"Using Playwright: "
            f"{url}"
        )

        with sync_playwright() as p:

            browser = (
                p.chromium.launch(
                    headless=True
                )
            )

            page = (
                browser.new_page()
            )

            page.goto(
                url,
                wait_until=(
                    "networkidle"
                ),
                timeout=30000
            )

            # Extract visible text
            content = (
                page.locator(
                    "body"
                ).inner_text()
            )

            # Extract rendered HTML
            html = (
                page.content()
            )

            browser.close()

            return {
                "content": content,
                "html": html,
            }

    # -------------------------
    # METADATA
    # -------------------------

    def extract_metadata(
        self,
        html: str
    ) -> dict:

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        title = ""

        description = ""

        title_tag = soup.find(
            "title"
        )

        if title_tag:

            title = (
                title_tag.text.strip()
            )

        meta_description = (
            soup.find(
                "meta",
                attrs={
                    "name": (
                        "description"
                    )
                }
            )
        )

        if meta_description:

            description = (
                meta_description.get(
                    "content",
                    ""
                )
            )

        return {
            "title": title,
            "description": (
                description
            ),
        }

    # -------------------------
    # TECHNOLOGY DETECTION
    # -------------------------

    def detect_technologies(
        self,
        html: str
    ) -> list:

        signals = {
            "React": [
                "react"
            ],
            "Next.js": [
                "_next"
            ],
            "Vue": [
                "vue"
            ],
            "Angular": [
                "angular"
            ],
            "WordPress": [
                "wp-content"
            ],
            "Shopify": [
                "shopify"
            ],
            "Tailwind": [
                "tailwind"
            ],
            "Bootstrap": [
                "bootstrap"
            ],
            "Google Analytics": [
                "gtag",
                "analytics"
            ],
        }

        html_lower = (
            html.lower()
        )

        detected = []

        for tech, keys in (
            signals.items()
        ):

            if any(
                key in html_lower
                for key in keys
            ):

                detected.append(
                    tech
                )

        return detected

    # -------------------------
    # MAIN PIPELINE
    # -------------------------

    def enrich_company(
        self,
        website_url: str
    ) -> dict:

        website_url = (
            self.normalize_url(
                website_url
            )
        )

        if not (
            self.validate_website(
                website_url
            )
        ):

            return {
                "success": False,
                "error": (
                    "Website "
                    "not accessible"
                )
            }

        try:

            logger.info(
                f"Enriching: "
                f"{website_url}"
            )

            rendered_data = (
                self.fetch_rendered_data(
                    website_url
                )
            )

            content = (
                rendered_data[
                    "content"
                ]
            )

            html = (
                rendered_data[
                    "html"
                ]
            )

            metadata = (
                self.extract_metadata(
                    html
                )
            )

            technologies = (
                self.detect_technologies(
                    html
                )
            )

            return {
                "success": True,
                "data": {
                    "website": (
                        website_url
                    ),
                    "domain": (
                        self.get_domain(
                            website_url
                        )
                    ),
                    "title": (
                        metadata[
                            "title"
                        ]
                    ),
                    "description": (
                        metadata[
                            "description"
                        ]
                    ),
                    "content": (
                        content[
                            :MAX_CONTENT_LENGTH
                        ]
                    ),
                    "technologies": (
                        technologies
                    ),
                }
            }

        except Exception as error:

            logger.error(
                f"Enrichment failed: "
                f"{error}"
            )

            return {
                "success": False,
                "error": (
                    str(error)
                )
            }


enrichment_service = (
    EnrichmentService()
)