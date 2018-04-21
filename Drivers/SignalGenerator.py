from InstrumentResources import InstrumentResource
from InstrumentResources import InstrumentNames
import InstrumentExceptions


class SignalGenerator(InstrumentResource):
    def __init__(self, resource_name, sim_path=None):
        super().__init__(resource_name, sim_path)
        inst_name = str(self.query("*IDN?")).split(',')[1]
        if inst_name not in InstrumentNames.CosSignalGenerators:
            print("The specified VISA resource is not known and/or tested by COS, driver may not interface correctly.")
        self.__name__ = inst_name

    def reset(self):
        self.write("*RST")

    def set_output_state(self, state):
        states = ["ON", "OFF"]
        if state in states:
            self.write("OUTP:STATE {}".format(state.upper()))
        else:
            raise InstrumentExceptions.InvalidValue(state)

    def get_out_state(self):
        return str(self.query("OUTP:STATE?"))

    def set_center_frequency(self, frequency, unit="MHz"):
        if isinstance(frequency, float) or isinstance(frequency, int):
            switcher = {
                "GHz": 1000000000,
                "MHz": 1000000,
                "kHz": 1000,
                "Hz": 1,
            }
            if unit in switcher:
                self.write("FREQ:CW {}".format(frequency * switcher.get(unit)))
            else:
                raise InstrumentExceptions.InvalidValue(unit)
        else:
            raise InstrumentExceptions.InvalidValue(frequency)

    def get_center_frequency(self, unit="MHz"):
        switcher = {
            "GHz": 1000000000,
            "MHz": 1000000,
            "kHz": 1000,
            "Hz": 1,
        }
        if unit in switcher:
            return float(self.query("FREQ:CW?")) / switcher.get(unit)
        else:
            raise InstrumentExceptions.InvalidValue(unit)

    def set_output_power(self, power):
        if isinstance(power, float) or isinstance(power, int):
            self.write("POW:LEV {}".format(power))
        else:
            raise InstrumentExceptions.InvalidValue(power)

    def get_output_power(self):
        return float(self.query("POW:LEV?"))

    def set_mode(self, sweep_mode):
        modes = ["SWEEP", "CW"]
        if sweep_mode in modes:
            self.write("FREQ:MODE {}".format(sweep_mode.upper()))
        else:
            raise InstrumentExceptions.InvalidValue(sweep_mode)

    def get_mode(self):
        return str(self.query("FREQ:MODE?"))

    def set_sweep_params(self, start_frequency, stop_frequency, sweep_type="AUTO", step_size=0.1, dwell_time_ms=5, unit="MHz"):
        types = ["AUTO", "SINGLE", "STEP"]
        if type in types:
            self.write("SOUR:SWE:FREQ:MODE {}".format(sweep_type.upper()))
        else:
            raise InstrumentExceptions.InvalidValue(type)

        switcher = {
            "GHz": 1000000000,
            "MHz": 1000000,
            "kHz": 1000,
            "Hz": 1,
        }

        if unit in switcher:
            self.write("SOUR:FREQ:START {}".format(start_frequency * switcher.get(unit)))
            self.write("SOUR:FREQ:STOP {}".format(stop_frequency * switcher.get(unit)))
            self.write("SOUR:SWE:FREQ:SPAC LIN")
            self.write("SOUR:SWE:FREQ:STEP:LIN {}".format(step_size * switcher.get(unit)))
            self.write("SOUR:SWE:FREQ:DWEL {} ms".format(dwell_time_ms))
        else:
            raise InstrumentExceptions.InvalidValue(unit)

    def run_sweep(self):
        self.write("SOUR:SWE:FREQ:EXEC")

    def stop_sweep(self):
        self.set_mode("CW")

    def test(self):
        pass