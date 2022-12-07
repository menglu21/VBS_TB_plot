import ROOT
import time
import os
import math
from math import sqrt
import argparse

#TTC_header_path = os.path.join("TB.h")
#ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))
ROOT.gInterpreter.ProcessLine('#include "TB.h"')

RDataFrame = ROOT.RDataFrame

def main():
  usage = 'usage: %prog [options]'
  parser = argparse.ArgumentParser(usage)
  parser.add_argument('-i', '--inputs',dest='inputs',help='input root file',default='dummy.root')
  parser.add_argument('-r', '--region',dest='region',help='SR or which CR',default='onelep_b_region')
  parser.add_argument('-c', '--category',dest='category',help='one lep or two lep category',default='one')
  parser.add_argument('-s', '--channel',dest='channel',help='ele or muon channel',default='muon')
  args = parser.parse_args()
  inputroot=args.inputs
  output_name='output.root'
  regions=args.region
  category=args.category
  channel=args.channel
  TB_Analysis(inputroot,output_name,regions,category,channel)

def overunder_flowbin(h1):
  h1.SetBinContent(1,h1.GetBinContent(0)+h1.GetBinContent(1))
  h1.SetBinError(1,sqrt(h1.GetBinError(0)*h1.GetBinError(0)+h1.GetBinError(1)*h1.GetBinError(1)))
  h1.SetBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX())+h1.GetBinContent(h1.GetNbinsX()+1))
  h1.SetBinError(h1.GetNbinsX(),sqrt(h1.GetBinError(h1.GetNbinsX())*h1.GetBinError(h1.GetNbinsX())+h1.GetBinError(h1.GetNbinsX()+1)*h1.GetBinError(h1.GetNbinsX()+1)))
  return h1

def mc_trigger(df):
  all_trigger = df.Filter("HLT_IsoMu27 || HLT_passEle32WPTight")
  return all_trigger

def singleele_trigger(df):
  sin_ele_trigger = df.Filter("HLT_passEle32WPTight")
  return sin_ele_trigger

def singlemuon_trigger(df):
  single_mu_trigger = df.Filter("HLT_IsoMu27")
  return single_mu_trigger



MET_filter = "Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter"


def TB_Analysis(inputfile,outputname,regions,category,channel):

  ismc=False

  #histograms name
  hists_name_common = {
  'n_tight_jet':[10,0,10],
  'n_bjet_DeepB_M':[4,0,4],
  'n_bjet_DeepB_L':[4,0,4],
  'n_tight_nob':[10,0,10],
  'HT':[40,0,1000],
  'j1_pt':[25,0,500],
  'j1_eta':[20,-5,5],
  'j1_phi':[20,-4,4],
  'j1_mass':[20,0,40],
  'j2_pt':[15,0,300],
  'j2_eta':[20,-5,5],
  'j2_phi':[20,-4,4],
  'j2_mass':[15,0,30],
  'j3_pt':[15,0,150],
  'j3_eta':[20,-5,5],
  'j3_phi':[20,-4,4],
  'j3_mass':[10,0,20],
  'j4_pt':[10,0,100],
  'j4_eta':[20,-5,5],
  'j4_phi':[20,-4,4],
  'j4_mass':[10,0,20],
  'met_user':[10,0,200],
  'met_phi_user':[20,-4,4],
  'mjj_nob':[40,60,100],
  'detajj_nob':[20,0,10]
  }

  hists_name_others = {}
  
  if category=='one':
    hists_name_others = {
    'Onelep_l1_pt':[25,0,250],
    'Onelep_l1_eta':[20,-2.5,2.5],
    'Onelep_l1_phi':[20,-4,4]
    }
  
  if category=='two':
    hists_name_others = {
    'Twolep_l1_pt':[20,0,200],
    'Twolep_l1_eta':[20,-2.5,2.5],
    'Twolep_l1_phi':[20,-4,4],
    'Twolep_l2_pt':[20,0,200],
    'Twolep_l2_eta':[20,-2.5,2.5],
    'Twolep_l2_phi':[20,-4,4],
    'Twolep_mll':[20,0,200]
    }
  
  hists_common_keys=list(hists_name_common.keys())
  hists_common_bins=[hists_name_common[x][0] for x in hists_common_keys]
  hists_common_edgeLow=[hists_name_common[x][1] for x in hists_common_keys]
  hists_common_edgeHigh=[hists_name_common[x][2] for x in hists_common_keys]
  
  hists_others_keys=list(hists_name_others.keys())
  hists_others_bins=[hists_name_others[x][0] for x in hists_others_keys]
  hists_others_edgeLow=[hists_name_others[x][1] for x in hists_others_keys]
  hists_others_edgeHigh=[hists_name_others[x][2] for x in hists_others_keys]
  
  HIST_names=hists_common_keys[:]
  HIST_names.extend(hists_others_keys)
  HIST_bins=hists_common_bins[:]
  HIST_bins.extend(hists_others_bins)
  HIST_edgeLow=hists_common_edgeLow[:]
  HIST_edgeLow.extend(hists_others_edgeLow)
  HIST_edgeHigh=hists_common_edgeHigh[:]
  HIST_edgeHigh.extend(hists_others_edgeHigh)

  Filter=""
  if regions=="onelep_b_region":
    if channel=='ele':
      Filter="onelep_b_region==1 && Onelep_l1_pt>30 && Onelep_l1_faketag==1 && abs(Onelep_l1_pdgid)==11"
    else:
      Filter="onelep_b_region==1 && Onelep_l1_pt>30 && Onelep_l1_faketag==1 && abs(Onelep_l1_pdgid)==13"
  if regions=="onelep_nob_region":
    if channel=='ele':
      Filter="onelep_b_region==1 && Onelep_l1_pt>30 && Onelep_l1_faketag==1 && abs(Onelep_l1_pdgid)==11"
    else:
      Filter="onelep_b_region==1 && Onelep_l1_pt>30 && Onelep_l1_faketag==1 && abs(Onelep_l1_pdgid)==13"
  if regions=="tt2L_region":
    if channel=='ee':
      Filter="tt2L_region==1 && Twolep_l1_pt>30 && Twolep_l2_pt>25 && Twolep_2P0F==1 && abs(Twolep_l1_pdgid)==11 && abs(Twolep_l2_pdgid)==11 && (Twolep_l1_pdgid+Twolep_l2_pdgid)==0"
    elif channel=='em':
      Filter="tt2L_region==1 && Twolep_l1_pt>30 && Twolep_l2_pt>25 && Twolep_2P0F==1 && abs(Twolep_l1_pdgid)==13 && abs(Twolep_l2_pdgid)==11 && abs(Twolep_l1_pdgid+Twolep_l2_pdgid)==2"
    else:
      Filter="tt2L_region==1 && Twolep_l1_pt>30 && Twolep_l2_pt>25 && Twolep_2P0F==1 && abs(Twolep_l1_pdgid)==13 && abs(Twolep_l2_pdgid)==13 && (Twolep_l1_pdgid+Twolep_l2_pdgid)==0"
  if regions=="dy_region":
    if channel=='ee':
      Filter="dy_region==1 && Twolep_l1_pt>30 && Twolep_l2_pt>25 && Twolep_2P0F==1 && abs(Twolep_l1_pdgid)==11 && abs(Twolep_l2_pdgid)==11 && (Twolep_l1_pdgid+Twolep_l2_pdgid)==0"
    elif channel=='em':
      Filter="dy_region==1 && Twolep_l1_pt>30 && Twolep_l2_pt>25 && Twolep_2P0F==1 && abs(Twolep_l1_pdgid)==11 && abs(Twolep_l2_pdgid)==11 && (Twolep_l1_pdgid+Twolep_l2_pdgid)==2"
    else:
      Filter="dy_region==1 && Twolep_l1_pt>30 && Twolep_l2_pt>25 && Twolep_2P0F==1 && abs(Twolep_l1_pdgid)==13 && abs(Twolep_l2_pdgid)==13 && (Twolep_l1_pdgid+Twolep_l2_pdgid)==0"

  fout = ROOT.TFile.Open(outputname,'recreate')

  filein=ROOT.TFile.Open(inputfile)
  fout.cd()
  if not 'Single' in inputfile:
    hweight=ROOT.TH1D()
    hweight=filein.Get("nEventsGenWeighted")
    hweight.Write()
    ismc=True
  filein.Close()

  df_histos=[]

  df_tree_ = ROOT.RDataFrame("Events", inputfile)
  if ismc: df_tree = mc_trigger(df_tree_)
  else:
    if channel=='muon': df_tree = singlemuon_trigger(df_tree_)
    if channel=='ele': df_tree = singleele_trigger(df_tree_)
  df_filter_ = df_tree.Filter(MET_filter)
  df_filter = df_filter_.Filter(Filter)
  df_filter = df_filter.Define('mjj_nob',"bugfix_mj1j2_nob(n_tight_nob, j1_isB, j2_isB, j3_isB, j4_isB, mj1j2, mj1j3, mj1j4, mj2j3, mj2j4, mj3j4)")
  df_filter = df_filter.Define('detajj_nob',"bugfix_detaj1j2_nob(n_tight_nob, j1_isB, j2_isB, j3_isB, j4_isB, detaj1j2, detaj1j3, detaj1j4, detaj2j3, detaj2j4, detaj3j4)")
                   

  if ismc:
    if channel=='ele':
      df_filter = df_filter.Define('genweight','puWeight*PrefireWeight*Electron_RECO_SF[Onelep_l1_id]*Electron_CutBased_TightID_SF[Onelep_l1_id]*genWeight/abs(genWeight)')
    if channel=='muon':
      df_filter = df_filter.Define('genweight','puWeight*PrefireWeight*Muon_CutBased_TightID_SF[Onelep_l1_id]*Muon_TightRelIso_TightIDandIPCut_SF[Onelep_l1_id]*genWeight/abs(genWeight)')


  # further cuts
  #Filters_TT1L = "met_user>50 && mjj_nob>60 && mjj_nob<100"
  Filters_signal = "met_user>50 && mjj_nob>500 && detajj_nob>2.5"

  for i in range(0,len(HIST_names)):
    if ismc:
      df_filter_tmp=df_filter.Filter(Filters_signal)
      df_histo = df_filter_tmp.Histo1D((HIST_names[i]+'_'+category+'_'+channel,'',HIST_bins[i],HIST_edgeLow[i],HIST_edgeHigh[i]), HIST_names[i],'genweight')
    else:
      df_filter_tmp=df_filter.Filter(Filters_signal)
      df_histo = df_filter_tmp.Histo1D((HIST_names[i]+'_'+category+'_'+channel,'',HIST_bins[i],HIST_edgeLow[i],HIST_edgeHigh[i]), HIST_names[i])
    df_histos.append(overunder_flowbin(df_histo))


  fout.cd()
  for ij in range(0,len(HIST_names)):
    h_temp = df_histos[ij].GetValue()
    h_temp.Write()

  fout.Close()

if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 
  print "Job starts"
  main()
  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1

