#!/usr/bin/env python3
# Build the brightwork omni.ja pair(s) from this directory using this script.
# modify all metadata from metadata.json. ONLY USE THIS TOOL TO PACK.
# Hijacking this thing to make it do something else is not recommended
#
# Each adk-<platform>/ holds one platform's layout, and src/ is shared.
# By default every available platform is packed, producing
# dist/<platform>/omni.ja, dist/<platform>/browser/omni.ja
# plus a single dist/brightwork.json that records which platforms are present.

import argparse
import os
import sys
from dataclasses import replace

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(HERE, "tools"))
for entry in sorted(os.listdir(os.path.join(HERE, "tools"))):
    p = os.path.join(HERE, "tools", entry)
    if os.path.isdir(p):
        sys.path.insert(0, p)

from mozpack.brightwork.build import build_from_recipe  # noqa: E402
from mozpack.brightwork.token import (  # noqa: E402
    BrightworkToken,
    write_metadata_into_dir,
)


def _available_platforms():
    out = []
    for name in sorted(os.listdir(HERE)):
        if name.startswith("adk-") and os.path.isdir(os.path.join(HERE, name)):
            out.append(name[len("adk-"):])
    return out


def main():
    avail = _available_platforms()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=os.path.join(HERE, "dist"),
                    help="output directory (default: ./dist)")
    ap.add_argument("--metadata", default=os.path.join(HERE, "metadata.json"),
                    help="package metadata.json (default: ./metadata.json)")
    ap.add_argument("--platform", action="append", choices=avail or None,
                    help="platform(s) to pack; repeatable "
                         "(default: all available%s). Pack just the one you are "
                         "testing to roughly halve build time."
                         % (": " + ", ".join(avail) if avail else ""))
    ap.add_argument("--fast", action="store_true",
                    help="store the omni.ja entries uncompressed -- packs much "
                         "faster (skips deflate) at the cost of larger jars. "
                         "Ideal for local dev iteration (e.g. a symlinked dist); "
                         "the loader reads uncompressed jars fine. Compress for "
                         "release.")
    args = ap.parse_args()

    if not avail:
        sys.exit("No adk-<platform> directories found next to build.py.")
    targets = args.platform or avail

    with open(args.metadata, "rb") as fh:
        token = BrightworkToken.from_metadata_bytes(fh.read())

    src = os.path.join(HERE, "src")
    built = []
    for plat in targets:
        adk = os.path.join(HERE, "adk-" + plat)
        out = os.path.join(args.out, plat)
        gre, skipped = build_from_recipe(adk, src, out, token,
                                         compress=not args.fast,
                                         write_metadata=False)
        built.append(plat)
        print("Built", gre)
        print("Built", os.path.join(out, "browser", "omni.ja"))
        if skipped:
            print("%d resource(s) not in the source tree for %s (built only by"
                  " full packaging; usually harmless):" % (len(skipped), plat))
            for dest, _ in skipped:
                print("   ", dest)

    write_metadata_into_dir(
        args.out,
        replace(token, platforms=built),
        icon_source_dir=os.path.dirname(os.path.abspath(args.metadata)),
    )
    print("Wrote", os.path.join(args.out, "brightwork.json"),
          "(platforms: %s)" % ", ".join(built))


if __name__ == "__main__":
    main()
