from InstrumentResources import InstrumentResource
from InstrumentResources import InstrumentNames
import InstrumentExceptions


class SignalGenerator(InstrumentResource):
    def __init__(self, resource_name, sim_path=None, verbose=False):
        super().__init__(resource_name, sim_path)
        self._verbose = verbose
        self.inst_name = self.query("*IDN?").split(',')[1]
        if self.inst_name not in InstrumentNames.CosSignalGenerators:
            print("The specified VISA resource is not known and/or tested by COS, driver may not interface correctly.")
        self.clear_state()
        self._init_error = self.get_errors()
        if self._init_error is not None:
            print("The specified VISA resource has the following error(s):\n{}".format(self._init_error))
        self.__name__ = self.inst_name

    def reset(self):
        self.write("*RST")

    def clear_state(self):
        self.write("*CLS")

    def identify(self):
        self.query("*IDN?")

    def get_errors(self):
        errors = self.query("SYST:ERR?")
        if "No error" in errors:
            pass
        else:
            return errors

    def set_output_state(self, state):
        states = ["ON", "OFF"]
        if state in states:
            self.write("OUTP:STATE {}".format(state.upper()))
            self.query("*OPC?")
        elif isinstance(state, bool):
            if state is True:
                self.write("OUTP:STATE ON")
            else:
                self.write("OUTP:STATE OFF")
            self.query("*OPC?")
            errors = self.get_errors()
            if errors is not None:
                print("Device error: {}".format(errors))
        else:
            raise InstrumentExceptions.InvalidValue(state)
        if self.verbose is True:
            print("Set {} state to {}".format(self.inst_name, state))

    def get_output_state(self):
        state = self.query("OUTP:STATE?")
        if int(state) is 1:
            return True
        else:
            return False

    def set_center_frequency(self, frequency, unit="MHz"):
        if (isinstance(frequency, float) or isinstance(frequency, int)) and frequency >= 1:
            unit = unit.upper()
            switcher = {
                "GHZ": 1000000000,
                "MHZ": 1000000,
                "KHZ": 1000,
                "HZ": 1,
            }
            if unit in switcher:
                self.write("FREQ:CW {}".format(frequency * switcher.get(unit)))
                self.query("*OPC?")
                errors = self.get_errors()
                if errors is not None:
                    print("Device error: {}".format(errors))
            else:
                raise InstrumentExceptions.InvalidValue(unit)
        else:
            raise InstrumentExceptions.InvalidValue(frequency)
        if self.verbose is True:
            print("Set {} frequency to {} {}".format(self.inst_name, frequency, unit))

    def get_center_frequency(self, unit="MHz"):
        unit = unit.upper()
        switcher = {
            "GHZ": 1000000000,
            "MHZ": 1000000,
            "KHZ": 1000,
            "HZ": 1,
        }
        if unit in switcher:
            return float(self.query("FREQ:CW?")) / switcher.get(unit)
        else:
            raise InstrumentExceptions.InvalidValue(unit)

    def set_output_power(self, power):
        if isinstance(power, float) or isinstance(power, int):
            self.write("POW:LEV {}".format(power))
            self.query("*OPC?")
            errors = self.get_errors()
            if errors is not None:
                print("Device error: {}".format(errors))
        else:
            raise InstrumentExceptions.InvalidValue(power)
        if self.verbose is True:
            print("Set {} power to {} dBm".format(self.inst_name, power))

    def get_output_power(self):
        return float(self.query("POW:LEV?"))

    def set_mode(self, sweep_mode):
        modes = ["SWEEP", "CW"]
        if sweep_mode in modes:
            self.write("FREQ:MODE {}".format(sweep_mode.upper()))
            self.query("*OPC?")
        else:
            raise InstrumentExceptions.InvalidValue(sweep_mode)
        if self.verbose is True:
            print("Set {} mode to {}".format(self.inst_name, sweep_mode))

    def get_mode(self):
        return str(self.query("FREQ:MODE?"))

    def setup_sweep(self, start_frequency, stop_frequency, start_now=True, start_from_start=True, sweep_type="AUTO", sweep_mode="SWEEP", step_size=0.1, dwell_time_ms=5, unit="MHz"):
        unit = unit.upper()
        switcher = {
            "GHZ": 1000000000,
            "MHZ": 1000000,
            "KHZ": 1000,
            "HZ": 1,
        }

        if unit in switcher:
            if start_frequency is 0:
                raise InstrumentExceptions.InvalidValue(start_frequency)
            if start_from_start:
                self.set_mode("CW")
                self.set_mode("SWEEP")
                self.set_center_frequency(start_frequency, unit)
            self.write("SOUR:FREQ:START {}".format(start_frequency * switcher.get(unit)))
            self.write("SOUR:FREQ:STOP {}".format(stop_frequency * switcher.get(unit)))
            self.write("SOUR:SWE:FREQ:SPAC LIN")
            self.write("SOUR:SWE:FREQ:STEP:LIN {}".format(step_size * switcher.get(unit)))
            self.write("SOUR:SWE:FREQ:DWEL {} ms".format(dwell_time_ms))
            self.write("TRIG:FSW:SOUR AUTO")
            self.query("*OPC?")
        else:
            raise InstrumentExceptions.InvalidValue(unit)

        sweep_types = ["AUTO", "SINGLE", "STEP"]
        if sweep_type in sweep_types:
            self.write("SOUR:SWE:FREQ:MODE {}".format(sweep_type.upper()))
            self.query("*OPC?")
        else:
            raise InstrumentExceptions.InvalidValue(sweep_type)

        if sweep_mode is "SWEEP":
            self.set_mode("SWEEP")
            self.query("*OPC?")
        else:
            raise InstrumentExceptions.InvalidValue(sweep_mode)

        if self.verbose is True:
            print("Set {}'s start frequency to {} and stop frequency to {}".format(self.inst_name, start_frequency, stop_frequency))

        if start_now:
            self.start_sweep()
            if self.verbose is True:
                print("Running sweep...")

        errors = self.get_errors()
        if errors is not None:
            print("Device error: {}".format(errors))

    def start_sweep(self):
        self.set_mode("SWEEP")
        self.write("SOUR:SWE:FREQ:EXEC")
        self.query("*OPC?")
        errors = self.get_errors()
        if errors is not None:
            print("Device error: {}".format(errors))
        if self.verbose is True:
            print("Running sweep...")

    def stop_sweep(self):
        self.set_mode("CW")
        self.query("*OPC?")
        errors = self.get_errors()
        if errors is not None:
            print("Device error: {}".format(errors))
        if self.verbose is True:
            print("Sweep stopped.")