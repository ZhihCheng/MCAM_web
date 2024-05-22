import numpy as np
import sys
from sys_py_FeSiCr.model_load import *
from pymoo.core.problem import ElementwiseProblem
from pymoo.factory import get_sampling, get_crossover, get_mutation

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_termination
from pymoo.optimize import minimize
from pymoo.decomposition.asf import ASF

input_data = [sys for sys in sys.argv]
class customize(ElementwiseProblem):    # max mu and min Pcv
    def __init__(self,mode1, mode2, mode3 ,cus_par ,*args, **kwargs):
        super().__init__(n_var=4,
                         n_obj=2,
                         n_constr=0,
                         xl=np.array([0,100,300,0.045]),  # lower bound
                         xu=np.array([8000,200,1500,0.12])) # upper bound
        self.mode1 = mode1  # mu model selected
        self.mode2 = mode2  # Pcv model selected
        self.mode3 = mode3  # tensile model selected
        # the user input characteristic
        self.mu = cus_par[0]
        self.Pcv = cus_par[1]
        self.tensile = cus_par[2]

    def _evaluate(self,x, out, *args, **kwargs):
        f1 = np.abs(self.mu-np.float64(self.mode1.predict(np.array(x).reshape(1, -1))))   #mu
        f2 = np.abs(self.Pcv-np.float64(self.mode2.predict(np.array(x).reshape(1, -1))))  #Pcv
        f3 = np.abs(self.tensile - np.float64(self.mode3.predict(np.array(x).reshape(1, -1))))  # tensile
        out["F"] = [f1, f2, f3]
        
        
        
def FeSiCr_customize(input_data):
    mode = input_data[1]    # frequency mode selected
    cus_characteristic = [int(input_data[2]), int(input_data[3]), int(input_data[4])]

    # Multi type of model can be select (base on R2 score)
    ##############################################################################################
    model_mu_input = [  model_mu_xgb_50,      ## mu model
                        model_mu_xgb_200,
                        model_mu_cat_400,
                        model_mu_lgb_800]
    
    model_Pcv_input = [ model_Pcv_xgb_50,    ## Pcv model
                        model_Pcv_xgb_200,
                        model_Pcv_cat_400,
                        model_Pcv_cat_800]

    model_tensile_input = model_tensile_xgb # tensile model no relate to frequency
    ##############################################################################################


    problem = customize(mode1=model_mu_input[int(mode)],
                        mode2=model_Pcv_input[int(mode)],
                        mode3=model_tensile_input,cus_par=cus_characteristic)   # input different mode
                    

    # Initialize an Algorithm

    algorithm = NSGA2(
        pop_size=40,
        n_offsprings=10,
        sampling=get_sampling("real_random"),
        crossover=get_crossover("real_sbx", prob=0.9, eta=15),
        mutation=get_mutation("real_pm", eta=20),
        eliminate_duplicates=True
    )


    # Define a Termination Criterion
    termination = get_termination("n_gen", 40)

    res = minimize(problem,
                algorithm,
                termination,
                display= None,
                seed=1,
                save_history=True,
                verbose=False)    #verbose -> dont show any thing
    F = res.F  
    X = res.X

    # Multi-Criteria Decision Making
    fl = F.min(axis=0)
    fu = F.max(axis=0)
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)

    # Normalizing the obtained objective values regarding the boundary
    # points is relatively simple by:

    nF = (F - approx_ideal) / (approx_nadir - approx_ideal)
    # nF shape = (40, 2)

    fl = nF.min(axis=0) 
    fu = nF.max(axis=0) 

    ## Compromise Programming

    # Here for a bi-objective problem, let us assume the 
    # first objective is less a bit less important than the 
    # second objective by setting the weights to

    weights = np.array([0.4, 0.4,0.2])

    # the decomposition method called Augmented Scalarization Function (ASF)

    decomp = ASF()
    i = decomp.do(nF, 1/weights).argmin()   ## BEST index
    data_for_pred = [np.int16(X[i][0]),                ## ox
                    np.int16(X[i][1]),                ## power
                    np.int16(X[i][2]),                ## speed
                    X[i][3].round(decimals=2)]        ## spacing

    data_for_pred = np.array(data_for_pred).reshape(1,-1)   # reshape for input

    ################################
    # mode = 0 for freq 50Hz       #
    # mode = 1 for freq 200Hz      #
    # mode = 2 for freq 400Hz      #
    # mode = 3 for freq 800Hz      #
    ################################

    # tensile strength is decouple with operation frequency
    pred_tensile = model_tensile_xgb.predict(data_for_pred)

    if(mode == "0"):
        pred_mu_50 = model_mu_xgb_50.predict(data_for_pred)
        pred_Pcv_50 = model_Pcv_xgb_50.predict(data_for_pred)
        # print('%.3f'%pred_mu_50[0], '%.3f'%pred_Pcv_50[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_50[0],pred_Pcv_50[0],pred_tensile[0]]
    if(mode == "1"):
        pred_mu_200 = model_mu_xgb_200.predict(data_for_pred)
        pred_Pcv_200 = model_Pcv_xgb_200.predict(data_for_pred)
        # print('%.3f'%pred_mu_200[0], '%.3f'%pred_Pcv_200[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_200[0],pred_Pcv_200[0],pred_tensile[0]]
    if(mode == "2"):
        pred_mu_400 = model_mu_xgb_400.predict(data_for_pred)
        pred_Pcv_400 = model_Pcv_xgb_400.predict(data_for_pred)
        # print('%.3f'%pred_mu_400[0], '%.3f'%pred_Pcv_400[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_400[0],pred_Pcv_400[0],pred_tensile[0]]
    if(mode == "3"):
        pred_mu_800 = model_mu_xgb_800.predict(data_for_pred)
        pred_Pcv_800 = model_Pcv_xgb_800.predict(data_for_pred)
        # print('%.3f'%pred_mu_800[0], '%.3f'%pred_Pcv_800[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_800[0],pred_Pcv_800[0],pred_tensile[0]]

    ########manufacturing parameter suggestion################
    # print(  np.int16(X[i][0]),                ## ox            #
            # np.int16(X[i][1]),                ## power         #
            # np.int16(X[i][2]),                ## speed         #
            # X[i][3].round(decimals=2))        ## spacing       #
    ##########################################################

    out_list2 = [np.int16(X[i][0]),np.int16(X[i][1]),np.int16(X[i][2]),X[i][3].round(decimals=2)]
    # print("mode = ", mode)

    # print("Parameter suggestion finish!!- mmmt")
    return out_list1,out_list2



class max_mu_max_tensile(ElementwiseProblem):    # max mu and max tensile
    def __init__(self,mode1, mode2 ,*args, **kwargs):
        super().__init__(n_var=4,
                         n_obj=2,
                         n_constr=0,
                         xl=np.array([0,100,300,0.045]),  # lower bound
                         xu=np.array([8000,200,1500,0.12])) # upper bound
        self.mode1 = mode1  # mu model selected
        self.mode2 = mode2  # tensile model selected
    def _evaluate(self,x, out, *args, **kwargs):
        f1 = -np.float64(self.mode1.predict(np.array(x).reshape(1, -1)))   # mu
        f2 = -np.float64(self.mode2.predict(np.array(x).reshape(1, -1)))  # tensile

        out["F"] = [f1, f2]




def FeSiCr_max_mu_max_tensile(input_data):
    mode = input_data[1]    # frequency mode selected
    # Multi type of model can be select (base on R2 score)
    model_mu_input = [  model_mu_xgb_50,      ## mu model
                        model_mu_xgb_200,
                        model_mu_cat_400,
                        model_mu_lgb_800]

    model_tensile_input = model_tensile_xgb # tensile model no relate to frequency

    problem = max_mu_max_tensile(mode1=model_mu_input[int(mode)], mode2=model_tensile_input)   # input different mode


    ## Initialize an Algorithm

    algorithm = NSGA2(
        pop_size=40,
        n_offsprings=10,
        sampling=get_sampling("real_random"),
        crossover=get_crossover("real_sbx", prob=0.9, eta=15),
        mutation=get_mutation("real_pm", eta=20),
        eliminate_duplicates=True
    )


    # Define a Termination Criterion
    termination = get_termination("n_gen", 40)

    res = minimize(problem,
                algorithm,
                termination,
                display= None,
                seed=1,
                save_history=True,
                verbose=False)    #verbose -> dont show any thing
    F = res.F
    X = res.X



    ## Multi-Criteria Decision Making

    fl = F.min(axis=0)
    fu = F.max(axis=0)
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)

    ### parameter suggestion from NSGA-II

    # Normalizing the obtained objective values regarding the boundary
    # points is relatively simple by:

    nF = (F - approx_ideal) / (approx_nadir - approx_ideal)
    # nF shape = (40, 2)

    fl = nF.min(axis=0) 
    fu = nF.max(axis=0) 

    # Compromise Programming

    #  Here for a bi-objective problem, let us assume the 
    # first objective is less a bit less important than the 
    # second objective by setting the weights to
    weights = np.array([0.2, 0.8])

    # the decomposition method called Augmented Scalarization Function (ASF)
    decomp = ASF()

    i = decomp.do(nF, 1/weights).argmin()   ## BEST index

    data_for_pred = [np.int16(X[i][0]),                ## ox
                    np.int16(X[i][1]),                ## power
                    np.int16(X[i][2]),                ## speed
                    X[i][3].round(decimals=2)]        ## spacing



    data_for_pred = np.array(data_for_pred).reshape(1,-1)   # reshape for input

    ################################
    # mode = 0 for freq 50Hz       #
    # mode = 1 for freq 200Hz      #
    # mode = 2 for freq 400Hz      #
    # mode = 3 for freq 800Hz      #
    ################################

    ## tensile strength is decouple with operation frequency
    pred_tensile = model_tensile_xgb.predict(data_for_pred)

    if(mode == "0"):
        pred_mu_50 = model_mu_xgb_50.predict(data_for_pred)
        pred_Pcv_50 = model_Pcv_xgb_50.predict(data_for_pred)
        # print('%.3f'%pred_mu_50[0], '%.3f'%pred_Pcv_50[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_50[0],pred_Pcv_50[0],pred_tensile[0]]

    if(mode == "1"):
        pred_mu_200 = model_mu_xgb_200.predict(data_for_pred)
        pred_Pcv_200 = model_Pcv_xgb_200.predict(data_for_pred)
        # print('%.3f'%pred_mu_200[0], '%.3f'%pred_Pcv_200[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_200[0],pred_Pcv_200[0],pred_tensile[0]]

    if(mode == "2"):
        pred_mu_400 = model_mu_xgb_400.predict(data_for_pred)
        pred_Pcv_400 = model_Pcv_xgb_400.predict(data_for_pred)
        # print('%.3f'%pred_mu_400[0], '%.3f'%pred_Pcv_400[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_400[0],pred_Pcv_400[0],pred_tensile[0]]

    if(mode == "3"):
        pred_mu_800 = model_mu_xgb_800.predict(data_for_pred)
        pred_Pcv_800 = model_Pcv_xgb_800.predict(data_for_pred)
        # print('%.3f'%pred_mu_800[0], '%.3f'%pred_Pcv_800[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_800[0],pred_Pcv_800[0],pred_tensile[0]]

    ########manufacturing parameter suggestion################
    # # print(np.int16(X[i][0]),              ## ox            #
    #     np.int16(X[i][1]),                ## power         #
    #     np.int16(X[i][2]),                ## speed         #
    #     X[i][3].round(decimals=2))        ## spacing       #
    ##########################################################
    out_list2 = [np.int16(X[i][0]),np.int16(X[i][1]),np.int16(X[i][2]),X[i][3].round(decimals=2)]
    # # print("mode = ", mode)

    # # print("Parameter suggestion finish!!- mmmt")
    return out_list1,out_list2

class max_mu_min_pcv(ElementwiseProblem):    # max mu and min Pcv
    def __init__(self,mode1, mode2 ,*args, **kwargs):
        super().__init__(n_var=4,
                         n_obj=2,
                         n_constr=0,
                         xl=np.array([0,100,300,0.045]),  # lower bound
                         xu=np.array([8000,200,1500,0.12])) # upper bound
        self.mode1 = mode1  # mu model selected
        self.mode2 = mode2  # Pcv model selected
    def _evaluate(self,x, out, *args, **kwargs):
        f1 = -np.float64(self.mode1.predict(np.array(x).reshape(1, -1)))   #mu
        f2 = np.float64(self.mode2.predict(np.array(x).reshape(1, -1)))  #Pcv

        out["F"] = [f1, f2]

def FeSiCr_max_mu_min_pcv(input_data):
    mode = input_data[1]    # frequency mode selected

    # Multi type of model can be select (base on R2 score)
    ##############################################################################################
    model_mu_input = [  model_mu_xgb_50,      ## mu model
                        model_mu_xgb_200,
                        model_mu_cat_400,
                        model_mu_lgb_800]
    
    model_Pcv_input = [ model_Pcv_xgb_50,    ## Pcv model
                        model_Pcv_xgb_200,
                        model_Pcv_cat_400,
                        model_Pcv_cat_800]


    problem = max_mu_min_pcv(mode1=model_mu_input[int(mode)], mode2=model_Pcv_input[int(mode)])   # input different mode
    ##############################################################################################

    # Initialize an Algorithm
    algorithm = NSGA2(
        pop_size=40,
        n_offsprings=10,
        sampling=get_sampling("real_random"),
        crossover=get_crossover("real_sbx", prob=0.9, eta=15),
        mutation=get_mutation("real_pm", eta=20),
        eliminate_duplicates=True
    )

    # Define a Termination Criterion
    termination = get_termination("n_gen", 40)

    res = minimize(problem,
                algorithm,
                termination,
                display= None,
                seed=1,
                save_history=True,
                verbose=False)    #verbose -> dont show any thing
    F = res.F
    X = res.X

    # give parameter to model and caculate the output


    # Multi-Criteria Decision Making
    fl = F.min(axis=0)
    fu = F.max(axis=0)
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)

    # parameter suggestion from NSGA-II
    # Normalizing the obtained objective values regarding the boundary
    # points is relatively simple by:

    nF = (F - approx_ideal) / (approx_nadir - approx_ideal)
    # nF shape = (40, 2)

    fl = nF.min(axis=0) 
    fu = nF.max(axis=0)

    ## Compromise Programming

    #  Here for a bi-objective problem, let us assume the 
    # first objective is less a bit less important than the 
    # second objective by setting the weights to

    weights = np.array([0.2, 0.8])

    ## the decomposition method called Augmented Scalarization Function (ASF)
    decomp = ASF()

    i = decomp.do(nF, 1/weights).argmin()   ## BEST index

    ###characteristic prediction from NSGA-II###
    # # print(-F[i][0].round(decimals = 2), F[i][1].round(decimals = 2))    ## characteristic
    ##########################

    data_for_pred = [np.int16(X[i][0]),                ## ox
                    np.int16(X[i][1]),                ## power
                    np.int16(X[i][2]),                ## speed
                    X[i][3].round(decimals=2)]        ## spacing

    data_for_pred = np.array(data_for_pred).reshape(1,-1)   # reshape for input

    ################################
    # mode = 0 for freq 50Hz       #
    # mode = 1 for freq 200Hz      #
    # mode = 2 for freq 400Hz      #
    # mode = 3 for freq 800Hz      #
    ################################

    ## tensile strength is decouple with operation frequency
    pred_tensile = model_tensile_xgb.predict(data_for_pred)

    if(mode == "0"):
        pred_mu_50 = model_mu_xgb_50.predict(data_for_pred)
        pred_Pcv_50 = model_Pcv_xgb_50.predict(data_for_pred)
        # print('%.3f'%pred_mu_50[0], '%.3f'%pred_Pcv_50[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_50[0],pred_Pcv_50[0],pred_tensile[0]]
    if(mode == "1"):
        pred_mu_200 = model_mu_xgb_200.predict(data_for_pred)
        pred_Pcv_200 = model_Pcv_xgb_200.predict(data_for_pred)
        # print('%.3f'%pred_mu_200[0], '%.3f'%pred_Pcv_200[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_200[0],pred_Pcv_200[0],pred_tensile[0]]
    if(mode == "2"):
        pred_mu_400 = model_mu_xgb_400.predict(data_for_pred)
        pred_Pcv_400 = model_Pcv_xgb_400.predict(data_for_pred)
        # print('%.3f'%pred_mu_400[0], '%.3f'%pred_Pcv_400[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_400[0],pred_Pcv_400[0],pred_tensile[0]]
    if(mode == "3"):
        pred_mu_800 = model_mu_xgb_800.predict(data_for_pred)
        pred_Pcv_800 = model_Pcv_xgb_800.predict(data_for_pred)
        # print('%.3f'%pred_mu_800[0], '%.3f'%pred_Pcv_800[0], '%.3f'%pred_tensile[0])
        out_list1 = [pred_mu_800[0],pred_Pcv_800[0],pred_tensile[0]]


    
    ########manufacturing parameter suggestion################
    # print(np.int16(X[i][0]),                ## ox            #
            # np.int16(X[i][1]),                ## power         #
            # np.int16(X[i][2]),                ## speed         #
            # X[i][3].round(decimals=2))        ## spacing       #
    ##########################################################
    out_list2 = [np.int16(X[i][0]),np.int16(X[i][1]),np.int16(X[i][2]),X[i][3].round(decimals=2)]
    # print("mode = ", mode)

    # print("Parameter suggestion finish!!- mmmt")
    return out_list1,out_list2