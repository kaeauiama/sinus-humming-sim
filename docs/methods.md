# 方法

## 1. 共鳴モデル（集中定数、ヘルムホルツ共鳴器）

洞の容積 V、自然口の直径 d（半径 r、面積 A）、長さ L。端補正つきの有効長 L_e = L + 1.7r。

- 質量 M = ρL_e/A、コンプライアンス C = V/(ρc²)、リアクタンス X = ωM − 1/(ωC)。共鳴 f₀ = (c/2π)·√(A/(V·L_e))。
- 線形損失 R_l = max(ポアズイユ 8μL/(πr⁴), 振動境界層 (L/(πr³))·√(2ρμω)) + 放射 ρω²/(2πc)。
- 噴流損失 K = 1.5。記述関数で等価抵抗 k·q、k = (8/3π)·K·ρ/(2A²)。
- 振幅 q（体積流量のピーク）は |Z(q)|·q = P₀ を二分法で解く。1周期の流入体積 V_in = 2q/ω、空気柱 L₀ = V_in/A。
- 定数：ρ = 1.14、c = 350 m/s、μ = 1.9×10⁻⁵ Pa·s。実装は `pages/integrated.template.html` の `lumped()`（換気マップ・tools/ も同じ式）。
- 換気速度（1/s）：ハミング k_H = η(L₀/L, L/d)·V_in·f/V、拡散 k_D = D·A/(V·L_e)（D = 2×10⁻⁵ m²/s）。
- 混合の式（2026-11-21〜）：η = 0.695·(1 − e^(−(x/1.68)^1.76))·(1 − e^(−(j/1.15)^0.57))·e^(−(L/d)/48)、x = L₀/L、j = L₀/d。理想形状の 3D LBM（L/d = 0.5〜20、L₀/L = 0.5〜4（L/d > 3 では 2 まで）、Re = 300）に当てはめたもの（results/deadspace_law_fit.md）。この範囲の外は外挿。
- 倍音：2〜6 倍音を振幅 P₀·h^(−HARM)（弱 HARM = 2 → −12 dB/oct、強 HARM = 1 → −6 dB/oct）で足し合わせる。
- 粘膜：実効直径 d − 2t。粘液：膜厚 h > 0.12·r_eff で閉塞。

## 2. 3D LBM エンジン（engine/parts.json）

- D3Q19 BGK + Smagorinsky（C_s = 0.14）。pull 型の streaming、halfway bounce-back。
- 流体セルだけを詰めて保存し、19 方向の近傍表 `nb[q·nf + k]` で参照（P001 0.4 mm で約 35 万セル）。
- セル種別：1 = 鼻腔、2 = 洞（測定対象）、3 = 流入面（速度平衡、呼気流 `chRatio·UPEAK`）、4 = 流出面（ρ = 1 の平衡）、5 = 自然口（円筒で掘ったもの）。
- 粘性：ν = UPEAK·d_cells/Re（UPEAK = 0.08、Re 既定 300）、τ = 3ν + 0.5。
- **駆動**：自然口の中ほどの1層（slab）に振動する体積力 F₀·cos(ωt)（速度シフト法）。洞全体に、前のステップの自然口流量（stats[2]）と同じ量の一様な吸い込みを置いて、圧縮を模す。格子の共鳴（音速 1/√3 の定在波）を拾わないための工夫。
- **直流を消す PI 制御**：1周期の移動平均流量（リングバッファ）をゼロに保つ。ゲインは writeUniform の uF[15], uF[16]。
- **周期**：T = π·L₀/UPEAK（200〜16000 ステップ）。最初に `warm` ステップ駆動なしで呼気流を落ち着かせる。
- **スカラー（NO）**：semi-Lagrangian MacCormack＋最小最大クランプ、拡散係数 ν/0.8、4 ステップごと。初期値は洞 = 1、自然口内は線形。保存的ではない点に注意。
- **周期末**：洞セルの濃度和（固定小数点 FIX = 4096、u32 atomic）と、流入・流出体積（stats[0], [1]）を読み戻し、`onCycle(k, inflow, outflow, C)` を呼ぶ。
- uniform U（80 バイト）：nf, nx, ny, nz / tau0, cs, uin, invSin / omega, dc, dtc, sgn / slabN, T, F0, kp / ki, ax, ay, az。

### 測定手順（tune → freeze → measure、2026-11-21〜）

1. 周期ごとに流入体積と目標（共鳴モデルの L₀）を比べ、F₀ ← F₀·(目標/実測)^0.9（1周期で 0.4〜2.5 倍まで、上限 1.5×10⁻²）。
2. 周期 2 以降で ±8% に入ったら F₀ を固定。1 周期待つ。
3. 周期 4（スカラーの助走）以降の 3 周期を測る。η = Σ(V_sinus·(1 − C_k/C_{k−1})) / Σ流入。測定中に ±12% を超えてずれたら手順 1 に戻る。
4. 18 周期で打ち切り。目標に届かなければ、式の比 η_law(目標)/η_law(実測) で補正して「届かず」と表示。

### 長い計算（pages/agefield.template.html、2026-11-22〜）

- 手順 1〜2 と同じく振幅を合わせて固定したあと、`cycles` 周期まで回し続ける（固定後は周期の境目で止めない）。`snaps` の周期で濃度の場を読み戻し、tools/devserver.py に POST する（u8、255 = 固体、流体は c×254）。周期ごとの記録は cycles.json（周期、流入、洞の濃度の平均、η、固定済みか）。
- URL：`auto`（開始）、`cycles`、`snaps`、`tag`（保存先の名前）、`f`・`P0`・`d`（共鳴モデルの条件）、`l0d`（目標を直接）、`re`（既定 300）、`ch`（鼻腔の気流、ジェットの最大速度に対する比。既定 0.12、0 で止める）、`warm`、`dbg`。
- 解析：tools/agefield_pack.py（洞全体・自然口側と奥の半分・2 区画のモデルとの比較、ページ用に 0.8 mm に詰める）、tools/agefield_spread.py（むら）、tools/agefield_budget.py（濃度の収支）。

## 3. NO モデル

**2026-11-22〜（ページと tools/no_model.mjs の `o.store`）**：洞の空気は 1 区画で dC/dt = g_e·(S − C) − (k_D + k_H)·C。粘膜のたくわえ（空気の σ 倍）は σ·dS/dt = P − σ·k_l·S − g_e·(S − C)。σ = 0.6·f、g_e = f/24 s（f = その洞の面積÷容積 ／ 上顎洞の面積÷容積）、k_l = 1/120 s。P は面積に比例し、上顎洞の安静時の空気が 8 ppm になるよう決める。鼻腔粘膜は安静時の鼻の NO の 70%。実効音圧 180 Pa。校正は tools/no_calibrate3.mjs（results/no_kinetics_store.md）。以下は 2026-11-21 までの形。


- 各洞：dC/dt = P − k_loss·C − (k_D + k_H)·C。P は表面積 S = 4.836·V^(2/3) に比例。
- 校正：上顎洞の回復時定数 τ_rec = 4.5 分（k_loss + k_D = 1/τ_rec）、上顎洞の安静時濃度 8 ppm。
- 鼻から出る NO = (M + Σ n·V·k·C)/F（F = 100 mL/s）。鼻腔粘膜の寄与 M は、健康な参照条件の静かな呼気の 70%。
- 洞：上顎洞（CT 値か 14 mL / 2.8 mm / 2.1 mm）、蝶形骨洞 4 mL / 2.2 / 1.5、前頭洞 2.9 / 7.5 / 4.0、篩骨蜂巣 0.4 / 1.5 / 1.5 × 8 室。
- 手順：静かな呼気 5 s → [吸気 3 s・ハミング 10 s] × 3 → 吸気 3 s → 静かな呼気 5 s → 休憩 180 s → ハミング 10 s → 吸気 3 s → 静かな呼気 5 s。

## 4. 形状

- `geometry/build_geom.py`：P001 のラベル 2・4 を 0.5 mm ガウスで平滑化し、0.4 mm 等方格子に再標本化。最大連結成分だけを残し、壁 2 セルを確保する。自然口は CT の空気の通り道（元ボクセル (104.5, 85.5, 34.6) → (101.0, 85.5, 34.6)）を A → B の円筒で掘る。
- マスクは z 優先（index = (z·ny + y)·nx + x）で gzip。0.4 mm：111×107×140、洞 14.0 mL、鼻腔 8.27 mL。
- NasalSeg のラベル番号は資料の記載と違い、重心から判定した：1, 2 = 上顎洞、3, 4 = 鼻腔、5 = 上咽頭。
- 理想形状（検証ページ）：球の空洞（半径 3.2d）＋円筒の自然口＋鼻腔の流路。

## 5. 落とし穴（踏んだもの）

1. **非同期の読み戻しと振幅更新**（2026-11-21 に修正）。周期末の mapAsync を待つ間もフレームループが次の周期を進めていたため、F₀ の変更が次の周期の途中の不定な位置で入り、往復の中心がずれていた。症状は、同条件でも毎回値が違う、L₀/L = 1 で η が 0〜116% に散る、目標に届かない。`build/patch_sync.py` で周期末に計算を止め、読み戻し後に再開する。**verify-dlaw.html と sinus3d.html は未修正**。
2. ヘッドレス Chrome＋SwiftShader では WebGPU のキャンバスが "Device was destroyed" になる。オフスクリーンのテクスチャに描く偽コンテキストで回避（test/run.mjs `--fake-canvas`）。
3. WGSL：フラグメントシェーダの引数に `@builtin(position)` を二重に書けない（VO.pos を使う）。定数配列を実行時の添字で引くには関数内の `var` にする。`fn_` のような識別子は避ける。
4. 自然口の slab：軸が半整数座標にあると `|s| < 0.5` で 1 層も拾えない。半開区間 `-0.5 ≤ s < 0.5` にする（assemble.py で置換）。
5. 測定の助走：最初の数周期は、自然口内の濃度分布の初期値と流れの立ち上がりで η が過大になる。洞のセルだけを数え、周期 4 以降を使う。
6. SwiftShader は遅い（4 万セルで約 10 ステップ/秒）。本番解像度は実 GPU で。
7. 内蔵ブラウザ（desktop app）では file:// で開くと WebGPU が無い（data: URL 扱いでセキュアコンテキストにならない）。localhost で配信する（CLAUDE.md「3D ページを回す」）。
8. **駆動層（slab）の float32 丸め**（2026-11-21 に修正、コミット 4b1da7d）。
   - 自然口の中ほどの 1 層は `tParam·len − len/2` の半開区間で選んでいた。`tParam` が float32 なので、管の格子数によっては ±0.5 の境目が丸めでずれ、0 層や 2 層になっていた。
   - 2 層だと流量を 2 倍に数え、実際の空気柱は目標の半分、η は約 1/5 に出る。0 層だと駆動がかからない。
   - 例：理想形状の L/d = 10 は、10 格子と 12 格子で 2 層、16 格子で 0 層だった。
   - いまは正確な軸方向の座標 t で判定する（assemble.py がエンジンにも同じ修正を入れる）。層の大きさが空か断面の 1.4 倍を超えると、ページにエラーを出す。
   - 修正前の記録済みの測定はすべて 1 層だったことを確かめてある（E1・E2・統合版・数値の確認・L/d ≤ 3 の当て直し）。
9. **長い計算の後半のずれ**（2026-11-22）。振幅を固定しても、2000 周期を超えると流入が目標から離れていく（0.4 mm で 3000 周期に 0.82 倍、0.8 mm では 3.6 倍に発散し、η が 1 を超える）。洞に残る量が少なくなるほど、相対的な減り方が速くなる。スカラーの移流（セミラグランジュ＋マコーマック、保存的でない）か、駆動・圧縮の扱いの長時間のずれが疑わしい。2000 周期より後の結果は使わない（results/agefield_maxillary.md）。

## 6. 同じ式・定数が複数の場所に書かれている

ページごとに自己完結させているため、式や定数が共有されていない。式を変えたら下の場所をすべて直し、その式に依存する findings の数値を出し直す。行番号は 2026-11-21 時点（`MIX`、`mix=`、`0.60`、`RHO` で検索すれば見つかる）。

| 中身 | 書かれている場所 |
|---|---|
| 混合の式（2026-11-21 の当て直し：m = 0.695, x₀ = 1.68, n = 1.76, k = 1.15, p = 0.57, λ = 48。引数は L₀/L と L/d） | `pages/integrated.template.html:193`（統合版と丸み検証の両方に入る）、`dist/hum-map.html:192`、`dist/hum-3d.html`（`MIX`）、`proto/model-candidates.html`（`MIX`）、`tools/model.mjs`（Node のツールはここから import）、`tools/population_pitch.py`（`MIX`） |
| 旧 soft law（m = 0.59, x₀ = 1.89, n = 1.76）を意図的に残しているもの | `tools/model.mjs` の `mixOld`（比較用。`LAW=old` で旧結果を再現）、`tools/syringe_fit.mjs`・`tools/syringe_length_scan.mjs`（記録済みの結果のための履歴） |
| 古い 2D の式（0.70·max(0, 1 − 0.60·L/L₀)） | `tools/population_pitch.py`（`LAW=2d` で最初の結果を再現）、`pages/dlaw.template.html:270,298` と `dist/verify-dlaw.html:840,869`（検証の「予測」として）、`tools/lumped_mixing_compare.py:15`（2D と比べるための意図的なもの） |
| さらに古い仮置きの式（1 − exp(−(L₀/L)/2)） | `dist/sinus3d.html:896` の `etaAssumed`（旧 3D ページ。比較用の曲線） |
| 共鳴モデルの定数（ρ = 1.14, c = 350, μ = 1.9×10⁻⁵, K = 1.5, 端補正 1.7r） | `pages/integrated.template.html:190`、`pages/dlaw.template.html:253`、`dist/hum-map.html:190`、`dist/sinus-humming.html:164`、`dist/sinus-lbm.html:857`、`dist/sinus3d.html:949`、`dist/verify-dlaw.html:823`、`dist/hum-3d.html`・`proto/model-candidates.html`（`lumped`）、tools/ の全ファイル |
| hum-3d の架空の形（鼻腔の壁・鼻甲介・篩骨胞、上顎洞） | `pages/hum3d.template.html`（`nasal`、`maxSDF`）と `geometry/build_fict.py`（同じ形の numpy 版。上顎洞の 3D 格子を作る）。鼻腔か上顎洞の形を変えたら、格子を作り直して長い計算を回し直す |
| NO のたくわえ（σ 0.6、τ_ex 24 s、τ_rec 120 s、粘膜 70%、180 Pa、2026-11-22〜） | `tools/no_model.mjs`（`o.store`、既定値は呼ぶ側）、`tools/no_calibrate3.mjs`、`tools/no_recovery.mjs`（`STORE`）、`pages/integrated.template.html`（`NOP`、`STORE`）、`dist/hum-map.html`（`NO`、`STORE`）、`pages/hum3d.template.html`（`P0` のみ。換気だけ） |
| 自然口ごとの音圧の比（results/ostium_pressure.json）と 2 区画（自然口側 0.5、区画間 40 秒。2026-11-22 にページからは外した。tools の一部に残る） | `tools/no_model.mjs`（json を読む）、`tools/population_pitch.py`（json を読む）、`dist/hum-map.html`（`OSTP`、`TWO`）、`pages/integrated.template.html`（`OSTP`、`TWO`）、`dist/hum-3d.html`（`GT` に json を書き写したもの、`TWO`） |
| NO モデル（τ_rec = 270 s、安静時 8000 ppb、鼻腔の寄与 70%、S = 4.836·V^(2/3)） | `pages/integrated.template.html:287–302`（`NOP`）、`dist/hum-map.html:452–481`（`NO`）。呼気流量 `Fside` は統合版が mL/s（100）、換気マップが m³/s（1e-4）で単位が違う |
