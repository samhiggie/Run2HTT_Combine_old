import ROOT
import math

#clculate the background content at given point
#takes the point number, and the full histogram dictionary
def CalculateB(i,FullDictionary):
    content = FullDictionary['jetFakes'].GetBinContent(i)
    content += FullDictionary['ZT'].GetBinContent(i)
    content += FullDictionary['ZL'].GetBinContent(i)
    content += FullDictionary['TTL'].GetBinContent(i)
    content += FullDictionary['TTT'].GetBinContent(i)
    content += FullDictionary['VVL'].GetBinContent(i)
    content += FullDictionary['VVT'].GetBinContent(i)
    content += FullDictionary['STL'].GetBinContent(i)
    content += FullDictionary['STT'].GetBinContent(i)
    return content

#this function will blind our datapoints,
#i.e set them to -1 upon a given condition
#the current condition is just S/root(B) > 0.5
def BlindDataPoints(SignalDictionary,FullDictionary,DataDictionary):
    dataPointRangeLow = 1
    dataPointRangeHigh = DataDictionary['data_obs'].GetNbinsX() + 1
    for i in range(dataPointRangeLow,dataPointRangeHigh):
        backgroundContentAtPoint = CalculateB(i,FullDictionary)
        signalContentAtPoint = SignalDictionary['Higgs'].GetBinContent(i)        
        try:
            if signalContentAtPoint / math.sqrt(backgroundContentAtPoint) > 0.5:
                DataDictionary['data_obs'].SetBinContent(i,-1.0)
        except ZeroDivisionError:
            print("Skipping zero prediction bin...")
