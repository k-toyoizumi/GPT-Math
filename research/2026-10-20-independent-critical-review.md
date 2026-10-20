# GPT-Math 独立・批判的レビュー

監査日：2026-10-20（日本時間）。監査対象：https://github.com/k-toyoizumi/GPT-Math

**結論：研究を止める必要はないが、現状を「新しい一般定理を継続的に検証・蓄積できる基盤」と認定することはできない。最大の問題は、成果・コミット・実行した検証の対応が切れていること。まず既存の改善を1本のCIへ統合し、その後、Wの補題を範囲の狭い研究候補として評価する。**

リポジトリへの変更、push、PR作成、Actions再実行は行っていない。ローカルの監査用コピーと別ディレクトリで検証した。本レビューで新しいLean証明は実行していない。

## 1. 総合評価

### 実体と報告を分離した評価

| 観点 | 判定 | 根拠 |
|---|---|---|
| 既存の代数的証明 | 有用な検証資産がある | mainの4ファイルを実際の成功ログで確認。一般的な残差公式、再構成恒等式など |
| 数学的新規性 | 未確立 | 既知の二項単位分数の因数分解、Type IIの再構成、有限探索が中心 |
| Wの漸近公式 | 独立の紙上導出で支持。Leanでは未証明 | 第3節に誤差項を含む独立導出。元Agentの導出ファイルはリポジトリ内で未確認 |
| 論文化価値 | 単独では限定的。短報の候補になり得る | Dahan自身の予測値を厳密化する余地はあるが、方法の新規性・先行研究との重複は未確定 |
| 全証明のCI網羅 | mainは現在の4ファイルを明示的にチェック。追加ファイルへの保証なし | 別ブランチには未登録・未実行のLeanファイルが残る |
| 再現性・継続性 | 部分的。運用基盤は未完成 | 未使用の検証スクリプト、未統合の依存ロック、更新されない研究ノート |

### 監査時点の固定スナップショット

- main：`f7866a810ba4efcdf329c6bae921b242b1c046b0`。
- 実リモートブランチ47本。そのうち39本はmainと同じSHA（main自身を含む）。したがって38本の別名ブランチにmainとの差分がない。
- Actions全97実行をAPIで取得：成功83、失敗14。44実行が上記mainと同じSHA。
- イベント内訳：push 90、pull_request 6、workflow_dispatch 1。取得した実行履歴にscheduleイベントはない。
- 名前が `research/totient-sieve-constant-20261020` の最新実行も上記mainのSHAであり、Wの新しい証明を検査していない。

参照：[main固定コミット](https://github.com/k-toyoizumi/GPT-Math/tree/f7866a810ba4efcdf329c6bae921b242b1c046b0)、[最新確認実行39329989543](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39329989543)。実行数とブランチ数は監査時点の値で、将来の増加を反映しない。

**成功回数、ブランチ数、依存ライブラリを含む7358 build jobsを、研究成果数に換算してはいけない。mainのプロジェクト自身のLean定理宣言は10件である。**

## 2. 重大な指摘

### P0：CI成功が、新しい改善の検証を意味していない

1. `ci/lean-coverage-evidence-20261020-0338`（`483b33b77b98926e834a6036dce0beddf590055b`）にはinventoryスクリプトと8テストがある。しかしworkflowはmainと同じで、どちらも実行しない。成功ログにあるのは従来の4 Leanターゲットだけである。
2. `ci/dependency-integrity-20261019-1944`（`a49ffbdeca0395e97daac91caf98a6092d8e95df`）には依存ロックと分類スクリプトがある。しかしworkflowはそれらを呼ばず、従来通り `lake update` を行う。
3. この依存チェックをそのままローカル実行すると、正しい `leanprover/lean4:v4.24.0` を拒否する。正規表現のraw文字列で `\\d`、`\\.`、`\\Z` と二重にエスケープしているため。40桁SHA用の式も同じ問題を持つ。**CI成功で隠れていた、再現可能な実装不具合である。**
4. 最新inventoryスクリプトは追跡ファイルを列挙する機能であり、それだけではビルド漏れ・proof holeを拒否しない。隔離fixtureに未登録の `B.lean` と `sorry` を追加すると、inventoryは正常に一覧を返した。ファイル一覧を実際のビルド・公理監査へ接続する工程が必要。

ローカル結果：inventoryの既存8テストは全成功。依存チェックはexit 1、`DEPENDENCY LOCK FAIL: lean-toolchain is not an exact Lean 4 release`。これはGitHub Actions上でそのチェックが失敗したという意味ではない。Actionsでは未実行である。

参照：[inventoryソース](https://github.com/k-toyoizumi/GPT-Math/blob/483b33b77b98926e834a6036dce0beddf590055b/scripts/lean_inventory_gate.py)、[その成功ジョブ](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39304480567/job/118237851116)、[依存チェックスクリプト](https://github.com/k-toyoizumi/GPT-Math/blob/a49ffbdeca0395e97daac91caf98a6092d8e95df/scripts/dependency_lock_gate.py)、[同ブランチの実行](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39239766378)。

### P0：有限探索と、その数学的完全性を分ける必要がある

mainの `TypeIIDepthSeven.noWitnessInFiniteSearch` は、定義されたBool値がfalseであることを `native_decide` で示す。`List.range` の範囲と全正約数の対応、Bool検索と量化命題の同値を別途Leanで結ぶ定理は、mainにない。

数式を読めば検索範囲は自然で、Pythonによる独立確認も一致する。しかし「全候補を含むことまで形式化済み」とは報告できない。

別ブランチ `research/typeii-670849-certificate-20261018`（`9adfe595522f613a94c29d70ba1d2f2d3766874e`）には `ProgressionCompleteness.lean` と `TypeIIDivisorComplete.lean` が存在するが、workflowが追加でコンパイルするのは `TypeIIDepthSeven_UNCOMPILED.lean` だけ。前2ファイルは、ブランチ全体の成功表示からLean検証済みと認定できない。

ローカルで既存Pythonを再実行し、以下を確認した。

- p=670849、深さ7までの互いに素な35組、正約数426個に該当する証人なし。
- 深さ8では(u,a)=(8,1)、s=319と7711が一致。
- 35組中25組では、元の法の真の約数を法としても不可能性を検出できる。
- 素数判定も2から整数平方根までの試し割りで独立確認した。ただしLean素数証明ではない。

これらは有限の結果であり、全素数の深さ上界、Type II不存在、予想への反例ではない。

参照：[対象ブランチの固定ソース](https://github.com/k-toyoizumi/GPT-Math/tree/9adfe595522f613a94c29d70ba1d2f2d3766874e/research/2026-10-18-typeii-670849)、[成功ジョブ117509425759](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39071339019/job/117509425759)。このジョブでは既存Pythonの実行もログで確認した。

### P1：Lean証拠の正確な範囲

| 対象 | コミットSHA | 成功ジョブ | 認定できる範囲 |
|---|---|---|---|
| XuGeneralAudit、XuTheorem41Audit | f7866a810ba4efcdf329c6bae921b242b1c046b0 | 118325436655 / run 39329989543 | 残差・等号条件、転記された有理数式の数値的不一致と修正例 |
| TypeIIReconstruction | 同上 | 同上 | 仮定付き多項式恒等式、p=670849の正の数値解の交差積 |
| TypeIIDepthSeven | 同上 | 同上 | 有限Bool検索結果はnative_decide。深さ8の証人数式・有理数恒等式もビルド成功 |
| FixedXFactorizationの2定理 | 8212448c91ccc378023537ea6e3d9c998c46f80f | 118236172872 / run 39303991740 | 整数の多項式恒等式と非零shift下の因数分解同値。正の整数解の存在までは含まない |
| Wの漸近公式 | 該当コードなし | 該当成功ログなし | Leanでは未証明 |

ログで確認した公理依存：XuGeneralAuditは `[propext, Classical.choice, Quot.sound]`、既存TypeIIReconstructionは `[propext]`、FixedXFactorizationの恒等式は `[propext, Quot.sound]`、同値定理は `[propext, Classical.choice, Quot.sound]`。これらは通常のLeanの標準公理であり、自作の未証明仮定とは区別する。

有限Bool定理には `#print axioms` がなく、その正確な依存一覧は既存ログでは未確認。ソース上の `native_decide` 利用は明白であり、コンパイラ・実行系への信頼を追加する。通常のカーネル検査だけで完結する証明として扱わない。現在の最新Leanの説明をそのまま4.24.0へ当てはめず、固定版で実際に依存を出力すべきである。

参照：[mainの成功ログ](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39329989543/job/118325436655)、[FixedXFactorizationのソース](https://github.com/k-toyoizumi/GPT-Math/blob/8212448c91ccc378023537ea6e3d9c998c46f80f/TypeIIReconstruction.lean)、[その成功ログ](https://github.com/k-toyoizumi/GPT-Math/actions/runs/39303991740/job/118236172872)、[Lean公式の信頼モデル](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)。

### P1：再現性と研究記録が未統合

- Leanは4.24.0、Mathlibはv4.24.0を指定済み。mainにプロジェクトの `lake-manifest.json` はなく、CIで毎回生成する。成功ログのMathlib解決先は `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`。Mathlib自体のmanifestもあるため「全依存が毎回無制限に浮動」とは断定しないが、プロジェクトで固定・照合する仕組みはmainに未統合。
- mainのPython2本はCIで実行しない。ローカル再実行では1181素数、固定分母で575成功・606不成立、offset分布も既存assertと一致した。
- mainのworkflowにCSV/JSON/実行ログ/SHA-256をartifact保存する処理がない。run 39329989543、39304480567のartifacts APIも空配列だった。有限証明ブランチはCSVを生成するが、workflowはアップロードしない。
- `research/2026-10-17-xu-numerical-audit.md` は一般残差補題を未検証としたままで、後の成功ログに追随していない。過大評価だけでなく、検証済み成果の取りこぼしも起きている。
- mainの `defaultTargets` はXuTheorem41Auditのみ。CIは4ターゲットを明示しているため現在のmainの直接の漏れではないが、単なる `lake build` とCIの意味が一致しない。
- リポジトリのworkflowに定期実行設定はない。別サービス側の毎時Agent設定・実行環境・引き継ぎ成功は今回未確認であり、GitHubの履歴だけでは保証できない。

### P1：文献の扱い

Xu arXiv:2609.29250v1の(4.29)は定数88、(4.30)は89、(4.31)は88を使う。原文で不整合を確認した。repoの一般残差公式と整合する修正は `m=138r+88+c(138r+89)`。この局所的誤植を直すことと、その論文全体を否定することは別である。

Bradford (2025)の約数・合同条件と解の対応、およびPomerance–WeingartnerのType I/II条件は、今後の「一般補題」の先行研究として必ず比較する。単に同値式を書き換えるだけでは新規性にならない。

最新文献検索では arXiv:2609.09204 がヒットしたが、現在のarXivページは撤回を表示している。今回の結論の根拠には採用しなかった。新しい文献ほど、版・撤回状態の確認が必要である。

参照：[Xu原文](https://arxiv.org/html/2609.29250v1)、[Bradfordの刊行版](https://math.colgate.edu/~integers/z54/z54.pdf)、[Pomerance–Weingartnerの著者公開稿 §2](https://math.dartmouth.edu/~carlp/ESS-ExceptionsV8.pdf)、[撤回状態](https://arxiv.org/abs/2609.09204)。DahanがType IIの先行結果をCor.2.2と呼ぶ箇所も、確認したPomerance–Weingartner稿ではCor.2.4が対応する。引用番号も原文で合わせる。

### GitHub書き込み拒否：事実と推測

**確認した事実**：多数のブランチ作成、実コミットの追加、PR #1、push起因のActionsが存在する。したがって「GitHub書き込みが全面的に不可能」は事実と合わない。一方、未統合スクリプト、同一SHAのブランチ大量作成、ノート中の安全チェック拒否の記述がある。

**未確認**：各拒否のツール呼び出し、拒否本文、どの権限・内容・経路が問題だったか。GitHub側の権限不足なのかChatGPT側の自動承認審査なのかは、repositoryだけでは原因確定できない。今回、書き込みを試していないため、新しい拒否は発生していない。

**推奨**：拒否を回避する別経路の試行を繰り返さず、拒否本文と対象操作を記録する。読み取り・検証・artifact出力を進め、書き込みは既に許可されている1つの運用経路へ集約する。許可された経路でもブロックされる場合は、reviewableなpatchと実行結果を残し、人が適用する経路を正式な代替とする。workflow編集、研究ファイル編集、PR/mergeの権限と成功条件を分ける。

## 3. 直近のW補題候補の判定

### 定義と判定

対象は、正整数の**順序付き**組を正方形領域で数える

\[
W(J)=\sum_{\substack{1\le u,a\le J\\(u,a)=1}}\frac1{\varphi(4ua)},\qquad J\ge2.
\]

ここでφはEulerのトーシェント関数、logは自然対数。u,aを素数だけに限定したり、順序を同一視したり、ua≤Jへ領域を変えたりすると別の問題になる。W自体には探索対象素数nやNは含まれない。

**独立判定**：この定義なら候補の係数とO(log J)誤差は、以下の通常の解析的導出で支持できる。ただし元Agentの導出は未入手であり、その導出過程の正当性は未確認。本レビューはLean未実行なので、プロジェクトの認定上は**Leanでは未証明**、新規性未確立の候補として扱う。

### 独立導出：Euler積だけでなく誤差項まで

\[
g(u,a)=\frac{2ua}{\varphi(4ua)}\mathbf1_{(u,a)=1}
\]

とおく。これは2変数の乗法的関数である。2変数Dirichlet畳み込みで `g = 1 * 1 * h`、すなわち

\[
g(u,a)=\sum_{d\mid u}\sum_{e\mid a}h(d,e)
\]

となるhをとる。奇素数pでの局所母関数は

\[
\sum_{i,j\ge0}g(p^i,p^j)X^iY^j
=1+\frac{p}{p-1}\left(\frac X{1-X}+\frac Y{1-Y}\right).
\]

(1−X)(1−Y)を掛けると

\[
1+\frac{X+Y}{p-1}-\frac{p+1}{p-1}XY.
\]

p=2の局所因子は1−XY。従ってhの奇素数での非零値は `h(p,1)=h(1,p)=1/(p−1)`、`h(p,p)=−(p+1)/(p−1)` で、2では `h(2,2)=−1`。定数項はいずれも1、その他の正の指数の局所値は0。

H_k=∑_{r≤k}1/rとすれば、有限和の交換から**厳密に**

\[
W(J)=\frac12\sum_{d,e\le J}\frac{h(d,e)}{de}
H_{\lfloor J/d\rfloor}H_{\lfloor J/e\rfloor}.
\]

絶対値を取った局所因子は1+O(p⁻²)であり、log²pを掛けても収束する。そのため

\[
\sum_{d,e\ge1}\frac{|h(d,e)|}{de}\{1+\log^2(de)\}<\infty.
\]

これは単に形式的なEuler積を展開しただけではなく、後の誤差評価を正当化する可和性条件である。

L=log Jとする。d≤Jでは `H_floor(J/d)=L−log d+O(1)` が絶対定数で成り立つ。上の可和性から、調和数積をL²へ置き換えた総誤差はO(L)。さらにmax(d,e)>Jの尾部は

\[
\sum_{\max(d,e)>J}\frac{|h(d,e)|}{de}
\le\frac1L\sum_{d,e}\frac{|h(d,e)|\log(de)}{de}=O(1/L),
\]

なので、主項の有限和を無限和へ延長する誤差もL²×O(1/L)=O(L)。従って

\[
W(J)=\frac{L^2}{2}\sum_{d,e\ge1}\frac{h(d,e)}{de}+O(L).
\]

主係数は

\[
\begin{aligned}
\frac12\sum_{d,e}\frac{h(d,e)}{de}
&=\frac12\left(1-\frac14\right)\prod_{p>2}\left(1+\frac1{p^2}\right)\\
&=\frac38\frac{\zeta(2)}{\zeta(4)}\frac1{1+1/4}
=\frac9{2\pi^2}.
\end{aligned}
\]

ここではRiemann予想や素数分布の仮定は不要。O(log J)の定数はJに依存しない。任意のJ(N)→∞への代入自体は可能だが、下流の篩のN,J,zに関する一様性まで、これで証明したことにはならない。有限のJに対する明示的な誤差定数は今回計算していない。

### 独立した数値検証

小さいJでは、φ(4ua)を直接計算する有理数和と、次の別の有限和をFractionで照合した。

\[
W(J)=\frac12\sum_{d\le J}\mu(d)
\left(\sum_{k\le J/d}\frac1{\varphi(2dk)}\right)^2.
\]

理由は、互いに素なu,aに限れば `φ(4ua)=2φ(2u)φ(2a)` となり、Möbius反転で互いに素という制約を除けるため。J=1,2,3,8,16,30,64ですべて厳密一致。例えばW(3)=7/4、W(8)=355/96。

大きいJの値はNumPy long doubleによる近似計算で、区間演算による保証値ではない。

| J | W(J) | W(J)/(log J)² |
|---:|---:|---:|
| 100 | 13.317254584 | 0.627947497 |
| 1,000 | 27.253212761 | 0.571141634 |
| 10,000 | 46.042326377 | 0.542757582 |
| 100,000 | 69.667942214 | 0.525607552 |
| 1,000,000 | 98.128558318 | 0.514116497 |

候補の極限係数は0.4559453264。最後の3点のlog Jに関する2階差分からの推定は0.4559688026。整合的だが、有限計算から漸近公式を証明したとはいわない。反例が出ないことも証明の代用にはならない。

### Dahanとの比較、新規性、重要性

Dahan v1 §4.3、Lemma 4.22のWと定義は一致する。そこで使う下界の主係数3/(2π²)に対し、候補係数は**ちょうど3倍**。しかし、同論文はすでに数値から約0.46、約3倍と予測している。独自性の候補は「予測値そのもの」ではなく、厳密な値・誤差項の証明である。

論文のCorollary 4.31の式を係数κの関数として読むと、最適化後の定数は

\[
c(\kappa)=\frac12\left(\frac{\kappa}{25e}\right)^{1/3}.
\]

よってκを3倍にしてもcは3^(1/3)≈1.442倍。約0.0653から約0.0943への変更が候補であって、3倍ではない。固定λの別の評価ではκが線形に現れる。この区別はDahan自身の説明にもある。下流の篩の証明全体を今回形式化・完全再検証したわけではないため、新定数を持つ完成定理として認定しない。

同じ漸近公式の既刊証明は、今回の対象文献・検索範囲では発見できなかった。しかし不在の証明ではない。多変数乗法的関数の平均値評価の標準手法と、同じ和の別表現まで調べてから優先権を判断する必要がある。

**採否：棄却しない。範囲を絞って保留採用。** まず上の有限恒等式と局所因子をLean化し、可和性・尾部評価・Euler積を順に接続する。解析的部分は既存の初等的代数証明より相当に重く、1週間で完了するとは保証しない。Leanでの完全検証、新規性確認、下流の篩の監査が揃うまで「新定理完成」「論文化確定」としない。

参照：[Dahan v1 §4.3、Lemma 4.22、Corollary 4.31](https://arxiv.org/html/2608.24035v1)。

## 4. 研究方向の比較

点数は客観的な成功確率ではなく、現在のプロジェクトでの推奨優先度。内訳は数学的意義30、新規性余地25、短期実行可能性25、検証可能性20。

| 方向 | 意義 /30 | 新規性 /25 | 実行性 /25 | 検証 /20 | 合計 | 狙いと弱点 |
|---|---:|---:|---:|---:|---:|---|
| 既知の完全な判定条件と証明付き証人チェッカー | 22 | 12 | 24 | 20 | **78** | 研究基盤の主軸。既知数学なので数学論文としての新規性は弱い |
| Wの係数・明示的誤差、必要なら篩の定数移送 | 23 | 18 | 20 | 15 | **76** | 短期の数学候補。予測値の追認だけでは弱く、解析形式化が重い |
| Type I/II双方の未被覆集合と共通障害の構造 | 28 | 22 | 12 | 13 | **75** | 理論的に縮小できれば価値が高い。有限残差の観察だけでは不足 |
| adaptiveな探索順序・圧縮された検証証明書 | 18 | 13 | 22 | 19 | **72** | Agentに適した計算研究。既存法との同条件比較、負の判定の完全性が必要 |
| Bright–Loughranを起点とする算術幾何 | 29 | 19 | 5 | 7 | **60** | 長期研究候補。専門家なしで短期に全面移行するのは非推奨 |

推奨配分は、基盤統合を先に行い、その後は数学作業の約半分をW候補、約3割をType I/IIの障害構造、残りを文献比較・検証へ。これは運用提案であり、研究成果を保証する比率ではない。

Type IIだけの未被覆をESC全体の未被覆と呼ばない。固定shift、固定a、有限J、全Type II、Type I∪IIを別々に記録する。有限に多数成功したことから「全素数を一定深さで覆える」と推測を昇格させない。

Elsholtz–Taoは既知の解数評価・パラメータ化の基準、Pomerance–Weingartnerは明確なType I/IIの出発点、Salezは有限計算の既知水準の比較対象とする。Bright–Loughranの「Brauer–Manin障害がない」は解の存在証明ではなく、この経路の限界を理解するために使う。

文献：[Elsholtz–Tao](https://arxiv.org/abs/1107.1010)、[Pomerance–Weingartner](https://math.dartmouth.edu/~carlp/ESS-ExceptionsV8.pdf)、[Salez](https://arxiv.org/abs/1406.6307)、[Bright–Loughran Theorem 1.1](https://arxiv.org/pdf/1908.02526)。

### 補題候補の採用・中断基準

1. 量化・定義・正値条件・既知の同値変形との差分を1ページで特定する。できなければ探索しない。
2. 独立した実装または導出で最小反例を優先探索する。元の実装を呼び直すだけでは独立再現としない。
3. 反例が出たら、範囲を後付けで狭めて成功扱いせず、旧主張を棄却として残す。
4. 一般補題として採用するには、読み下せる証明と成功したLean検証を要求する。数値確認・公理依存・新規性は別欄にする。
5. 2回連続の作業単位で新しい反例・構造・補題・改善指標が増えなければ、同じ走査を停止してレビューへ戻す。
6. 先行研究の命題と同値で新しい帰結がなければ、再発見として保管し主研究から外す。誤植監査も追加の理論的帰結がなければ打ち切る。

## 5. 自動化基盤の改善計画

| 優先 | 改善 | 完了条件 | 検証方法 |
|---|---|---|---|
| P0 | 既存ブランチの成果を棚卸しし統合候補を1本へ集約 | 各候補に差分、SHA、実行コマンド、状態がある。空差分を成果扱いしない | mainとのdiff、CI head_sha照合 |
| P0 | 実際に走るworkflowへ全Lean・Pythonを接続 | 対象一覧と実行一覧が一致。未検証草稿は理由付き隔離。全採用証明を実行 | 不正な新規Lean、失敗するPythonを一時fixtureに入れ、CIが失敗することを確認 |
| P0 | 依存ロックの正規表現修正と実行接続 | 正常な固定環境で通り、改変SHA・欠損manifest・版不一致で落ちる | 正常/異常の両テスト、実Actionsログ |
| P1 | 証拠artifactと結果台帳 | theorem名、statement hash、source SHA、toolchain、依存SHA、run/attempt、コマンド、信頼区分、出力SHA-256を保存 | 成功時も失敗時もartifact取得可能。保存後の再現runで一致 |
| P1 | 公理依存監査 | 採用定理すべての依存一覧。native使用は明示 | 全定理の#print axioms、許可外公理・sorryAxを拒否 |
| P1 | 状態分類と研究ノート同期 | source_changed / compile_failed / check_omitted / execution_failed / publication_blocked等を分ける | 最小故障注入。成功していない状態を成功と表示しない |
| P1 | 継続研究用の状態管理 | task ID、仮説、直前の結果、次の最小検証、重複判定、予算が固定される | 中断後の次実行が同じmainから空ブランチを再作成しない |
| P2 | 定期実行と承認済み公開経路 | schedulerの実行実績と、研究状態・保存先が対応する | 連続2回以上の引き継ぎと重複抑止、失敗後再開を実測 |

同じSHAでCIを再実行しても、無条件に新たな研究成果と数えない。ただし環境の再現性確認として目的を明示した再実行には意味がある。研究テーマの採用・論文化・方向転換は人が判断し、Agentは反例探索、定義の照合、形式化の小ステップ、証拠の記録を担当する。

現在の `grep sorry/admit/axiom` は補助に留める。コメントによる誤検出や、名前を経由した信頼依存を扱えない。標準公理・native由来の信頼・自作公理を区分する。`native_decide` を全面禁止する必要はないが、有限証明書の小さなチェッカーを通常のカーネルで検証する方式を優先すると信頼範囲を狭められる。

## 6. 次の1週間の推奨アクション

| 日 | 実行順序 | 期待成果・完了判定 |
|---|---|---|
| 1 | 現在のSHAと47ブランチを固定、成果台帳を作る。空差分の作業を停止 | 何が実在し、何が未検証かを一覧で説明できる |
| 2 | 依存gateの不具合修正、実workflowへ接続、Pythonと全採用Leanを走らせる | 故障注入で赤、正常入力で緑になる実Actions |
| 3 | 全定理の公理依存、Boolと量化命題の橋渡し、artifact保存を統合 | p=670849の有限主張が正確な信頼区分で再現できる |
| 4 | Wの上の独立導出と先行研究を照合。局所因子・有限畳み込みを小さく形式化 | Wを続ける/既知として整理/解析部分を保留、の判断材料 |
| 5 | Wの可和性・尾部誤差のLean可用性調査。篩の係数移送を別文書で点検 | 最も重い未証明ステップが特定される。未完なら未完として残す |
| 6 | 事前に決めた小さい範囲で、Type I/II双方の未被覆と障害の最小証明書を比較 | 追加範囲走査ではなく、一般化できそうな差分か反例1件 |
| 7 | クリーン環境再現と独立レビュー。作業数でなく採用成果・反証・残課題を評価 | 自動化完了なら数学へ戻る。未完なら具体的な失敗工程だけ残す |

1週間の達成目標は「予想の解決」や「Wの全解析形式化の確約」ではなく、**新しい成果を追加した時に、本当にその成果が検証・保存される運用を作ること**。現時点ではここを最優先にする判断が妥当である。

## 付録：独立数値検証スクリプト

下のコードは本レビュー用に作成・実行した。Python 3.12.14、NumPy 2.3.5で実行。小さいJはFractionによる厳密計算、大きいJは浮動小数点計算。リポジトリには追加していない。Leanの検証済みコードではない。

```python
#!/usr/bin/env python3
"""Independent audit; no Lean verification or novelty claim. Python 3 + NumPy.

Exact rational direct sum and a separate Mobius inclusion-exclusion agree for
small J. Larger sums use long double arithmetic, not certified intervals.
"""
from fractions import Fraction
from math import gcd, log, pi, isqrt
import json
import numpy as np

def phi(n):
    ans, t, p = n, n, 2
    while p*p <= t:
        if t % p == 0:
            ans -= ans//p
            while t % p == 0: t //= p
        p += 1
    if t > 1: ans -= ans//t
    return ans

def mobius(n):
    ans, p = 1, 2
    while p*p <= n:
        if n % p == 0:
            n //= p; ans = -ans
            if n % p == 0: return 0
        p += 1
    return -ans if n > 1 else ans

def exact_direct(j):
    return sum((Fraction(1,phi(4*u*a)) for u in range(1,j+1)
                for a in range(1,j+1) if gcd(u,a)==1),Fraction())

def exact_mobius(j):
    return sum((mobius(d)*sum((Fraction(1,phi(2*u))
                for u in range(d,j+1,d)),Fraction())**2
                for d in range(1,j+1)),Fraction())/2

def main():
    exact=[]
    for j in [1,2,3,8,16,30,64]:
        a,b=exact_direct(j),exact_mobius(j)
        assert a==b
        exact.append({'J':j,'W_numerator':str(a.numerator),
                      'W_denominator':str(a.denominator),'methods_equal':True})
    maxj=1_000_000
    ph=np.arange(2*maxj+1,dtype=np.int64)
    mu=np.ones(maxj+1,dtype=np.int8);mu[0]=0
    for p in range(2,2*maxj+1):
        if ph[p]==p:
            ph[p::p]-=ph[p::p]//p
            if p<=maxj:
                mu[p::p]*=-1
                if p*p<=maxj:mu[p*p::p*p]=0
    b=np.longdouble(1)/ph[2*np.arange(1,maxj+1)]
    k=9/(2*pi*pi);rows=[]
    for j in [100,300,1000,3000,10000,100000,1000000]:
        terms=[]
        for d0 in np.flatnonzero(mu[1:j+1]):
            d=int(d0)+1
            s=np.sum(b[d-1:j:d],dtype=np.longdouble)
            terms.append(int(mu[d])*s*s/2)
        w=float(np.sum(terms,dtype=np.longdouble))
        rows.append({'J':j,'W':w,'W_over_log_squared':w/log(j)**2,
                     'residual_over_log':(w-k*log(j)**2)/log(j)})
    last=[r['W'] for r in rows[-3:]]
    estimate=(last[2]-2*last[1]+last[0])/(2*log(10)**2)
    output={'exact_cross_checks':exact,'numeric':rows,'predicted_coefficient':k,
            'second_log_difference_coefficient':estimate,
            'warning':'Finite numerics do not prove an asymptotic; no rigorous floating-point intervals.'}
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
```
