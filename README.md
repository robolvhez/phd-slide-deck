# PhD Slide Deck: Genomic Association Studies in Mexicans

This repository contains the LaTeX source code and assets for the Beamer presentation: **"Estudios de Asociación Genómica libres de sesgos poblacionales para rasgos complejos y enfermedades en más de 100 mil Mexicanos"**.

**Author:** Ing. Roberto Olvera Hernández  
**Institution:** Programa de Doctorado en Ciencias Biomédicas (PDCB) | Centro de Ciencias Genómicas (CCG) | Universidad Nacional Autónoma de México (UNAM)

This presentation is generated using a Beamer template with a custom theme and specialized code listings tailored for presentations at CCG-UNAM.

## Requirements

Ensure you have the following packages installed:

- LuaLaTeX (for compilation)
- `biblatex` with `biber` backend (for bibliography management)
- `fontspec` (for custom fonts)
- `csquotes`, `multicol`, `listings`

## Project Structure

```shell
├── img/ # Image assets
│   └── presentation-images.svg # Every PNG is generated here
│   └── ccg-logo.png
│   └── unam-logo.png
│   └── title-slide-background-wide.png # Ration 16:9
│   └── title-slide-background.png # Ration 4:3
│   # Specific for every source
│   └── section1/
│       └── file1a/
│       └── file1b/
│   └── section2/
│       └── file2a/
│       └── file2b/
├── slides/ # Directory for slides
│   └── section1/
│       └── file1a.tex
│       └── file1b.tex
│   └── section2/
│       └── file2a.tex
│       └── file2b.tex
├── bibliography.bib         # Bibliography file
├── main.tex                 # Main LaTeX source file
├── beamerthemeccgunam.sty   # Beamer custom theme
└── mycodestyle.sty          # Custom `listings` style (Catpuccin based)
```

## Compilation Instructions

1. Ensure `lualatex` is installed on your system.

2. Compile the document using the following commands:

```bash
lualatex main.tex
biber main
lualatex main.tex
lualatex main.tex
```

Alternatively, use a Makefile or an integrated LaTeX editor like [Overleaf](https://www.overleaf.com) or [TeXShop](https://pages.uoregon.edu/koch/texshop/) configured for LuaLaTeX.

## Customization

- **Aspect Ratio**: Use `\documentclass{beamer}` for 4:3 or `\documentclass[aspectratio=169]{beamer}` for 16:9.
- **Fonts**: Uses `XCharter`, `Cabin`, and `Source Code Pro`. Modify in the `\setmainfont`, `\setsansfont`, and `\setmonofont` commands.
- **Bibliography**: Managed by `biblatex` through the `bibliography.bib` file.

## Example Slide Inclusion

Add slides by placing `.tex` files in the `slides/` directory and including them with `\input{slides/dir/your_slide}`.

## Listings

Beamer does not support, by default, listings or verbatims for code, we have to include the `[fragile]` option for the environment. A frame that should work is:

```tex
\begin{frame}[fragile]{Test for code (BASH)}
  \begin{lstlisting}[language=bash]
    #!/bin/bash
    # Quick System Info and Cleanup
    echo "System Info:"; uname -a
    echo "Disk Usage:"; df -h | grep '^/dev'
    echo "Cleaning /tmp..."; sudo rm -rf /tmp/*
    echo "Updating System..."; sudo apt-get update && sudo apt-get upgrade -y
    echo "Done!"
  \end{lstlisting}
\end{frame}
```

## License

This project is intended for academic and educational use. Modify and share freely.
