import unittest

import SignalIntegrity as si
from numpy import linalg
from numpy import array
from numpy import matrix

class TestConversions(unittest.TestCase):
    def testABCD2SDefault(self):
        R=100
        ABCD=[[1,-R],[0,1]]
        difference = linalg.norm(si.dev.SeriesZ(R)-array(si.cvt.ABCD2S(ABCD)))
        self.assertTrue(difference<1e-10,'100 Ohm ABCD not equal S with default Z0, K')
    def testABCD2S50(self):
        R=20
        ABCD=[[1,-R],[0,1]]
        Z0=50.0
        difference = linalg.norm(si.dev.SeriesZ(R,Z0)-array(si.cvt.ABCD2S(ABCD,Z0)))
        self.assertTrue(difference<1e-10,'20 Ohm ABCD not equal S with  Z0=50 Ohm, default K')
    def testABCD2S150(self):
        R=85
        ABCD=[[1,-R],[0,1]]
        Z0=100.0
        difference = linalg.norm(si.dev.SeriesZ(R,Z0)-array(si.cvt.ABCD2S(ABCD,Z0)))
        self.assertTrue(difference<1e-10,'85 Ohm ABCD not equal S with  Z0=150 Ohm, default K')
    def testABCD2SZ0ListConstant(self):
        R=29
        ABCD=[[1,-R],[0,1]]
        Z0=[45.,45.]
        difference = linalg.norm(si.dev.SeriesZ(R,Z0)-array(si.cvt.ABCD2S(ABCD,Z0)))
        self.assertTrue(difference<1e-10,'29 Ohm ABCD not equal S with  Z0=list same, default K')
    def testABCD2SZ0ListDifferent(self):
        R=134
        ABCD=[[1,-R],[0,1]]
        Z0=[25.,95.]
        difference = linalg.norm(si.dev.SeriesZ(R,Z0)-array(si.cvt.ABCD2S(ABCD,Z0)))
        self.assertTrue(difference<1e-10,'134 Ohm ABCD not equal S with  Z0=list different, default K')
    def testABCD2SComplexZ(self):
        R=23+1j*134
        ABCD=[[1,-R],[0,1]]
        Z0=[25.,95.]
        difference = linalg.norm(si.dev.SeriesZ(R,Z0)-array(si.cvt.ABCD2S(ABCD,Z0)))
        self.assertTrue(difference<1e-10,'Complex Series Z ABCD not equal S with  Z0=list different, default K')
    def testABCD2SComplexZComplexZ0List(self):
        R=23+1j*134
        ABCD=[[1,-R],[0,1]]
        Z0=[25+1j*34,95.-1j*91]
        difference = linalg.norm(si.dev.SeriesZ(R,Z0)-array(si.cvt.ABCD2S(ABCD,Z0)))
        self.assertTrue(difference<0.0001,'Complex Series Z ABCD not equal S with  Z0=list different, default K')
    def testABCD2SComplexZComplexZ0array(self):
        R=23+1j*134
        ABCD=[[1,-R],[0,1]]
        Z0=array([[25+1j*34,0.0],[0.0,95.-1j*91]])
        difference = linalg.norm(si.dev.SeriesZ(R,Z0)-array(si.cvt.ABCD2S(ABCD,Z0)))
        self.assertTrue(difference<1e-10,'Complex Series Z ABCD not equal S with  Z0=list different, default K')
    def testABCD2SComplexZComplexZ0matrix(self):
        R=23+1j*134
        ABCD=[[1,-R],[0,1]]
        Z0=matrix([[25+1j*34,0.0],[0.0,95.-1j*91]])
        difference = linalg.norm(si.dev.SeriesZ(R,Z0)-array(si.cvt.ABCD2S(ABCD,Z0)))
        self.assertTrue(difference<1e-10,'Complex Series Z ABCD not equal S with  Z0=list different, default K')
    def testShuntZ(self):
        """
        This test tests the s-parameters of the shunt z by building a circuit using the system descriptions
        and computing the s-parameters that way and comparing to those computed through the normal calculation
        """
        Z=23+43*1j
        normalResult = array(si.dev.ShuntZ(Z))
        D=si.sd.SystemDescription()
        D.AddDevice('D1',2,si.dev.SeriesZ(Z))
        D.AddDevice('G1',1,si.dev.Ground())
        D.ConnectDevicePort('D1',2,'G1',1)
        D.AddPort('D1',1,1)
        D.AddPort('D1',1,2)
        theRealResult=array(si.sd.SystemSParametersNumeric(D).SParameters())
        difference = linalg.norm(normalResult-theRealResult)
        self.assertTrue(difference<1e-10,'Shunt Z incorrect')
    def testZ2SComplexZComplexZ0matrix(self):
        R=23+1j*134
        Z=[[R,R],[R,R]]
        Z0=matrix([[25+1j*34,0.0],[0.0,95.-1j*91]])
        difference = linalg.norm(si.dev.ShuntZ(R,Z0)-array(si.cvt.Z2S(Z,Z0)))
        self.assertTrue(difference<1e-10,'Complex Series Z Z not equal S with  Z0=list different, default K')
    def testZ2SComplexZComplexZ0List(self):
        R=23+1j*134
        Z=[[R,R],[R,R]]
        Z0=[25+1j*34,95.-1j*91]
        difference = linalg.norm(si.dev.ShuntZ(R,Z0)-array(si.cvt.Z2S(Z,Z0)))
        self.assertTrue(difference<0.0001,'Complex Series Z ABCD not equal S with  Z0=list different, default K')
    def testSw2SpDefault(self):
        Sw=[[1,2],[3,4]]
        Sp=si.cvt.Sw2Sp(Sw)
        difference = linalg.norm(array(Sw)-array(Sp))
        self.assertTrue(difference<0.0001,'Sw2Sp incorrect with default')
    def testSp2SwDefault(self):
        Sp=[[1,2],[3,4]]
        Sw=si.cvt.Sp2Sw(Sp)
        difference = linalg.norm(array(Sw)-array(Sp))
        self.assertTrue(difference<0.0001,'Sp2Sw incorrect with default')
    def testSw2SpComplexSameZ0wZ0pDefaultKpKw(self):
        Sw=[[0.3+0.06*1j,0.811+0.268*1j],[0.325-0.693*1j,-0.967+0.278*1j]]
        Sp=[[0.308+0.108*1j,0.672-0.106*1j],[-0.022-0.61*1j,0.34+1.078*1j]]
        Z0=[0.567+0.04*1j,0.752+0.912*1j]
        Spcalc=si.cvt.Sw2Sp(Sw,Z0)
        difference = linalg.norm(array(Spcalc)-array(Sp))
        self.assertTrue(difference<0.005,'Sw2Sp incorrect with same Z0 default Kp Kw')
    def testSp2SwComplexSameZ0wZ0pDefaultKpKw(self):
        Sw=[[0.3+0.06*1j,0.811+0.268*1j],[0.325-0.693*1j,-0.967+0.278*1j]]
        Sp=[[0.308+0.108*1j,0.672-0.106*1j],[-0.022-0.61*1j,0.34+1.078*1j]]
        Z0=[0.567+0.04*1j,0.752+0.912*1j]
        Swcalc=si.cvt.Sp2Sw(Sp,Z0)
        difference = linalg.norm(array(Swcalc)-array(Sw))
        self.assertTrue(difference<0.005,'Sp2Sw incorrect with same Z0 default Kp Kw')
    def testSw2SpComplexDifferentZ0wZ0pDefaultKpKw(self):
        Sw=[[-0.13-0.459*1j,0.935+0.614*1j],[0.646-0.767*1j,-0.888+0.555*1j]]
        Sp=[[0.308+0.108*1j,0.672-0.106*1j],[-0.022-0.61*1j,0.34+1.078*1j]]
        Z0w=[0.724+0.559*1j,0.994+0.223*1j]
        Z0p=[0.567+0.04*1j,0.752+0.912*1j]
        Spcalc=si.cvt.Sw2Sp(Sw,Z0w,Z0p)
        difference = linalg.norm(array(Spcalc)-array(Sp))
        self.assertTrue(difference<0.005,'Sw2Sp incorrect with different Z0 default Kp Kw')
    def testSp2SwComplexDifferentZ0wZ0pDefaultKpKw(self):
        Sw=[[-0.13-0.459*1j,0.935+0.614*1j],[0.646-0.767*1j,-0.888+0.555*1j]]
        Sp=[[0.308+0.108*1j,0.672-0.106*1j],[-0.022-0.61*1j,0.34+1.078*1j]]
        Z0w=[0.724+0.559*1j,0.994+0.223*1j]
        Z0p=[0.567+0.04*1j,0.752+0.912*1j]
        Swcalc=si.cvt.Sp2Sw(Sp,Z0w,Z0p)
        difference = linalg.norm(array(Swcalc)-array(Sw))
        self.assertTrue(difference<0.005,'Sp2Sw incorrect with different Z0 default Kp Kw')
    def testSw2SpComplexDifferentZ0wZ0pKwDefaultKp(self):
        Sw=[[-0.13-0.459*1j,0.039-0.487*1j],[0.827+2.14*1j,-0.888+0.555*1j]]
        Sp=[[0.308+0.108*1j,0.672-0.106*1j],[-0.022-0.61*1j,0.34+1.078*1j]]
        Z0w=[0.724+0.559*1j,0.994+0.223*1j]
        Z0p=[0.567+0.04*1j,0.752+0.912*1j]
        Kw=[0.354-0.982*1j,-0.448+0.176*1j]
        Spcalc=si.cvt.Sw2Sp(Sw,Z0w,Z0p,Kw)
        difference = linalg.norm(array(Spcalc)-array(Sp))
        self.assertTrue(difference<0.006,'Sw2Sp incorrect with different Z0, Kw specified, default Kp')
    def testSp2SwComplexDifferentZ0wZ0pKwDefaultKpKw(self):
        Sw=[[-0.13-0.459*1j,0.039-0.487*1j],[0.827+2.14*1j,-0.888+0.555*1j]]
        Sp=[[0.308+0.108*1j,0.672-0.106*1j],[-0.022-0.61*1j,0.34+1.078*1j]]
        Z0w=[0.724+0.559*1j,0.994+0.223*1j]
        Z0p=[0.567+0.04*1j,0.752+0.912*1j]
        Kw=[0.354-0.982*1j,-0.448+0.176*1j]
        Swcalc=si.cvt.Sp2Sw(Sp,Z0w,Z0p,Kw)
        difference = linalg.norm(array(Swcalc)-array(Sw))
        self.assertTrue(difference<0.006,'Sp2Sw incorrect with different Z0, Kw specified, default Kp')
    def testSw2SpComplexDifferentZ0wZ0pKwKp(self):
        Sw=[[-0.13-0.459*1j,0.039-0.487*1j],[0.827+2.14*1j,-0.888+0.555*1j]]
        Sp=[[0.308+0.108*1j,0.074-0.012*1j],[-0.205-5.548*1j,0.34+1.078*1j]]
        Z0w=[0.724+0.559*1j,0.994+0.223*1j]
        Z0p=[0.567+0.04*1j,0.752+0.912*1j]
        Kw=[0.354-0.982*1j,-0.448+0.176*1j]
        Kp=[0.451,0.057]
        Spcalc=si.cvt.Sw2Sp(Sw,Z0w,Z0p,Kw,Kp)
        difference = linalg.norm(array(Spcalc)-array(Sp))
        self.assertTrue(difference<0.008,'Sw2Sp incorrect with different Z0, Kw, Kp specified')
    def testSp2SwComplexDifferentZ0wZ0pKwKpKw(self):
        Sw=[[-0.13-0.459*1j,0.039-0.487*1j],[0.827+2.14*1j,-0.888+0.555*1j]]
        Sp=[[0.308+0.108*1j,0.074-0.012*1j],[-0.205-5.548*1j,0.34+1.078*1j]]
        Z0w=[0.724+0.559*1j,0.994+0.223*1j]
        Z0p=[0.567+0.04*1j,0.752+0.912*1j]
        Kw=[0.354-0.982*1j,-0.448+0.176*1j]
        Kp=[0.451,0.057]
        Swcalc=si.cvt.Sp2Sw(Sp,Z0w,Z0p,Kw,Kp)
        difference = linalg.norm(array(Swcalc)-array(Sw))
        self.assertTrue(difference<0.008,'Sp2Sw incorrect with different Z0, Kw, Kp specified')
    def testSw2SpComplexSingleZ0SameZ0wZ0pDefaultKpKw(self):
        Sw=[[-0.296-0.173*1j,1.251+0.89*1j],[0.926-1.018*1j,-1.401+0.604*1j]]
        Sp=[[-0.302-0.082*1j,1.307+0.799*1j],[0.851-1.078*1j,-1.348+0.768*1j]]
        Z0=0.567+0.04*1j
        Spcalc=si.cvt.Sw2Sp(Sw,Z0)
        difference = linalg.norm(array(Spcalc)-array(Sp))
        self.assertTrue(difference<0.005,'Sw2Sp incorrect with same single Z0 default Kp Kw')
    def testSp2SwComplexSingleZ0SameZ0wZ0pDefaultKpKw(self):
        Sw=[[-0.296-0.173*1j,1.251+0.89*1j],[0.926-1.018*1j,-1.401+0.604*1j]]
        Sp=[[-0.302-0.082*1j,1.307+0.799*1j],[0.851-1.078*1j,-1.348+0.768*1j]]
        Z0=0.567+0.04*1j
        Swcalc=si.cvt.Sp2Sw(Sp,Z0)
        difference = linalg.norm(array(Swcalc)-array(Sw))
        self.assertTrue(difference<0.005,'Sp2Sw incorrect with same single Z0 default Kp Kw')
    def testSw2SpComplexSingleDifferentZ0wZ0pDefaultKpKw(self):
        Sw=[[0.692-0.523*1j,1.011+0.399*1j],[0.464-0.857*1j,0.064+0.198*1j]]
        Sp=[[-0.302-0.082*1j,1.307+0.799*1j],[0.851-1.078*1j,-1.348+0.768*1j]]
        Z0p=0.567+0.04*1j
        Z0w=-0.468+0.68*1j
        Spcalc=si.cvt.Sw2Sp(Sw,Z0w,Z0p)
        difference = linalg.norm(array(Spcalc)-array(Sp))
        self.assertTrue(difference<0.005,'Sw2Sp incorrect with different single Z0w, Z0p default Kp Kw')
    def testSp2SwComplexSingleDifferentZ0wZ0pDefaultKpKw(self):
        Sw=[[0.692-0.523*1j,1.011+0.399*1j],[0.464-0.857*1j,0.064+0.198*1j]]
        Sp=[[-0.302-0.082*1j,1.307+0.799*1j],[0.851-1.078*1j,-1.348+0.768*1j]]
        Z0p=0.567+0.04*1j
        Z0w=-0.468+0.68*1j
        Swcalc=si.cvt.Sp2Sw(Sp,Z0w,Z0p)
        difference = linalg.norm(array(Swcalc)-array(Sw))
        self.assertTrue(difference<0.005,'Sp2Sw incorrect with different single Z0w, Z0p default Kp Kw')
    def testSw2SpComplexSingleDifferentZ0wZ0pKwDefaultKp(self):
        Sw=[[0.692-0.523*1j,1.011+0.399*1j],[0.464-0.857*1j,0.064+0.198*1j]]
        Sp=[[-0.302-0.082*1j,1.307+0.799*1j],[0.851-1.078*1j,-1.348+0.768*1j]]
        Z0p=0.567+0.04*1j
        Z0w=-0.468+0.68*1j
        Kw=0.423+0.804*1j
        Spcalc=si.cvt.Sw2Sp(Sw,Z0w,Z0p,Kw)
        difference = linalg.norm(array(Spcalc)-array(Sp))
        self.assertTrue(difference<0.005,'Sw2Sp incorrect with different single Z0w, Z0p, Kw default Kp')
    def testSp2SwComplexSingleDifferentZ0wZ0pKwDefaultKp(self):
        Sw=[[0.692-0.523*1j,1.011+0.399*1j],[0.464-0.857*1j,0.064+0.198*1j]]
        Sp=[[-0.302-0.082*1j,1.307+0.799*1j],[0.851-1.078*1j,-1.348+0.768*1j]]
        Z0p=0.567+0.04*1j
        Z0w=-0.468+0.68*1j
        Kw=0.423+0.804*1j
        Swcalc=si.cvt.Sp2Sw(Sp,Z0w,Z0p,Kw)
        difference = linalg.norm(array(Swcalc)-array(Sw))
        self.assertTrue(difference<0.005,'Sp2Sw incorrect with different single Z0w, Z0p, Kw default Kp ')
    def testSw2SpComplexSingleDifferentZ0wZ0pKwKp(self):
        Sw=[[0.692-0.523*1j,1.011+0.399*1j],[0.464-0.857*1j,0.064+0.198*1j]]
        Sp=[[-0.302-0.082*1j,1.307+0.799*1j],[0.851-1.078*1j,-1.348+0.768*1j]]
        Z0p=0.567+0.04*1j
        Z0w=-0.468+0.68*1j
        Kw=0.423+0.804*1j
        Kp=0.753
        Spcalc=si.cvt.Sw2Sp(Sw,Z0w,Z0p,Kw,Kp)
        difference = linalg.norm(array(Spcalc)-array(Sp))
        self.assertTrue(difference<0.005,'Sw2Sp incorrect with different single Z0w, Z0p, Kw default Kp')
    def testSp2SwComplexSingleDifferentZ0wZ0pKwKp(self):
        Sw=[[0.692-0.523*1j,1.011+0.399*1j],[0.464-0.857*1j,0.064+0.198*1j]]
        Sp=[[-0.302-0.082*1j,1.307+0.799*1j],[0.851-1.078*1j,-1.348+0.768*1j]]
        Z0p=0.567+0.04*1j
        Z0w=-0.468+0.68*1j
        Kw=0.423+0.804*1j
        Kp=0.753
        Swcalc=si.cvt.Sp2Sw(Sp,Z0w,Z0p,Kw,Kp)
        difference = linalg.norm(array(Swcalc)-array(Sw))
        self.assertTrue(difference<0.005,'Sp2Sw incorrect with different single Z0w, Z0p, Kw default Kp ')



if __name__ == '__main__':
    unittest.main()

