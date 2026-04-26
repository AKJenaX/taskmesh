# TaskMesh - OpenEnv Hackathon Pitch (< 2 Mins)

**[0:00 - 0:15] The Hook & Problem**
*Visual: Show the chaotic TaskMesh UI queue filling up with high and low priority tasks.*
"Scheduling tasks efficiently in distributed systems is notoriously difficult. Static rules like Shortest-Job-First completely fail when a 60-second background job blocks a 1-second critical payment process. We built TaskMesh to replace rigid heuristics with an AI that learns to optimize the chaos."

**[0:15 - 0:45] The Environment & OpenEnv**
*Visual: Show the openenv.yaml manifest and the OpenEnv Python wrapper code.*
"To solve this, we formulated task scheduling as a Reinforcement Learning problem. We wrapped our dynamic scheduling engine into the new `OpenEnv` framework. 
The agent's state is a flattened 41-dimensional vector observing the global queue time and up to 20 waiting tasks. 
The action? Choosing the precise index of the next task to execute. 
The reward? A heavy penalty for every second of wait time, balanced against a massive bonus for scheduling urgent tasks early."

**[0:45 - 1:15] The Training & TRL**
*Visual: Open the Google Colab Notebook and show the Policy Gradient/DQN training loop converging.*
"Instead of using a massive, sluggish LLM, we implemented a lightning-fast PyTorch Policy network. You can run our Colab notebook and watch it learn in under 5 minutes. As you can see from our reward curves, the agent rapidly discovers how to balance maximum throughput against tail latency, escaping the local minimums of standard sorting algorithms."

**[1:15 - 1:45] The Results & HF Space**
*Visual: Show the Gradio App running on Hugging Face Spaces.*
"We deployed our trained agent to Hugging Face Spaces using Gradio. You can input any JSON array of tasks and watch the PyTorch model infer the optimal schedule in under 100 milliseconds. It produces wildly different—and mathematically superior—orderings compared to a baseline priority queue."

**[1:45 - 2:00] Conclusion**
*Visual: Show the GitHub repo / README.*
"TaskMesh proves that lightweight, episodic RL can solve critical infrastructure problems better than static code. Try the environment on our Hugging Face space today. Thank you!"
