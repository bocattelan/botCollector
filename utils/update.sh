#!/usr/bin/env bash

statistics=$(Rscript ././plots/plot.r)

bash writeRedame.sh ${statistics} > "README.md"

git add ././plots/plot.pdf
git add ././plots/plot.png
git commit -m "updating plot"

git add README.md
git commit -m "updating README.md"

git push