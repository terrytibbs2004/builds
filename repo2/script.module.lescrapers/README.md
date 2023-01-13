## How to Import LE Scrapers Into Any Addon

Any multi-source Kodi addon can be altered to use these new scrapers instead of its own, you can follow the
instructions below to get things updated. When applying to a different addon, change "name_of_addon" with the name
of the addon.

Open the `addons/plugin.video.name_of_addon/addon.xml`.

Add the following line to the addon.xml file:

`<import addon=”script.module.lescrapers/>`

Open addons/script.module.name_of_addon/lib/resources/lib/modules/sources.py

Add the following line to the `sources.py` file:

`import lescrapers`

Add it right after the line that says:

`import re

You will also need to change a few lines in the def `getConstants(self)` function in `sources.py` file:

Find the line that says:

`from resources.lib.sources import sources`

Comment out that line by adding a pound/hashtag at the beginning like this:

`#from resources.lib.sources import sources`

add the following:

`from lescrapers import sources`

Enjoy!
