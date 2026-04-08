# Presentation Script
## "Learning an Interpretable Traffic Signal Control Policy"
### Paper by: Ault, Hanna, Sharon (2020) | Presented by: 

---

## SLIDE 1 — Title Slide
**[~30 seconds]**

> "Good morning/afternoon everyone. Today I'll be presenting a research paper titled **'Learning an Interpretable Traffic Signal Control Policy'** by James Ault, Josiah Hanna, and Guni Sharon, published on arXiv in 2020. This paper sits at the intersection of reinforcement learning and real-world transportation systems — and tackles a very practical question: can we make AI-powered traffic lights that humans can actually understand?"

---

## SLIDE 2 — Presentation Outline
**[~20 seconds]**

> "Here's a quick overview of what I'll cover. First, the motivation and objective behind this research — why is this problem important. Then, the key techniques and algorithms the authors developed. After that, the experimental setup they used for evaluation. Then we'll look at the main results and what they mean. And finally, the limitations and future scope of this work."

---

## SLIDE 3 — Motivation & Problem
**[~1 minute 30 seconds]**

> "Let's start with the motivation. Traffic congestion is a massive global problem — costing billions of dollars in wasted fuel, lost time, and increased emissions every year. Researchers have shown that Reinforcement Learning using deep neural networks can reduce vehicle delay at intersections by up to 73% compared to fixed-timing controllers."

> "But here's the catch — and this is the core problem the paper addresses. Deep neural networks are *black boxes*. You feed them traffic sensor data, and they output a signal change, but nobody — not the engineer, not the city planner — can explain *why* the light turned green at that particular moment."

> "Now, for something like a product recommendation, that's fine. But for traffic signals, this is a serious issue. As you can see on the right, interpretability matters for four critical reasons: **liability** — who's responsible if an AI-controlled signal causes an accident? **Regulation** — government agencies must approve the control logic. **Trust** — engineers need to understand and manually tune the system. And **safety** — black-box failures in traffic systems can be catastrophic."

> "So the core tension is: high-performing DNNs versus interpretable simple rules. Can we have both?"

---

## SLIDE 4 — Paper Objective
**[~1 minute]**

> "The paper's objective is clear: design interpretable, what they call 'regulatable', control policies for traffic signals that can match deep neural network performance while remaining human-understandable."

> "The authors make six specific contributions. They formally define what a 'regulatable' function means. They compare these interpretable functions against DNN policies. They study three different optimization methods — CMA-ES, PPO, and Deep Q-Learning. They develop three novel DQN variants specifically designed to work with regulatable functions. And importantly, they test everything on simulations of *real* intersections with *real* observed traffic demand — not synthetic data. And they compare against actually deployed actuated controllers, not just basic fixed-timing signals."

---

## SLIDE 5 — Regulatable Control Function
**[~1 minute 30 seconds]**

> "This slide covers the most important concept in the paper — the **regulatable control function**. On the left, you can see the formal definition. A precedence function is called 'regulatable' if for every input state variable, its partial derivative is always non-negative or always non-positive. In simpler terms, this means the relationship between each input and the output is *monotonic* — it always pushes in the same direction."

> "Why does this matter? Look at the intuition box on the right. With a regulatable function, an engineer can say: 'Green was given to Phase 4 *because* stopped Southbound vehicles increased while Eastbound queue decreased.' Every decision has a human-readable explanation. And engineers can adjust individual weights to tune the behavior."

> "The state variables they track for each phase are listed here — things like stopped vehicle count, approaching vehicle count, cumulative waiting time, average queue length, and vehicle speed."

> "The actual mathematical function is a polynomial — a weighted sum of state variables raised to learned exponents, multiplied by clearance interval flags. For their test intersection with 8 phases and 8 non-conflicting pairs, this gives 256 tunable parameters. They prove via Lemma 1 that this function is indeed regulatable — the partial derivatives maintain constant sign since all inputs are non-negative."

---

## SLIDE 6 — Three DQN Variants
**[~1 minute 30 seconds]**

> "Now, the key innovation. The authors found that you can't just directly train the polynomial function using standard Q-learning — the function can't represent the necessary intermediate approximations during learning. So their solution is elegant: **train a powerful DQN first** — the black-box neural network — and then **teach the interpretable function G to imitate it**."

> "They develop three variants with increasing levels of relaxation:"

> "**DRQ** — Deep Regulatable Q-Learning — tries to match the exact Q-values. The goal is G(s,a) = Q(s,a). But this is too ambitious — a polynomial simply cannot replicate the full capacity of a neural network. This one performs the worst."

> "**DRSQ** — Deep Regulatable Softmax Q — relaxes the goal. It only needs G to match the *relative ranking* of actions, not exact values. It uses cross-entropy between the softmax distributions of Q and G. This works much better because proportional equivalence is sufficient for the same policy."

> "**DRHQ** — Deep Regulatable Hardmax Q — relaxes even further. It only needs the argmax of G to match the argmax of Q — meaning, it only cares about *which action wins*, not the values or even the ranking. This gives maximum flexibility to the polynomial function and produces the best results."

> "The key insight is this progression at the bottom: match values, which is hard... match rankings, which is easier... match only the winner, which is easiest and actually works best."

---

## SLIDE 7 — CMA-ES & PPO
**[~1 minute]**

> "The paper also tests two alternative optimization methods. **CMA-ES** — Covariance Matrix Adaptation Evolution Strategy — is an evolutionary approach. It has few hyperparameters and can achieve near-DQN performance, which proves the regulatable function *can* work well. But it's completely impractical — it needs 24 full episodes per parameter update and requires roughly 4,000 episodes to stabilize, which translates to 11 years of simulated traffic."

> "**PPO** — Proximal Policy Optimization — is a popular policy gradient method. It produces smooth, safe learning curves with bounded gradient steps. But it gets stuck in local optima due to over-regularization. In high demand scenarios, it can't even beat the basic actuated controller."

> "The conclusion is clear: neither CMA-ES nor PPO are suitable for practical deployment. The DQN variants, particularly DRHQ, win decisively."

---

## SLIDE 8 — Experimental Setup
**[~1 minute]**

> "For experiments, the authors use **SUMO** — Simulation of Urban Mobility — a well-established traffic simulator. They use real traffic data from the Utah Department of Transportation, covering over 2,000 signalized intersections."

> "Their test intersection is **State Street and East 4500 South in Murray, Utah** — a real intersection handling over 50,000 vehicles per day with a peak rate of 95 cars per minute. It has 10 traffic phases and 11 non-conflicting phase pairs, giving 352 tunable parameters for the regulatable policy."

> "They test three demand profiles — low, medium, and high — corresponding to real traffic data from specific dates in 2019, with 14-hour windows from 7 AM to 9 PM."

> "The DQN uses 3 hidden layers with 64 units each, a replay buffer of 100,000 transitions, and epsilon-greedy exploration that decays to zero after 20 episodes."

> "The baseline is SUMO's actuated signal controller — this is what real intersections actually use today — with a maximum green time of 300 seconds."

---

## SLIDE 9 — Main Results
**[~1 minute 30 seconds]**

> "Now the results. This table shows average vehicle delay across all methods and demand profiles. Lower is better."

> "The actuated baseline — what real intersections use — gives about 60, 70, and 95 seconds of average delay for low, medium, and high demand respectively."

> "**DRHQ** — the best interpretable method — achieves approximately 50, 60, and 85 seconds. That's a significant improvement."

> "The full black-box DQN achieves 48, 57, and 82 seconds. So the gap between DRHQ and DQN is only about 1 to 3 seconds."

> "Meanwhile, PPO fails to beat the actuated controller in high demand, and DRQ performs poorly across the board."

> "The key finding, highlighted at the bottom: DRHQ achieves **up to 19.4% reduced vehicle delay** compared to commonly deployed actuated signal controllers, while remaining fully interpretable. And it's only marginally worse than the opaque neural network."

---

## SLIDE 10 — Interpretation of Results
**[~1 minute]**

> "Why does DRHQ work best? Because it only needs to match *which action wins* — not exact values, not even rankings. This gives the polynomial function maximum flexibility to find a good fit. It converges within a single episode for low and medium demand. It's the 'less is more' principle — an easier learning target paradoxically produces a better practical policy."

> "The other methods fall short for specific reasons. DRQ asks too much of a polynomial. DRSQ's softmax ranking is still harder to match than just the winner. PPO is over-regularized. CMA-ES needs too many episodes. And pure polynomial or Fourier basis approximators without the DQN-imitation framework can't even complete basic scenarios."

> "The critical insight is in the box at the bottom. The gap between DRHQ and full DQN is only 1 to 3 seconds. This small price buys **complete interpretability** — every single decision can be explained, audited, and manually adjusted by traffic engineers. That's an excellent trade-off for safety-critical infrastructure."

---

## SLIDE 11 — Limitations & Future Scope
**[~1 minute]**

> "No paper is without limitations. First, they only tested on **a single intersection** — we don't know if these results transfer to other layouts or cities. Second, all results are from **simulation only** — no real-world deployment has been attempted. CMA-ES, while proving the function *can* achieve good performance, is impractical for actual use. PPO simply doesn't work well here. They didn't explore warm-starting from existing controllers, which could accelerate learning. And while 352 parameters is far less than a neural network, it still requires significant compute to optimize."

> "For future work, the authors suggest several directions: warm-starting by observing currently deployed controllers, extending to multi-intersection coordination — because real traffic networks have many connected intersections. Real-world field testing is essential before any of this sees actual deployment. They also mention transferability across intersection types, incorporating pedestrian and cyclist signals, and integrating with connected and autonomous vehicle data — which is increasingly available."

---

## SLIDE 12 — Conclusion & Key Takeaways
**[~1 minute]**

> "Let me wrap up with six key takeaways."

> "First, interpretable polynomial policies *can* match DNN performance — the gap is at most 1 to 3 seconds."

> "Second, DRHQ is the best approach, achieving 19.4% delay reduction versus deployed actuated controllers."

> "Third, 'regulatable' means monotonic input-output relationships — which makes decisions human-understandable."

> "Fourth, policy gradient methods like PPO are unsuitable for traffic signal optimization in this setting."

> "Fifth, this paper successfully bridges the gap between AI performance and real-world deployability."

> "And sixth — perhaps most importantly — interpretability is not a luxury or a nice-to-have. For safety-critical systems like traffic signals, it's a **requirement**."

> "As the quote at the bottom says: we can build AI systems that are both powerful and explainable. We don't always have to choose one over the other."

---

## SLIDE 13 — Thank You
**[~15 seconds]**

> "Thank you for listening. I'm happy to take any questions or discuss any aspect of the paper in more detail."

---

## TIPS FOR RECORDING

1. **Total target time**: 12-15 minutes
2. **Pace yourself**: Don't rush. Pause briefly between slides.
3. **Emphasize key numbers**: 19.4% delay reduction, 1-3 second gap, 256 parameters
4. **Use pointer/cursor**: When recording, point at the relevant section as you speak
5. **Confidence on algorithms**: Practice the DRQ/DRSQ/DRHQ slide especially — it's the technical core
6. **Close strong**: The conclusion slide ties everything together — deliver it with conviction
