## OpenAI suggests either use temperature or top_p
- Temperature → reshapes the probability distribution.
- Top P → cuts off the long tail of unlikely tokens.
- Both → reshape and then filter the candidate distribution.
So I'd phrase it as:
> “You can combine them, but unless you have a specific reason to do so, use one. Using both introduces another interaction to tune, making experimentation, debugging, and reproducibility harder.”
>
> # LLM Sampling Parameters Reference

## Temperature
- **Definition:** Controls how random/creative the token selection is. Higher = more varied; lower = more focused/deterministic. OpenAI documents it as 0–2.
- **Problem it solves / Benefits it brings:** Lets you trade consistency for creativity.
- **Limited support?:** No. It is widely supported, including Hugging Face, Gemini, Anthropic, and OpenAI.
- **OpenAI Responses API?:** Yes, `temperature`.

## Top P
- **Definition:** Keeps only the smallest group of likely tokens whose combined probability reaches P. Example: `top_p=0.9` considers tokens making up roughly the most likely 90% of probability.
- **Problem it solves / Benefits it brings:** Prevents very unlikely tokens from being selected while still allowing variety.
- **Limited support?:** No. It is widely supported. Hugging Face and Gemini document it explicitly.
- **OpenAI Responses API?:** Yes, `top_p`. OpenAI recommends changing either temperature or top_p, rather than both.

## Top K
- **Definition:** Keeps only the K most likely tokens. For example, `top_k=50` means sampling can choose only among the 50 highest-probability next tokens.
- **Problem it solves / Benefits it brings:** Gives a simple hard limit on how many candidate tokens can be considered, reducing unlikely/weird outputs.
- **Limited support?:** Yes. It is model/provider dependent. Hugging Face supports it broadly; Gemini supports it for models that expose topK, but some Gemini models don't allow it.
- **OpenAI Responses API?:** No `top_k` parameter. OpenAI's Responses API exposes temperature and top_p, but not top_k.

---

## Easy Mental Model
- **Temperature:** “How adventurous should I be?”
- **Top P:** “Only consider tokens within this probability budget.”
- **Top K:** “Only consider the best K tokens.”

Sampling techniques control how language models choose the next word during text generation. The model assigns probabilities to possible words and sampling determines which one is picked. By adjusting these methods, you can balance creativity and accuracy in generated responses.

Temperature controls randomness in predictions
- Top-K limits choices to the most probable tokens
- Top-P selects tokens based on cumulative probability
Used to tune output diversity and coherence

- Low temperature: Safer, more predictable text
- High temperature: More creative and varied text
> **Important:** `top_p` and `top_k` are not competing versions of temperature—they filter the candidate pool, while temperature changes the probability distribution itself.
