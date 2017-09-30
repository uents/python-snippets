#!/bin/sh

## conda-env環境を作成
conda create --name python-snippets-env python=3.6

## conda-env環境にスイッチ
## - pyenv+anaconda環境ではフルパス指定が必要
## - https://qiita.com/y__sama/items/f732bb7bec2bff355b69
#source activate python-snippets-env
source $PYENV_ROOT/versions/anaconda3-4.3.0/bin/activate python-snippets-env

python ./app.py
