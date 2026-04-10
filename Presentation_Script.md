# Closing Presentation Script — Slides 15-19 (~3 minutes)

**Paper:** Learning an Interpretable Traffic Signal Control Policy (AAMAS 2020)
**Subject:** Deep Reinforcement Learning
**Presenter:** Naaz (Closing Section)

---

## SLIDE 15 — Main Results: Average Vehicle Delay Comparison (~55 sec)

> Now let's look at how all these methods actually performed. The table here shows the average vehicle delay across three demand scenarios — low, medium, and high traffic. Lower is better.
>
> The baseline is the commonly deployed actuated controller — what's actually running on real intersections today — giving us around 60 seconds delay in low demand, 70 in medium, and 95 in high.
>
> Our key method, DRHQ, brings that down to about 50, 60, and 85 seconds respectively — that's up to a 19.4% reduction while remaining fully interpretable.
>
> Now compare that to the black-box DQN — the upper bound — which achieves 48, 57, and 82 seconds. The gap between DRHQ and DQN is only 1 to 3 seconds across all scenarios. So we're giving up almost nothing in performance to gain full interpretability.
>
> Looking at the other methods — DRSQ comes close at 52, 62, and 87 seconds, but DRHQ consistently edges it out. PPO, which is a policy-gradient method, manages around 55 and 65 in low and medium demand but completely fails in high demand, stuck at 95 — same as the baseline. DRQ performed poorly across the board. And CMA-ES, while matching DRHQ at around 50, 58, and 85 seconds, requires thousands of episodes to get there, making it impractical for online use.
>
> You'll also notice the performance drop at episode 20 across the DQN variants — that's when epsilon in the epsilon-greedy exploration is reduced to zero, switching from exploration to full exploitation — and from that point, the learned policy takes over completely.

---

## SLIDE 16 — Interpretation of Results (~50 sec)

> So why does DRHQ work the best among all interpretable variants? This comes down to a core idea in deep reinforcement learning — function approximation. The regulatable polynomial function G has far fewer parameters and is much more constrained than a deep neural network. So asking G to approximate exact Q-values, like DRQ does, is simply infeasible — the function approximator doesn't have enough capacity.
>
> DRHQ solves this elegantly. It only needs to match *which action has the highest Q-value* — the argmax — not the values themselves. This is a much easier target for a polynomial to fit. And because DQN is an off-policy algorithm, this works — the Q-network trains independently using experience replay, while the regulatable function G acts as the actual controller, imitating the Q-network's action selection through minibatch sampling from the same replay buffer.
>
> In contrast, PPO — a policy-gradient method — directly optimizes the regulatable function's parameters. Its clipped objective bounds the policy update steps, which is normally a strength for stability, but here it causes PPO to converge to local optima. The value-based approach clearly wins in this domain.
>
> The bottom line: that 1 to 3 second cost buys us complete interpretability — every signal decision can be explained, audited, and manually adjusted by a traffic engineer. For safety-critical infrastructure, that is an excellent trade-off.

---

## SLIDE 17 — Limitations & Future Scope (~45 sec)

> That said, this work does have notable limitations. First, all experiments were done on a single intersection in Utah using the SUMO simulator — there's no real-world deployment yet, and we don't know how well the learned policy transfers to different intersection types or geographies. The discount factor had to be manually tuned — raised from 0.8 to 0.9 for high demand to give the agent a longer planning horizon — which means hyperparameter sensitivity across scenarios is still an open problem.
>
> From a DRL perspective, the MDP formulation here is single-agent. Scaling to multi-intersection control would turn this into a multi-agent reinforcement learning problem with a combinatorial action space — significantly harder.
>
> For future work, the paper suggests warm-starting by observing a currently deployed controller — essentially using imitation learning to bootstrap the Q-network before online fine-tuning. Beyond that, multi-intersection coordination, real-world field testing, incorporating pedestrian and cyclist phases, and integration with connected and autonomous vehicle data are all promising directions.

---

## SLIDE 18 — Conclusion & Key Takeaways (~30 sec)

> To wrap up — the core message of this paper is that interpretability does not have to come at the cost of performance. The polynomial-based regulatable policy matches DNN performance within 1 to 3 seconds of delay. DRHQ achieves a 19.4% reduction over deployed actuated controllers.
>
> From a deep reinforcement learning standpoint, this paper demonstrates that value-based methods like DQN outperform policy-gradient methods like PPO for training constrained function approximators. And the off-policy nature of DQN is what makes the two-stage approach — train a powerful Q-network, then distill into an interpretable policy — possible in the first place.
>
> As the authors put it: we can build AI systems that are both powerful and explainable. We don't always have to choose one over the other. Thank you.

---

## SLIDE 19 — Thank You

> *(Pause, smile, open for questions)*

---

## Timing Tips

| Slide | Topic | Duration |
|-------|-------|----------|
| 15 | Main Results | ~55 sec |
| 16 | Interpretation | ~50 sec |
| 17 | Limitations & Future | ~45 sec |
| 18 | Conclusion | ~30 sec |
| 19 | Thank You | ~5 sec |
| **Total** | | **~3:00** |

- **If running short:** Trim the CMA-ES/PPO details on slide 15 or the discount factor point on slide 17.
- **If need to stretch:** Add a brief pause before the closing quote on slide 18 for emphasis.

---

## DRL Concepts Referenced (for Q&A prep)

| Concept | Where It Appears | What to Know |
|---------|-------------------|--------------|
| **Off-policy learning** | Slide 16 | DQN is off-policy — the Q-network can learn from data generated by any policy, which is why G can act while Q trains separately |
| **Experience replay** | Slide 16 | Both Q-network and G train on minibatches sampled from the same replay buffer of stored transitions (s, a, r, s') |
| **Epsilon-greedy** | Slide 15 | Exploration decays from 0.05 to 0 after 20 episodes — the visible performance drop in the graphs |
| **Value-based vs Policy-gradient** | Slides 15, 16, 18 | DQN (value-based) outperforms PPO (policy-gradient) for constrained function approximators |
| **Function approximation** | Slide 16 | The core DRL challenge — polynomial has far less capacity than a DNN, so the learning target must be simplified |
| **Discount factor (γ)** | Slide 17 | Set to 0.8 for low/medium demand, 0.9 for high — longer planning horizon needed when clearing queues takes more time |
| **MDP formulation** | Slide 17 | States = sensor inputs, Actions = phase assignments, Reward = delay reduction, single-agent formulation |
| **Policy distillation** | Slide 16, 18 | The two-stage idea: train a powerful DNN policy, then distill/compress it into a simpler interpretable function |
