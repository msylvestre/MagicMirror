#!/usr/bin/python
class SignalNoiseCleaner():

    smoothingBuffer = 3
    smoothDistance  = -1
    cleanDistance   = -1
    peakCounter     = 0
    peakSize        = 0.25
    maxPeak         = 3
    arr             = []


    def avgArray(self, arr):
        
        totalArr = 0
        avgArr   = 0
        
        for i in range(len(arr)):
            totalArr += arr[i]

        avgArr = totalArr / len(arr)

        return avgArr

                
    def shiftArray(self, arr):

        shiftedArr = []

        # Pop out the first value, move the other to the beginning of the array
        # to make space for a new value
        for i in range(len(arr) - 1):
            shiftedArr.append(arr[i + 1])

        return shiftedArr


    def cleanNoise(self, newDistance):

        maxDistanceAllowed = SignalNoiseCleaner.cleanDistance * (1 + SignalNoiseCleaner.peakSize)
        minDistanceAllowed = SignalNoiseCleaner.cleanDistance * (1 - SignalNoiseCleaner.peakSize)
        
        # If it's the first read
        if SignalNoiseCleaner.cleanDistance == -1:
            SignalNoiseCleaner.cleanDistance = newDistance

        # If newDistance is bigger/smaller than 25% of the last read, we have a peak !
        elif newDistance > maxDistanceAllow or newDistance < minDistanceAllowed:
            
            if SignalNoiseCleaner.peakCounter < SignalNoiseCleaner.maxPeak:
                # Increase the peak counter
                SignalNoiseCleaner.peakCounter += 1
                print "peak ! -> ", SignalNoiseCleaner.peakCounter

            else:
                # if we get 3 peak in a row, it's not a peak anymore
                SignalNoiseCleaner.cleanDistance = newDistance
                SignalNoiseCleaner.peakCounter = 0
                print "3 peak isn't a peak, it's the new value !"

        else:
            # The reading is valid (+/- 25% of the last reading), so let's reset the peak counter 
            SignalNoiseCleaner.cleanDistance = newDistance
            SignalNoiseCleaner.peakCounter = 0


        return SignalNoiseCleaner.cleanDistance


    def smoothNoise(self, newDistance):

        if len(SignalNoiseCleaner.arr) < SignalNoiseCleaner.smoothingBuffer - 1:
            SignalNoiseCleaner.arr.append(newDistance)
            SignalNoiseCleaner.smoothDistance = -1
            
        else:

            if SignalNoiseCleaner.smoothDistance == -1:
                SignalNoiseCleaner.arr.append(newDistance)
                SignalNoiseCleaner.smoothDistance = self.avgArray(SignalNoiseCleaner.arr)

            else:
                SignalNoiseCleaner.arr = self.shiftArray(SignalNoiseCleaner.arr)
                SignalNoiseCleaner.arr.append(newDistance)
                SignalNoiseCleaner.smoothDistance = self.avgArray(SignalNoiseCleaner.arr)

        return SignalNoiseCleaner.smoothDistance

