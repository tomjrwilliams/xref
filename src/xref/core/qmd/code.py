from __future__ import annotations


# ------------------------------------


def _indent(code: str, n=1):
    return "\n".join(
        [("    " * n) + l for l in code.split("\n")]
    )


def qmd_print_error(
    filter_ends_with: list[str] = [],
    filter_starts_with: list[str] = [],
):
    filts = [
        f"""not l.strip().startswith('{s}')"""
        for s in filter_starts_with
    ] + [
        f"""not l.strip().endswith('{s}')"""
        for s in filter_ends_with
    ]
    return _indent(
        "\n".join(
            [
                "if error:",
                """    ls = tb.split("\\n")""",
                """    ls = [""",
                """        l for l in ls""",
                """        if not any([""",
            ]
            + filts
            + [
                """        ])""",
                """    ]""",
                """    assert False, "\\n".join(ls)""",
            ]
        )
    )


def qmd_catch_error(
    code: str, print: bool = True, **print_kwargs
):
    return _indent(
        "\n".join(
            [
                "error = False",
                "tb = ''",
                "try:",
            ]
            + [_indent(code)]
            + [
                "except Exception:",
                "    sys.stdout.flush()",
                "    sys.stderr.flush()",
                "    error = True",
                "    tb = traceback.format_exc()",
            ]
        )
    ) + (
        "" if not print else qmd_print_error(**print_kwargs)
    )


def qmd_code_block(
    code, yml=None, catch=True, print=True, **print_kwargs
):
    return "\n".join(
        [
            "```{" + "python}",
            # "#| error: true",
            "#| warning: false",
            "#| fig-align: center",
            "#| layout-align: center",
        ]
        + ([] if yml is None else [yml])
        + [
            (
                code
                if catch is False
                else qmd_catch_error(
                    code, print=print, **print_kwargs
                )
            ),
            "```",
        ]
    )


# ------------------------------------
