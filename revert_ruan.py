import sys

with open("slides/introduction.tex", "r") as f:
    content = f.read()

# Revert image
new_content = content.replace("img/diagrams/marnetto2020-pipeline.png", "img/diagrams/ruan2022-prs-csx.png")

# Revert citations and text
new_content = new_content.replace(r"\parencite{marnetto2020-ancestry}", r"\parencite{ruan2022-prs}")

with open("slides/introduction.tex", "w") as f:
    f.write(new_content)
