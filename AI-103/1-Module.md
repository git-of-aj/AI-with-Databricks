> Agenda : platform basics → models → endpoints/SDKs → chat app development → optimization → responsible AI.

## what changed with chatgpt release in 2022?
- Classic ML: Learn a mapping input → prediction (f(x)=y).
- Generative AI: Learn patterns from data to understand language, reason about requests, and generate new content (text, code, images, etc.).
- **Traditional AI = Calculator**
1. Designed for specific operations
2. Extremely reliable within its scope.

**LLMs = Universal language interface**
1. Can perform many different knowledge and communication tasks.
2. More flexible, but also more prone to mistakes.

- Model: The entire machine.
- Parameters: The knobs inside the machine.

For a radio:

The radio = model
The tuning settings = parameters

Training is the process of adjusting all the knobs until the radio receives the signal clearly. For an LLM, there may be hundreds of billions of such "knobs."

```sh
Input
  ↓
Neuron
  ↓
Neuron
  ↓
Output
```
- each neuron has parameter that it learns over trainig
```sh
  Input --0.7--> Neuron
Input --1.3--> Neuron
Neuron --2.1--> Output
```
