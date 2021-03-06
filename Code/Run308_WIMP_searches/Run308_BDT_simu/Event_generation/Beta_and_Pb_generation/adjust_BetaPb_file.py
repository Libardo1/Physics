#! /usr/bin/env python
from ROOT import *
import BDT_file_handler as BDT_fh

def adjust_BetaPb_file(bolo_name, d_cut, analysis_type, d_event_type_num_event):

    """Change the value of the FWHM/ energycuts used in the build_Gamma_tree.C file
    
    Detail:
        Read the file once to save its content. 
        Then rewrite it with the appropriate modifications

    Args:
        bolo_name              = (str) bolometer name
        d_cut                  = (dict) dictionnary which states which cut to use on heat/ion/veto
        analysis_type          = (str) name of analysis (which FWHM, which cuts)
        d_event_type_num_event = (dict) events for S1Beta, S2Beta, S1P, S2Pb 

    Returns:
        void

    Raises:
        void
    """

    gen_path = "/home/irfulx204/mnt/tmain/Desktop/Run308_BDT_simu_corr/"

    #Load the FWHM
    d_std_true_events = BDT_fh.open_true_event_FWHM_file(bolo_name, "")

    #Load estimator to update the EI and EC expression
    d_estimator = BDT_fh.open_estimator_file(bolo_name, "")

    list_cpp_lines =[]

    with open(gen_path + "Event_generation/Beta_and_Pb_generation/build_BetaPb_tree.C", "r") as f_cpp:
        list_cpp_lines = f_cpp.readlines()
   
    with open(gen_path + "Event_generation/Beta_and_Pb_generation/build_BetaPb_tree.C", "w") as f_cpp:
        for line in list_cpp_lines:

            # if "float s_heat=" in line:
            #     f_cpp.write("\tfloat s_heat=" + str(d_std_true_events["FWHEAT"]) + ";\n")
            # elif "float s_EC1=" in line:
            #     f_cpp.write("\tfloat s_EC1=" + str(d_std_true_events["OWC1"]) + ";\n")
            # elif "float s_EC2=" in line:
            #     f_cpp.write("\tfloat s_EC2=" + str(d_std_true_events["OWC2"]) + ";\n")

            if "float s_IA=" in line:
                f_cpp.write("\tfloat s_IA=" + str(d_std_true_events["FWIA"]) + ";\n")
            elif "float s_IB=" in line:
                f_cpp.write("\tfloat s_IB=" + str(d_std_true_events["FWIB"]) + ";\n")
            elif "float s_IC=" in line:
                f_cpp.write("\tfloat s_IC=" + str(d_std_true_events["FWIC"]) + ";\n")
            elif "float s_ID=" in line:
                f_cpp.write("\tfloat s_ID=" + str(d_std_true_events["FWID"]) + ";\n")

            elif "float cut_vetA=" in line:
                f_cpp.write("\tfloat cut_vetA=" + str(d_cut["sigma_vet"]*d_std_true_events["FWIA"]) + ";\n")
            elif "float cut_vetC=" in line:
                f_cpp.write("\tfloat cut_vetC="  + str(d_cut["sigma_vet"]*d_std_true_events["FWIC"]) + ";\n")

            elif "float ECinf=" in line:
                f_cpp.write("\tfloat ECinf=" + str(d_cut["ECinf"]) + ";\n")
            elif "float ECsup=" in line:
                f_cpp.write("\tfloat ECsup=" + str(d_cut["ECsup"]) + ";\n")
            elif "float EIinf=" in line:
                f_cpp.write("\tfloat EIinf=" + str(d_cut["EIinf"]) + ";\n")
            elif "float EIsup=" in line:
                f_cpp.write("\tfloat EIsup=" + str(d_cut["EIsup"]) + ";\n")

            # elif "float EC =" in line:
            #     f_cpp.write("\t\t\tfloat EC =" + str(d_estimator["HEAT"][:5]) + "*EC1+" +str(1-float(d_estimator["HEAT"][:5])) + "*EC2;\n")
            # elif "float EI =" in line:
            #     f_cpp.write("\t\t\tfloat EI =" + str(d_estimator["FID"][:5]) + "*EIB+" +str(1-float(d_estimator["FID"][:5]) )+ "*EID;\n")

            elif "TString bolo_name = TString" in line:
                f_cpp.write('\tTString bolo_name = TString("' + bolo_name + '");\n')
            elif "TString analysis_type = TString" in line:
                f_cpp.write('\tTString analysis_type = TString("' + analysis_type + '");\n')
            elif "num_event[0] =" in line:
                f_cpp.write("\tnum_event[0] =" + str(d_event_type_num_event["S1Beta"]) + ";\n")
            elif "num_event[1] =" in line:
                f_cpp.write("\tnum_event[1] =" + str(d_event_type_num_event["S2Beta"]) + ";\n")
            elif "num_event[2] =" in line:
                f_cpp.write("\tnum_event[2] =" + str(d_event_type_num_event["S1Pb"]) + ";\n")
            elif "num_event[3] =" in line:
                f_cpp.write("\tnum_event[3] =" + str(d_event_type_num_event["S2Pb"]) + ";\n")
            else:
                f_cpp.write(line)

    with open(gen_path + "Event_generation/Beta_and_Pb_generation/build_BetaPb_tree_straggle_test.C", "r") as f_cpp:
        list_cpp_lines = f_cpp.readlines()
   
    with open(gen_path + "Event_generation/Beta_and_Pb_generation/build_BetaPb_tree_straggle_test.C", "w") as f_cpp:
        for line in list_cpp_lines:


            if "float cut_vetA=" in line:
                f_cpp.write("\tfloat cut_vetA=" + str(d_cut["sigma_vet"]*d_std_true_events["FWIA"]) + ";\n")
            elif "float cut_vetC=" in line:
                f_cpp.write("\tfloat cut_vetC="  + str(d_cut["sigma_vet"]*d_std_true_events["FWIC"]) + ";\n")

            elif "float ECinf=" in line:
                f_cpp.write("\tfloat ECinf=" + str(d_cut["ECinf"]) + ";\n")
            elif "float ECsup=" in line:
                f_cpp.write("\tfloat ECsup=" + str(d_cut["ECsup"]) + ";\n")
            elif "float EIinf=" in line:
                f_cpp.write("\tfloat EIinf=" + str(d_cut["EIinf"]) + ";\n")
            elif "float EIsup=" in line:
                f_cpp.write("\tfloat EIsup=" + str(d_cut["EIsup"]) + ";\n")
                
            elif "TString bolo_name = TString" in line:
                f_cpp.write('\tTString bolo_name = TString("' + bolo_name + '");\n')
            elif "TString analysis_type = TString" in line:
                f_cpp.write('\tTString analysis_type = TString("' + analysis_type + '");\n')
            else:
                f_cpp.write(line)