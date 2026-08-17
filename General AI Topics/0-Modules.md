## ROI on AI
[IBM Docs](https://www.ibm.com/think/insights/ai-roi)

> Current AI use in Software Dev is giving suboptimal results in terms of velocity and software quality 
 - AI in software development through two primary approaches:
 - **AI-assisted development**: where AI enhances specific tasks like documentation, code completion, and testing
 - **AI-autonomous development**: where AI is expected to generate entire applications without human intervention based on user requirements.

I'd be happy to walk you through the fundamental concepts of AI, structured exactly as they are in the video.

Here is a breakdown of the key areas, moving from the big picture of Artificial Intelligence down to the specific mechanics of neural networks and the differences between Generative AI and AI Agents.

## The Big Picture: AI, ML, and Deep Learning

**Artificial Intelligence (AI)** is the broad overarching field in computer science focused on training computers to perform tasks that humans are naturally good at, such as recognizing patterns, processing visual information, or understanding voice and text [[00:15](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=15)].

**Machine Learning (ML)** is a major subdomain *within* AI [[00:35](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=35)]. The core idea of ML is that instead of explicitly programming a computer with logic (like you would in traditional software engineering), you provide the computer with data (inputs and outputs), and it figures out the logic or patterns on its own [[06:13](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=373)].

Within Machine Learning, there are two main branches:

1. **Statistical Machine Learning:** This uses statistical algorithms like linear regression, decision trees, or k-means clustering [[00:45](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=45)]. These are typically best suited for structured data (like data in rows and columns) [[17:03](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1023)].
2. **Deep Learning (DL):** This involves **Neural Networks** [[01:10](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=70)]. Deep learning is designed to mimic the human brain's ability to recognize patterns, making it especially powerful for unstructured data like images, audio, and raw text [[16:37](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=997)].

> It's important to note that you can have AI systems that are *not* machine learning—such as rule-based systems or regular expressions [[01:53](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=113)].

---

## Statistical Machine Learning: Supervised vs. Unsupervised

When looking at Statistical ML, we generally divide problems into two types based on how the model is trained.

### Supervised Learning

In supervised learning, the model is trained on **labeled data**—meaning you provide both the inputs (X) and the known correct outputs (Y) [[11:03](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=663)]. The model learns to map the inputs to those specific outputs.

There are two major categories of tasks in supervised learning:

* **Classification:** The output is mapped to discrete categories.
* *Example:* Classifying an email as spam or non-spam [[07:52](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=472)].
* *Example:* Identifying an image as a cat or a dog.


* **Regression:** The output is a continuous number.
* *Example:* Predicting the price of a house based on features like area, age, and number of bedrooms (similar to a Zillow "Zestimate") [[08:46](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=526)]. The output could be $925,000, $921,450, etc.



### Unsupervised Learning

In unsupervised learning, the model is given a massive amount of **unlabeled data**. The algorithm's job is to find underlying patterns, structures, or groupings without any explicit guidance [[15:02](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=902)].

* *Analogy:* Imagine asking a child to sort a messy pile of toys into two buckets, without telling them *how* to sort them. The child might sort them by color, size, or type (cars vs. dolls) purely by noticing patterns [[12:13](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=733)].
* *Technique:* A common unsupervised technique is **Clustering**, which can be used to organize different types of legal documents into groups or detect outliers in financial data [[13:41](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=821)]. Algorithms like K-means and DBSCAN are used here [[14:33](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=873)].

---

## Deep Learning & Neural Networks

When you are dealing with unstructured data (like an image of a cat), simple statistical algorithms struggle because they look for predefined features in specific locations (like rows and columns). A cat's eyes or whiskers might appear in different parts of an image depending on the photo [[18:20](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1100)].

Deep learning solves this using **Neural Networks**, which can detect features regardless of their location or scale [[18:36](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1116)].

### How Neural Networks Make Decisions

Imagine training a group of students to identify if an image contains a Koala.

1. **Input Layer:** Individual students (neurons) are assigned highly specific tasks—one detects only eyes, another only noses [[19:32](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1172)]. They analyze the image and give a confidence score between 0 and 1.
2. **Hidden Layers:** The scores from the eye and nose detectors are passed to the next group of students (the hidden layer), whose job is to determine if the image contains a *Koala face* [[21:03](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1263)]. They use a formula to weigh the inputs (e.g., giving more weight to a Koala's distinct nose) [[21:37](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1297)].
3. **Output Layer:** The final student takes the findings from the face detectors and body detectors to make the final yes/no decision on whether it is a Koala [[22:47](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1367)].

### How Neural Networks Learn: Backward Error Propagation

How do the individual "students" (neurons) get good at their specific tasks?

1. Initially, they make random guesses [[24:19](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1459)].
2. The final output is checked against the correct answer by a supervisor.
3. If the network made a mistake, that error feedback is passed *backward* through the network—from the output layer back to the hidden layers and input layers [[25:22](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1522)].
4. The individual neurons adjust their "weights" (how they evaluate their specific feature) based on this feedback.
5. By repeating this process with thousands of images, the network gradually improves its accuracy [[26:14](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1574)].

---

## Neural Network Architectures

Different tasks require different structural arrangements of these neurons:

* **Feed Forward Neural Network:** Information moves in only one direction—from input, through hidden layers, to output. (Analogy: A juicer where fruit goes in one side and juice comes out the other) [[31:14](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1874)].
* **Recurrent Neural Network (RNN):** Features a feedback loop. The output from one step is fed back into the network as input for the next step, making it useful for sequential data over time. (Analogy: Tasting and adjusting a soup while cooking it) [[31:39](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1899)].
* **Transformer:** A highly complex architecture that processes sequential data efficiently. This is the foundational architecture behind modern Generative AI and Large Language Models (LLMs) [[32:23](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1943)]. (The "T" in ChatGPT stands for Transformer [[33:00](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=1980)]).

---

## Generative AI vs. Traditional AI

With the rise of ChatGPT, it's important to distinguish what Generative AI actually is.

**Generative AI** is a category of AI designed to create *new* content—be it text, code, audio, or video [[35:22](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=2122)]. It is powered by **Large Language Models (LLMs)**, which are trained on massive datasets (like Wikipedia or books) to predict the next logical set of words, much like a highly advanced "stochastic parrot" [[41:56](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=2516)].

**Traditional AI** refers to the tasks we discussed earlier: analyzing, classifying, or predicting based on existing data (spam detection, house price prediction) [[37:54](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=2274)].

* **Output:** Generative AI produces creative, unstructured content. Traditional AI produces discrete labels (yes/no) or numbers.
* **Autonomy:** Generative AI has limited autonomy; it reacts to your prompts.

---

## The Next Evolution: AI Agents and Agentic AI

While Generative AI is powerful for answering questions or creating content, it is generally reactive. The next level of complexity is **Agentic AI**.

Let's look at how an AI system can evolve using an HR chatbot as an example:

1. **Workflow (RAG - Retrieval Augmented Generation):** A chatbot that can read private company PDF policies to answer a question like, "What is the sick leave policy?" It just retrieves information and generates an answer [[45:15](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=2715)].
2. **Tool-Augmented Chatbot:** A chatbot hooked up to company APIs that can answer, "How many leaves do I have left?" and also execute the command, "Apply for a two-day leave." It is still reacting to a direct instruction [[46:27](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=2787)].
3. **AI Agent:** A system where you give a high-level goal, and the AI autonomously creates a multi-step plan, uses various tools, and executes the tasks [[48:04](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=2884)].
* *Example Prompt:* "Onboard the new intern joining next Monday."
* *Agent Action:* The agent reasons through the goal, schedules a welcome meeting via Outlook, creates an HR profile, creates an IT ticket for Wi-Fi credentials, and orders a laptop [[49:30](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=2970)].



**Agentic AI** refers to a system that utilizes one or more of these AI Agents [[52:08](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=3128)]. Generative AI (the LLM) is simply the "brain" or a subcomponent *within* the Agentic AI system that allows it to reason and generate the text needed to interact with those tools [[57:16](https://www.youtube.com/watch?v=VGFpV3Qj4as&t=3436)].


I would be happy to explain the fundamentals of AI Agents exactly as they are broken down in this video.

Here is a deep dive into the concepts, flowing from what an AI agent actually is, to how they operate, and finally how to secure and evaluate them.

### What is an AI Agent?

If you ask a pure Large Language Model (LLM) a question about a real-time event—like finding the latest flight prices—it shouldn't be able to answer because the model has a strict knowledge cutoff date [[01:21](http://www.youtube.com/watch?v=GScUjc-A4yE&t=81)]. However, if you see an icon saying "Searching the web," it means the LLM has been given access to the internet.

A prime example is Amazon's Rufus chatbot. If you tell it to "find organic honey with a 4.5 rating under $20 and buy the first one," it actually does it [[01:54](http://www.youtube.com/watch?v=GScUjc-A4yE&t=114)]. It does this by combining several components:

* **The Brain:** The LLM itself.
* **Knowledge:** A product database it can search.
* **Tools:** APIs it can call (e.g., a Review API, a Checkout API).
* **Memory:** Context of your past conversation.

**Definition:** An AI Agent is a program that uses an LLM as its brain and takes input, thinks, and acts to complete a complex goal in an **autonomous** fashion using tools, memory, and knowledge [[03:28](http://www.youtube.com/watch?v=GScUjc-A4yE&t=208)]. Just like a human can't drill a screw into a wall with their bare hands, an LLM can't act without tools (like a screwdriver or drill). When equipped with tools, it can perform multi-step reasoning and planning [[04:03](http://www.youtube.com/watch?v=GScUjc-A4yE&t=243)].

---

### Levels of Agency

Not all agents are created equal. You can assign different levels of "agency" (autonomy) to an AI system. As agency increases, your ability to predict its exact behavior decreases [[07:04](http://www.youtube.com/watch?v=GScUjc-A4yE&t=424)].

1. **Low Agency (ChatGPT):** Very limited tool access. It primarily answers questions and maybe searches the web [[05:35](http://www.youtube.com/watch?v=GScUjc-A4yE&t=335)].
2. **Workflow Agency (Zapier / n8n):** You define a workflow using a drag-and-drop interface. The AI has access to your Gmail or Slack but operates within strict boundaries [[05:54](http://www.youtube.com/watch?v=GScUjc-A4yE&t=354)].
3. **High Agency (Claude Code):** Given access to your local code repository, it can autonomously plan, code, test, and review thousands of lines of code [[06:22](http://www.youtube.com/watch?v=GScUjc-A4yE&t=382)].
4. **Fully Autonomous (OpenDevin / Open Claude):** Runs on a Virtual Private Server (VPS) with access to dozens of tools. You give it a task, go to sleep, and it works completely on its own without asking for clarification [[06:43](http://www.youtube.com/watch?v=GScUjc-A4yE&t=403)].

---

### The ReAct Loop (Reason + Act)

How does an agent actually solve a problem? It uses something called the **ReAct Loop** [[07:46](http://www.youtube.com/watch?v=GScUjc-A4yE&t=466)].
When you give an agent a task, it doesn't just blindly execute. It goes through a cycle:

1. **Think/Plan (Reason):** "What steps do I need to take?"
2. **Act:** It calls a tool (like writing a line of code or querying an API).
3. **Observe:** It looks at the result of that action.
4. **Refine:** It adjusts its plan based on the observation.

It stays in this loop continuously until the end goal is achieved [[08:05](http://www.youtube.com/watch?v=GScUjc-A4yE&t=485)].

---

### Multi-Agent Systems & Multimodal Agents

* **Multi-Agent Systems:** Sometimes a problem is too complex for one agent. You can have multiple agents collaborate. For example, a "Product Search Agent" finds the items, and then hands the task off to a "Checkout Agent" to process the payment [[08:28](http://www.youtube.com/watch?v=GScUjc-A4yE&t=508)]. In coding, one agent might write the code while a separate agent reviews it.
* **Multimodal Agents:** These agents can process more than just text. They can look at images, audio, and video. For example, a health insurance agent that can extract text from a scanned PDF or process an image of a patient's ID card [[09:09](http://www.youtube.com/watch?v=GScUjc-A4yE&t=549)].

---

### Workflows vs. AI Agents

It's a common misconception that *any* application using an LLM is an AI Agent. That is not true [[12:36](http://www.youtube.com/watch?v=GScUjc-A4yE&t=756)].

* **Workflow:** You use Python code to fetch a news article, pass it to an LLM with strict instructions to "generate a summary," and then post-process that summary [[12:57](http://www.youtube.com/watch?v=GScUjc-A4yE&t=777)]. The control flow is hard-wired by the programmer. The LLM is just a simple text-processing component [[13:11](http://www.youtube.com/watch?v=GScUjc-A4yE&t=791)].
* **AI Agent:** You give the LLM a goal and a toolbox, and *the LLM decides* which tools to call and in what order [[13:20](http://www.youtube.com/watch?v=GScUjc-A4yE&t=800)].

---

### Guardrails

An autonomous agent without restrictions is like a "monkey with a gun"—it can cause severe damage [[13:45](http://www.youtube.com/watch?v=GScUjc-A4yE&t=825)].

* *Air Canada* was sued because their AI chatbot hallucinated a fake refund policy [[13:51](http://www.youtube.com/watch?v=GScUjc-A4yE&t=831)].
* *Chipotle's* food-ordering bot was tricked into answering programming questions (like reversing a linked list) because it lacked scope restrictions [[14:23](http://www.youtube.com/watch?v=GScUjc-A4yE&t=863)].

Hackers can also use "jailbreaks" (e.g., asking the AI to tell a story about their Grandma working in a napalm factory to trick it into providing a dangerous recipe) [[14:45](http://www.youtube.com/watch?v=GScUjc-A4yE&t=885)].

To prevent this, developers build **Guardrails** (using middleware) to intercept requests and responses. Guardrails ensure the agent redacts emails, masks credit cards (PII protection), stays on topic, and rejects toxic or dangerous prompts [[15:44](http://www.youtube.com/watch?v=GScUjc-A4yE&t=944)].

---

### Evaluating AI Agents

Evaluating traditional deterministic software is easy. Evaluating an AI agent is difficult because it is probabilistic—it might give you a slightly different output every time you ask the exact same question [[16:27](http://www.youtube.com/watch?v=GScUjc-A4yE&t=987)].

You must evaluate them across three categories using tools like LangSmith or Ragas [[17:13](http://www.youtube.com/watch?v=GScUjc-A4yE&t=1033)]:

1. **Functional:** Is the answer factually correct? Is it faithful to the source data without hallucinating? [[16:41](http://www.youtube.com/watch?v=GScUjc-A4yE&t=1001)] Because strings won't match exactly, developers use mathematical concepts like *Cosine Similarity* to check if the generated answer carries the same semantic meaning as the expected answer [[17:50](http://www.youtube.com/watch?v=GScUjc-A4yE&t=1070)].
2. **Cost & Latency:** Does the agent take too long to run? (Measured in P50 and P99 percentiles). Are token costs going through the roof? [[16:50](http://www.youtube.com/watch?v=GScUjc-A4yE&t=1010)]
3. **Safety:** Did it leak any PII or fail a jailbreak test? [[17:04](http://www.youtube.com/watch?v=GScUjc-A4yE&t=1024)]

 ## Tokens GOAT Video
 https://youtu.be/nKSk_TiR8YA?si=Wt_8TgCeAmd0iOrg
 - Here is an explanation of how LLM tokens work, using the exact examples and analogies from the video.

### Tokens: The Currency of LLMs

Tokens are the currency of Large Language Models. When you use an API to prompt an LLM, you are billed based on the number of tokens you send (input tokens) and the number of tokens the model generates (output tokens). These are usually billed at different rates (e.g., a tiny fraction of a cent per 1,000 tokens) [[00:34](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=34)].

However, different models count tokens differently [[01:20](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=80)]. For example, if you send the exact same prompt—"Hello World"—to two different models:

* **Anthropic (Claude 3.5 Haiku):** Might count it as 11 input tokens.
* **Google (Gemini 2.0 Flash):** Might count it as 4 input tokens.

To understand why this happens, we have to look at what the LLM is actually doing under the hood.

### How the LLM Processes Text

LLMs do not process text; they compute using **numbers** [[04:04](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=244)]. Every model has a "vocabulary" consisting of words, subwords, and characters, and each of these is assigned a specific number.

Here is the exact end-to-end process [[03:52](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=232)]:

1. **Encoding:** The text you provide is broken down into the largest individual chunks (tokens) that the model recognizes in its vocabulary. For example, "Hello world!" might be split into `Hello`, `_world`, and `!`. The tokenizer looks up the corresponding numbers for these chunks in its vocabulary.
2. **Computing:** The LLM does all of its thinking and processing using those raw numbers.
3. **Decoding:** The LLM outputs a sequence of new numbers, which are then decoded back into text and joined together for you to read [[04:11](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=251)].

To put the token-to-text ratio in perspective: If you run a 2,300-character paragraph (like a story about a "wise owl of moonlight forest") through GPT-4o's tokenizer (`o200k_base`), it compresses down to fewer than 500 tokens (numbers) [[03:18](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=198)].

### How Tokenizers are Trained (And Why They Differ)

The reason Anthropic and Google count "Hello World" differently is because they use different tokenizers trained on different data. Let's look at how tokenizers are built using a tiny training corpus: *"the cat sat on the mat"* [[05:05](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=305)].

**1. Character-Level Tokenizer**
The most basic tokenizer just maps individual characters. In our corpus, there are only 10 unique characters (spaces, t, h, e, c, a, etc.). If we feed the input `"cats sat mat"` (11 characters) into this tokenizer, it outputs exactly 11 tokens [[06:01](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=361)].

This is incredibly inefficient. The more tokens an LLM has to process, the more memory it requires and the harder it has to work [[06:31](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=391)].

**2. The Vocabulary Size Trade-off**
To reduce the number of tokens, developers group frequently occurring characters into "subwords." Let's look at the word **"understanding"** [[06:43](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=403)]:

* **Small Vocabulary (e.g., 1,000 tokens):** The model might not have "understanding" in its dictionary. It has to break it down into smaller subwords it *does* know: `under` + `st` + `and` + `ing` (5 tokens).
* **Medium Vocabulary (e.g., 50,000 tokens):** It can match larger chunks: `under` + `standing` (3 tokens).
* **Large Vocabulary (e.g., 200,000 tokens):** It recognizes the whole word: `understanding` (2 tokens).

Fewer tokens are vastly more efficient for the LLM. However, you cannot scale the vocabulary size to infinity because housing a massive dictionary requires a much larger model and significantly more memory to execute [[07:15](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=435)].

**3. Unusual Words and Languages**
Tokenizers are optimized for the data they were trained on. If you use a rare word, like **"frabjous"** (a made-up word from a Lewis Carroll poem), the model won't have it in its vocabulary [[09:04](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=544)]. GPT-4o has to aggressively split "frabjous" into 4 separate tokens just to process it.

This is also why coding in JavaScript is cheaper than coding in Haskell in the AI era [[09:37](http://www.youtube.com/watch?v=nKSk_TiR8YA&t=577)]. Because LLMs see vastly more JavaScript than Haskell in their training data, they have highly optimized subwords for JavaScript. Sending 20 lines of JS costs fewer tokens than 20 lines of Haskell!
