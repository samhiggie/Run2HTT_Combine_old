#!/usr/bin/env python
import ROOT
from ROOT import *
import re
from array import array
import argparse

parser = argparse.ArgumentParser(description="Script for smoothing combine input files.")
parser.add_argument("--bins_per_slice",type=int,nargs="?",help="# of bins in a slice",default=0)
parser.add_argument("--bins_per_slice_0jet",type=int,nargs="?",help="# of bins per each 0jet slice",default=8)
parser.add_argument("--bins_per_slice_boosted",type=int,nargs="?",help="# of bins per boosted slice",default=10)
parser.add_argument("--bins_per_slice_vbf",type=int,nargs="?",help="# of bins per vbf slice",default=6)

parser.add_argument("--nslices",type=int,nargs="?",help="# of slices",default=0)
parser.add_argument("--nslices_0jet",type=int,nargs="?",help="# of slices in 0jet",default=5)
parser.add_argument("--nslices_boosted",type=int,nargs="?",help="# of slices in boosted",default=5)
parser.add_argument("--nslices_vbf",type=int,nargs="?",help="# of slices in 0jet",default=5)

parser.add_argument("--file_in",nargs="?",help="Name of input file",default="smh_et.root")
parser.add_argument("--file_out",nargs="?",help="Name of output file",default="smh_et_smooth.root")


args = parser.parse_args()

bins_per_slice=args.bins_per_slice
bins_per_slice_0jet=args.bins_per_slice_0jet
bins_per_slice_boosted=args.bins_per_slice_boosted
bins_per_slice_vbf=args.bins_per_slice_vbf

nslices=args.nslices
nslices_0jet=args.nslices_0jet
nslices_boosted=args.nslices_boosted
nslices_vbf=args.nslices_vbf

file_in=ROOT.TFile(args.file_in,"r")
file_out=ROOT.TFile(args.file_out,"recreate")

file_in.cd()

dirList = gDirectory.GetListOfKeys()
for k1 in dirList:
         h1 = k1.ReadObj()
         file_out.mkdir(h1.GetName())
	 if "0jet" in h1.GetName():
	    nslices=nslices_0jet
	    bins_per_slice=bins_per_slice_0jet
         if "boosted" in h1.GetName():
            nslices=nslices_boosted
            bins_per_slice=bins_per_slice_boosted
         if "vbf" in h1.GetName():
            nslices=nslices_vbf
            bins_per_slice=bins_per_slice_vbf

         h1.cd()
         dirList2 = gDirectory.GetListOfKeys()
         for k2 in dirList2:
	    h2 = k2.ReadObj()
	    h_shape=h2.Clone()
	    if "Down" in k2.GetName() or "Up" in k2.GetName():
	      shortname=k2.GetName().split("_")[0]
	      if shortname=="ggH" or shortname=="qqH" or shortname=="WH" or shortname=="ZH":
		shortname=k2.GetName().split("_")[0]+"_"+k2.GetName().split("_")[1]
              h_nominal=h2.Clone()
	      for k3 in dirList2:
		if k3.GetName()==shortname:
		   h_nominal=k3.ReadObj()
	      for i in range(0,nslices):
		 same_bins=0
		 for j in range(0,bins_per_slice):
		    if h_shape.GetBinContent(i*bins_per_slice+1+j)==h_nominal.GetBinContent(i*bins_per_slice+1+j):
			same_bins=same_bins+1
		 if (same_bins>bins_per_slice/2):
		     factor=0.0
		     if h_nominal.Integral(i*bins_per_slice+1,i*bins_per_slice+8)>0:
			factor=h_shape.Integral(i*bins_per_slice+1,i*bins_per_slice+8)/h_nominal.Integral(i*bins_per_slice+1,i*bins_per_slice+8)
		     for j in range(0,bins_per_slice):
			h_shape.SetBinContent(i*bins_per_slice+1+j,h_nominal.GetBinContent(i*bins_per_slice+1+j)*factor)
	    file_out.cd(h1.GetName())
            h_shape.SetName(k2.GetName())
            h_shape.Write()



