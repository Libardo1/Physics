#! /usr/bin/env python

import BDT_file_handler as BDT_fh

def adjust_WIMP_files(bolo_name, d_cut, analysis_type, d_event_type_num_event):

    """Change the value of the FWHM/ energycuts used in the build_WIMP_tree.C file
    
    Detail:
        Read the file once to save its content. 
        Then rewrite it with the appropriate modifications

    Args:
        bolo_name     = (str) bolometer name
        d_cut         = (dict) dictionnary which states which cut to use on heat/ion/veto
        analysis_type = (str) name of analysis (which FWHM, which cuts)
        d_event_type_num_event = (dict) indicates how many events to simulate

    Returns:
        void

    Raises:
        void
    """

    gen_path = "/home/irfulx204/mnt/tmain/Desktop/Run308_BDT_simu_corr/"

    #Load the FWHM
    d_std_true_events = BDT_fh.open_true_event_FWHM_file(bolo_name,)

    #Load estimator to update the EI and EC expression
    d_estimator = BDT_fh.open_estimator_file(bolo_name)

    list_cpp_lines =[]

    with open(gen_path + "Event_generation/WIMP_generation/build_WIMP_tree.C", "r") as f_cpp:
        list_cpp_lines = f_cpp.readlines()
   
    with open(gen_path + "Event_generation/WIMP_generation/build_WIMP_tree.C", "w") as f_cpp:
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

            elif "Wmass_vec.push_back(5);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(5);num_events.push_back(" + str(d_event_type_num_event["5GeV"]) + ");\n")
            elif "Wmass_vec.push_back(6);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(6);num_events.push_back(" + str(d_event_type_num_event["6GeV"]) + ");\n")
            elif "Wmass_vec.push_back(7);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(7);num_events.push_back(" + str(d_event_type_num_event["7GeV"]) + ");\n")
            elif "Wmass_vec.push_back(10);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(10);num_events.push_back(" + str(d_event_type_num_event["10GeV"]) + ");\n")
            elif "Wmass_vec.push_back(25);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(25);num_events.push_back(" + str(d_event_type_num_event["25GeV"]) + ");\n")

            else:
                f_cpp.write(line)


    with open(gen_path + "Event_generation/WIMP_generation/build_WIMP_tree_nocut.C", "r") as f_cpp:
        list_cpp_lines = f_cpp.readlines()
   
    with open(gen_path + "Event_generation/WIMP_generation/build_WIMP_tree_nocut.C", "w") as f_cpp:
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

            elif "Wmass_vec.push_back(5);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(5);num_events.push_back(" + str(d_event_type_num_event["5GeV"]) + ");\n")
            elif "Wmass_vec.push_back(6);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(6);num_events.push_back(" + str(d_event_type_num_event["6GeV"]) + ");\n")
            elif "Wmass_vec.push_back(7);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(7);num_events.push_back(" + str(d_event_type_num_event["7GeV"]) + ");\n")
            elif "Wmass_vec.push_back(10);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(10);num_events.push_back(" + str(d_event_type_num_event["10GeV"]) + ");\n")
            elif "Wmass_vec.push_back(25);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(25);num_events.push_back(" + str(d_event_type_num_event["25GeV"]) + ");\n")

            else:
                f_cpp.write(line)

    with open(gen_path + "Event_generation/WIMP_generation/WIMP_recoil_generation.C", "r") as f_cpp:
        list_cpp_lines = f_cpp.readlines()
   
    with open(gen_path + "Event_generation/WIMP_generation/WIMP_recoil_generation.C", "w") as f_cpp:
        for line in list_cpp_lines:

            if "TString bolo_name = TString" in line:
                f_cpp.write('\tTString bolo_name = TString("' + bolo_name + '");\n')
            elif "TString analysis_type = TString" in line:
                f_cpp.write('\tTString analysis_type = TString("' + analysis_type + '");\n')
            elif "TString analysis_type = TString" in line:
                f_cpp.write('\tTString analysis_type = TString("' + analysis_type + '");\n')
                
            elif "Wmass_vec.push_back(5);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(5);num_events.push_back(" + str(d_event_type_num_event["5GeV"]) + ");\n")
            elif "Wmass_vec.push_back(6);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(6);num_events.push_back(" + str(d_event_type_num_event["6GeV"]) + ");\n")
            elif "Wmass_vec.push_back(7);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(7);num_events.push_back(" + str(d_event_type_num_event["7GeV"]) + ");\n")
            elif "Wmass_vec.push_back(10);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(10);num_events.push_back(" + str(d_event_type_num_event["10GeV"]) + ");\n")
            elif "Wmass_vec.push_back(25);num_eve" in line:
                f_cpp.write("\tWmass_vec.push_back(25);num_events.push_back(" + str(d_event_type_num_event["25GeV"]) + ");\n")

            else:
                f_cpp.write(line)