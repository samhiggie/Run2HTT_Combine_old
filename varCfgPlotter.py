### Nov 13, 2016
### File to store all of the configurations for the
### SM HTT postfit/postfit plotter
###
###
# FIXME FIXME FIXME
# Once the most updated root files are uploaded, the default paths can be set
# in getFile()
# ETau, MuTau and EMu need to double check getBinMap() whic
# provides the number of times unrolled and number of mass bins per
# unroll and labeling

from collections import OrderedDict

# Provide the category names (folder names)
# where we should look for histograms
#def getCategories( channel="tt", prefix="" ) :
#    preCategories=["_0jet","_boosted","_VBF"] 
#    if channel == "em" or channel == "et" or channel == "mt": # FIXME vbf --> VBF when ready
#        preCategories=["_0jet","_boosted","_vbf"] 
#    categories=[prefix+channel+cat for cat in preCategories]
#    return categories

def getCategories( channel="mt", prefix="", year="2017" ) :
    if channel =="mt" :
    	preCategories=["_0jet_PTH_0_10","_0jet_PTH_GE10","_boosted_1J","_boosted_GE2J","_vbf_PTH_0_200","_vbf_PTH_GE_200"]
    #preCategories=["_3_"]
    #categories=["htt_"+channel+cat+"13TeV_postfit" for cat in preCategories]
    	categories=[channel+cat+"_"+year+"_prefit" for cat in preCategories]
    if channel =="em" or channel == "et" :
        preCategories=["_0jetlow_","_0jethigh_","_boosted1_","_boosted2_","_vbflow_","_vbfhigh_"]
      	categories=[channel+cat+year+"_prefit" for cat in preCategories]
    if channel == "tt" :
        preCategories=["cat0_","cat1_","cat2_","cat3_","cat4_"]
      	categories=[cat+year+"_prefit" for cat in preCategories]
    return categories

# Provide standard mapping to our files
# this can be overridden with --inputFile
def getFile( channel ) :
    fileMap = {
       #"mt" : "/home/abhi/CERN/analysis/'prefit plots'/prefit_2017_mt_240719.root",
       # "mt" : "/afs/cern.ch/work/a/amallamp/private/CMSSW_10_2_13/src/CombineHarvester/Run2HTT_Combine/HTT_Output/AllNonEmbedded/Output_220719_3EdNAR/prefit_2017_mt_240719.root",
       # "et" : "shapes/USCMS/htt_et.inputs-sm-13TeV-mvis.root", # Not up to date
       # "mt" : "shapes/USCMS/htt_mt.inputs-sm-13TeV-mvis.root", # Not up to date
       # "em" : "emu_unrolled.root", # Not saved publically
        #"em" : "shapes/USCMS/htt_em.inputs-sm-13TeV-mvis.root", # Not up to date
       # "tt" : "tautau.root",
        #"tt" : "shapes/USCMS/htt_tt.inputs-sm-13TeV-svfitmass2D.root", # Not up to date
        "mt" :"/afs/cern.ch/work/a/amallamp/private/CMSSW_10_2_13/src/CombineHarvester/Run2HTT_Combine/HTT_Output/Output_220819_C7LeJr/prefit_2017_mt_220819.root" ,
        "em" : "/afs/cern.ch/work/a/amallamp/private/CMSSW_10_2_13/src/CombineHarvester/Run2HTT_Combine/HTT_Output/Output_220819_XVeJb8/prefit_2017_em_220819.root",
        "et" : "/afs/cern.ch/work/a/amallamp/private/CMSSW_10_2_13/src/CombineHarvester/Run2HTT_Combine/HTT_Output/Output_220819_tumD5d/prefit_2017_et_220819.root",
        "tt" : "/afs/cern.ch/work/a/amallamp/private/CMSSW_10_2_13/src/CombineHarvester/Run2HTT_Combine/HTT_Output/Output_220819_e9GJjB/prefit_2017_tt_220819.root",
    }
    return fileMap[ channel ]

def getInfoMap( higgsSF, channel ) :
    if channel == "mt" : sub = ("h", "#mu")  
    if channel == "et" : sub = ("h", "e")
    if channel == "em" : sub = ("e", "#mu")
    if channel == "tt" : sub = ("h", "h")
    
    infoMap = OrderedDict()
    # Name : Add these shapes [...], legend name, leg type, fill color
    infoMap["data_obs"] = [["data_obs"],"Observed","elp",1]
    # infoMap["ZTT"] = [["ZTT","EWKZ"],"Z#rightarrow#tau#tau","f","#ffcc66"]
   # infoMap["ZJ"] = [["ZJ","ZL",],"Z#rightarrow#mu#mu/ee","f","#4496c8"]

# drell yan to taus, replaced by embedded in 2017,2018
    infoMap["ZT"] = [["ZT"],"DY #rightarrow #tau#tau","f","#ffcc66"]
    infoMap["DYT"] = [["DYT"],"DY #rightarrow #tau#tau","f","#ffcc66"]
    infoMap["embedded"] = [["embedded"],"Embedded","f","#ffcc66"]

# drell yan to light leptons
    infoMap["ZL"] = [["ZL"],"DY #rightarrow ll","f","#4496c8"]
    infoMap["DYL"] = [["DYL"],"DY #rightarrow ll","f","#4496c8"]


    infoMap["TT"] = [["TTL","TTT"],"t#bar{t}","f","#9999cc"]

    infoMap["jetFakes"] = [["jetFakes"],"Fakes","f","#ffccff"]
    infoMap["QCD"] = [["QCD"],"QCD","f","#ffccff"]  # present in em channel
    infoMap["W"] = [["W"],"W+Jets","f","#ffccff"]    

    infoMap["Other"] = [["VVT","VVL","STL","STT"],"Other","f","#12cadd"] 

    infoMap["TotalSig"] = [["TotalSig"],"Signal","f","kRed"]  #FIXME
      #  if channel == "em" :
        # This is intentional and will not be changed
  #      infoMap["TT"] = [["TT",],"t#bar{t}+jets","f","#9999cc"]
  #  else :
  #      infoMap["TT"] = [["TTT","TTJ",],"t#bar{t}+jets","f","#9999cc"]
  #  infoMap["W"] = [["W",],"W+jets","f","#de5a6a"]
  #  infoMap["QCD"] = [["QCD",],"QCD multijet","f","#ffccff"]
  #  if channel == "tt" :
  #      infoMap["VV"] = [["VVT","VVJ",],"Others","f","#12cadd"]
  #  elif channel == "em" :
  #      infoMap["VV"] = [["VV","HWW_qq125","HWW_gg125",],"Others","f","#12cadd"]
  #  else:
  #      infoMap["VV"] = [["VV",],"Others","f","#12cadd"]
    #infoMap["H125"] = [["ggH125","WH125","ZH125","qqH125",],"H#rightarrow#tau#tau 125 (X%i)"%higgsSF,"l","#000000"]
  #  infoMap["H125"] = [["ggH","WH","ZH","qqH",],"H#rightarrow#tau#tau (#mu = 1.06)","l","#000000"]
    return infoMap


def getBackgrounds() :    
    #bkgs=["VV", "QCD", "W", "TT", "ZJ", "ZTT"]
    #bkgs=["TTL","TTT", "ZL", "jetFakes", "ZT", "VVL", "VVT"]
    bkgs=["TT", "ZL","DYL","DYT","QCD","W","jetFakes", "ZT", "Other","embedded"]      # FIXME 
    return bkgs

def getSignals() :
    #signals=["H125"]
    signals=["TotalSig"]  
    return signals

# Labeling map, this provides, for each channel   
# and category :                                           
# unrolling binning in "binning"                  
# the number of times unrolled in a variable "nx" 
# the number of mass bins per unroll "ny"         
# and labeling for the divider lines
def getBinMap() :
    binMap = {                  #@@# means that we need to check binning
        "em" : {
            "em_0jetlow_2016_prefit" :{},#@@#27
            "em_0jetlow_2017_prefit" : {
		"nx" : 3,
		"ny" : 11,  # 11 because there are actually 10, 11th is overflow bin
		"binning" : [30,40,50,9000], # 9000 is the infinity that we are using..can be any high value..
		"name" : "#tau_{Pt}", 
             },
            "em_0jetlow_2018_prefit" :{},
# -------------------------------------------------
            "em_0jethigh_2016_prefit" :{},#@@#36
	    "em_0jethigh_2017_prefit" : {
		"nx" : 5,
		"ny" : 11,
		"binning" : [30,40,50,60,70,9000],
		"name" : "#tau_{Pt}",
             },
            "em_0jethigh_2018_prefit" :{},
#-------------------------------------------------------
            "em_boosted1_2016_prefit" : {},
            "em_boosted1_2017_prefit" : {
		"nx" : 6,
		"ny" : 9,
		"binning" : [0.0,60.0,120.0,200.0,250.0,300.0,9000.0],
		"name" : "H_{Pt}",
             },
            "em_boosted1_2018_prefit" : {},
#--------------------------------------------------------
            "em_boosted2_2016_prefit" : {},#@@#36
            "em_boosted2_2017_prefit" : {
		"nx" : 6,
		"ny" :9 ,
		"binning" : [0.0,60.0,120.0,200.0,250.0,300.0,9000.0],
		"name" : "H_{Pt}",
             },
            "em_boosted2_2018_prefit" : {},
#-----------------------------------------------------------
            "em_vbflow_2016_prefit" : {},
            "em_vbflow_2017_prefit" : {
		"nx" : 4,
		"ny" : 9,
		"binning" :[350.0,700.0,1000.0,1500.0,9000.0] ,
		"name" : "m_{jj}",
             },
            "em_vbflow_2018_prefit" : {},
#-----------------------------------------------------
	    "em_vbfhigh_2016_prefit" : {},#@@#54
            "em_vbfhigh_2017_prefit" : {
		"nx" : 4,
		"ny" :9 ,
		"binning" : [350.0,700.0,1000.0,1500.0,9000.0],
		"name" : "m_{jj}",
             },
            "em_vbfhigh_2018_prefit" : {},
#            "htt_em_1_13TeV_postfit" : {
#                "nx" : 3,
#                "ny" : 12,
#                "binning" : [15,25,35],
#                "name" : "p_{T}(#mu)",
#            },
#            "htt_em_2_13TeV_postfit" : {
#                "nx" : 6,
#                "ny" : 10,
#                "binning" : [0,100,150,200,250,300],
#                "name" : "p_{T}^{#tau#tau}",
#            },
#            "htt_em_3_13TeV_postfit" : { # FIXME vbf --> VBF when ready
#                "nx" : 4,
#                "ny" : 5,
#                "binning" : [300,700,1100,1500],
#                "name" : "m_{jj}",
#            },
        }, # end 'em'
        "mt" : {
 #           "htt_mt_1_13TeV_postfit" : {
 #               "nx" : 3,
  #              "ny" : 12,
  #              "binning" : ["1 prong","1 prong + #pi^{0}", "3 prongs"],
  #              "name" : "p_{T}(#tau_{h})",
  #          },
  #          "htt_mt_2_13TeV_postfit" : {
  #              "nx" : 6,
 #               "ny" : 10,
 #               "binning" : [0,100,150,200,250,300],
 #               "name" : "p_{T}^{#tau#tau}",
  #          },
  #          "htt_mt_3_13TeV_postfit" : { 
 #               "nx" : 4,
 #               "ny" : 5,
 #               "binning" : [300,700,1100,1500],
 #               "name" : "m_{jj}",
 #           },
            "mt_0jet_PTH_0_10_2016_prefit" : {},
            "mt_0jet_PTH_0_10_2017_prefit" : {
		"nx" : 3,
		"ny" : 11, 
		#"binning" : [30,40,50,60,70,80,9000], 
                "binning" : [30,40,50,9000],
		"name" : "#tau_{Pt}", 
             },
            "mt_0jet_PTH_0_10_2018_prefit" : {},
#---------------------------------------------------
            "mt_0jet_PTH_GE10_2016_prefit" : {},
	    "mt_0jet_PTH_GE10_2017_prefit" : {
		"nx" : 5,
		"ny" : 11,
		#"binning" : [30,40,50,60,70,80,9000],
                "binning" : [30,40,50,60,70,9000],
		"name" : "#tau_{Pt}",
             },
            "mt_0jet_PTH_GE10_2018_prefit" : {},
#------------------------------------------------------
            "mt_boosted_1J_2016_prefit" : {},
            "mt_boosted_1J_2017_prefit" : {
		"nx" : 6,
		"ny" : 9,
		"binning" : [0.0,60.0,120.0,200.0,250.0,300.0,9000.0],
		"name" : "H_{Pt}",
             },
            "mt_boosted_1J_2018_prefit" : {},
#--------------------------------------------------------
            "mt_boosted_GE2J_2016_prefit" : {},
            "mt_boosted_GE2J_2017_prefit" : {
		"nx" : 6,
		"ny" :9 ,
		"binning" : [0.0,60.0,120.0,200.0,250.0,300.0,9000.0],
		"name" : "H_{Pt}",
             },
            "mt_boosted_GE2J_2018_prefit" : {},
#----------------------------------------------------------
	    "mt_vbf_PTH_0_200_2016_prefit" : {},
            "mt_vbf_PTH_0_200_2017_prefit" : {
		"nx" : 4,
		"ny" : 9,
		"binning" :[350.0,700.0,1000.0,1500.0,9000.0] ,
		"name" : "m_{jj}",
             },
            "mt_vbf_PTH_0_200_2018_prefit" : {},
#------------------------------------------------------------
            "mt_vbf_PTH_GE_200_2016_prefit" : {},
            "mt_vbf_PTH_GE_200_2017_prefit" : {
		"nx" : 4,
		"ny" :9 ,
		"binning" : [350.0,700.0,1000.0,1500.0,9000.0],
		"name" : "m_{jj}",
             },
	    "mt_vbf_PTH_GE_200_2018_prefit" : {},
        }, # end 'mt'
        "et" : {
            "et_0jetlow_2016_prefit" :{},#@@#54
            "et_0jetlow_2017_prefit" : {
		"nx" : 3, 
		"ny" : 11,  
		"binning" : [30,40,50,9000], 
		"name" : "#tau_{Pt}", 
             },
            "et_0jetlow_2018_prefit" :{},
# -------------------------------------------------
            "et_0jethigh_2016_prefit" :{},
	    "et_0jethigh_2017_prefit" : {
		"nx" : 5,
		"ny" : 11,
		"binning" : [30,40,50,60,70,9000],
		"name" : "#tau_{Pt}",
             },
            "et_0jethigh_2018_prefit" :{},
#-------------------------------------------------------
            "et_boosted1_2016_prefit" : {},
            "et_boosted1_2017_prefit" : {
		"nx" : 6,
		"ny" : 9,
		"binning" : [0.0,60.0,120.0,200.0,250.0,300.0,9000.0],
		"name" : "H_{Pt}",
             },
            "et_boosted1_2018_prefit" : {},
#--------------------------------------------------------
            "et_boosted2_2016_prefit" : {}, #@@#36
            "et_boosted2_2017_prefit" : {
		"nx" : 6,
		"ny" : 9 ,
		"binning" : [0.0,60.0,120.0,200.0,250.0,300.0,9000.0],
		"name" : "H_{Pt}",
             },
            "et_boosted2_2018_prefit" : {},
#-----------------------------------------------------------
            "et_vbflow_2016_prefit" : {},
            "et_vbflow_2017_prefit" : {
		"nx" : 4,
		"ny" : 9,
		"binning" :[350.0,700.0,1000.0,1500.0,9000.0] ,
		"name" : "m_{jj}",
             },
            "et_vbflow_2018_prefit" : {},
#-----------------------------------------------------
	    "et_vbfhigh_2016_prefit" : {},#@@#33
            "et_vbfhigh_2017_prefit" : {
		"nx" : 4,
		"ny" :9 ,
		"binning" : [350.0,700.0,1000.0,1500.0,9000.0],
		"name" : "m_{jj}",
             },
            "et_vbfhigh_2018_prefit" : {}, 
#            "htt_et_1_13TeV_postfit" : {
#                "nx" : 3,
#                "ny" : 12,
#                "binning" : ["1 prong","1 prong + #pi^{0}", "3 prongs"],
#                "name" : "p_{T}(#tau_{h})",
#            },
#            "htt_et_2_13TeV_postfit" : {
#                "nx" : 6,
#                "ny" : 10,
#                "binning" : [0,100,150,200,250,300],
#                "name" : "p_{T}^{#tau#tau}",
#            },
#            "htt_et_3_13TeV_postfit" : { 
#                "nx" : 4,
#                "ny" : 5,
#                "binning" : [300,700,1100,1500],
#                "name" : "m_{jj}",
#            },
        }, # end 'et'
        "tt" : {
            "cat0_2016_prefit" :{},
            "cat0_2017_prefit" : {
		"nx" : 1,
		"ny" : 9,  #
# Commenting these out because no rolling is used in tt cat0..you can know this by looking at the "prefit_2016_tt_020919.root" file..it has only 9 bins unlike the other categories
		#"binning" : [30,40,50,60,70,80,9000], 
		#"name" : "#tau_{Pt}", 
             },
            "cat0_2018_prefit" :{},
#-------------------------------------------------------
            "cat1_2016_prefit" : {},
            "cat1_2017_prefit" : {
		"nx" : 6,
		"ny" : 9,
		"binning" : [0.0,60.0,120.0,200.0,250.0,300.0,9000.0],
		"name" : "H_{Pt}",
             },
            "cat1_2018_prefit" : {},
#--------------------------------------------------------
            "cat2_2016_prefit" : {},
            "cat2_2017_prefit" : {
		"nx" : 6,
		"ny" :9 ,
		"binning" : [0.0,60.0,120.0,200.0,250.0,300.0,9000.0],
		"name" : "H_{Pt}",
             },
            "cat2_2018_prefit" : {},
#-----------------------------------------------------------
            "cat3_2016_prefit" : {},
            "cat3_2017_prefit" : {
		"nx" : 5,
		"ny" : 9,
		"binning" :[0,350.0,700.0,1000.0,1500.0,9000.0] ,
		"name" : "m_{jj}",
             },
            "cat3_2018_prefit" : {},
#-----------------------------------------------------
	    "cat4_2016_prefit" : {},
            "cat4_2017_prefit" : {
		"nx" : 5,
		"ny" :9 ,
		"binning" : [0,350.0,700.0,1000.0,1500.0,9000.0],
		"name" : "m_{jj}",
             },
            "cat4_2018_prefit" : {},
#            "htt_tt_1_13TeV_postfit" : {
#                "nx" : 1,
#                "ny" : 30,
#                "binning" : [0,],
#                "name" : "N/A",
#            },
#            "htt_tt_2_13TeV_postfit" : {
#                "nx" : 4,
#                "ny" : 12,
#                "binning" : [0,100,170,300],
#                "name" : "p_{T}^{#tau#tau}",
#            },
#            "htt_tt_3_13TeV_postfit" : {
#                "nx" : 4,
#                "ny" : 12,
#                "binning" : [0,300,500,800],
#                "name" : "m_{jj}",
#            },
        }, # end 'tt'
    }
    binMap["em"]["em_0jetlow_2016_prefit"] = binMap["em"]["em_0jetlow_2017_prefit"]
    binMap["em"]["em_0jetlow_2018_prefit"] = binMap["em"]["em_0jetlow_2017_prefit"]
    binMap["et"]["et_0jetlow_2016_prefit"] = binMap["et"]["et_0jetlow_2017_prefit"]
    binMap["et"]["et_0jetlow_2018_prefit"] = binMap["et"]["et_0jetlow_2017_prefit"]
    
    binMap["em"]["em_0jethigh_2016_prefit"] = binMap["em"]["em_0jethigh_2017_prefit"]
    binMap["em"]["em_0jethigh_2018_prefit"] = binMap["em"]["em_0jethigh_2017_prefit"]
    binMap["et"]["et_0jethigh_2016_prefit"] = binMap["et"]["et_0jethigh_2017_prefit"]
    binMap["et"]["et_0jethigh_2018_prefit"] = binMap["et"]["et_0jethigh_2017_prefit"]

    binMap["em"]["em_boosted1_2016_prefit"] = binMap["em"]["em_boosted1_2017_prefit"]
    binMap["em"]["em_boosted1_2018_prefit"] = binMap["em"]["em_boosted1_2017_prefit"]
    binMap["et"]["et_boosted1_2016_prefit"] = binMap["et"]["et_boosted1_2017_prefit"]
    binMap["et"]["et_boosted1_2018_prefit"] = binMap["et"]["et_boosted1_2017_prefit"]

    binMap["em"]["em_boosted2_2016_prefit"] = binMap["em"]["em_boosted2_2017_prefit"]
    binMap["em"]["em_boosted2_2018_prefit"] = binMap["em"]["em_boosted2_2017_prefit"]
    binMap["et"]["et_boosted2_2016_prefit"] = binMap["et"]["et_boosted2_2017_prefit"]
    binMap["et"]["et_boosted2_2018_prefit"] = binMap["et"]["et_boosted2_2017_prefit"]

    binMap["em"]["em_vbflow_2016_prefit"] = binMap["em"]["em_vbflow_2017_prefit"]
    binMap["em"]["em_vbflow_2018_prefit"] = binMap["em"]["em_vbflow_2017_prefit"]
    binMap["et"]["et_vbflow_2016_prefit"] = binMap["et"]["et_vbflow_2017_prefit"]
    binMap["et"]["et_vbflow_2018_prefit"] = binMap["et"]["et_vbflow_2017_prefit"]

    binMap["em"]["em_vbfhigh_2016_prefit"] = binMap["em"]["em_vbfhigh_2017_prefit"]
    binMap["em"]["em_vbfhigh_2018_prefit"] = binMap["em"]["em_vbfhigh_2017_prefit"]
    binMap["et"]["et_vbfhigh_2016_prefit"] = binMap["et"]["et_vbfhigh_2017_prefit"]
    binMap["et"]["et_vbfhigh_2018_prefit"] = binMap["et"]["et_vbfhigh_2017_prefit"]

    binMap["tt"]["cat0_2016_prefit"] = binMap["tt"]["cat0_2017_prefit"]
    binMap["tt"]["cat0_2018_prefit"] = binMap["tt"]["cat0_2017_prefit"]
    binMap["tt"]["cat1_2016_prefit"] = binMap["tt"]["cat1_2017_prefit"]
    binMap["tt"]["cat1_2018_prefit"] = binMap["tt"]["cat1_2017_prefit"]
    binMap["tt"]["cat2_2016_prefit"] = binMap["tt"]["cat2_2017_prefit"]
    binMap["tt"]["cat2_2018_prefit"] = binMap["tt"]["cat2_2017_prefit"]
    binMap["tt"]["cat3_2016_prefit"] = binMap["tt"]["cat3_2017_prefit"]
    binMap["tt"]["cat3_2018_prefit"] = binMap["tt"]["cat3_2017_prefit"]
    binMap["tt"]["cat4_2016_prefit"] = binMap["tt"]["cat4_2017_prefit"]
    binMap["tt"]["cat4_2018_prefit"] = binMap["tt"]["cat4_2017_prefit"]
    
    binMap["mt"]["mt_0jet_PTH_0_10_2016_prefit"] = binMap["mt"]["mt_0jet_PTH_0_10_2017_prefit"]
    binMap["mt"]["mt_0jet_PTH_0_10_2018_prefit"] = binMap["mt"]["mt_0jet_PTH_0_10_2017_prefit"]  
    binMap["mt"]["mt_0jet_PTH_GE10_2016_prefit"] = binMap["mt"]["mt_0jet_PTH_GE10_2017_prefit"]
    binMap["mt"]["mt_0jet_PTH_GE10_2018_prefit"] = binMap["mt"]["mt_0jet_PTH_GE10_2017_prefit"]  
    binMap["mt"]["mt_boosted_1J_2016_prefit"] = binMap["mt"]["mt_boosted_1J_2017_prefit"]
    binMap["mt"]["mt_boosted_1J_2018_prefit"] = binMap["mt"]["mt_boosted_1J_2017_prefit"]  
    binMap["mt"]["mt_boosted_GE2J_2016_prefit"] = binMap["mt"]["mt_boosted_GE2J_2017_prefit"]
    binMap["mt"]["mt_boosted_GE2J_2018_prefit"] = binMap["mt"]["mt_boosted_GE2J_2017_prefit"]  
    binMap["mt"]["mt_vbf_PTH_0_200_2016_prefit"] = binMap["mt"]["mt_vbf_PTH_0_200_2017_prefit"]
    binMap["mt"]["mt_vbf_PTH_0_200_2018_prefit"] = binMap["mt"]["mt_vbf_PTH_0_200_2017_prefit"]  
    binMap["mt"]["mt_vbf_PTH_GE_200_2016_prefit"] = binMap["mt"]["mt_vbf_PTH_GE_200_2017_prefit"]
    binMap["mt"]["mt_vbf_PTH_GE_200_2018_prefit"] = binMap["mt"]["mt_vbf_PTH_GE_200_2017_prefit"] 

    return binMap

