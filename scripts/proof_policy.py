"""Trust policy shared by production audit and isolated fault controls."""
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool', 'Lean.trustCompiler'}
def classify(axioms):
    unexpected = set(axioms) - ALLOWED
    if unexpected:
        raise ValueError('unapproved axioms: ' + ', '.join(sorted(unexpected)))
    return 'native-assisted' if any(a.startswith('Lean.') for a in axioms) else 'kernel-checked'
