
import io
import yaml

def header_defaults(hide_code=False):
    res = {
        "page-layout": "full",
        "format": {
            "html": {
                "toc": True,
                "number-sections": True,
                "self-contained": True,
            },
        }
    }
    if not hide_code:
        res["format"]["html"]["code-fold"] = True
    else:
        res["format"]["html"]["echo"] = False
    return res

def qmd_header(
    yml: dict,
    hide_code=False,
):
    yml = {
        **yml,
        **header_defaults(hide_code=hide_code)
    }
    with io.StringIO() as f:
        yaml.dump(yml, f, default_flow_style=False)
        s = f.getvalue()
    return "\n".join([
        "---",
        s,
        "---",
    ])