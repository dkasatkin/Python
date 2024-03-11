import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl
import matplotlib.lines as mlines
mpl.rcParams.update(mpl.rcParamsDefault)  # defaul parameter for rc

# Считывание данных из документа
# pathToFile = 'Some_path'
pathToFile = 'Some_path'

numGraphs = 32  # кол-во графиков

nameOfPlot = [  '0 Давление в ПГ 1-4'
              , '1 Давление в ПГ4 и ГПК'
              , '2 Весовой уровень 1-4'
              , '3 Давление над а.з.'
              , '4 Относителья мощность тепловыделений 3600с'
              , '5 Реактивность а.з. по обратному уравнению кинетики'
              , '6 Расход теплоносителя на входных патрубках реактора'
              , '7 Расход воды через а.з.'
              , '8 Максимальная энтальпия топлива'
              , '9 Максимальная температура топлива'
              ,'10 Максимальная температура оболочки твэла'
              ,'11 Минимальный DNBR'
              ,'12 Температура холодной нитки'
              ,'13 Температура горячей нитки'
              ,'14 Коэффициенты пространственной неравномерности'
              ,'15 Относительная частота вращения ГЦН'
              ,'16 Аксиальный офсет'
              ,'17 Положение групп ОР СУЗ'
              ,'18 Максимальное энерговыделение топлива'
              ,'19 Расход пит. воды в ПГ'
              ,'20 Расход пара через БРУ-А'
              ,'21 Уровень в КД'
              ,'22 Мощность САР ПГ'
              ,'23 Разность температуры насыщения первого контура и ПГ'
              ,'24 Расход от системы аварийного ввода бора'
              ,'25 Масса выброса через БРУ-А'
              ,'26 Масса выброса в разрыв'
              ,'27 Расход пара в разрыв ЗА БЗОК'
              ,'28 Концентрация борной кислоты в нитках'
              ,'29 Концентрация борной кислоты в а.з.'
              ,'30 Суммарный расход на турбину'
              ,'31 Относительная мощность тепловыделений 200с']

                 #1         #2             #3       #4        #5                   #6            #7         #8        #9           #10
nameOfYAxis = ['P, MPa',  'P, MPa',       'H, m',  'P, MPa', 'N, %',         'Ro, rel.units', 'G, ks/s', 'G, ks/s', 'I, J/g',     'T, °C',
               'T, °C',   'n, rel.units', 'T, °C', 'T, °C',  'K, rel.units', 'w, rel.units',  'AO, %',   'H, cm'  , 'Qlin, W/cm', 'G, kg/s',
               'G, kg/s', 'H, m',         'Q, MW', 'T, °C',  'G, kg/s',      'M, t',          'M, t',    'G, kg/s', 'Cb, g/kg',   'Cb, g/kg',
               'G, kg/s', 'N, %']

someE       = [  1.0E6,   1.0E6,            1.0,    1.0E6,     1.0,                1.0,          1.0,        1.0,       1.0,          1.0,
                   1.0,     1.0,            1.0,      1.0,     1.0,                1.0,          1.0,        1.0,       1.0,          1.0,
                   1.0,     1.0,            1.0E6,    1.0,     1.0,               1.0E3,         1.0E3,      1.0,       1.0,          1.0E3,
                   1.0,     1.0 ]

xTicksMax   = [ 3600.0,  3600.0,           3600.0,   3600.0,   3600.0,            600.0,         3600.0,     3600.0,    200.0,       200.0,
                 600.0,   200.0,           3600.0,   3600.0,   3600.0,           3600.0,          300.0,      200.0,    200.0,      3600.0,
                3600.0,  3600.0,           3600.0,   3600.0,   3600.0,           3600.0,         3600.0,      600.0,    3600.0,     3600.0,
                 600.0,   200.0 ]

xTicksMin   = 0.0

xTicksStep  = [  400.0,   400.0,            400.0,    400.0,    400.0,             60.0,          400.0,      400.0,     25.0,        25.0,
                  60.0,    25.0,            400.0,    400.0,    400.0,            400.0,           30.0,       25.0,     25.0,       400.0,
                  400.0,  400.0,            400.0,    400.0,    400.0,            400.0,          400.0,       60.0,    400.0,       400.0,
                   60.0,   25.0 ]

yTicksMin  = [      0.0,    0.0,              0.0,    12.0,       0.0,            -0.08,            0.0,        0.0,     60.0,         0.0,
                  200.0,    0.5,            200.0,   270.0,       1.0,             0.00,         -100.0,        0.0,      0.0,         0.0,  
                    0.0,    2.0,              0.0,    25.0,       0.0,              0.0,            0.0,        0.0,      0.0,         0.0, 
                    0.0,    0.0 ]

yTicksMax  = [      7.5,    9.0,              2.5,    20.0,     125.0,             0.01,         4500.0,    18000.0,    600.0,      3000.0,
                  900.0,    5.0,            320.0,   330.0,       4.5,              1.0,          -20.0,      400.0,    600.0,       450.0, 
                  120.0,    9.0,             32.0,   275.0,       4.5,             40.0,          120.0,     4000.0,      0.6,         0.4, 
                 1750.0,  125.0 ]

yTicksStep = [     0.75,    1.0,              0.5,     1.0,      25.0,             0.01,          500.0,     2000.0,     60.0,       500.0,
                  100.0,    0.5,             20.0,    10.0,       0.5,              0.2,           10.0,       50.0,     60.0,        50.0, 
                   20.0,    1.0,              4.0,    25.0,       0.5,              5.0,           20.0,      500.0,      0.1,        0.05, 
                  250.0,   25.0 ]

                     #1     #2                 #3        #4         #5                 #6            #7           #8        #9           #10
firstInRange = [      1,     4,                 6,       29,        32,               39,             40,         56,       57,          59,
                     61,    63,                65,       69,        73,               76,             80,         89,       92,          94, 
                     98,   102,               104,      112,       116,              128,            131,        143,      133,         132, 
                    146,   32  ] 

numOfRange   = [      4,     2,                 4,        1,         3,                1,              4,          1,        2,           2,
                      2,     2,                 4,        4,         3,                4,              1,          2,        2,           4, 
                      4,     2,                 4,        4,         4,                1,              1,          1,        4,           1, 
                      1,     3 ]



acceptCriteria= [     0,     3,                 0,        2,         0,                0,              0,          0,        3,          34,
                      3,     3,                 0,        0,         0,                0,              0,          0,        0,           0, 
                      0,     0,                 0,        0,         0,                0,              0,          0,        0,           0, 
                      0,     0 ]

acceptCritValue =[    0,    8.73,              0,    19.51,         0,                0,              0,          0,    586.0, [2800,2672],
                  800.0,     1.0,              0,        0,         0,                0,              0,          0,        0,           0, 
                      0,       0,              0,        0,         0,                0,              0,          0,        0,           0, 
                      0,       0 ]

legendNumMarkers = [  4,     3,                 4,        2,         3,                1,              4,          1,        3,           4,
                      3,     3,                 4,        4,         3,                4,              1,          2,        2,           4, 
                      4,     2,                 4,        4,         4,                1,              1,          1,        4,           1, 
                      1,     3 ]

legendPosition   = [0.775, 0.705, 0.565] # 0.775, 0.705, 0.565

f = open(pathToFile, 'r')
# someE = 1.0 # 1.0E6

namesOfVars  = []  # np.array([])
valuesOfVars = []  # np.array([])

for count, line in enumerate(f):
    if count==0:
        numOfVars = int(line.strip())
        
    elif count <= numOfVars:
        namesOfVars.append(line.strip()) # = np.append(namesOfVars, line.strip())
        
    else:
        valuesOfVars.append(list(map(lambda x: float(x), line.split())))
        
f.close()       



# Построение графиков        
for nGraph in range(numGraphs):
    
    def transVarTime(someArray, col):
        xyArray = []
        for string in range(len(someArray)):
                xyArray.append(someArray[string][col])
        return(xyArray)

    def transVar(someArray, col):
        xyArray = []
        for string in range(len(someArray)):
                xyArray.append(someArray[string][col]/someE[nGraph])
        return(xyArray)
        
    sizeOfText = 48 # 48
    plt.rc('figure', figsize=[16.3*2, 8.07*2])
    plt.rc('font', family='serif', style='normal', size=sizeOfText)  # cmr10 не работает
    markersForGraph = ['o', 's', 'D', '^']
    colorsForGraph  = ['red', 'blue', 'green', 'black']
    numbersOfLines = [1, 2, 3, 4]
    legendParams = []

    fig, ax = plt.subplots()

    # Изменяемые параметры
    # setYticks = np.arange(0.0, 4500.0, 500.0) # Тики по оси Y
    # firstInRange  = 11
    # secondInRange = 9
    # nameOfPlot  = 'Расход пара в разрыв' 
    # nameOfYAxis = r'G, kg/s' # °

    for i in range(0, numOfRange[nGraph]):
        plt.plot(transVarTime(valuesOfVars, 0),
                 transVar(valuesOfVars, firstInRange[nGraph] + i),
                 linewidth=6.0,
                 color=colorsForGraph[i],
                 )  # Строим линии
    for i in range(0, numOfRange[nGraph]):    
        plt.plot(transVarTime(valuesOfVars, 0),
                 transVar(valuesOfVars, firstInRange[nGraph] + i),
                 linewidth=6.0,
                 linestyle='',
                 color=colorsForGraph[i],
                 marker=markersForGraph[i],
                 markersize=20,
                 markerfacecolor='white',
                 markeredgewidth=4,
                 fillstyle='full',
                 markevery=np.arange((i+1)**2*250 + 100, 36000, int(xTicksStep[nGraph]*10 + 2000))
                 )  # Строим маркеры
    
    for i in range(0, legendNumMarkers[nGraph]):    
        legendParams.append(mlines.Line2D([], [], color=colorsForGraph[i],
                                          marker=markersForGraph[i],
                                          linestyle='none',
                                          markersize=25,
                                          label=str(numbersOfLines[i]),
                                          markerfacecolor='white',
                                          markeredgewidth=4
                                          )  # close mlines.Line2D
                            )  # close append

    if acceptCriteria[nGraph] == 2:
        acceptY = np.ones(8, dtype=float) * acceptCritValue[nGraph]    
        acceptX = np.linspace(0.0, xTicksMax[nGraph], 8)
        plt.plot(acceptX, acceptY,
                 linewidth=6.0, color='blue', marker='s', markersize=20,
                 markerfacecolor='white', markeredgewidth=4, markevery=np.arange(1, 7, 2))  # Приёмочный критерий
        
    if acceptCriteria[nGraph] == 3:
        acceptY = np.ones(8, dtype=float) * acceptCritValue[nGraph]    
        acceptX = np.linspace(0.0, xTicksMax[nGraph], 8)
        plt.plot(acceptX, acceptY,
                 linewidth=6.0, color='green', marker='D', markersize=20,
                 markerfacecolor='white', markeredgewidth=4, markevery=np.arange(1, 7, 2))  # Приёмочный критерий

    if acceptCriteria[nGraph] == 4:
        acceptY = np.ones(5, dtype=float) * acceptCritValue[nGraph]    
        acceptX = np.linspace(0.0, xTicksMax[nGraph], 5)
        plt.plot(acceptX, acceptY,
                 linewidth=6.0, color='black', marker='^', markersize=20,
                 markerfacecolor='white', markeredgewidth=4, markevery=np.arange(1, 5, 2))  # Приёмочный критерий
    
    if acceptCriteria[nGraph] == 34:
        acceptY = np.ones(8, dtype=float) * acceptCritValue[nGraph][0]    
        acceptX = np.linspace(0.0, xTicksMax[nGraph], 8)
        plt.plot(acceptX, acceptY,
                 linewidth=6.0, color='green', marker='D', markersize=20,
                 markerfacecolor='white', markeredgewidth=4, markevery=np.arange(1, 7, 2))  # Приёмочный критерий
        
        acceptY = np.ones(5, dtype=float) * acceptCritValue[nGraph][1]    
        acceptX = np.linspace(0.0, xTicksMax[nGraph], 5)
        plt.plot(acceptX, acceptY,
                 linewidth=6.0, color='black', marker='^', markersize=20,
                 markerfacecolor='white', markeredgewidth=4, markevery=np.arange(1, 5, 2))  # Приёмочный критерий


    # Сетка и легенда
    if legendNumMarkers[nGraph] == 1:
        legendPosition = 0.565
        
    elif legendNumMarkers[nGraph] == 2:
        legendPosition = 0.635
        
    elif legendNumMarkers[nGraph] == 3:
        legendPosition = 0.705
        
    else:
        legendPosition = 0.775
        
    plt.grid(color='black', which='major', linestyle='-', linewidth=1.5)
    plt.legend(handles=legendParams, fontsize=sizeOfText, bbox_to_anchor=(legendPosition, -0.05),
               ncols=4, frameon=False) # 775, 705, 565

    # Настройки оси X
    plt.xlabel(r't, s', fontsize=sizeOfText+4*2)
    ax.xaxis.set_label_coords(1.00, -0.015)
    plt.xlim(0.0, xTicksMax[nGraph])
    plt.xticks(np.arange(0.0, xTicksMax[nGraph], xTicksStep[nGraph]))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(xTicksStep[nGraph]/5))
    ax.spines['left'].set_linewidth(4)
    ax.tick_params(which='major', width=4.0, length=18.0)
    ax.tick_params(which='minor', width=4.0, length=10.0)
    # ax.set_title('')
    # plt.semilogx()
    # plt.xscale('log')

    # Настройки осей верхней и правой
    ax.spines['right'].set_color('black')
    ax.spines['right'].set_linewidth(3)
    ax.spines['top'].set_color('black')
    ax.spines['top'].set_linewidth(3)

    # Настройки оси Y
    plt.ylabel(nameOfYAxis[nGraph], fontsize=sizeOfText, rotation=0)
    ax.yaxis.set_label_coords(0.0, 1.04)
    # plt.title(label= r'$P, MPa$', loc='left', size=24)
    if nGraph in [2, 4, 6, 15, 19, 20, 22, 24, 25, 27, 28, 29, 30, 31]:
        plt.ylim(yTicksMin[nGraph] - yTicksStep[nGraph]/10, yTicksMax[nGraph])
    else:
        plt.ylim(yTicksMin[nGraph], yTicksMax[nGraph])
    plt.yticks(np.arange(yTicksMin[nGraph], yTicksMax[nGraph] + yTicksStep[nGraph], yTicksStep[nGraph]))
    ax.spines['bottom'].set_linewidth(4)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(yTicksStep[nGraph]/5))
    ax.tick_params(which='major', width=4.0, length=18.0)
    ax.tick_params(which='minor', width=4.0, length=10.0)
    # ax.xaxis.set_zorder(10)

    plt.savefig('Some_path' + nameOfPlot[nGraph] + '.png', dpi=100,
                bbox_inches = 'tight', pad_inches=0.62)
   # plt.show()



