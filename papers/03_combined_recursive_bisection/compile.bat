@echo off
REM Compile Paper 3: Recursive Bisection with Edge-Weighted Cuts

cd /d %~dp0

echo Compiling Paper 3: Recursive Bisection with Edge-Weighted Cuts...
echo ==================================================
echo.

REM First pass
echo LaTeX pass 1/3...
pdflatex -interaction=nonstopmode recursive_bisection_with_edge_weighted_cuts.tex >nul 2>&1

REM BibTeX
echo BibTeX...
bibtex recursive_bisection_with_edge_weighted_cuts >nul 2>&1

REM Second pass
echo LaTeX pass 2/3...
pdflatex -interaction=nonstopmode recursive_bisection_with_edge_weighted_cuts.tex >nul 2>&1

REM Third pass
echo LaTeX pass 3/3...
pdflatex -interaction=nonstopmode recursive_bisection_with_edge_weighted_cuts.tex >nul 2>&1

echo.
echo Compilation complete!
echo Output: recursive_bisection_with_edge_weighted_cuts.pdf
echo.

REM Clean up auxiliary files
echo Cleaning auxiliary files...
del /Q *.aux *.log *.bbl *.blg *.out *.toc 2>nul

echo Done!
pause
