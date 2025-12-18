# A Dawn - Algorithmic MIDI Composition

## Overview

"A Dawn" is a multitrack MIDI composition (~3 minutes) generated using algorithmic techniques and neural network-assisted melody generation. The piece evokes the feeling of sunrise through soft, contemplative piano melodies supported by warm bass and atmospheric percussion.

## Structure

| Section     | Bars  | Time      | Description                          |
|-------------|-------|-----------|--------------------------------------|
| Intro       | 1-16  | 0:00-0:53 | Solo piano, delicate arpeggios       |
| Development | 17-32 | 0:53-1:46 | Bass enters, then light drums        |
| Climax      | 33-48 | 1:46-2:40 | Full ensemble, expressive piano      |
| Ending      | 49-56 | 2:40-3:07 | Fade out, piano solo                 |

## Algorithms & AI Techniques

### 1. Markov Chain Rhythm Generation (`rhythm_generator.py`)

Used for kick drum patterns. A 4-state transition matrix models the probability of transitioning between:
- State 0: Rest
- State 1: Soft hit
- State 2: Medium hit  
- State 3: Hard hit

```python
transition_matrix = [
    [0.3, 0.4, 0.2, 0.1],  # From rest
    [0.4, 0.2, 0.3, 0.1],  # From soft
    [0.3, 0.3, 0.2, 0.2],  # From medium
    [0.5, 0.2, 0.2, 0.1],  # From hard
]
```

### 2. Random Walk Algorithm

Used for hi-hat dynamics. A bounded random walk creates natural-feeling velocity variations:
- Step probabilities: -1 (30%), 0 (40%), +1 (30%)
- Bounded between velocity levels 0-3

### 3. Fractal Rhythm Subdivision

Used for snare patterns. Creates self-similar rhythmic structures through recursive subdivision:
1. Start with a single hit
2. Subdivide each hit into two events
3. Apply random variations to create organic patterns
4. Repeat for desired depth

### 4. LSTM Neural Network (`neural_melody.py`)

A recurrent neural network trained on synthetic musical data to suggest melodic progressions:

**Architecture:**
```
Input (15 timesteps × 3 features) →
LSTM (64 units) → Dropout (0.2) →
LSTM (32 units) → Dropout (0.2) →
Dense (16, ReLU) →
Dense (3, Sigmoid) → [note, velocity, duration]
```

**Training Data:**
- Synthetic sequences based on common chord progressions
- Melodic patterns in C major
- 200 sequences, 30 epochs

**Features per timestep:**
- Note (normalized 0-1)
- Velocity (normalized 0-1)
- Duration (normalized 0-1)

### 5. Algorithmic Bass Improvisation (`bass_generator.py`)

Bass lines use probabilistic note selection:
- 70% probability: root note
- 30% probability: variation (5th, octave up/down)

Rhythmic variation:
- 70%: quarter notes
- 30%: eighth, dotted quarter, or half notes

## Output Files

### A_Dawn_Multitrack.mid

Multitrack MIDI file containing:

| Track | Channel | Instrument          | Usage                    |
|-------|---------|---------------------|--------------------------|
| 0     | 0       | Acoustic Grand Piano| Full composition         |
| 1     | 1       | Electric Bass       | Enters at development    |
| 2     | 9       | Drums (GM)          | Enters mid-development   |

Each track can be:
- Used independently as a loop
- Combined with other tracks
- Imported into any DAW for further editing

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Generate composition
python compose_a_dawn.py
```

## Technical Notes

- **Tempo:** 72 BPM (contemplative, sunrise feel)
- **Key:** C major (peaceful, open)
- **Time Signature:** 4/4
- **Total Duration:** ~3 minutes (56 bars)

## Dependencies

- `midiutil`: MIDI file generation
- `numpy`: Numerical operations, random generation
- `tensorflow` (optional): Neural network for melody suggestions

If TensorFlow is not available, the system falls back to rule-based melody generation using the C major pentatonic scale.

## Future Enhancements

1. Train on larger MIDI datasets (e.g., Classical Piano MIDI)
2. Add more sophisticated harmonic analysis
3. Implement genetic algorithms for pattern evolution
4. Add support for different musical styles/moods
