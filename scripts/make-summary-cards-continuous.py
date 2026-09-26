from pathlib import Path


SOURCE = Path("profile-summary-card-output/github_dark")
DIST = Path("dist")


STYLE = """
<style id="lostparadise-continuous-animation">
  @media (prefers-reduced-motion: no-preference) {
    * {
      animation-iteration-count: infinite !important;
    }
  }
</style>
"""


CARD_PATTERNS = {
    "profile-details.svg": "*profile-details*.svg",
    "stats.svg": "*stats*.svg",
    "repos-per-language.svg": "*repos-per-language*.svg",
    "most-commit-language.svg": "*most-commit-language*.svg",
    "productive-time.svg": "*productive-time*.svg",
}


def find_card(pattern: str) -> Path:
    matches = sorted(SOURCE.glob(pattern))

    if not matches:
        raise FileNotFoundError(
            f"No generated card matched {pattern!r} in {SOURCE}"
        )

    return matches[0]


def inject_continuous_animation(svg: str) -> str:
    if "lostparadise-continuous-animation" in svg:
        return svg

    marker = "</svg>"

    if marker not in svg:
        raise ValueError("Generated file is not a valid SVG document.")

    return svg.replace(
        marker,
        STYLE + "\n" + marker,
        1,
    )


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Missing generated card directory: {SOURCE}"
        )

    DIST.mkdir(
        parents=True,
        exist_ok=True,
    )

    for output_name, pattern in CARD_PATTERNS.items():

        source = find_card(pattern)

        svg = source.read_text(
            encoding="utf-8"
        )

        svg = inject_continuous_animation(svg)

        destination = DIST / output_name

        destination.write_text(
            svg,
            encoding="utf-8",
        )

        print(
            f"Created {destination}"
        )


if __name__ == "__main__":
    main()
