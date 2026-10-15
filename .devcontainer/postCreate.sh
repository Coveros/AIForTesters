#!/usr/bin/env bash
set -euo pipefail

python -m ipykernel install --user --name ai-for-testers --display-name "Python (AIForTesters)"
Rscript -e 'IRkernel::installspec(user=TRUE, name="modificare-r", displayname="R (Modificare)")'

cd "$(dirname "${BASH_SOURCE[0]}")/.."
if [[ ! -e modificare ]]; then
	git clone --depth 1 https://github.com/Coveros/modificare.git modificare
fi
