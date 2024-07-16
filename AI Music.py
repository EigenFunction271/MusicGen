# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:39:58 2024

@author: brendanb
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib
import music21
from music21 import converter, instrument, note, chord, stream

# Step 1: Define the architecture

class Generator(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Tanh()
        )

    def forward(self, x):
        return self.model(x)

class Discriminator(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_size, hidden_size),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_size, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

# Step 2: Prepare the dataset (placeholder function)
def prepare_dataset(num_samples=1000, sequence_length=50, num_features=88):
    # Create a dummy dataset
    dataset = np.random.rand(num_samples, sequence_length, num_features)
    
    # Convert to tensor
    dataset = torch.FloatTensor(dataset)
    
    return dataset

# Now, when you call this function:
dataset = prepare_dataset()



# Step 3 & 4: Implement the generator and discriminator
input_size = 100
hidden_size = 256
output_size = 88  # Number of MIDI notes

generator = Generator(input_size, hidden_size, output_size)
discriminator = Discriminator(output_size, hidden_size)

# Step 5: Train the GAN
def train_gan(generator, discriminator, dataset, num_epochs, batch_size):
    criterion = nn.BCELoss()
    g_optimizer = optim.Adam(generator.parameters(), lr=0.0002)
    d_optimizer = optim.Adam(discriminator.parameters(), lr=0.0002)

    for epoch in range(num_epochs):
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i+batch_size]
            
            # Train discriminator
            d_optimizer.zero_grad()
            
            real_data = batch
            real_labels = torch.ones(batch_size, 1)
            real_output = discriminator(real_data)
            d_loss_real = criterion(real_output, real_labels)

            noise = torch.randn(batch_size, input_size)
            fake_data = generator(noise)
            fake_labels = torch.zeros(batch_size, 1)
            fake_output = discriminator(fake_data.detach())
            d_loss_fake = criterion(fake_output, fake_labels)

            d_loss = d_loss_real + d_loss_fake
            d_loss.backward()
            d_optimizer.step()

            # Train generator
            g_optimizer.zero_grad()
            
            noise = torch.randn(batch_size, input_size)
            fake_data = generator(noise)
            fake_output = discriminator(fake_data)
            g_loss = criterion(fake_output, real_labels)

            g_loss.backward()
            g_optimizer.step()

        print(f"Epoch [{epoch+1}/{num_epochs}], d_loss: {d_loss.item():.4f}, g_loss: {g_loss.item():.4f}")

# Step 6: Generate new music
def generate_music(generator, num_samples=1):
    noise = torch.randn(num_samples, input_size)
    generated_data = generator(noise).detach().numpy()
    
    # Convert generated data to MIDI
    midi_stream = stream.Stream()

    for sample in generated_data:
        for step, note_prob in enumerate(sample):
            if note_prob > 0:
                new_note = note.Note(step)
                new_note.volume.velocity = int(note_prob * 127)
                midi_stream.append(new_note)

    midi_stream.write('midi', fp='generated_music.mid')

# Main execution
dataset = prepare_dataset()
train_gan(generator, discriminator, dataset, num_epochs=100, batch_size=32)
generate_music(generator)