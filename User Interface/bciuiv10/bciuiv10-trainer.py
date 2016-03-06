class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): 
        # I/O
        self.initOutputs() # Set output stimulation headers
        return

    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        #input[3] is target and input[2] is flash
        if(self.input[3]==self.input[2]):
            self.sendOutput(0,OVTK_StimulationId_Target)
        else:
            self.sendOutput(0,OVTK_StimulationId_NonTarget)
        return

    def uninitialize(self): # Called once when stopping the scenario
        self.closeOutputs()
        return

    def initOutputs(self):
        print(len(self.output))
        for index in range(len(self.output)):
            # OV protocol requires an output stim header; dates are 0
            self.output[index].append(OVStimulationHeader(0., 0.))
        return

    def sendOutput(self, index, stimLabel):
        # A stimulation set is a chunk which starts at current time and end time is the time step between two calls
        stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
        stimSet.append( OVStimulation(stimLabel, self.getCurrentTime(), 0.) )
        self.output[index].append(stimSet)
        return

    def closeOutputs(self):
        for index in range(len(self.output)):
            # OV protocol requires an output stim end
            end = self.getCurrentTime()
            self.output[index].append(OVStimulationEnd(end, end))
        return 

OVTK_StimulationId_Target = 33285
OVTK_StimulationId_NonTarget = 33286
OVTK_StimulationId_Label_00 = 33024
OVTK_StimulationId_Label_01 = 33025
OVTK_StimulationId_Label_07 = 33031
box = MyOVBox()
