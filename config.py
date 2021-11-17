import toml
import logging
import os

EXAMPLE_CONFIG = """\"token\"=\"ODg4NDUwNTIyNDg1NTEwMTY0.YUS4Bw.KeUrMZ4GEUTRJFFP5WVTR_jg7hE\" # the bot's token
\"prefix\"=\"?\" # prefix used to denote commands

[music]
# Options for the music commands
"max_volume"=250 # Max audio volume. Set to -1 for unlimited.
[hub]
#Options for the voice chat hub
"category_id"=910433640364781598 # The category where the vc are going to be created.
"hub_vc_id"=910433688578297866 # The hub id.
"""


def load_config(path="./config.toml"):
    """Loads the config from `path`"""
    if os.path.exists(path) and os.path.isfile(path):
        config = toml.load(path)
        return config
    else:
        with open(path, "w") as config:
            config.write(EXAMPLE_CONFIG)
            logging.warn(
                f"No config file found. Creating a default config file at {path}"
            )
        return load_config(path=path)
