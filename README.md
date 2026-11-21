# sinus-humming-sim

ハミングで副鼻腔の空気がどれだけ入れ替わるかを、共鳴モデル（集中定数）・WebGPU の格子ボルツマン法（3D 流体計算）・NO（一酸化窒素）のモデルの 3 段で調べる研究用プロジェクトです。

**これは換気の物理を調べるための計算で、診断や治療の効果を示すものではありません。**

## ページ

GitHub Pages：https://kaeauiama.github.io/sinus-humming-sim/

| ページ | 内容 | 動く環境 |
|---|---|---|
| [換気 3D](dist/hum-3d.html) | マイクで声の高さを取り、架空の頭の中で副鼻腔の換気を 3D で見る。上顎洞の中の空気の広がり方は、事前に回した 3D 流体計算の結果 | スマホ・パソコン（WebGL2）。マイクは https で |
| [換気マップ](dist/hum-map.html) | 4 種類の副鼻腔 × 音の高さ。拡散、粘膜・粘液、倍音、鼻の NO の出方 | スマホ・パソコン |
| [統合版](dist/sinus3d-integrated.html) | 実際の上顎洞（NasalSeg P001）で 3D 流体計算 → NO モデル → 文献との照合 | パソコンの Chrome / Edge（WebGPU） |
| [丸み検証](dist/verify-rounding.html) | 自然口の縁の丸みと換気 | パソコンの Chrome / Edge（WebGPU） |

`dist/` には、ほかに古いモデルや不具合のあるエンジンで作った旧版のページ（`sinus-humming`、`sinus-lbm`、`sinus3d`、`verify-dlaw`）も残してありますが、Pages には出していません。

## 分かったこと（要約）

詳しくは [docs/findings.md](docs/findings.md)。数値はすべて `results/` に記録があります。

- ハミング（100〜300 Hz）は上顎洞の共鳴（約 550〜600 Hz）より低く、洞の空気は音圧でばねのように縮む。1 往復で出入りする体積は「容積 × 音圧」で決まる。
- 自然口を往復する空気柱が自然口の長さより短いと、空気は入れ替わらない（混合の式、3D で 22 点を測って当てはめた）。前頭洞が換気されにくいのはこのため。
- 洞の中の空気は、ハミングの噴流で 2〜3 秒のうちによく混ざる（長い 3D 計算、架空の形と実形状の両方）。
- 人の NO の測定（Menzel 2005、Maniscalco 2003 など）に合わせると、実効音圧は約 180 Pa。10 秒のハミングで上顎洞の空気の約 95% が入れ替わる。NO がゆっくりとしか減らないのは、粘膜の側の NO のたくわえで説明した。
- 鼻腔内の音圧は誰も測っておらず、いちばん大きな仮定のまま。

## 手元で動かす

- 各ページは外部依存のない単一の HTML。`dist/` のファイルを、ローカルのサーバー経由でブラウザで開く（`python -m http.server 8765 --bind 127.0.0.1` など。WebGPU とマイクは `file://` では動かない）。
- ページの組み立て：
  ```
  python build/assemble.py integrated geometry/p001_040 dist/sinus3d-integrated.html
  python build/assemble.py rounding   geometry/p001_040 dist/verify-rounding.html
  python build/build_hum3d.py results/lbm/fict_max_040_150hz_v2 dist/hum-3d.html
  ```
- 集中定数モデルの道具は `tools/`（Node と Python。numpy だけ）。
- モデルの式・エンジンの構造・測り方は [docs/methods.md](docs/methods.md)、次にやることは [docs/roadmap.md](docs/roadmap.md)、文献は [docs/references.md](docs/references.md)。

## 構成

```
engine/parts.json        3D LBM エンジン（D3Q19, WGSL）の断片
pages/*.template.html    ページの雛形
build/                   組み立て（assemble.py, build_hum3d.py ほか）
geometry/                計算格子（NasalSeg P001 由来と、架空の上顎洞）と生成スクリプト
dist/                    組み立て済みのページ
tools/                   集中定数モデル・NO モデル・解析の道具
results/                 計算結果の記録
docs/                    分かったこと、方法、文献、予定
```

## ライセンスと出典

- コードは MIT、文章・記録・図は CC BY 4.0。詳しくは [LICENSES.md](LICENSES.md)。
- 実形状の格子は NasalSeg（Zhang Y. et al., *Scientific Data* 2024, [doi:10.5281/zenodo.13893419](https://doi.org/10.5281/zenodo.13893419), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)）の症例 P001 を改変したもの。

## このリポジトリについて

研究の作業履歴とは別に、公開用にまとめたものです。記録（docs/、results/）に出てくるコミット番号は、非公開の作業履歴のものです。開発に使った Claude Code 用の作業メモ（CLAUDE.md）は含めていません。
