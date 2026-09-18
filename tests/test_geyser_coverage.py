"""Structural coverage for the pinned Manual:Geyser revision."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "plugins/mudlet-toolbox/skills/mudlet-geyser-ui/references"
INDEX = REFERENCES / "topic-index.md"

EXPECTED_TOPICS = set("""
introduction motivation main-features assets constraints-format constraint-math
geyser-elements technical-manual
container container-create container-nesting container-negative-alignment
label label-basic label-color label-font-size label-parent label-image label-image-stretch
label-image-alignment label-show-hide label-clickable-images label-styling label-tooltip
label-tooltip-inheritance label-content-alignment label-wordwrap label-hover label-checkboxes
label-sprites label-whitespace label-transparency label-cursor label-flyouts label-flyout-demo
label-flyout-layouts label-right-click-menu label-menu-style label-menu-action label-menu-access
label-menu-example label-menu-existing-click label-name
stylesheet stylesheet-basic stylesheet-css stylesheet-target stylesheet-set stylesheet-get
stylesheet-table-get stylesheet-table-set stylesheet-reset stylesheet-inheritance
miniconsole miniconsole-text miniconsole-copy-color miniconsole-clear miniconsole-edit
miniconsole-gag miniconsole-clickable miniconsole-background miniconsole-commandline
miniconsole-command-action
gauge gauge-update gauge-style gauge-orientation gauge-colors gauge-click gauge-tooltip
hbox-vbox
userwindow userwindow-floating userwindow-docked userwindow-autodock userwindow-style
userwindow-container
commandline commandline-create commandline-action commandline-style commandline-extra
adjustable adjustable-create adjustable-key-functions adjustable-constraints adjustable-title
adjustable-autosave adjustable-all adjustable-custom-storage adjustable-custom-directory
adjustable-custom-slot adjustable-delete-save adjustable-menu adjustable-custom-menu
adjustable-lock-styles adjustable-style adjustable-border adjustable-frame adjustable-scrollbox
change-container mapper
tutorial tutorial-hello tutorial-containers tutorial-boxes
walkthroughs walkthrough-compass compass-assets compass-script compass-screen-size
compass-namespace compass-parent compass-style compass-grid compass-callback compass-hover
compass-grid-styles compass-resize
walkthrough-tabs tabs-script tabs-namespace tabs-container tabs-hbox tabs-label tabs-windows
tabs-callback tabs-content walkthrough-resize-label
""".split())


class GeyserCoverageTests(unittest.TestCase):
    def test_pinned_manual_topics_are_mapped_once(self):
        text = INDEX.read_text()
        listed = []
        for group in re.findall(r"<!-- geyser-topics: ([a-z0-9 -]+) -->", text):
            listed.extend(group.split())
        self.assertEqual(len(listed), len(set(listed)), "duplicate Geyser topic identifiers")
        self.assertEqual(set(listed), EXPECTED_TOPICS)

    def test_index_local_links_resolve_and_live_manual_is_canonical(self):
        text = INDEX.read_text()
        self.assertIn("https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser", text)
        links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
        local = [link for link in links if "://" not in link and not link.startswith("#")]
        self.assertGreaterEqual(len(local), 20)
        for link in local:
            target = (INDEX.parent / link.split("#", 1)[0]).resolve()
            self.assertTrue(target.is_file(), link)
            self.assertTrue(target.is_relative_to(REFERENCES), link)


if __name__ == "__main__":
    unittest.main()
