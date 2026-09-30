# Profile artwork

The README is made of generated SVG panels, because GitHub can't restyle README markdown.
Edit the text in `panels.py` (the `PROJECTS` list, `mission()`, `toolkit()`, and so on) and regenerate:

```bash
python tools/panels.py assets
python tools/banner.py assets/banner.svg banner "Dominick Kubica" "Builder who sells  ·  Python  ·  LLMs  ·  GTM automation" "HELLO, WORLD" 7
```
