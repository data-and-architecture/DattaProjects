
import os
import logging
from PythonProducer import Rproducer
logging.basicConfig(format="%(levelname)s:%(name)s:%(message)s")

class control:
    def __init__(self):
         param : dict = None
         fileFullPath : str = None
         kafkaParameter :dict =None


    # This method will get the file path and name from paramter file and prepare full path. 
    def getFilePath(self):
        pathName =  self.param.get('CPATH_NAME')
        fileName =  self.param.get('CFILE_NAME')
        self.fileFullPath =  os.path.join(pathName,fileName)
        
    #Getting kafka parameter    
    def getKafkaParameters(self):
        kafkaParameter = self.param
        keysToRemove = ('CPATH_NAME', 'CFILE_NAME')
        for key in keysToRemove:
            del kafkaParameter[key]
        self.kafkaParameter = kafkaParameter
        #logging.warning(kafkaParameter)


    def Controller(self,param:dict):
        self.param = param
        self.getFilePath()
        self.getKafkaParameters()
        Rproducer.produce().RProducer(self.fileFullPath,self.kafkaParameter)





def main():
    print ('Good')
   # param = loadParamters()



if __name__ =='__main__':
    main()