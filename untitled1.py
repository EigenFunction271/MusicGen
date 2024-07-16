# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:22:15 2024

@author: brendanb
"""

import os
from music21 import converter, instrument, note, chord
import numpy as np
import torch

def prepare_dataset(data_path, sequence_length=50):
    notes = []
    for file in os.listdir(data_path):
        if file.endswith(".mid"):
            midi = converter.parse(os.path.join(data_path, file))
            notes_to_parse = None
            try:
                s2 = instrument.partitionByInstrument(midi)
                notes_to_parse = s2.parts[0].recurse() 
            except:
                notes_to_parse = midi.flat.notes
            
            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))

    # Get all pitch names
    pitch_names = sorted(set(item for item in notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitch_names))

    network_input = []
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])

    n_patterns = len(network_input)
    n_vocab = len(pitch_names)

    # Reshape the input into a format compatible with LSTM layers
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))

    # Normalize input
    network_input = network_input / float(n_vocab)

    return torch.FloatTensor(network_input)

# Usage:
dataset = prepare_dataset('path/to/your/midi/files')