**Paper 1-Jerker Denrell, “Adaptive Sampling Policies Imply Biased Beliefs: A Generalization of the Hot Stove Effect”, CogSci 2020**   
**Question it asks**:- The standard Hot Stove effect states that algorithms that pursue positive outcomes and avoid negative outcomes will correct errors of overestimation but fail to correct errors of underestimation. Does this assumption still hold true if we assume that the algorithm takes a smaller sample or pursues it less? Does Bayesian learning which accounts for size escape this effect?

**How it answers it:**\- We take a setup in which we draw a fixed amount of sample k and calculate its average. Now the amount of samples we take is an increasing function of the average that we have calculated. The average of all this sampling would be biased is proven with an intuitive example.

1) We draw 2 samples and take f(av1)=10 if av1\>0 and 1 if av1\<=0. Let us take av1=1 and av1=-1 as two cases. The expected value of av2 gives 2/12 whereas in case2 it gives \-2/3. This is as more samples pull the result more towards the mean.  
2) This intuition is generalised and holds for any distribution whenever f(av1)is a strictly increasing function of av1.\[Theorem1\]  
3) The paper also proves that while the Bayesian updating is unbiased as it accounts for the number of samples, this only happens if we average over all the learners and a negative bias does exist for most Bayesian learners if positive beliefs lead to larger sample sizes.

**One assumption or limitation you would question**: The research paper mostly gives examples where f(av1) is increasing and tells about the problems of underestimation, however most of the Theorems also have a counterpart where when f(av1) is decreasing there would be the errors of overestimation.  
**How it connects to gridworld:**  
Going back to the question it answers,The explorer behaves as a hot stove not sampling at all from a colour that crosses the danger threshold. A color that is wrongly believed to be lethal on the other hand gets corrected as we sample it more than a color we believe to be dangerous.   
accident\_death  cases=  80  touched again=   2  rate=0.025  
harmless        cases= 376  touched again= 302  rate=0.803  
Here we can see if an accidental death \[false warning\]occurred it was never touched again whereas if it was an\[false endorsement\] that belief was quickly corrected.  
I was able to follow the maths for Theorem 1 and Theorem 2 intuition but I was not able to dive into the maths for Bayesian learning.

**Paper 2-Cédric Colas and colleagues, “Language and Experience: A Computational Model of Social Learning in Complex Tasks”, ICLR 2026**   
**Question it asks**:- Knowledge that is transferred in humans through social learning and experience. Can we model similar behaviour in AI Agents through bayesian inference and social learning to speed up the millions of steps that are needed for traditional reinforcement learning?  
**How it answers it:**\- They set up a gridworld experiment in which the person playing has to learn how they can win a level without being told about the game rules.  
The model maintains theories about game rules. It plays the game, updates its Bayesian inference and then writes advice for the next agent. This is done.using LLaMA-3.1-70B to generate linguistic advice and adjust the theories accordingly   
.Now to see how this experiment fares both humans and agents are allowed to play limited levels and are allowed to take advice from someone else in the form of linguistic advice thus modelling social learning.  
Pure deep reinforcement learning fails whereas the bayesian model combined with LLaMa learns to solve levels. Using social learning humans require around 1.75 less attempts to win for humans and the attempts to win were 1.25 less times for models.These benefits were maximum in games which required multiple unknown roles rather than those that required coordination.  
LLM generated advice improved the outcome for both human and AI agents significantly. Models learned better from model-advice than humans which might be due to using metaphors or contextual knowledge that the model cannot infer on its own.  
A generational learning experiment is carried out where to see how partial knowledge is inherited across multiple layers a 2 lives/agent 10 agents setup was created. There was no scope of one agent to update its beliefs fast enough so the main source it relies upon was the advice. The results of this also shows a decrease in the number of attempts needed to get the first win despite having way fewer lives/agent and opening the possibility of inheritance of wisdom across multiple lives of AI agents as there is in humans.

**One assumption or limitation you would question**: I feel using Bayesian inference only and not testing it out on multiple other probability models is a shortcoming.

**How it connects to gridworld:** The gridworld is very similar to the experiment carried out in this research paper. We model a generational agent learning model in which the knowledge is transferred via beliefs to the next agent who plays this gridworld game.Then we generate different types of advice such as best guess and a selective mode where we only allow beliefs that are greater than tau to be passed onto the next generation. Then we either allow the next agent to inherit these beliefs in confidence learners  or amplify them using literal learners. Then we carry out the process of Bayesian inference again hence creating a form of social learning in this framework.. 

