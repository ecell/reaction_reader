・pybngl.py 用テストデータ

  - testODE_1.py : 基本的なケース

  - testODE_2.py : testODE_1.py の初期値を変更

  - testODE_3.py : ルールに適合する分子が複数存在するケース
    - L(r) + R(l) <> L(r[1]).R(l[1])、初期分子[L(r), R(l, d, Y(U)], R(l, d, Y(pU)]

  - testODE_4.py : 分子の初期値が 0 

  - testODE_5.py : testODE_1.py に反応ルールをひとつ追加

  - testODE_6.py : 反応条件を設定
    - [include_reactants], [include_products], [exclude_reactants], [exclude_products]

  - testODE_7.py : 複数の反応条件を設定

  - testODE_8.py : 不完全なルールが与えられたときにエラー表示して終了
    - L(r) + R() > L(r[1]).R(l[1]) 

  - testODE_9.py : 上記ルールが与えられたときに解釈してシミュレーション実行
    - m.disallow_implicit_disappearance = False にして実行

  - testODE_10.py : 複数のルールを展開中に同一のルールが出てきたときにエラー表示して終了
    - L(r) + R(l) > L(r[1]).R(l[1])
      L(r) + R(l, Y(U)) > L(r[1]).R(l[1], Y(U))

  - testODE_11.py : 3 個以上の反応物/生成物が存在するケース
    - L(r) + R(l, Y(U)) + A(SH2) <> L(r[1]).R(l[1], Y(U)[2]).A(SH2[2])

  - testODE_12.py : 生成物/反応物に同一な分子が含まれているケース
    - R(d) + R(d) <> R(d[1]).R(d[1])

  - testODE_13.py : 分子種、反応式が限りなく増大するケース
    - R(r2) + R(r1, r2) <> R(r2[1]).R(r1[1], r2)

  - testODE_14.py : 複雑なケース
    - http://vcell.org/bionetgen/models/icsb2009-sample.bngl

  - testODE_15.py : 分子が消滅するケース
    - L(r) + R(l, d, Y(U)) > R(l, d, Y(U))

  - testODE_16.py : 分子が生成されるケース
    - L(r) > L(r) + R(l, d, Y(U))

  - testODE_17.py : 分子が消えるときにエラー表示して終了
    - R(Y(U)[1]).A(SH2[1]) > A(SH2[1])

  - testODE_18.py : 上記ルールが与えられたときに解釈してシミュレーション実行
    - m.disallow_implicit_disappearance = False にして実行

  - testODE_C.py : 反応条件を式の双方向に設定
