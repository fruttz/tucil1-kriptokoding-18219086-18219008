from enigma.machine import EnigmaMachine

def initEnigma(wheelOrder, ringSettings, reflector, plugboardSettings):
    machine = EnigmaMachine.from_kunci_sheet(
        rotors = wheelOrder,
        ring_settings = ringSettings,
        reflector = reflector,
        plugboard_settings = plugboardSettings
    )
    return machine

def enigma(machine, initPosition, key, inputText):
    machine.set_display(initPosition)
    key = machine.process_text(key)
    machine.set_display(key)

    text = machine.process_text(inputText, replace_char='')
    return text

def rotorPosition(machine):
    return machine.get_display()