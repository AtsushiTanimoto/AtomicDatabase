# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概要

FAC（Flexible Atomic Code）の Python バインディング `pfac` を使って原子データを計算し、それを加工・整形して独自フォーマットの原子データベースを生成するスクリプト群。すべてのコードは `source/` にある。ビルド・テスト・リンタの設定はない。

依存ライブラリ：`pfac`（`pfac.fac`, `pfac.atom`, `pfac.spm`, `pfac.crm`）、`numpy`、`scipy`、`pandas`。

## 実行方法

各スクリプトは `../database01`、`../database02` という相対パスで読み書きするため、**必ず `source/` ディレクトリをカレントにして実行する**。

パイプラインは次の 3 段階で、この順に実行する必要がある：

```sh
cd source
python atomic_data.py        # 1. pfac.atom.atomic_data で FAC の生データを database01/<元素>/ に生成
python spectrum.py          # 2. pfac.spm.spectrum で準位占有数 (*_spec/*.sp) を計算し、crm.SelectLines で輝線 (*_line/*.ln) を抽出
python generate_database.py  # 3. database01 を読み、整形済みデータベースを database02/<元素>/ に出力
```

- 対象元素（原子番号）は `config.py` の `ATOMIC_NUMBERS` で 3 スクリプト共通に指定する（現状は O = 8 のみ）。電子数は各スクリプト末尾の `for j in range(...)` をハードコードで書き換えて指定する。温度・密度グリッドは `config.py` の `TEMPERATURES`（eV）・`DENSITIES`（cm⁻³）で一元管理しており、`spectrum.py`・`generate_database.py`・`line_probability.py` がこれを使う（インデックス `tNN`/`dNN` でファイルを対応づけているため、ここ以外で定義しない。FAC に渡す密度は `spectrum.py` で 1e10 cm⁻³ 単位に換算する）。
- 各段階は開始時に出力ディレクトリを削除してから作り直す。
- 生成物（`*.en`, `*.tr`, `*.rr`, `*.sp`, `*.ln`, `*.pop` など）は `.gitignore` で除外されており、`database01/`・`database02/` はリポジトリに含まれない。

## アーキテクチャ

### データの流れ

- **database01**：FAC が出力する生データ。ファイル名は `<元素記号><電子数2桁>a.<拡張子>`（例 `Fe05a.en`, `Fe05a.tr`, `Fe05a.rr`, `Fe05a.ai`）、および温度・密度ごとの `<元素><NN>_spec/…a_tXXdYi2.sp`（pfac が出力。密度インデックスは桁埋めなし） / `<元素><NN>_line/…a_tXXdYYi02.ln`。
- **database02**：本リポジトリが生成する最終データベースで、X 線モンテカルロ放射輸送コード MONACO（`~/software/monaco`）の入力。`<元素><NN>.<拡張子>` と、温度・密度ごとのサブディレクトリ `<元素><NN>_pop/`, `<元素><NN>_ln/`（ファイル名 `…_tXXdYYi2.pop` / `.ln`）。ファイル名と固定幅フォーマットは MONACO の `source/processes/src/AtomicDataSet.cc` などの読み込み処理に合わせる必要がある。

### モジュール構成

`source/` の各データモジュールは同じパターンのクラス 1 つを持つ：

- `generate(...)`：database01（および既に生成した database02 のファイル）を読み、辞書のリストを返す
- `write(...)`：`generate` の結果を固定幅フォーマットで database02 に書き出す

ファイルパスは各モジュール内で `pfac.fac.ATOMICSYMBOL[atomic_number]` を使って組み立てられている。

### モジュール間の依存（generate_database.py 内の実行順が重要）

モジュール同士が database02 の中間ファイルを介して依存しているため、`generate_database.py` での呼び出し順を崩すと失敗する：

| モジュール | 出力 | 読み込む database02 ファイル |
|---|---|---|
| `population_data` | `_pop/*.pop`（占有確率 ≥ 1e-3 の準位） | — |
| `photoexcitation_data` | `.px.tr` | `.pop` |
| `recombination_rate` | `.rates`（RR/DR 率。`spectrum.py` が書き出した衝突輻射モデルの率ダンプ `database01/…_spec/*.d0–d5` から計算し、輝線強度と同じモデルで規格化する） | — |
| `autoionization_data` | `.ai` | `.px.tr` |
| `level_data` | `.en` | — |
| `line_probability` | `_ln/*.ln`（輝線強度を再結合率×密度で規格化） | `.rates` |
| `photoionization_data` | `.pi`（断面積を `σ(E/I)^-3 exp(-E/τ)` でフィット） | `.pop` |
| `radiative_decay_data` | `.rd.tr` | `.px.tr` |
| `radiative_recombination_data` | `.rrc.pi`（フィットパラメータ） | — |
| `temperature_density_grid` | `.grid`（温度・密度グリッド） | — |
| `summary_data` | `.sum`（MONACO が配列確保と遷移の登録に使う件数表） | `.en`, `.px.tr`, `.pi`, `.rd.tr`, `.ai`, `_ln/*.ln` |

つまり `population_data` で抽出した「有意な占有を持つ準位集合」が、後続の光励起・光電離・放射遷移・自動電離データの絞り込みに使われる、という構造になっている。
