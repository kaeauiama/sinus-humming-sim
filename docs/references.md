# 文献とデータ

- Weitzberg E, Lundberg JO. Humming greatly increases nasal nitric oxide. Am J Respir Crit Care Med 2002;166:144–145. https://pubmed.ncbi.nlm.nih.gov/12119224/ — ハミングで鼻の NO が約 15 倍（10 人、一定流量）。短報で、山と平均のどちらを比べたかは要旨に無い。全文は自動アクセスを拒否されて未読。
- Shusterman DJ, Jansen K, Weaver EM, Koenig JQ. Documentation of the nasal nitric oxide response to humming: methods evaluation. Eur J Clin Invest 2007. doi:10.1111/j.1365-2362.2007.01845.x（PubMed 17696966）— 10 人、ATS の parallel 法で平均 4.2 倍（series 法では 2.1 倍）。
- 要旨は Europe PMC の API（https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:<PMID>&resultType=core&format=json）で読める。PubMed と ATS のサイトは、自動での読み取りに確認画面を出す。
- Maniscalco M ら. Assessment of nasal and sinus nitric oxide output using single-breath humming exhalations. Eur Respir J 2003;22:323–329. https://doi.org/10.1183/09031936.03.00017903 （PubMed 12952268）— 反復での段階的低下、3 分で回復、鼻腔粘膜由来の割合、注射器模型（自然口の太さ・周波数）。人での増加は、10 秒の吐く息の最後の 8 秒の平均で 2233 対 471 nL/min（4.7 倍、0.2 L/s、10 人）。本文は無料で読める：https://publications.ersnet.org/content/erj/22/2/323 （Fig. 6 が太さ別の入れ替わり割合。2026-11-21 確認）
- Lundberg J, Weitzberg E（Aerocrine AB）. US Patent 7,270,638 B2「Method and device for diagnosis using an oscillating airflow」. https://patents.google.com/patent/US7270638B2/en — 上の注射器模型と同じ記述（2 つ目の太さを 1.29 mm と記載）。先端の長さは書かれていない。
- Maniscalco M. Humming, nitric oxide and paranasal sinus ventilation（学位論文, Karolinska Institutet, 2006）. https://openarchive.ki.se/xmlui/handle/10616/38896
- Menzel L, Hess A, Bloch W, Michel O, Schuster KD, Gäbler R, Urban W. Temporal nitric oxide dynamics in the paranasal sinuses during humming. J Appl Physiol 2005;98:2064–2071. doi:10.1152/japplphysiol.01151.2003。https://researchportal.vub.be/en/publications/temporal-nitric-oxide-dynamics-in-the-paranasal-sinuses-during-hu/ （要旨。ページの誌名表示 "Journal of Applied Physics" は誤り）— 8 人、レーザー磁気共鳴分光。ハミング中に NO が山のあと指数関数的に減る時定数 3.0 ± 1.2 秒、ハミングの間隔をあけるほど山が高くなり、回復（補充）の時定数 4.5 ± 3.2 分。1 区画モデル（一定の産生、濃度に比例した消失と放出）で説明できるとする。PMID 15691901。全文は出版社（journals.physiology.org）が自動アクセスに確認画面を出し、PMC にも無いので未読。
- Granqvist S ら. Paranasal sinus ventilation by humming. J Acoust Soc Am 2006 — 管の模型と計算（../sinus-rescue/docs/01-hum-mechanics.md に要約あり）。
- Dang J, Honda K. Acoustic characteristics of the human paranasal sinuses derived from transmission characteristic measurement and morphological observation. J Acoust Soc Am 1996;100(5):3374–3383 — 副鼻腔の共鳴（谷）の実測、約 310〜1070 Hz（3 人）。書誌は ../sinus-rescue/docs/01-hum-mechanics.md から転記（原典は未確認）。
- Maniscalco M. Humming, nitric oxide and paranasal sinus ventilation（学位論文, Karolinska Institutet, 2006）は https://openarchive.ki.se/articles/thesis/Humming_nitric_oxide_and_paranasal_sinus_ventilation/26916211 。PDF（496 kB）は未入手。収録論文は Maniscalco 2003（Eur Respir J）、Lundberg 2003（JAMA）、Maniscalco 2004・2003・2006（Eur J Clin Invest）で、Weitzberg 2002 は含まない。
- 副鼻腔の寸法（results/sinus_dimensions_literature.md。いずれも要旨・検索の要約経由）：
  - Cohen O ら. Volumetric analysis of the maxillary, sphenoid and frontal sinuses: a comparative computerized tomography based study. Auris Nasus Larynx 2018;45:96–102 — 上顎洞 12.75 ± 4.38、蝶形骨洞 4.00 ± 1.99、前頭洞 2.92 ± 2.57 mL（健康な成人）。https://cris.bgu.ac.il/en/publications/volumetric-analysis-of-the-maxillary-sphenoid-and-frontal-sinuses/
  - 蝶形骨洞の自然口の CBCT 計測（トルコ、2022）：女性 2.18 ± 0.42 mm、男性 2.26 ± 0.53 mm。https://dergipark.org.tr/en/download/article-cite-file/1219507/type/2
  - 前頭洞の開口の前後径 7.5 ± 2.7 mm（2〜15 mm、5 mm 未満が 17.6%）：内視鏡手術の難しさと結びつけた CT 研究（検索の要約。原典の書誌は未確認）。
  - 篩骨洞の容積（前群 4.33〜4.92、後群 3.01〜3.47 cm³）：Rom J Rhinol 2017, doi:10.1515/rjr-2017-0020。篩骨蜂巣は片側平均 9 室（4〜17）。
- 気道の液膜が半径の約 12% を超えると液体の栓：https://pmc.ncbi.nlm.nih.gov/articles/PMC8074672
- 形状データ：NasalSeg（Zhang ら, Scientific Data 2024, CC BY 4.0）https://doi.org/10.5281/zenodo.13893419
