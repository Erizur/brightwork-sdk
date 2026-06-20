# My new addon
Update this if needed!

# Installation instructions
- On the add-ons manager, go to the brightwork section and install the package after building it or downloading it.
- You can do this by using the cog icon on the top and pressing the Brightwork-related options.
- If nothing failed, activate it and restart your browser!
- enjoi.

# Building the omni.ja
You need atleast **Python 3.12** installed on your system.
To build the addon, run the following command:
```python
# Optional values:
# --out (path) - Define a custom output directory. default is the dist folder that will get created in your repo.
# --metadata (path/to/metadata.json) - Define a custom metadata builder. useful if you want to write different metadata for specific versions of your package.
# --platform (win,linux) - Define whether to build for a windows or linux only environment. Rewrites the platform check in metadata.json.
# --fast - Allow to build an uncompressed (skips deflate) omni.ja for faster compilation times. This should only be used when developing addons, and not used when deploying an actual release due to its uncompressed size.

python build.py
```

