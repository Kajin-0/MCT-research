#!/usr/bin/env python3
"""Build deterministic Semiconductor Science and Technology submission assets.

The builder keeps the scientific manuscript in its controlled Markdown form,
injects citations through an explicit anchor manifest, converts the deterministic
SVG figures to journal-preferred vector PDF, creates named and double-anonymous
LaTeX variants, optionally compiles review PDFs, and emits checksum-controlled
source archives.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import textwrap
from typing import Any, Iterable
import zipfile

from tools.build_distributional_band_edge_manuscript_assets import (
    FIGURE_FILES,
    TABLE_FILES,
    build as build_manuscript_assets,
)

MANUSCRIPT_RELATIVE = Path("manuscript/distributional_band_edge/manuscript_draft.md")
REFERENCES_RELATIVE = Path(
    "manuscript/distributional_band_edge/references_verified.json"
)
METADATA_RELATIVE = Path(
    "manuscript/distributional_band_edge/journal_submission/submission_metadata.json"
)
CITATION_ANCHORS_RELATIVE = Path(
    "manuscript/distributional_band_edge/journal_submission/citation_anchors.json"
)
POSITIONING_RELATIVE = Path(
    "manuscript/distributional_band_edge/journal_submission/semiconductor_science_and_technology.md"
)

FIGURE_CAPTIONS = {
    "figure1_forward_hierarchy.svg": (
        "Forward hierarchy from latent signed gap to reported observable and the "
        "evidence classes used throughout the study."
    ),
    "figure2_transition_distribution.svg": (
        "Model-conditioned near-critical transition distributions, crossing "
        "probabilities, and local-approximation error."
    ),
    "figure3_herrmann_tail_nonuniqueness.svg": (
        "Source-conditioned Gaussian-gap convolution and fit-window dependence "
        "of the apparent exponential-tail energy."
    ),
    "figure4_chang_cutoff_rank.svg": (
        "Effective-thickness-dependent cutoff and structural-rank diagnostics "
        "for the source-bounded Chang operator."
    ),
    "figure5_carrier_filling.svg": (
        "Parabolic and nonparabolic carrier-filling sensitivity and density-series "
        "conditioning for the declared illustrative parameters."
    ),
    "figure6_unified_structural_rank.svg": (
        "Exact spectral equivalence, singular values, and structural null "
        "directions of the declared unified spectrum model."
    ),
    "figure7_measurement_design.svg": (
        "Independent information required to remove the model-specific null "
        "directions and the present external-validation boundary."
    ),
}

FIGURE_AFTER_HEADING = {
    "2. Forward hierarchy": "figure1_forward_hierarchy.svg",
    "4.1 Composition distributions broaden and censor the apparent transition": "figure2_transition_distribution.svg",
    "4.2 A Gaussian gap distribution produces an apparent tail but not a unique inverse width": "figure3_herrmann_tail_nonuniqueness.svg",
    "4.3 Tail-only cutoff data identify at most two combinations": "figure4_chang_cutoff_rank.svg",
    "4.4 Nonparabolic carrier filling can be a large correction": "figure5_carrier_filling.svg",
    "4.6 The declared distributed spectrum has three identifiable combinations": "figure6_unified_structural_rank.svg",
    "5.3 Minimum independent information": "figure7_measurement_design.svg",
}

TABLE_TITLES = {
    "table1_theorem_summary.md": "Exact statements and evidence classes",
    "table2_quantitative_results.md": "Controlled quantitative headline results",
    "table3_claim_provenance.md": "Claim provenance and validation status",
}

FORBIDDEN_ANONYMOUS_DEFAULTS = ("Terence Fisher", "Brooks Photonics", "Florida, USA", "Kajin-0")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _portable_name(path: Path) -> bool:
    return re.fullmatch(r"[A-Za-z0-9_./-]+", path.as_posix()) is not None and " " not in path.as_posix()


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stdout}"
        )


def _latex_escape_plain(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in text)


def _normalize_unicode(text: str) -> str:
    replacements = {
        "–": "--",
        "—": "---",
        "−": "-",
        "“": "``",
        "”": "''",
        "‘": "`",
        "’": "'",
        "µ": r"\ensuremath{\mu}",
        "μ": r"\ensuremath{\mu}",
        "≤": r"\ensuremath{\leq}",
        "≥": r"\ensuremath{\geq}",
        "×": r"\ensuremath{\times}",
        "±": r"\ensuremath{\pm}",
        "Å": r"\AA{}",
        "å": r"\aa{}",
        "√": r"\ensuremath{\sqrt{\ }}",
        " ": " ",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def _inline_to_latex(text: str) -> str:
    tokens: dict[str, str] = {}

    def protect(value: str) -> str:
        token = f"@@TOKEN{len(tokens):04d}@@"
        tokens[token] = value
        return token

    citation_pattern = re.compile(r"\[@([A-Za-z0-9_]+(?:;@[A-Za-z0-9_]+)*)\]")

    def citation_replacement(match: re.Match[str]) -> str:
        keys = match.group(1).replace(";@", ",")
        return protect(rf"\cite{{{keys}}}")

    text = citation_pattern.sub(citation_replacement, text)

    inline_math_pattern = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)")
    text = inline_math_pattern.sub(lambda match: protect(f"${match.group(1)}$"), text)

    text = re.sub(
        r"`([^`]+)`",
        lambda match: protect(r"\texttt{" + _latex_escape_plain(match.group(1)) + "}"),
        text,
    )
    text = re.sub(
        r"\*\*([^*]+)\*\*",
        lambda match: protect(r"\textbf{" + _latex_escape_plain(match.group(1)) + "}"),
        text,
    )

    text = _normalize_unicode(text)
    text = _latex_escape_plain(text)
    for token, replacement in tokens.items():
        text = text.replace(_latex_escape_plain(token), replacement)
    return text


def _strip_heading_number(text: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", text).strip()


def _inject_citations(
    markdown: str,
    anchor_manifest: dict[str, Any],
    reference_keys: set[str],
) -> tuple[str, set[str]]:
    cited: set[str] = set()
    for anchor in anchor_manifest["anchors"]:
        needle = str(anchor["needle"])
        count = markdown.count(needle)
        if count != 1:
            raise ValueError(f"citation anchor must match exactly once: {needle!r}, found {count}")
        keys = [str(key) for key in anchor.get("citation_keys", [])]
        append_text = str(anchor.get("append_text", ""))
        append_keys = [str(key) for key in anchor.get("append_citation_keys", [])]
        unknown = (set(keys) | set(append_keys)) - reference_keys
        if unknown:
            raise ValueError(f"unknown citation keys for anchor {needle!r}: {sorted(unknown)}")
        replacement = needle
        if keys:
            replacement += " [@" + ";@".join(keys) + "]"
            cited.update(keys)
        if append_text:
            replacement += append_text
        if append_keys:
            replacement += " [@" + ";@".join(append_keys) + "]"
            cited.update(append_keys)
        markdown = markdown.replace(needle, replacement, 1)
    if anchor_manifest["requirements"].get("every_verified_reference_must_be_cited"):
        missing = reference_keys - cited
        if missing:
            raise ValueError(f"verified references lack citation anchors: {sorted(missing)}")
    return markdown, cited


def _markdown_table_to_latex(lines: list[str], *, title: str | None = None) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        raise ValueError("markdown table requires header and separator")
    header = rows[0]
    body = rows[2:]
    columns = len(header)
    if any(len(row) != columns for row in body):
        raise ValueError("inconsistent markdown table column count")

    if columns == 2:
        widths = [0.35, 0.59]
    elif columns == 3:
        widths = [0.22, 0.28, 0.44]
    elif columns == 4:
        widths = [0.12, 0.25, 0.24, 0.33]
    elif columns == 5:
        widths = [0.08, 0.20, 0.22, 0.22, 0.20]
    else:
        widths = [0.92 / columns] * columns
    spec = "@{}" + "".join(f"p{{{width:.3f}\\linewidth}}" for width in widths) + "@{}"

    output = [r"\begingroup", r"\scriptsize", rf"\begin{{longtable}}{{{spec}}}"]
    if title:
        output.append(rf"\caption{{{_inline_to_latex(title)}}}\\")
    output.append(r"\toprule")
    output.append(" & ".join(rf"\textbf{{{_inline_to_latex(cell)}}}" for cell in header) + r" \\")
    output.append(r"\midrule")
    output.append(r"\endfirsthead")
    output.append(r"\toprule")
    output.append(" & ".join(rf"\textbf{{{_inline_to_latex(cell)}}}" for cell in header) + r" \\")
    output.append(r"\midrule")
    output.append(r"\endhead")
    for row in body:
        output.append(" & ".join(_inline_to_latex(cell) for cell in row) + r" \\")
    output.extend([r"\bottomrule", r"\end{longtable}", r"\endgroup"])
    return "\n".join(output)


def _figure_latex(svg_name: str) -> str:
    pdf_name = Path(svg_name).with_suffix(".pdf").name
    label = Path(svg_name).stem.replace("_", ":")
    caption = FIGURE_CAPTIONS[svg_name]
    return "\n".join(
        [
            r"\begin{figure}[p]",
            r"\centering",
            rf"\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{{figures/{pdf_name}}}",
            rf"\caption{{{_inline_to_latex(caption)}}}",
            rf"\label{{fig:{label}}}",
            r"\end{figure}",
            r"\clearpage",
        ]
    )


def _markdown_to_latex(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    index = 0
    in_abstract = False

    def close_abstract() -> None:
        nonlocal in_abstract
        if in_abstract:
            output.append(r"\end{abstract}")
            in_abstract = False

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            output.append("")
            index += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            index += 1
            block: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                block.append(lines[index])
                index += 1
            if index >= len(lines):
                raise ValueError("unterminated fenced code block")
            index += 1
            output.extend([r"\begin{verbatim}", *block, r"\end{verbatim}"])
            continue

        if stripped == "$$":
            index += 1
            math_lines: list[str] = []
            while index < len(lines) and lines[index].strip() != "$$":
                math_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise ValueError("unterminated display-math block")
            index += 1
            output.extend([r"\[", *math_lines, r"\]"])
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            heading = stripped[level:].strip()
            if level == 1:
                index += 1
                continue
            if level == 2 and heading == "Abstract":
                close_abstract()
                output.append(r"\begin{abstract}")
                in_abstract = True
                index += 1
                continue
            close_abstract()
            clean = _strip_heading_number(heading)
            command = {2: "section", 3: "subsection", 4: "subsubsection"}.get(level, "paragraph")
            output.append(rf"\{command}{{{_inline_to_latex(clean)}}}")
            if heading in FIGURE_AFTER_HEADING:
                output.append(_figure_latex(FIGURE_AFTER_HEADING[heading]))
            index += 1
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and re.match(
            r"^\s*\|?\s*:?-+", lines[index + 1]
        ):
            table_lines = [line, lines[index + 1]]
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            output.append(_markdown_table_to_latex(table_lines))
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            output.extend(
                [
                    r"\begin{quote}\itshape",
                    _inline_to_latex(" ".join(quote_lines)),
                    r"\end{quote}",
                ]
            )
            continue

        if re.match(r"^[-*]\s+", stripped):
            items: list[str] = []
            while index < len(lines) and re.match(r"^\s*[-*]\s+", lines[index]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[index]).strip())
                index += 1
            output.append(r"\begin{itemize}")
            output.extend(rf"\item {_inline_to_latex(item)}" for item in items)
            output.append(r"\end{itemize}")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while index < len(lines) and re.match(r"^\s*\d+\.\s+", lines[index]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[index]).strip())
                index += 1
            output.append(r"\begin{enumerate}")
            output.extend(rf"\item {_inline_to_latex(item)}" for item in items)
            output.append(r"\end{enumerate}")
            continue

        paragraph = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate:
                break
            if candidate.startswith(("#", "```", "$$", ">", "|")):
                break
            if re.match(r"^[-*]\s+", candidate) or re.match(r"^\d+\.\s+", candidate):
                break
            paragraph.append(candidate)
            index += 1
        output.append(_inline_to_latex(" ".join(paragraph)))

    close_abstract()
    return "\n".join(output).strip() + "\n"


def _author_to_bibtex(author: str) -> str:
    if author == "International Union of Pure and Applied Chemistry":
        return "{International Union of Pure and Applied Chemistry}"
    parts = author.split()
    if len(parts) < 2:
        return author
    return f"{' '.join(parts[:-1])}, {parts[-1]}"


def _escape_bibtex(text: str) -> str:
    replacements = {
        "Å": r"{\AA}",
        "å": r"{\aa}",
        "ö": r"{\"o}",
        "é": r"{\'e}",
        "ä": r"{\"a}",
        "ü": r"{\"u}",
        "í": r"{\'i}",
        "–": "--",
        "−": "-",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def _generate_bibtex(references: list[dict[str, Any]]) -> str:
    entries: list[str] = []
    for reference in references:
        entry_type = "misc" if reference["key"] == "iupac_beer_lambert_2025" else "article"
        fields = {
            "author": " and ".join(
                _author_to_bibtex(_escape_bibtex(str(author)))
                for author in reference["authors"]
            ),
            "title": "{" + _escape_bibtex(str(reference["title"])) + "}",
            "year": str(reference["year"]),
            "doi": str(reference["doi"]),
        }
        if entry_type == "article":
            fields["journal"] = _escape_bibtex(str(reference["journal"]))
            if reference.get("volume"):
                fields["volume"] = str(reference["volume"])
            if reference.get("issue"):
                fields["number"] = str(reference["issue"])
            if reference.get("pages"):
                fields["pages"] = str(reference["pages"]).replace("-", "--")
            if reference.get("article_number"):
                fields["pages"] = str(reference["article_number"])
        else:
            fields["howpublished"] = _escape_bibtex(str(reference["journal"]))
        lines = [f"@{entry_type}{{{reference['key']},"]
        for key, value in fields.items():
            lines.append(f"  {key} = {{{value}}},")
        lines.append("}")
        entries.append("\n".join(lines))
    return "\n\n".join(entries) + "\n"


def _reference_to_latex(reference: dict[str, Any]) -> str:
    authors = [str(author) for author in reference["authors"]]
    if len(authors) == 1:
        author_text = authors[0]
    elif len(authors) == 2:
        author_text = f"{authors[0]} and {authors[1]}"
    else:
        author_text = ", ".join(authors[:-1]) + f" and {authors[-1]}"
    pieces = [
        _inline_to_latex(author_text),
        str(reference["year"]),
        _inline_to_latex(str(reference["title"])),
        rf"\textit{{{_inline_to_latex(str(reference['journal']))}}}",
    ]
    if reference.get("volume"):
        pieces.append(rf"\textbf{{{_inline_to_latex(str(reference['volume']))}}}")
    locator = reference.get("pages") or reference.get("article_number")
    if locator:
        pieces.append(_inline_to_latex(str(locator)))
    doi = str(reference["doi"])
    pieces.append(rf"\href{{https://doi.org/{doi}}}{{doi:{_latex_escape_plain(doi)}}}")
    return " ".join(pieces)


def _generate_references_tex(references: list[dict[str, Any]]) -> str:
    lines = [r"\begin{thebibliography}{99}"]
    for reference in references:
        lines.append(rf"\bibitem{{{reference['key']}}} {_reference_to_latex(reference)}.")
    lines.append(r"\end{thebibliography}")
    return "\n".join(lines) + "\n"


def _preamble(*, title: str, author_block: str, pdf_author: str) -> str:
    return textwrap.dedent(
        rf"""
        \documentclass[12pt]{{article}}
        \usepackage[letterpaper,margin=1in]{{geometry}}
        \usepackage[T1]{{fontenc}}
        \usepackage[utf8]{{inputenc}}
        \usepackage{{mathptmx}}
        \usepackage{{amsmath,amssymb}}
        \usepackage{{graphicx}}
        \usepackage{{booktabs,longtable,array}}
        \usepackage{{microtype}}
        \usepackage{{caption}}
        \usepackage[hidelinks]{{hyperref}}
        \setlength{{\parindent}}{{0pt}}
        \setlength{{\parskip}}{{0.65em}}
        \setlength{{\LTpre}}{{0.5em}}
        \setlength{{\LTpost}}{{0.5em}}
        \captionsetup{{font=small,labelfont=bf}}
        \renewcommand{{\arraystretch}}{{1.15}}
        \ifdefined\pdfinfoomitdate\pdfinfoomitdate=1\fi
        \ifdefined\pdftrailerid\pdftrailerid{{}}\fi
        \ifdefined\pdfsuppressptexinfo\pdfsuppressptexinfo=-1\fi
        \hypersetup{{pdftitle={{{_latex_escape_plain(title)}}},pdfauthor={{{_latex_escape_plain(pdf_author)}}}}}
        \title{{{_latex_escape_plain(title)}}}
        {author_block}
        \date{{}}
        \begin{{document}}
        \maketitle
        """
    ).strip() + "\n"


def _back_matter(metadata: dict[str, Any], *, anonymous: bool) -> str:
    if anonymous:
        data_statement = metadata["data_availability"]["anonymous"]
        return "\n".join(
            [
                r"\section*{Data availability}",
                _inline_to_latex(str(data_statement)),
                r"\section*{Code availability}",
                _inline_to_latex(
                    "The analysis code and deterministic build workflow will be supplied through the archived repository identified at revision."
                ),
            ]
        )

    funding = metadata["funding"]
    funding_statement = funding.get("statement") or (
        "Funding statement requires final author confirmation before submission."
    )
    credit = "; ".join(metadata["credit_roles"]) + "."
    return "\n".join(
        [
            r"\section*{Author contributions}",
            _inline_to_latex(credit),
            r"\section*{Funding}",
            _inline_to_latex(str(funding_statement)),
            r"\section*{Conflict of interest}",
            _inline_to_latex(str(metadata["conflict_of_interest"]["named_statement"])),
            r"\section*{Data availability}",
            _inline_to_latex(str(metadata["data_availability"]["named"])),
            r"\section*{Code availability}",
            _inline_to_latex(
                "The complete analysis implementation, tests, immutable numerical records, and deterministic figure-generation scripts will be deposited in the same DOI-issuing archive."
            ),
        ]
    )


def _append_controlled_tables(asset_dir: Path) -> str:
    output = [r"\appendix", r"\section{Controlled theorem, result, and provenance tables}"]
    for table_name in TABLE_FILES:
        path = asset_dir / table_name
        lines = path.read_text(encoding="utf-8").splitlines()
        start = next((index for index, line in enumerate(lines) if line.strip().startswith("|")), None)
        if start is None:
            raise ValueError(f"no markdown table found in {path}")
        table_lines = []
        for line in lines[start:]:
            if not line.strip().startswith("|"):
                break
            table_lines.append(line)
        output.append(_markdown_table_to_latex(table_lines, title=TABLE_TITLES[table_name]))
    return "\n\n".join(output)


def _write_tex_variants(
    output_dir: Path,
    manuscript_body: str,
    metadata: dict[str, Any],
    references_tex: str,
    table_appendix: str,
) -> tuple[Path, Path]:
    title = str(metadata["title"])
    author = metadata["author"]
    named_author_block = (
        r"\author{" + _latex_escape_plain(str(author["name"])) + r"\\"
        + r"\small " + _latex_escape_plain(str(author["affiliation"])) + ", "
        + _latex_escape_plain(str(author["location"])) + "}"
    )
    anonymous_author_block = r"\author{}"

    named_text = "\n\n".join(
        [
            _preamble(title=title, author_block=named_author_block, pdf_author=str(author["name"])),
            manuscript_body,
            table_appendix,
            _back_matter(metadata, anonymous=False),
            references_tex,
            r"\end{document}",
        ]
    )
    anonymous_text = "\n\n".join(
        [
            _preamble(title=title, author_block=anonymous_author_block, pdf_author=""),
            manuscript_body,
            table_appendix,
            _back_matter(metadata, anonymous=True),
            references_tex,
            r"\end{document}",
        ]
    )

    named_path = output_dir / "manuscript_named.tex"
    anonymous_path = output_dir / "manuscript_anonymous.tex"
    named_path.write_text(named_text, encoding="utf-8")
    anonymous_path.write_text(anonymous_text, encoding="utf-8")
    return named_path, anonymous_path


def _convert_figures(asset_dir: Path, figure_dir: Path, *, require_tools: bool) -> list[Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)
    converted = []
    converter = shutil.which("rsvg-convert")
    if require_tools and converter is None:
        raise RuntimeError("rsvg-convert is required for --compile")
    for svg_name in FIGURE_FILES:
        source = asset_dir / svg_name
        target = figure_dir / Path(svg_name).with_suffix(".pdf").name
        if converter:
            _run([converter, "-f", "pdf", "-o", str(target), str(source)], cwd=figure_dir)
            converted.append(target)
        elif not require_tools:
            placeholder = figure_dir / Path(svg_name).name
            shutil.copyfile(source, placeholder)
    return converted


def _compile_tex(output_dir: Path, tex_path: Path) -> Path:
    compiler = shutil.which("pdflatex")
    if compiler is None:
        raise RuntimeError("pdflatex is required for --compile")
    environment = os.environ.copy()
    environment.update(
        {
            "SOURCE_DATE_EPOCH": "946684800",
            "FORCE_SOURCE_DATE": "1",
            "TZ": "UTC",
        }
    )
    command = [compiler, "-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    _run(command, cwd=output_dir, env=environment)
    _run(command, cwd=output_dir, env=environment)
    pdf_path = output_dir / tex_path.with_suffix(".pdf").name
    if not pdf_path.is_file() or pdf_path.stat().st_size < 10_000:
        raise RuntimeError(f"compiled PDF missing or unexpectedly small: {pdf_path}")
    return pdf_path


def _deterministic_zip(path: Path, members: Iterable[tuple[Path, str]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, archive_name in sorted(members, key=lambda item: item[1]):
            info = zipfile.ZipInfo(archive_name, date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, source.read_bytes())


def _extract_cover_letter(positioning_path: Path, metadata: dict[str, Any]) -> str:
    text = positioning_path.read_text(encoding="utf-8")
    start_marker = "## Cover-letter draft"
    end_marker = "## Data availability statement"
    if start_marker not in text or end_marker not in text:
        raise ValueError("cover-letter markers not found")
    body = text.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    body = body.replace("[Author name]", str(metadata["author"]["name"]))
    body = body.replace("[Affiliation]", f"{metadata['author']['affiliation']}, {metadata['author']['location']}")
    body = body.replace("[Correspondence email]", "CORRESPONDENCE_EMAIL_PENDING")
    return body + "\n"


def _scan_anonymous_text(text: str, forbidden: Iterable[str]) -> None:
    lower = text.lower()
    leaks = [token for token in forbidden if token.lower() in lower]
    if leaks:
        raise ValueError(f"anonymous identity leakage: {leaks}")


def _source_readme(metadata: dict[str, Any]) -> str:
    blockers = "\n".join(f"- {item}" for item in metadata["unresolved_submission_blockers"])
    return textwrap.dedent(
        f"""
        SST INITIAL-SUBMISSION BUNDLE

        Journal: {metadata['journal']}
        Article type: {metadata['article_type']}
        Title: {metadata['title']}

        Generated files:
        - manuscript_named.pdf / manuscript_named.tex
        - manuscript_anonymous.pdf / manuscript_anonymous.tex
        - references.tex and references.bib
        - vector PDF figures under figures/
        - named and anonymous deterministic source ZIP archives
        - cover_letter_named.txt
        - submission_manifest.json

        Unresolved human metadata:
        {blockers}

        The anonymous source ZIP intentionally excludes all named metadata files.
        The archive DOI placeholder is not an issued DOI and must be replaced before final submission.
        """
    ).strip() + "\n"


def build(
    repository_root: str | Path,
    output_dir: str | Path,
    *,
    compile_pdf: bool = False,
    commit_sha: str = "unknown",
) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    output = Path(output_dir).resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    metadata = _load_json(root / METADATA_RELATIVE)
    reference_manifest = _load_json(root / REFERENCES_RELATIVE)
    citation_manifest = _load_json(root / CITATION_ANCHORS_RELATIVE)
    references = list(reference_manifest["references"])
    reference_keys = {str(reference["key"]) for reference in references}

    manuscript_markdown = (root / MANUSCRIPT_RELATIVE).read_text(encoding="utf-8")
    manuscript_markdown, cited = _inject_citations(
        manuscript_markdown, citation_manifest, reference_keys
    )
    if cited != reference_keys:
        raise ValueError("citation coverage differs from verified reference set")

    asset_dir = output / "generated_assets"
    asset_summary = build_manuscript_assets(root, asset_dir)
    figure_dir = output / "figures"
    converted_figures = _convert_figures(asset_dir, figure_dir, require_tools=compile_pdf)

    body = _markdown_to_latex(manuscript_markdown)
    table_appendix = _append_controlled_tables(asset_dir)
    references_tex = _generate_references_tex(references)
    references_bib = _generate_bibtex(references)
    (output / "references.tex").write_text(references_tex, encoding="utf-8")
    (output / "references.bib").write_text(references_bib, encoding="utf-8")

    named_tex, anonymous_tex = _write_tex_variants(
        output, body, metadata, references_tex, table_appendix
    )
    _scan_anonymous_text(
        anonymous_tex.read_text(encoding="utf-8"),
        metadata["identity_boundary"].get(
            "forbidden_anonymous_tokens", FORBIDDEN_ANONYMOUS_DEFAULTS
        ),
    )

    named_pdf: Path | None = None
    anonymous_pdf: Path | None = None
    if compile_pdf:
        named_pdf = _compile_tex(output, named_tex)
        anonymous_pdf = _compile_tex(output, anonymous_tex)
        pdftotext = shutil.which("pdftotext")
        if pdftotext:
            anonymous_text_path = output / "manuscript_anonymous.txt"
            _run(
                [pdftotext, str(anonymous_pdf), str(anonymous_text_path)],
                cwd=output,
            )
            _scan_anonymous_text(
                anonymous_text_path.read_text(encoding="utf-8", errors="replace"),
                metadata["identity_boundary"].get(
                    "forbidden_anonymous_tokens", FORBIDDEN_ANONYMOUS_DEFAULTS
                ),
            )

    cover_letter = _extract_cover_letter(root / POSITIONING_RELATIVE, metadata)
    (output / "cover_letter_named.txt").write_text(cover_letter, encoding="utf-8")
    (output / "submission_README.txt").write_text(
        _source_readme(metadata), encoding="utf-8"
    )
    (output / "unresolved_metadata.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "unresolved": metadata["unresolved_submission_blockers"],
                "archive_doi_issued": False,
                "submission_ready": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    named_members: list[tuple[Path, str]] = [
        (named_tex, "manuscript_named.tex"),
        (output / "references.tex", "references.tex"),
        (output / "references.bib", "references.bib"),
        (output / "submission_README.txt", "README.txt"),
    ]
    anonymous_members: list[tuple[Path, str]] = [
        (anonymous_tex, "manuscript_anonymous.tex"),
        (output / "references.tex", "references.tex"),
        (output / "references.bib", "references.bib"),
    ]
    for figure in converted_figures:
        named_members.append((figure, f"figures/{figure.name}"))
        anonymous_members.append((figure, f"figures/{figure.name}"))
    if named_pdf:
        named_members.append((named_pdf, "manuscript_named.pdf"))
    if anonymous_pdf:
        anonymous_members.append((anonymous_pdf, "manuscript_anonymous.pdf"))

    named_zip = output / "sst_named_source.zip"
    anonymous_zip = output / "sst_anonymous_source.zip"
    _deterministic_zip(named_zip, named_members)
    _deterministic_zip(anonymous_zip, anonymous_members)

    with zipfile.ZipFile(anonymous_zip) as archive:
        for name in archive.namelist():
            if name.endswith((".tex", ".txt", ".bib")):
                _scan_anonymous_text(
                    archive.read(name).decode("utf-8", errors="replace"),
                    metadata["identity_boundary"].get(
                        "forbidden_anonymous_tokens", FORBIDDEN_ANONYMOUS_DEFAULTS
                    ),
                )

    files = [path for path in output.rglob("*") if path.is_file()]
    manifest_entries = []
    for path in sorted(files):
        relative = path.relative_to(output)
        if relative.name == "submission_manifest.json":
            continue
        if not _portable_name(relative):
            raise ValueError(f"non-portable output filename: {relative}")
        manifest_entries.append(
            {
                "path": relative.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )

    manifest = {
        "schema_version": "1.0",
        "program_issue": 193,
        "journal": metadata["journal"],
        "article_type": metadata["article_type"],
        "commit_sha": commit_sha,
        "compiled": compile_pdf,
        "review_variants": metadata["review_variants"],
        "verified_reference_count": len(references),
        "cited_reference_count": len(cited),
        "figure_count": len(FIGURE_FILES),
        "table_count": len(TABLE_FILES),
        "asset_summary": asset_summary,
        "unresolved_submission_blockers": metadata["unresolved_submission_blockers"],
        "archive_doi_issued": False,
        "files": manifest_entries,
    }
    (output / "submission_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--compile", action="store_true", dest="compile_pdf")
    parser.add_argument("--commit-sha", default="unknown")
    args = parser.parse_args()
    result = build(
        args.repository_root,
        args.output_dir,
        compile_pdf=args.compile_pdf,
        commit_sha=args.commit_sha,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
