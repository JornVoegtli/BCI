class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): 
        # I/O
        self.initOutputs() # Set output stimulation headers

        # Input variables
        self.target = [0,0]
        return

    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        # Read target 
        for chunkIndex in range( len(self.input[1]) ):
		chunk = self.input[1].pop()
		if(type(chunk) == OVStimulationSet):
			for stimIdx in range(len(chunk)):
				stim=chunk.pop();
				if (33025 <= stim.identifier and stim.identifier <= 33030): # Row
					self.target[0] = stim.identifier
				elif (33031 <= stim.identifier and stim.identifier <= 33036): # Column
					self.target[1] = stim.identifier

        # Read flashes
	for chunkIndex in range( len(self.input[0]) ):
		chunk = self.input[0].pop()
		if(type(chunk) == OVStimulationSet):
			for stimIdx in range(len(chunk)):
				stim=chunk.pop();
				#print 'Current target:', self.target[0], self.target[1]
				#print 'Flashing row/col:', stim.identifier
				if (stim.identifier==self.target[0] or stim.identifier==self.target[1]):
					self.sendOutput(0,OVTK_StimulationId_Target)
					#print 'MATCH'
				else:
					self.sendOutput(0,OVTK_StimulationId_NonTarget)
        return

    def uninitialize(self): # Called once when stopping the scenario
        self.closeOutputs()
        return

    def initOutputs(self):
        #print(len(self.output))
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
box = MyOVBox()
