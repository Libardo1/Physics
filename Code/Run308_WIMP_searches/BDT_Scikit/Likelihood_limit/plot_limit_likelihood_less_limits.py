from ROOT import *
import numpy as np
import PyROOTPlots as PyRPl
import Poisson_90CL as Poisson90


def get_percentile(arr, WIMP_mass,analysis, exposure, detector_mass = 0.6):

	"""See detail
	
	Detail:
		From an array input of 90 CL: 
		extract the percentiles to get the expected 
		95 CL and 68 CL on the 90 CL result

	Args:
		arr           = (np array) array of 90 CL values on the number of WIMPs
		WIMP_mass     = (str) WIMP mass in GeV
		analysis      = (str) type of analysis cut
		exposure      = (float) exposure in days
		detector_mass = (float) fiducial mass
		
	Returns:
		d (dict) = the percentile dictionnary

	Raises:
		void
	"""

	#Fill a conversion dictionnary to convert Ncounts to limit on cross section
	d ={}
	count_arr = np.loadtxt("./Text_files/WIMP_counts_for_1kgday_" + analysis + "_2D.txt", delimiter = ",")

	d_conv={}
	for mass, Nevents in count_arr:
		d_conv[str(int(mass))] = float(Nevents)

	d["5"]=np.percentile(arr, 2.5)*1E-5/(d_conv[str(int(WIMP_mass))] * exposure * detector_mass)
	d["95"]=np.percentile(arr, 97.5)*1E-5/(d_conv[str(int(WIMP_mass))] * exposure * detector_mass)
	d["32"]=np.percentile(arr, 16)*1E-5/(d_conv[str(int(WIMP_mass))] * exposure * detector_mass)
	d["68"]=np.percentile(arr, 84)*1E-5/(d_conv[str(int(WIMP_mass))] * exposure * detector_mass)

	return d


def get_limit(bolo_name, arr, WIMP_mass,analysis, exposure, detector_mass = 0.6):

	"""See detail
	
	Detail:
		From a single observation, get the 90 CL limit

	Args:
		bolo_name = (str) bolometer name
		arr           = (np array) array of 90 CL values on the number of WIMPs
		WIMP_mass     = (str) WIMP mass in GeV
		analysis      = (str) type of analysis cut
		exposure      = (float) exposure in days
		detector_mass = (float) fiducial mass
		
	Returns:
		d (dict) = the percentile dictionnary

	Raises:
		void
	"""

	# #Original number of simulated events
	# d_N_ori         = {"5":15000000, "6":900000, "7":200000, "10":40000, "25":10000}

	# # Load WIMP trees to compute the WIMP events passing the cuts
	# WIMP_path = "../../BDT_" + bolo_name + "/" + analysis + "/WIMP/ROOT_files/"
	# tWIMP5, fWIMP5 = PyRPl.open_ROOT_object(WIMP_path + bolo_name + "_WIMP_mass_5_tree.root", "t_new0")
	# tWIMP6, fWIMP6 = PyRPl.open_ROOT_object(WIMP_path + bolo_name + "_WIMP_mass_6_tree.root", "t_new0")
	# tWIMP7, fWIMP7 = PyRPl.open_ROOT_object(WIMP_path + bolo_name + "_WIMP_mass_7_tree.root", "t_new0")
	# tWIMP10, fWIMP10 = PyRPl.open_ROOT_object(WIMP_path + bolo_name + "_WIMP_mass_10_tree.root", "t_new0")
	# tWIMP25, fWIMP25 = PyRPl.open_ROOT_object(WIMP_path + bolo_name + "_WIMP_mass_25_tree.root", "t_new0")

	# d_N_after       = {}
	# d_N_after["5"]  = tWIMP5.GetEntries()
	# d_N_after["6"]  = tWIMP6.GetEntries()
	# d_N_after["7"]  = tWIMP7.GetEntries()
	# d_N_after["10"] = tWIMP10.GetEntries()
	# d_N_after["25"] = tWIMP25.GetEntries()


	#Convert the obs counts in arr to a 90CL Poisson limit
	for i in range(len(arr)):
		arr[i] = Poisson90.compute_90CL_limit(arr[i])

	#Get the array with the efficiency
	count_eff = np.loadtxt("./Text_files/" + bolo_name + "_BDT_cut_and_eff_" + analysis + ".txt", delimiter = ",")
	d_eff={}
	for mass,truc, eff in count_eff:
		d_eff[str(int(mass))] = float(eff)


	count_arr = np.loadtxt("./Text_files/WIMP_counts_for_1kgday_" + analysis + "_2D.txt", delimiter = ",")
	#Fill a conversion dictionnary to convert Ncounts to limit on cross section
	# #Normalise with 1D PDF and with generated events
	# d_conv={}
	# for mass, Nevents in count_arr:
	# 	d_conv[str(int(mass))] = float(Nevents)

	# return arr[0]*1E-5*d_N_ori[str(int(WIMP_mass))]/(d_conv[str(int(WIMP_mass))] * exposure * detector_mass * d_N_after[str(int(WIMP_mass))])

	# Normalise with 2D PDF
	d_conv={}
	for mass, Nevents in count_arr:
		d_conv[str(int(mass))] = float(Nevents)

	# print arr[0], WIMP_mass, d_conv[str(int(WIMP_mass))]

	print WIMP_mass, arr[0], d_conv[str(int(WIMP_mass))] , exposure , detector_mass, arr[0]*1E-5/(d_conv[str(int(WIMP_mass))] * exposure * detector_mass)

	return arr[0]*1E-5/(d_conv[str(int(WIMP_mass))] * exposure * detector_mass* d_eff[str(int(WIMP_mass))] )

def get_expected_likelihood(list_mass, analysis, exposure, detector_mass = 0.6):

	"""Return graph of expected 90 CL likelihood
	
	Detail:

	Args:
		list_mass = (list) list of WIMP masses
		analysis      = (str) type of analysis cut
		exposure = (float) exposure in days
		detector_mass = (float) fiducial mass

	Returns:
		gr

	Raises:
		void
	"""

	#Load count array to convert NWIMP to sigma_lim
	d_conv={}
	count_arr = np.loadtxt("./Text_files/WIMP_counts_for_1kgday_" + analysis + "_2D.txt", delimiter = ",")
	for mass, Nevents in count_arr:
		d_conv[str(int(mass))] = float(Nevents)

	file_lim = np.loadtxt("./Text_files/" + bolo_name + "_" + analysis + "_NWIMP_at_limit.txt", delimiter = ",")
	list_mass, list_lim = [], []
	for i in range(file_lim.shape[0]):
		list_mass.append(file_lim[i][0])
		list_lim.append(file_lim[i][1]*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))

	npts = len(list_mass)
	list_mass = np.array(list_mass).astype(float)
	list_lim = np.array(list_lim).astype(float)
	gr = TGraph(npts, list_mass, list_lim)

	return gr

def get_expected_MCMC(list_mass, analysis, exposure, detector_mass = 0.6):

	"""Return graph of expected 90 CL likelihood
	
	Detail:

	Args:
		list_mass = (list) list of WIMP masses
		analysis      = (str) type of analysis cut
		exposure = (float) exposure in days
		detector_mass = (float) fiducial mass

	Returns:
		gr

	Raises:
		void
	"""

	#Load count array to convert NWIMP to sigma_lim
	d_conv={}
	count_arr = np.loadtxt("./Text_files/WIMP_counts_for_1kgday_" + analysis + "_2D.txt", delimiter = ",")
	for mass, Nevents in count_arr:
		d_conv[str(int(mass))] = float(Nevents)

	file_lim = np.loadtxt("./Text_files/" + bolo_name + "_" + analysis + "_NWIMP_at_limit_MCMC.txt", delimiter = ",")
	list_mass, list_lim, list_lim_plus_sigma, list_lim_min_sigma = [], [], [], []
	for i in range(file_lim.shape[0]):
		list_mass.append(file_lim[i][0])
		list_lim.append(np.mean(file_lim[i][1:])*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))
		list_lim_plus_sigma.append((np.mean(file_lim[i][1:])+ np.std(file_lim[i][1:]))*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))
		list_lim_min_sigma.append((np.mean(file_lim[i][1:])- np.std(file_lim[i][1:]))*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))
		# list_lim.append(2.3*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))

	#Save mean MCMC limit 
	arr_lim = zip(list_mass, list_lim)
	np.savetxt("./Text_files/" + bolo_name + "_" + analysis + "_mean_MCMC_limit.txt", arr_lim, delimiter = " ")


	npts = len(list_mass)
	list_mass = np.array(list_mass).astype(float)
	list_lim = np.array(list_lim).astype(float)
	list_lim_plus_sigma = np.array(list_lim_plus_sigma).astype(float)
	list_lim_min_sigma = np.array(list_lim_min_sigma).astype(float)
	gr = TGraph(npts, list_mass, list_lim)
	print list_lim_min_sigma + list_lim_plus_sigma
	gr_contour = TGraph(2*npts, np.concatenate((list_mass , list_mass[::-1])), np.concatenate((list_lim_min_sigma , list_lim_plus_sigma[::-1])))

	return gr, gr_contour

def get_expected_MCMC_proj(list_mass, analysis, exposure, detector_mass = 0.6):

	"""Return graph of expected 90 CL likelihood
	
	Detail:

	Args:
		list_mass = (list) list of WIMP masses
		analysis      = (str) type of analysis cut
		exposure = (float) exposure in days
		detector_mass = (float) fiducial mass

	Returns:
		gr

	Raises:
		void
	"""

	#Load count array to convert NWIMP to sigma_lim
	d_conv={}
	count_arr = np.loadtxt("./Text_files/WIMP_counts_for_1kgday_" + analysis + "_2D.txt", delimiter = ",")
	for mass, Nevents in count_arr:
		d_conv[str(int(mass))] = float(Nevents)

	file_lim = np.loadtxt("./Text_files/" + bolo_name + "_" + analysis + "_NWIMP_at_limit_MCMC_proj_" + str(int(exposure)) + "_jour.txt", delimiter = ",")
	list_mass, list_lim, list_lim_plus_sigma, list_lim_min_sigma = [], [], [], []
	for i in range(file_lim.shape[0]):
		list_mass.append(file_lim[i][0])
		list_lim.append(np.mean(file_lim[i][1:])*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))
		list_lim_plus_sigma.append((np.mean(file_lim[i][1:])+ np.std(file_lim[i][1:]))*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))
		list_lim_min_sigma.append((np.mean(file_lim[i][1:])- np.std(file_lim[i][1:]))*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))
		# list_lim.append(2.3*1E-5/(d_conv[str(int(list_mass[i]))] * exposure * detector_mass))

	#Save mean MCMC limit 
	arr_lim = zip(list_mass, list_lim)
	np.savetxt("./Text_files/" + bolo_name + "_" + analysis + "_mean_MCMC_limit.txt", arr_lim, delimiter = " ")


	npts = len(list_mass)
	list_mass = np.array(list_mass).astype(float)
	list_lim = np.array(list_lim).astype(float)
	list_lim_plus_sigma = np.array(list_lim_plus_sigma).astype(float)
	list_lim_min_sigma = np.array(list_lim_min_sigma).astype(float)
	gr = TGraph(npts, list_mass, list_lim)
	print list_lim_min_sigma + list_lim_plus_sigma
	gr_contour = TGraph(2*npts, np.concatenate((list_mass , list_mass[::-1])), np.concatenate((list_lim_min_sigma , list_lim_plus_sigma[::-1])))

	return gr, gr_contour

def get_true_event_limit(bolo_name, list_mass, analysis, exposure, detector_mass = 0.6):

	"""Get expected sensitivity confidence bands
	
	Detail:
		Return filled area graph for the 68 and 95 CI on the 
		expected sensitivity given a choice of analysis

	Args:
		bolo_name = (str) bolometer name
		list_mass = (list) list of WIMP masses
		analysis      = (str) type of analysis cut
		exposure = (float) exposure in days
		detector_mass = (float) fiducial mass

	Returns:
		gr_68, gr_95 (TGraph) = the 2 filled area graphs

	Raises:
		void
	"""

	d_mass_limit={}
	list_arr_obs = np.loadtxt("./Text_files/true_events_passing_cuts_" + analysis  +".txt", delimiter = ",")
	for i in range(list_arr_obs.shape[0]):
		WIMP_mass = list_arr_obs[i][0]
		arr_counts = list_arr_obs[i][1:]
		d_mass_limit[int(WIMP_mass)] = get_limit(bolo_name, arr_counts, WIMP_mass, analysis, exposure, detector_mass)

	list_lim = [d_mass_limit[int(mass)] for mass in list_mass]

	arr_lim = np.array([[list_mass[i], list_lim[i]] for i in range(len(list_mass))])
	np.savetxt("./Text_files/" + bolo_name + "_" + analysis + "_limit.txt", arr_lim, delimiter = " ")

	gr_lim = TGraph(len(list_mass), np.array(list_mass).astype(float), np.array(list_lim).astype(float))

	# # print list_mass, list_lim
	for i in range(len(list_mass)):
		print list_mass[i], list_lim[i]

	return gr_lim

def get_contour_graph(file_name,  color):

	"""Open the file to get the graph of the contour limit
	
	Detail:
		Return the limit graph of given file_name 
		Also modify color

	Args:
		file_name (str)    = the name of the limit file 
		line_width (int)   = the line width 
		color (ROOT color) = the color for the line
		
	Returns:
		void

	Raises:
		void
	"""


	if "cogent_contour" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), 1E36*np.array(list(arr[:,1])))
		gr.SetFillColor(color)
	elif "cresst" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), 1E-6*np.array(list(arr[:,1])))
		gr.SetFillColor(color)
	elif "dama" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), 1E-7*np.array(list(arr[:,1])))
		gr.SetFillColor(color)

	elif "cdms" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		for i in range(n_points):
			arr[i,0] = np.power(10, arr[i,0])
			arr[i,1] = 1E36*np.power(10, arr[i,1])
			print i, arr[i,0], arr[i,1]
		gr = TGraph(n_points, np.array(list(arr[:,0])), np.array(list(arr[:,1])))
		gr.SetFillColor(color)

	else:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), np.array(list(arr[:,1])))
		gr.SetFillColor(color)

	return gr

def get_limit_graph(file_name, line_width, color):

	"""Open the file to get the graph of the limit 
	for the given file name
	
	Detail:
		Return the limit graph of given file_name 
		Also modify line_width and color

	Args:
		file_name (str)    = the name of the limit file 
		line_width (int)   = the line width 
		color (ROOT color) = the color for the line
		
	Returns:
		void

	Raises:
		void
	"""

	if "cdms" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), 1E-10*np.array(list(arr[:,1])))
		gr.SetLineColor(color)
		gr.SetLineWidth(line_width)

	elif "coupp" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), 1E36*np.array(list(arr[:,1])))
		gr.SetLineColor(color)
		gr.SetLineWidth(line_width)

	elif "cdmlite" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), 1E-3*np.array(list(arr[:,1])))
		gr.SetLineColor(color)
		gr.SetLineWidth(line_width)

	elif "pico" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), 1E-7*np.array(list(arr[:,1])))
		gr.SetLineColor(color)
		gr.SetLineWidth(line_width)

	elif "xenon10s2" in file_name:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), 1E36*np.array(list(arr[:,1])))
		gr.SetLineColor(color)
		gr.SetLineWidth(line_width)

	else:
		arr = np.loadtxt(file_name, delimiter = ",") 
		n_points                  =int(arr[:,0].shape[0])
		gr = TGraph(n_points, np.array(list(arr[:,0])), np.array(list(arr[:,1])))
		gr.SetLineColor(color)
		gr.SetLineWidth(line_width)

	return gr

def plot_limit(bolo_name, list_mass, analysis_type, exposure, detector_mass = 0.6):

	"""Plot all the desired limits
	
	Detail:
		Modify the code to add more limits if needed

	Args:
		bolo_name = (str) bolometer name
		list_mass = (list) list of WIMP masses
		analysis_type      = (str) type of analysis cut
		exposure      = (float) exposure in days
		detector_mass = (float) fiducial mass
		
	Returns:
		void
	Raises:
		void
	"""


	gr_lim = get_true_event_limit(bolo_name,[5, 6, 7, 10, 25], "ana_1.5_0_5", exposure, detector_mass)
	PyRPl.process_TGraph(gr_lim, color = kBlue)

	gr_MCMC, gr_MCMC_contour = get_expected_MCMC(list_mass, analysis_type, exposure)
	gr_MCMC_contour.SetFillColor(kRed-9)
	gr_MCMC.SetLineColor(kRed)
	gr_MCMC.SetLineWidth(3)
	gr_MCMC.SetLineStyle(2)

	gr_MCMC_proj, gr_MCMC_proj_contour = get_expected_MCMC_proj(list_mass, analysis_type, exposure*10)
	gr_MCMC_proj_contour.SetFillColor(kRed-9)
	gr_MCMC_proj.SetLineColor(kRed)
	gr_MCMC_proj.SetLineWidth(3)
	gr_MCMC_proj.SetLineStyle(9)

	gr_edw_low = get_limit_graph("./Text_files/Published_limits/edw_lowmass_2012.txt", 2, kRed)
	gr_cdms = get_limit_graph("./Text_files/Published_limits/cdms_limit.txt", 3, kBlue-3)
	gr_cdmlite = get_limit_graph("./Text_files/Published_limits/cdmlite2013.txt", 3, kBlue-3)
	gr_cdmlite.SetLineStyle(7)
	gr_cdms_contour = get_contour_graph("./Text_files/Published_limits/cdms_contour_90CL.txt", kBlue-10)
	gr_dama_contour = get_contour_graph("./Text_files/Published_limits/dama2009.txt", kRed-10)
	gr_cogent_contour = get_contour_graph("./Text_files/Published_limits/cogent_contour_2013.txt", kOrange+1)
	gr_cressta = get_contour_graph("./Text_files/Published_limits/cresst11a.txt", kGreen+2)
	gr_cresstb = get_contour_graph("./Text_files/Published_limits/cresst11b.txt", kGreen+2)
	gr_lux = get_limit_graph("./Text_files/Published_limits/lux2013.txt", 3, kBlack)
	gr_cresst = get_limit_graph("./Text_files/Published_limits/cresst2014.txt", 2, kGreen+2)

	h = TH1F("h", "", 100, 3.8,25)
	PyRPl.process_TH1(h, X_title = "Mass (GeV)", Y_title = "#sigma (pb)", X_title_size = .06, Y_title_size = .06, X_title_offset = .98, Y_title_offset = .95)


	h.GetXaxis().SetTitleOffset(1.17)

	gr_edw_low.SetName("gr_edw_low")
	gr_cdms.SetName("gr_cdms")
	gr_cdmlite.SetName("gr_cdmlite")
	gr_cdms_contour.SetName("gr_cdms_contour")
	gr_dama_contour.SetName("gr_dama_contour")
	gr_cogent_contour.SetName("gr_cogent_contour")
	gr_cressta.SetName("gr_cressta")
	gr_cresstb.SetName("gr_cresstb")
	gr_cresst.SetName("gr_cresst")
	gr_lux.SetName("gr_lux")
	gr_lim.SetName("gr_lim")

	gr_lim.SetLineColor(kRed)
	gr_lim.SetLineWidth(5)

	cc = TCanvas("cc", "cc")
	gPad.SetLogy()
	gPad.SetLogx()
	h.SetMaximum(9E-3)
	h.SetMinimum(1E-8)
	h.Draw()

	gr_cdms_contour.Draw("sameF")
	gr_dama_contour.Draw("sameF")
	gr_cogent_contour.Draw("sameF")
	gr_cressta.Draw("sameF")
	gr_cresstb.Draw("sameF")

	gr_cdms.Draw("sameC")
	gr_cdmlite.Draw("sameC")
	gr_cresst.Draw("sameC")
	gr_lux.Draw("sameC")
	gr_edw_low.SetLineStyle(7)
	gr_edw_low.Draw("sameC")
	gr_lim.Draw("sameC")
	gr_MCMC.Draw("sameC")
	gr_MCMC_proj.Draw("sameC")

	leg =TLegend(0.564,0.584,0.83,0.857)
	leg.AddEntry("gr_dama_contour", "DAMA" , "f")
	leg.AddEntry("gr_cdms", "SCDMS" , "l")
	leg.AddEntry("gr_cdmlite", "CDMSLite" , "l")
	leg.AddEntry("gr_cdms_contour", "CDMS Si" , "f")
	leg.AddEntry("gr_cogent_contour", "CoGeNT" , "f")
	leg.AddEntry("gr_lux", "LUX" , "l")
	leg.AddEntry("gr_xenon10", "XENON 10 S2 only" , "l")
	leg.AddEntry("gr_simple", "SIMPLE" , "l")
	leg.AddEntry("gr_coupp", "COUPP" , "l")
	leg.AddEntry("gr_cresst", "CRESST" , "l")
	leg.AddEntry("gr_pico", "PICO 2L" , "l")
	leg.AddEntry("gr_edw_low", "EDW II" , "l")
	leg.AddEntry("gr_edw_quentin", "EDW III Quentin" , "l")
	leg.AddEntry("gr_edw_poisson", "EDW III Poisson" , "l")

	leg.AddEntry("gr_lim", "EDW III FID837" , "l")
	leg.SetFillColor(kWhite)
	leg.SetLineColor(kWhite)

	t_cdms = TText(0.3,1E-10,"truc")
	t_cdms.SetTextSize(0.03)
	t_cdms.SetTextColor(kBlue-3)
	t_cdms.DrawText(4.68,8.6E-6,"CDMS")

	t_dama = TText(0.3,1E-10,"truc")
	t_dama.SetTextSize(0.03)
	t_dama.SetTextColor(kRed-3)
	t_dama.DrawText(10.9,2E-4,"DAMA")

	t_cresst = TText(0.3,1E-10,"truc")
	t_cresst.SetTextSize(0.03)
	t_cresst.SetTextColor(kGreen+2)
	t_cresst.DrawText(19.9,1E-5,"CRESST")

	t_CoGeNT = TText(0.3,1E-10,"truc")
	t_CoGeNT.SetTextSize(0.03)
	t_CoGeNT.SetTextColor(kOrange+7)
	t_CoGeNT.DrawText(6.4,6.5E-5,"CoGeNT")

	t_lux = TText(0.3,1E-10,"truc")
	t_lux.SetTextSize(0.03)
	t_lux.SetTextColor(kBlack)
	t_lux.DrawText(5.8,3.3E-7,"LUX")

	t_edw2 = TText(0.3,1E-10,"truc")
	t_edw2.SetTextSize(0.03)
	t_edw2.SetTextColor(kRed)
	t_edw2.DrawText(7,7E-4,"EDW-II")

	t_edw3 = TText(0.3,1E-10,"truc")
	t_edw3.SetTextSize(0.03)
	t_edw3.SetTextColor(kRed)
	t_edw3.DrawText(9.9,2.16E-6,"EDW-III")

	t_edw3_like = TText(0.3,1E-10,"truc")
	t_edw3_like.SetTextSize(0.03)
	t_edw3_like.SetTextColor(kRed)
	t_edw3_like.DrawText(4,3E-3,"EDW-III likelihood FID837")

	t_edw3proj9 = TText(0.3,1E-10,"truc")
	t_edw3proj9.SetTextSize(0.03)
	t_edw3proj9.SetTextColor(kRed)
	t_edw3proj9.DrawText(13.8,6.3E-8,"EDW-III likelihood 9 bolo")

	raw_input()

	cc.Print("./Figures/FID837_" + analysis_type + "_limit_proj.eps")

analysis_type = "ana_0.5_0_5"
exposure = 65
list_mass = [4, 5, 6, 7, 10, 25]
bolo_name = "FID837"

plot_limit(bolo_name, list_mass, analysis_type, exposure)




