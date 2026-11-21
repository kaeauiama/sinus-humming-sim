# ライセンス（Licenses）

このリポジトリの中身は、種類によってライセンスが違います。

| 中身 | ライセンス |
|---|---|
| コード：`engine/`、`build/`、`tools/`、`test/`、`geometry/*.py`、`pages/` と `dist/` の HTML に含まれるスクリプト・シェーダ | MIT（[LICENSE](LICENSE)） |
| 文章・記録・図：`docs/`、`results/`（下の NasalSeg 由来のものを除く）、`README.md`、ページの文章 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) © kaeauiama |
| 架空の形と、その上での 3D 計算の結果：`geometry/fict_max_*`、`results/lbm/fict_max_*` | CC BY 4.0 © kaeauiama |
| **NasalSeg に由来するデータ**（下記） | **CC BY 4.0（原著作者：Zhang Y. et al.）** |

## NasalSeg 由来のデータ

- 出典：Zhang Y. et al., "NasalSeg: A Dataset for Automatic Segmentation of Nasal Cavity and Paranasal Sinuses from 3D CT Images", *Scientific Data* 11 (2024). データ：[doi:10.5281/zenodo.13893419](https://doi.org/10.5281/zenodo.13893419)
- ライセンス：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 改変の内容：
  - 症例 P001 のラベル 2（上顎洞）と 4（鼻腔）を 0.5 mm でぼかし、0.4 mm（と 0.8 mm）の等方格子に再標本化した。
  - 切り出し、洞と鼻腔のあいだに 2 格子の壁を確保し、自然口を円筒で掘り直した。
  - CT の画素値は含まない（ラベルを作り直した 0〜4 の格子だけ）。
- 該当するファイル：
  - `geometry/p001_040.*`、`geometry/p001_080.*`、`geometry/preview.png`
  - `results/nasalseg_maxillary_volumes.csv`（全症例のラベルから数えた容積）、`results/nasalseg_ct_extent.md`
  - `results/lbm/p001_040_150hz/`（P001 の形での計算記録）
  - 上の格子を埋め込んだページ：`dist/sinus3d-integrated.html`、`dist/verify-rounding.html`、`dist/sinus3d.html`
- 元の NasalSeg のデータそのもの（CT 画像・ラベル）は、このリポジトリに含めていない。使う場合は Zenodo から各自で入手する。

## 文献の数値

ページと記録には、論文から引用した数値（測定値、図から読み取った値）がある。いずれも出典を明記し、図や本文そのものは転載していない（`docs/references.md`）。
