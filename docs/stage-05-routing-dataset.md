# Stage 5 — Routing Dataset

## Kya banaya

`datasets/routing_dataset.json` — **109 labeled examples**, har ek
mein ek `prompt` aur uska sahi `complexity` label (`easy` / `medium`
/ `hard`).

Distribution:
- Easy: 40
- Medium: 36
- Hard: 33

(Roughly balanced — koi ek category dominate nahi karti)

## Format

```json
{"prompt": "Translate 'Good morning' into Hindi.", "complexity": "easy"}
```

## Dataset kaise design kiya

**Categories cover ki gayi:**
- Easy — translation, facts, unit conversion, short rewrites, simple math
- Medium — summarization, explanations, code writing, essay/email
  drafting, comparisons
- Hard — multi-file analysis, mathematical proofs, security review,
  architecture design, legal/financial deep-dives

**Sabse important design choice — "twin pairs":**
Dataset ke end mein jaanbujhke same topic ke easy/medium/hard
versions rakhe:

```json
{"prompt": "Explain how neural networks work.", "complexity": "medium"}
{"prompt": "Explain how neural networks work, including backpropagation math and gradient descent optimization in detail.", "complexity": "hard"}
```

**Kyun ye important hai:** Agar dataset mein ye pairs na hote, to
classifier sirf **topic keywords** pe reliant ho jata (jaise "neural
network" dekhte hi "hard" bol deta, chahe sawaal simple ho). Twin
pairs ki wajah se classifier ye seekhta hai ki **depth aur scope**
complexity decide karta hai, na ki sirf topic.

## Kyun ~100 examples kaafi hain

Hum koi bada LLM train nahi kar rahe — sirf ek chhota classifier
(Logistic Regression / Random Forest jaisa, Stage 6 mein banega) jo
simple features (length, keywords, etc.) pe based hoga. Aise chhote
models ke liye 100-300 quality examples generally kaafi hote hain.
Zyada important hai **diversity aur balance**, na ki raw quantity.

## Test kaise kiya

```python
import json
data = json.load(open('routing_dataset.json'))
print(len(data))  # 109
```

JSON validity aur class balance dono verify kiye.

## Status
✅ Complete — future mein Stage 6 se pehle chaho to apne domain-specific
examples isi format mein add kar sakte ho.
