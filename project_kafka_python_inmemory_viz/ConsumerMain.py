
import yaml
import configuration
from PythonProducer import producerControl
from PythonConsumer import consumerControl


# From the Config file , loading file path and name.
def loadConsuerParamters():
    with open('ConsumerConfig.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    # Print the values as a dictionary
    return (data)


# From the Config file , loading file path and name.
def loadProducerParamters():
    with open('ProducerConfig.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    # Print the values as a dictionary
    return (data)



def main():
    print('Scheduling pgm. Can be replaced with AirFlow')
    #pparam = loadProducerParamters()
    #producerControl.control().Controller(pparam)
    cparam = loadConsuerParamters()
    consumerControl.control().Controller(cparam)


    
    


if __name__ =='__main__':
    main()