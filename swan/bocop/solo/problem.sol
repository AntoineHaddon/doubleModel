# **************************** 
# **************************** 
# *****    DEFINITION    ***** 
# **************************** 
# **************************** 
# # #
# ********************** 
# ** problem.def
# ********************** 
# # #
# # This file defines all dimensions and parameters 
# # values for your problem :
# # #
# # Initial and final time :
# time.free string none
# time.initial double 0
# time.final double 100
# # #
# # Dimensions :
# state.dimension integer 3
# control.dimension integer 1
# algebraic.dimension integer 0
# parameter.dimension integer 0
# constant.dimension integer 0
# boundarycond.dimension integer 4
# constraint.dimension integer 0
# # #
# # Discretization :
# discretization.steps integer 100
# discretization.method string euler_imp
# # #
# # Optimization :
# optimization.type string single
# batch.type integer 0
# batch.index integer 0
# batch.nrange integer 1
# batch.lowerbound double 0
# batch.upperbound double 0
# batch.directory string none
# # #
# # Initialization :
# initialization.type string from_init_file
# initialization.file string none
# # #
# # Parameter identification :
# paramid.type string false
# paramid.separator string ,
# paramid.file string no_directory
# paramid.dimension integer 0
# # #
# # Names :
# state.0 string s
# state.1 string b
# state.2 string itot
# control.0 string i
# boundarycond.0 string s0
# boundarycond.1 string b0
# boundarycond.2 string itot0
# boundarycond.3 string itotF
# # #
# # Solution file :
# solution.file string problem.sol
# # #
# # #
# ********************** 
# ** problem.bounds
# ********************** 
# # #
# # This file contains all the bounds of your problem.
# # Bounds are stored in standard format : 
# # [lower bound]  [upper bound] [type of bound]
# # #
# # Dimensions (i&f conditions, y, u, z, p, path constraints) :
# 4 3 1 0 0 0
# # #
# # Bounds for the initial and final conditions :
# 0.4 0.4 equal
# 0 0 equal
# 0 0 equal
# -2e+19 50 upper
# # #
# # Bounds for the state variables :
# 0 1 both
# 0 2e+19 lower
# -2e+19 2e+19 free
# # #
# # Bounds for the control variables :
# 0 10 both
# # #
# # Bounds for the algebraic variables :
# # #
# # Bounds for the optimization parameters :
# # #
# # Bounds for the path constraints :
# # #
# ********************** 
# ** problem.constants
# ********************** 
# # #
# # This file contains the values of the constants of your problem.
# # Number of constants used in your problem : 
# 0
# # #
# # Values of the constants : 
# # #
# ********************** 
# ** init/state.0.init
# ********************** 
# # #
# # Starting point file.
# # This file contains the values of the initial points
# # for variable s
# # #
# # Type of initialization : 
# constant
# # #
# # Constant value for the starting point :
# 0.1
# # #
# ********************** 
# ** init/state.1.init
# ********************** 
# # #
# # Starting point file.
# # This file contains the values of the initial points
# # for variable b
# # #
# # Type of initialization : 
# constant
# # #
# # Constant value for the starting point :
# 0.1
# # #
# ********************** 
# ** init/state.2.init
# ********************** 
# # #
# # Starting point file.
# # This file contains the values of the initial points
# # for variable itot
# # #
# # Type of initialization : 
# constant
# # #
# # Constant value for the starting point :
# 0.1
# # #
# ********************** 
# ** init/control.0.init
# ********************** 
# # #
# # Starting point file.
# # This file contains the values of the initial points
# # for variable i
# # #
# # Type of initialization : 
# constant
# # #
# # Constant value for the starting point :
# 0.1
# # #
# discretization.stages integer 1
# discretization.steps.after.merge 100
# # #
# # #
# **************************** 
# **************************** 
# *****     SOLUTION     ***** 
# **************************** 
# **************************** 
# # #
# Objective value : 
-949.273111785489
# L2-norm of the constraints : 
4.49163051240757e-13
# Inf-norm of the constraints : 
1.13686837721616e-13
# Number of stages of discretization method : 
1

0
0.01
0.01
0.02
0.02
0.03
0.03
0.04
0.04
0.05
0.05
0.06
0.06
0.07
0.07
0.08
0.08
0.09
0.09
0.1
0.1
0.11
0.11
0.12
0.12
0.13
0.13
0.14
0.14
0.15
0.15
0.16
0.16
0.17
0.17
0.18
0.18
0.19
0.19
0.2
0.2
0.21
0.21
0.22
0.22
0.23
0.23
0.24
0.24
0.25
0.25
0.26
0.26
0.27
0.27
0.28
0.28
0.29
0.29
0.3
0.3
0.31
0.31
0.32
0.32
0.33
0.33
0.34
0.34
0.35
0.35
0.36
0.36
0.37
0.37
0.38
0.38
0.39
0.39
0.4
0.4
0.41
0.41
0.42
0.42
0.43
0.43
0.44
0.44
0.45
0.45
0.46
0.46
0.47
0.47
0.48
0.48
0.49
0.49
0.5
0.5
0.51
0.51
0.52
0.52
0.53
0.53
0.54
0.54
0.55
0.55
0.56
0.56
0.57
0.57
0.58
0.58
0.59
0.59
0.6
0.6
0.61
0.61
0.62
0.62
0.63
0.63
0.64
0.64
0.65
0.65
0.66
0.66
0.67
0.67
0.68
0.68
0.69
0.69
0.7
0.7
0.71
0.71
0.72
0.72
0.73
0.73
0.74
0.74
0.75
0.75
0.76
0.76
0.77
0.77
0.78
0.78
0.79
0.79
0.8
0.8
0.81
0.81
0.820000000000001
0.820000000000001
0.830000000000001
0.830000000000001
0.840000000000001
0.840000000000001
0.850000000000001
0.850000000000001
0.860000000000001
0.860000000000001
0.870000000000001
0.870000000000001
0.880000000000001
0.880000000000001
0.890000000000001
0.890000000000001
0.900000000000001
0.900000000000001
0.910000000000001
0.910000000000001
0.920000000000001
0.920000000000001
0.930000000000001
0.930000000000001
0.940000000000001
0.940000000000001
0.950000000000001
0.950000000000001
0.960000000000001
0.960000000000001
0.970000000000001
0.970000000000001
0.980000000000001
0.980000000000001
0.990000000000001
0.990000000000001
1
1

# State 0
0.4
0.383936059789124
0.377769276522587
0.375401174636728
0.373680895506119
0.37196618069016
0.370256617411497
0.368551755809961
0.366851105328349
0.365154130794879
0.363460248187171
0.36176882006444
0.36007915065718
0.358390480607177
0.35670198135549
0.355012749182174
0.353321798909339
0.351628057288875
0.349930356108092
0.348227425060897
0.346517884449286
0.344800237800005
0.34307286450446
0.341334012616392
0.339581791971364
0.337814167824491
0.336028955237466
0.334223814482015
0.332396247762986
0.33054359759875
0.328663047227011
0.326751623427698
0.324806202167909
0.322823517473117
0.320800173909749
0.318732663022847
0.316617384004833
0.314450668774599
0.312228811518604
0.309948102587899
0.307604866460098
0.305195503269399
0.302716533190386
0.300164642745058
0.297536731902732
0.294829960675926
0.292041793798999
0.289170042025476
0.286212898605997
0.283168969618143
0.280037297012727
0.276817373518318
0.273509148930055
0.270113027968483
0.2666298617576
0.263060942952049
0.259408054890204
0.2556738396411
0.251863870854789
0.247996418488668
0.24792732174155
0.248149909713988
0.248363795217119
0.248569320941349
0.248766753311377
0.248956299531432
0.249138121782588
0.249312349214283
0.249479088168479
0.249638430931651
0.249790463205529
0.246282123121353
0.241844953104197
0.237618594147078
0.233621498593217
0.22984972987794
0.226294971793537
0.222948008629262
0.219799414021928
0.216839749212878
0.214059661176214
0.211449950860726
0.209001626030399
0.206705942722
0.204554437178475
0.202538949584641
0.200651640732734
0.198885002614998
0.197231863825099
0.195685390542675
0.194239083779223
0.192886773483788
0.191622610047419
0.190441053706984
0.189336862329364
0.188305078050293
0.187341013239839
0.186440236258886
0.185598557449003
0.184812015754684
0.184076866309049

# State 1
0
0.204042020500636
0.429368164669384
0.678178471321519
0.95289597149704
1.25618832542604
1.59099134747993
1.96053453672906
2.36836872681552
2.81839596146427
3.31490169022582
3.86258936195388
4.46661746989158
5.13263907072206
5.86684375901273
6.67600202645777
7.56751187036556
8.54944743599883
9.63060938065896
10.8205765318567
12.1297582757488
13.5694469538159
15.151869364669
16.8902362639512
18.7987885298452
20.8928384176956
23.188804069871
25.704235184094
28.4578274861451
31.4694234158857
34.7599962377219
38.3516146508176
42.2673849271826
46.5313676767606
51.1684665588156
56.2042866583854
61.6649608515035
67.5769433116102
73.9667703680765
80.8607902051443
88.2848643537784
96.2640455237143
104.822237967079
113.981848153918
123.763434951771
134.18536960566
145.263516485257
157.010945695246
169.437688158975
182.550542656168
196.352942541989
210.844887539056
226.022942999613
241.880304505098
258.406914488356
275.589572383709
293.411754303283
311.851661920119
330.870769902369
350.359489356882
370.395631321199
390.970303430053
412.057041396343
433.628932156966
455.658908875712
478.120018676722
500.985659855178
524.229786858693
547.82708267237
571.753099345682
595.984368263085
620.252975724981
643.903205650254
666.445941612312
687.772218637943
707.89818730641
726.864911072718
744.718964540118
761.508557320421
777.282388822246
792.089062690973
805.976670375073
818.992463282048
831.182591121141
842.591895989004
853.263754679129
863.239962779783
872.560654838382
881.264255507834
889.387457189603
896.965220228603
904.030792166731
910.615742903075
916.750012833033
922.46197115883
927.778481612371
932.724972854782
937.325510869163
941.60287079485
945.578605901311
949.273111785489

# State 2
0
-9.99777433216152e-09
-1.99953682897791e-08
-2.99923182498838e-08
-3.99822408364806e-08
-4.99719584989108e-08
-5.99614617751025e-08
-6.9950740557917e-08
-7.99397840376601e-08
-8.99285806383294e-08
-9.99171179467945e-08
-1.09905382633988e-07
-1.19893360367047e-07
-1.2988103571118e-07
-1.39868392019847e-07
-1.49855411311609e-07
-1.59842074131748e-07
-1.69828359396423e-07
-1.79814244216772e-07
-1.89799703699903e-07
-1.99784710723185e-07
-2.09769235677582e-07
-2.19753246175004e-07
-2.29736706713654e-07
-2.3971957829419e-07
-2.49701817978046e-07
-2.59683378377463e-07
-2.69664207064515e-07
-2.79644245883581e-07
-2.89623430148146e-07
-2.99601687698229e-07
-3.09578937788879e-07
-3.19555089772557e-07
-3.29530041528268e-07
-3.39503677577153e-07
-3.49475866806672e-07
-3.59446459701787e-07
-3.69415284949161e-07
-3.79382145235485e-07
-3.89346811998123e-07
-3.99309018796507e-07
-4.09268452842749e-07
-4.1922474403817e-07
-4.29177450573885e-07
-4.39126039709409e-07
-4.49069861642568e-07
-4.59008113247041e-07
-4.68939786549448e-07
-4.78863593509735e-07
-4.88777852674582e-07
-4.98680311863899e-07
-5.08567858021048e-07
-5.1843601546165e-07
-5.28278015767789e-07
-5.38082910846084e-07
-5.47831248101121e-07
-5.57483270064066e-07
-5.66936686280389e-07
-5.75777651858961e-07
-5.74450784281681e-07
3.87835297808471
8.12813692212721
12.4450045070832
16.825280006058
21.2651953394836
25.760945932474
30.3087392763176
34.9048365775093
39.5455878745295
44.2274610240623
48.9470649824026
50.0000007885767
50.0000007793592
50.0000007695565
50.0000007596544
50.000000749717
50.0000007397619
50.0000007297964
50.000000719824
50.0000007098466
50.0000006998657
50.0000006898819
50.0000006798959
50.0000006699081
50.0000006599189
50.0000006499284
50.0000006399369
50.0000006299445
50.0000006199513
50.0000006099575
50.000000599963
50.0000005899681
50.0000005799727
50.0000005699769
50.0000005599807
50.0000005499842
50.0000005399874
50.0000005299904
50.0000005199931
50.0000005099956
50.0000004999979

# Control 0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
1.32686757728032e-09
3.87835355253549
4.2497839440425
4.31686758495597
4.38027549897479
4.43991533342566
4.49575059299034
4.54779334384359
4.59609730119171
4.64075129702021
4.68187314953275
4.71960395834032
1.05293580617413
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0

# Parameters

# Boundary conditions
0.4 0.4 0.4 4
0 -4.40032687095229e-41 0 4
0 0 0 4
-2e+19 50.0000004999979 50 2

# Dynamic constraint 0
0 0 4
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
5.55111512312578e-17
0
0
0
0
0
0
-5.55111512312578e-17
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
2.77555756156289e-17
-2.77555756156289e-17
0
0
0
0
-2.77555756156289e-17
0
0
0
0
0
0
0
0
0
0
0
0
0
-2.77555756156289e-17
0
0
0
0
2.77555756156289e-17
-2.77555756156289e-17
0
2.77555756156289e-17
-2.77555756156289e-17
0
2.77555756156289e-17
0
0
0
0
-2.77555756156289e-17
2.77555756156289e-17
-2.77555756156289e-17

# Dynamic constraint 1
0 0 4
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
5.6843418860808e-14
-5.6843418860808e-14
5.6843418860808e-14
-5.6843418860808e-14
0
5.6843418860808e-14
0
-5.6843418860808e-14
0
0
0
0
0
0
0
1.13686837721616e-13
0
1.13686837721616e-13
0
0
1.13686837721616e-13
-1.13686837721616e-13
1.13686837721616e-13
-1.13686837721616e-13
0
0
0
1.13686837721616e-13
1.13686837721616e-13
1.13686837721616e-13
0
0
0
1.13686837721616e-13
0
0
0
0
0
-1.13686837721616e-13
1.13686837721616e-13
0
1.13686837721616e-13
0
0
-1.13686837721616e-13
0

# Dynamic constraint 2
0 0 4
0
0
0
0
6.61744490042422e-24
0
1.32348898008484e-23
0
0
-1.32348898008484e-23
0
0
-2.64697796016969e-23
2.64697796016969e-23
0
0
-2.64697796016969e-23
2.64697796016969e-23
0
0
2.64697796016969e-23
-2.64697796016969e-23
0
0
0
-5.29395592033938e-23
5.29395592033938e-23
0
0
-5.29395592033938e-23
5.29395592033938e-23
0
0
5.29395592033938e-23
0
0
0
0
0
0
0
0
0
0
0
0
5.29395592033938e-23
1.05879118406788e-22
0
0
-1.05879118406788e-22
0
1.05879118406788e-22
0
0
0
0
0
0
0
0
0
0
0
-3.5527136788005e-15
0
0
0
7.105427357601e-15
-7.105427357601e-15
-7.105427357601e-15
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0

# Dimension of the constraints multipliers :
604

# Constraint Multipliers : 

# Multipliers associated to the boundary conditions
209.818591827559
1.00100000015114
-4.7028520207559
4.7028520207559

# Adjoint state 0
-546.649256808514
-1424.20638221878
-3710.53389308656
-3730.31052111436
-3750.17381538813
-3770.12210520957
-3790.15348458367
-3810.26578823598
-3830.45656550305
-3850.72305197363
-3871.06213876744
-3891.47033935313
-3911.94375382798
-3932.47803061087
-3953.06832553834
-3973.70925840343
-3994.39486703951
-4015.11855912968
-4035.87306201733
-4056.65037090829
-4077.44169599106
-4098.23740915983
-4119.02699120726
-4139.79898055927
-4160.5409248508
-4181.23933688714
-4201.87965679295
-4222.44622241292
-4242.92225028137
-4263.28982970763
-4283.5299327091
-4303.62244264142
-4323.54620439695
-4343.27909893935
-4362.79814468392
-4382.07962779092
-4401.09926279204
-4419.83238410399
-4438.25416790066
-4456.33988253638
-4474.06516427924
-4491.4063135915
-4508.34060567309
-4524.8466075714
-4540.90449297573
-4556.49634497663
-4571.60643667696
-4586.22147963712
-4600.33083060038
-4613.9266470528
-4627.00397862533
-4639.56075888377
-4651.59754745824
-4663.1163022202
-4674.1145748979
-4684.55656396031
-4694.22414930191
-4701.96916411126
-4702.85202075498
-4702.85202075531
-4702.85202075536
-4702.85202075542
-4702.85202075547
-4702.85202075551
-4702.85202075556
-4702.8520207556
-4702.85202075563
-4702.85202075567
-4702.8520207557
-4702.85202074754
-4690.07214479611
-4652.16338955622
-4600.75239492946
-4543.01441060424
-4480.33360862666
-4412.72914468507
-4339.94117930883
-4261.63448957298
-4177.43664119744
-4086.94453089102
-3989.72434802989
-3885.30997209801
-3773.20088978743
-3652.8598892158
-3523.71061184385
-3385.13501857405
-3236.47084929998
-3077.00920205635
-2905.99242359498
-2722.61258417835
-2526.01089941875
-2315.27855078224
-2089.45942952971
-1847.55536898407
-1588.53441863337
-1311.342633885
-1014.91969539158
-698.218428462888
-360.227974907686
-4.20690724030247e-11

# Adjoint state 1
-1.00000000015114
-1.00000000010213
-1.00000000007884
-1.00000000006409
-1.0000000000536
-1.00000000004564
-1.00000000003935
-1.00000000003425
-1.00000000003003
-1.00000000002648
-1.00000000002346
-1.00000000002088
-1.00000000001864
-1.00000000001669
-1.00000000001498
-1.00000000001349
-1.00000000001217
-1.000000000011
-1.00000000000996
-1.00000000000903
-1.00000000000821
-1.00000000000747
-1.00000000000681
-1.00000000000622
-1.00000000000569
-1.00000000000521
-1.00000000000478
-1.00000000000439
-1.00000000000404
-1.00000000000372
-1.00000000000343
-1.00000000000317
-1.00000000000294
-1.00000000000272
-1.00000000000253
-1.00000000000235
-1.00000000000219
-1.00000000000204
-1.0000000000019
-1.00000000000178
-1.00000000000167
-1.00000000000156
-1.00000000000147
-1.00000000000138
-1.0000000000013
-1.00000000000122
-1.00000000000116
-1.00000000000109
-1.00000000000103
-1.00000000000098
-1.00000000000093
-1.00000000000088
-1.00000000000084
-1.0000000000008
-1.00000000000076
-1.00000000000072
-1.00000000000069
-1.00000000000065
-1.00000000000062
-1.0000000000006
-1.00000000000057
-1.00000000000054
-1.00000000000052
-1.0000000000005
-1.00000000000047
-1.00000000000045
-1.00000000000043
-1.00000000000042
-1.0000000000004
-1.00000000000038
-1.00000000000036
-1.00000000000035
-1.00000000000033
-1.00000000000032
-1.0000000000003
-1.00000000000029
-1.00000000000027
-1.00000000000026
-1.00000000000025
-1.00000000000024
-1.00000000000022
-1.00000000000021
-1.0000000000002
-1.00000000000019
-1.00000000000017
-1.00000000000016
-1.00000000000015
-1.00000000000014
-1.00000000000013
-1.00000000000012
-1.00000000000011
-1.0000000000001
-1.00000000000008
-1.00000000000007
-1.00000000000006
-1.00000000000005
-1.00000000000004
-1.00000000000003
-1.00000000000002
-1.00000000000001

# Adjoint state 2
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559
4.7028520207559

# Coefficients of discretization method : 

# a(i,j) by column : 
1

# b  : 
1

# c  : 
1

# z_L and z_U : 

# z_L corresponding to state variable 0 : 
2.4999999375e-11
2.60460029334896e-11
2.64711832241611e-11
2.66381684694919e-11
2.67608000640436e-11
2.68841638038275e-11
2.70082944089645e-11
2.71332304649881e-11
2.72590148487065e-11
2.73856951977367e-11
2.7513324427482e-11
2.76419612994816e-11
2.77716710451919e-11
2.79025260493331e-11
2.80346065969505e-11
2.81680016882676e-11
2.83028099252316e-11
2.84391404733475e-11
2.85771141019269e-11
2.87168643052241e-11
2.88585385060498e-11
2.90022993423146e-11
2.91483260355228e-11
2.929681583848e-11
2.94479855573747e-11
2.9602073140919e-11
2.97593393263976e-11
2.9920069329283e-11
3.00845745595922e-11
3.02531943444482e-11
3.04262976325109e-11
3.06042846522227e-11
3.07875884923977e-11
3.09766765708634e-11
3.11720519549743e-11
3.13742544972263e-11
3.1583861750335e-11
3.18014896293739e-11
3.20277927942797e-11
3.22634647344854e-11
3.25092375487655e-11
3.27658814275323e-11
3.30342038615007e-11
3.33150486193103e-11
3.36092945565328e-11
3.39178543384651e-11
3.42416731780037e-11
3.45817277064327e-11
3.49390251079349e-11
3.53146026569899e-11
3.57095278006852e-11
3.61248989239806e-11
3.6561846919932e-11
3.70215376318369e-11
3.75051749981385e-11
3.80140035523357e-11
3.8549302637266e-11
3.91123300800509e-11
3.97039860025244e-11
4.03231613493053e-11
4.03343993167498e-11
4.02982197678152e-11
4.0263515818088e-11
4.02302245499448e-11
4.0198296054056e-11
4.01676905430567e-11
4.01383759621613e-11
4.01103259843008e-11
4.00835183124109e-11
4.00579332360834e-11
4.00335524076291e-11
4.06038386677145e-11
4.13488040918659e-11
4.20842468791305e-11
4.2804277997417e-11
4.35066839984696e-11
4.41901093905989e-11
4.48535046935263e-11
4.54960245892289e-11
4.61170038017921e-11
4.67159458157253e-11
4.72925128919111e-11
4.78465154145756e-11
4.83779004344837e-11
4.88867396330666e-11
4.93732169875247e-11
4.98376164037639e-11
5.02803095543354e-11
5.07017441251296e-11
5.11024326406978e-11
5.14829420042819e-11
5.18438838544917e-11
5.21859058055118e-11
5.2509683601569e-11
5.28159141796975e-11
5.3105309599118e-11
5.33785917630957e-11
5.36364878327518e-11
5.38797262147386e-11
5.4109032998068e-11
5.43251287207356e-11

# z_L corresponding to state variable 1 : 
0.001
4.90095103222806e-11
2.32900354286855e-11
1.47453808627394e-11
1.04943248729936e-11
7.96058976029934e-12
6.2853892656209e-12
5.10064972672067e-12
4.2223154885273e-12
3.54811747577278e-12
3.01668070559039e-12
2.58893685997523e-12
2.23883062407277e-12
1.94831544605572e-12
1.70449399945122e-12
1.49790247896717e-12
1.3214382954516e-12
1.16966623435764e-12
1.03835589154922e-12
9.24165173761078e-13
8.24418736501039e-13
7.36949709642986e-13
6.59984570400144e-13
5.92058029136184e-13
5.31949172086509e-13
4.7863290737672e-13
4.31242593001183e-13
3.89040946929154e-13
3.51397168366229e-13
3.17768770805452e-13
2.87687027603042e-13
2.60745214730597e-13
2.36589039394368e-13
2.14908791577284e-13
1.95432864624762e-13
1.77922371989198e-13
1.62166647968196e-13
1.47979466197639e-13
1.35195844686548e-13
1.23669333101906e-13
1.13269698855683e-13
1.03880944796754e-13
9.53996040628963e-14
8.77332677183737e-14
8.07993088030309e-14
7.45237728125092e-14
6.88404097688664e-14
6.36898271969703e-14
5.90187467030788e-14
5.47793496198316e-14
5.0928699463479e-14
4.74282308489617e-14
4.42432961311131e-14
4.13427625703018e-14
3.86986548692512e-14
3.62858431585138e-14
3.40817975183188e-14
3.20665278424613e-14
3.02232802330907e-14
2.8542112611451e-14
2.69981586015474e-14
2.55773901803089e-14
2.42684846881155e-14
2.30611918582719e-14
2.19462404991805e-14
2.09152505838754e-14
1.99606511745089e-14
1.90756043446741e-14
1.82539350757107e-14
1.74900669734352e-14
1.67789635640543e-14
1.61224538877065e-14
1.55302845398107e-14
1.50049679583272e-14
1.45396974883029e-14
1.41263251964372e-14
1.37577146007836e-14
1.34278841764705e-14
1.31318287939619e-14
1.28653371588974e-14
1.2624842925997e-14
1.24073070194728e-14
1.22101245716031e-14
1.20310508264991e-14
1.18681416798386e-14
1.17197055951865e-14
1.15842644352127e-14
1.14605213338867e-14
1.13473341706387e-14
1.12436935320482e-14
1.11487042912766e-14
1.10615701218782e-14
1.09815804062533e-14
1.09080991108884e-14
1.08405552885061e-14
1.07784349368756e-14
1.07212739992217e-14
1.06686523346842e-14
1.06201885211462e-14
1.05755353785341e-14
1.05343761197298e-14

# z_L corresponding to state variable 2 : 
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0

# z_L corresponding to control variable 0 : 
4.49303342892934
4.15620276394839
3.27864563853812
0.992318127670343
0.972541499642543
0.95267820536878
0.932729915547331
0.912698536173232
0.89258623252093
0.872395455253859
0.852128968783275
0.831789881989465
0.811381681403778
0.790908266928926
0.770373990146036
0.749783695218565
0.729142762353483
0.708457153717403
0.687733461627225
0.666978958739578
0.646201649848617
0.625410324765847
0.604614611597082
0.583825029549646
0.563053040197635
0.542311095906109
0.521612683869773
0.500972363963963
0.480405798343995
0.459929770475538
0.43956219104928
0.419322088047815
0.399229578115489
0.379305816359966
0.35957292181756
0.340053876072992
0.320772392965995
0.301752757964873
0.283019636652924
0.26459785285626
0.246512138220535
0.228786856477678
0.211445707165419
0.194511415083821
0.178005413185513
0.161947527781188
0.146355675780283
0.131245584079953
0.116630541119796
0.102521190156532
0.0889253737041143
0.0758480421315862
0.0632912618731478
0.0512544732986759
0.0397357185367244
0.0287374458590229
0.0182954567966087
0.00862787145500696
0.000882856645665678
2.57841371054948e-12
2.35306079276989e-12
2.31649449051541e-12
2.28296142092224e-12
2.25229519630534e-12
2.22432267335926e-12
2.19886859888839e-12
2.17575898048319e-12
2.15482350559761e-12
2.13589724865549e-12
2.11882184757052e-12
9.49725505238792e-12
0.0127798759608129
0.0506886312006999
0.102099625827464
0.159837610152689
0.222518412130265
0.290122876071859
0.362910841448097
0.441217531183944
0.525415379559491
0.615907489865905
0.713127672727039
0.817542048658926
0.929651130969505
1.04999213154114
1.17914140891308
1.31771700218289
1.46638117145695
1.62584281870059
1.79685959716195
1.98023943657859
2.17684112133819
2.3875734699747
2.61339259122723
2.85529665177287
3.11431760212357
3.39150938687194
3.68793232536536
4.00463359229405
4.34262404584897

# z_L corresponding to parameters : 

# z_U corresponding to state variable 0 : 
1.66666663888889e-11
1.62320810957646e-11
1.60712087365305e-11
1.60102764107524e-11
1.59663017918283e-11
1.59227091492654e-11
1.58794837987834e-11
1.58366104168378e-11
1.57940729680105e-11
1.57518546273323e-11
1.57099376974041e-11
1.56683035202489e-11
1.5626932383904e-11
1.55858034238727e-11
1.55448945196847e-11
1.55041821869788e-11
1.54636414657213e-11
1.54232458054141e-11
1.53829669484353e-11
1.53427748129884e-11
1.53026373775298e-11
1.526252056899e-11
1.52223881576041e-11
1.51822016617263e-11
1.51419202666005e-11
1.51015007616994e-11
1.50608975018895e-11
1.50200623983257e-11
1.49789449455646e-11
1.493749229189e-11
1.4895649360188e-11
1.48533590268412e-11
1.48105623659494e-11
1.47671989656419e-11
1.47232073222574e-11
1.46785253166337e-11
1.46330907746413e-11
1.45868421113574e-11
1.45397190549416e-11
1.44916634423966e-11
1.44426200751128e-11
1.43925376176026e-11
1.4341369518398e-11
1.42890749280425e-11
1.42356195858189e-11
1.41809766446906e-11
1.41251274032264e-11
1.40680619142923e-11
1.40097794431596e-11
1.39502887523858e-11
1.38896081972189e-11
1.38277656231495e-11
1.37647980667952e-11
1.37007512754464e-11
1.36356790959737e-11
1.35696429286321e-11
1.35027121628906e-11
1.34349703103657e-11
1.33665511886989e-11
1.32978088308097e-11
1.32965870934054e-11
1.3300523596653e-11
1.33043083919109e-11
1.33079472872307e-11
1.33114447622822e-11
1.33148042658677e-11
1.331802846425e-11
1.33211194513753e-11
1.3324078928535e-11
1.33269083585223e-11
1.33296090975227e-11
1.32675635991773e-11
1.31899140011597e-11
1.31167940246975e-11
1.30483825566087e-11
1.29844788194002e-11
1.29248221301249e-11
1.28691515913475e-11
1.28172165614201e-11
1.27687786276967e-11
1.27236119318288e-11
1.26815030752966e-11
1.26422508600022e-11
1.26056659345917e-11
1.25715703772528e-11
1.25397972344775e-11
1.25101900303702e-11
1.2482602257873e-11
1.24568968607547e-11
1.24329457131428e-11
1.24106291017393e-11
1.23898352146516e-11
1.23704596399981e-11
1.23524048770829e-11
1.23355798628987e-11
1.23198995169032e-11
1.23052843072767e-11
1.22916598420489e-11
1.22789564884449e-11
1.22671090234318e-11
1.22560563177109e-11

# z_U corresponding to state variable 1 : 
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0

# z_U corresponding to state variable 2 : 
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0

# z_U corresponding to control variable 0 : 
9.99999989000222e-13
9.99999989000241e-13
9.99999989000305e-13
9.99999989001008e-13
9.99999989001028e-13
9.9999998900105e-13
9.99999989001072e-13
9.99999989001096e-13
9.9999998900112e-13
9.99999989001146e-13
9.99999989001174e-13
9.99999989001202e-13
9.99999989001233e-13
9.99999989001265e-13
9.99999989001298e-13
9.99999989001334e-13
9.99999989001372e-13
9.99999989001412e-13
9.99999989001454e-13
9.99999989001499e-13
9.99999989001548e-13
9.99999989001599e-13
9.99999989001654e-13
9.99999989001713e-13
9.99999989001776e-13
9.99999989001844e-13
9.99999989001917e-13
9.99999989001996e-13
9.99999989002082e-13
9.99999989002174e-13
9.99999989002275e-13
9.99999989002385e-13
9.99999989002505e-13
9.99999989002637e-13
9.99999989002781e-13
9.99999989002941e-13
9.99999989003118e-13
9.99999989003314e-13
9.99999989003533e-13
9.99999989003779e-13
9.99999989004057e-13
9.99999989004371e-13
9.99999989004729e-13
9.99999989005141e-13
9.99999989005618e-13
9.99999989006175e-13
9.99999989006833e-13
9.99999989007619e-13
9.99999989008574e-13
9.99999989009754e-13
9.99999989011245e-13
9.99999989013184e-13
9.999999890158e-13
9.99999989019511e-13
9.99999989025166e-13
9.99999989034798e-13
9.99999989054658e-13
9.99999989115904e-13
9.99999990132686e-13
1.63354743245377e-12
1.73906505925686e-12
1.75959296629607e-12
1.77944662949777e-12
1.79853373101741e-12
1.81677810703621e-12
1.83411973302524e-12
1.85051441010473e-12
1.86593314989219e-12
1.88036128004079e-12
1.89379730833166e-12
1.11768504970963e-12
9.99999989078248e-13
9.99999989019728e-13
9.99999989009795e-13
9.99999989006256e-13
9.99999989004494e-13
9.99999989003447e-13
9.99999989002756e-13
9.99999989002266e-13
9.99999989001903e-13
9.99999989001624e-13
9.99999989001402e-13
9.99999989001223e-13
9.99999989001076e-13
9.99999989000953e-13
9.99999989000848e-13
9.99999989000759e-13
9.99999989000682e-13
9.99999989000615e-13
9.99999989000556e-13
9.99999989000505e-13
9.9999998900046e-13
9.99999989000419e-13
9.99999989000383e-13
9.9999998900035e-13
9.99999989000321e-13
9.99999989000295e-13
9.99999989000271e-13
9.9999998900025e-13
9.99999989000231e-13

# z_U corresponding to parameters : 

# Ipopt status : 
0

# Ipopt iterations : 
99
