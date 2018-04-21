import pyvisa
import InstrumentExceptions


class InstrumentResource:
    def __init__(self, resource_name, sim_path=None):
        self.__author__ = 'Jared Knott'
        if sim_path is not None:
            self.device = pyvisa.ResourceManager(sim_path + '@sim').open_resource(resource_name)
        else:
            self.device = pyvisa.ResourceManager().open_resource(resource_name)

    def write(self, message):
        try:
            self.device.write(message)
        except InstrumentExceptions.InstrumentNotResponding:
            print("Could not write to {}, reason unknown".format("device"))

    def query(self, message):
        try:
            return str(self.device.query(message))
        except InstrumentExceptions.InstrumentNotResponding:
            print("Could not query {}, instrument did not respond to {}".\
                  format("device", "command"))
            # someday come back and figure out how to get the class name and method

    def read(self):
        try:
            return str(self.device.read())
        except InstrumentExceptions.InstrumentNotResponding:
            print("Could not read from {}, instrument did not respond to {}". \
                  format("device", "command"))
            # someday come back and figure out how to get the class name and method

    def close(self):
        try:
            self.device.close()
            print("Connection to {} has been closed".format("device"))
        except InstrumentExceptions.InstrumentNotResponding:
            print("{} failed to close".format("Device"))


class InstrumentNames:
    CosSignalGenerators = ['SMF100A', 'SMT03', 'SMIQ06L', 'SMA100A']
    CosSpectrumAnalyzers = ['FSV', 'FSU', 'FSUP', 'FSW']
    CosMultiMeters = ['34401']
    CosOscilloscopes = ['3054']
    CosPowerSupplies = ['3631']
    CosSourceMeters = ['2602']
    CosWaveformGenerators = ['33250']
