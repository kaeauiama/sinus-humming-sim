# 公開（GitHub Pages）

## 決めたこと（2026-11-22、ユーザー）

- **公開用リポジトリは、研究一式を履歴なしで出す。**この作業リポジトリ（全履歴）は手元に残す。理由：全コミットの作者欄に個人のメールアドレスが入っていること、履歴を書き換えると記録に書いたコミット番号（どの版のエンジンで出た数字か）が合わなくなること。
- 公開用一式から除くもの：CLAUDE.md（作業メモ。ユーザー名の入ったパスがある）、作業用の README、legacy/tilt-danmaku.html（本筋と無関係な試作）、.claude/、build/export_public.py（個人情報の検出パターンを持つ）。
- **ライセンス：コードは MIT、文章・記録・図は CC BY 4.0。**NasalSeg 由来のデータは CC BY 4.0 のまま、出典と改変内容を表示（build/public/LICENSES.md）。
- **Pages に出すページ：**換気 3D、換気マップ、統合版、丸み検証、入り口（site/index.html）。旧版の 4 ページ（sinus-humming、sinus-lbm、sinus3d、verify-dlaw）は出さない（古いモデル・振幅更新の不具合のあるエンジン）。

## 点検の結果（2026-11-22）

- 秘密情報（鍵・トークン・パスワード）：全 55 コミットのどこにも無い。
- 個人情報：作者欄のメールアドレスと名前（全コミット）、CLAUDE.md のユーザー名入りのパス。公開用一式には入れない。書き出し時に自動で検査する。
- 消したファイル・大きなファイル：無い（最大 165 kB）。
- NasalSeg（Zenodo 10.5281/zenodo.13893419、CC BY 4.0、2026-11-21 に API で確認）：由来のデータを含むページに、出典・ライセンスへのリンク・改変内容を表示した（d8314ca）。元の CT 画像・ラベルは含めない。
- 文献の数値：出典つきの引用だけ。図や本文は転載していない。
- 外部ライブラリ・フォント：使っていない。
- 注意書き（診断や治療の効果を示すものではない）：全ページにある（丸み検証に足した、d8314ca）。

## 手順

1. ユーザーが GitHub に空の public リポジトリを作る（README・.gitignore・ライセンスは付けない）。
2. 書き出す：`python build/export_public.py ../sinus-humming-sim-public --holder "名前" --repo https://github.com/USER/REPO --pages https://USER.github.io/REPO/`（作業リポジトリはコミット済みであること）。
3. 公開用フォルダで `git init -b main`、作者は GitHub の noreply アドレスにして 1 コミット、リモートを足して push。
4. GitHub の Settings → Pages → Source を「GitHub Actions」にする。.github/workflows/pages.yml が site/index.html と 4 ページを配信する。
5. 更新するときは、作業リポジトリで直してコミット → 2 で書き出し → 公開用フォルダでコミットして push。
