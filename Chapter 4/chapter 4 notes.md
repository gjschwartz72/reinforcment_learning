# Chapter 4 Notes  

Chapter 3 and 4 are working with the fully specified environment.  So we know $p(s', r|s, a)$  
This implies that:  
*  Know all transition probablities
*  Know the reward distributions 
*  Can calculate the expectations exactly. 
  

Dynamic Programming (DP) is based on that model.  Chapters 3 and 4 are primarily to introduce the structure of RL problems and optimal solutions before moving to learning from data.

## Conceptial not on $v_/pi(s)$  

$v_\pi(s) = \sum_{a} \pi(a \mid s) q_\pi(s,a)$   
* $\pi(a \mid s)$ provides the action weights for state $s$ 
* $q_\pi(s,a)$ provides the valuies for each action $a$ in state $s$

This helps understand how the epsilon policy update below actually can work to find  
the optimal actions.  In the policy, most of the weight is given to the best action.  
This sys nothing about what that best action is.  
Recall the Bellman equations: 
* $q_\pi(s,a) = \sum_{s',r} p(s', r \mid s,a)\left[r + \gamma v_\pi(s')\right]$
* $v_\pi(s) = \sum_{a} \pi(a \mid s) \sum_{s',r} p(s', r \mid s,a)\left[r + \gamma v_\pi(s')\right]$ 
* as: $v_\pi(s) = \sum_{a} \pi(a \mid s) q_\pi(s,a)$  



## $\epsilon$-soft policy update

Here we are doing the following:  
1. Compute all $q_\pi(s,a) = \sum_{s',r} p(s', r \mid s,a)\left[r + \gamma v_\pi(s')\right] 
2. find $a* = \argmax_a q(s,a)$ 
3. Assign the weigts per the policy 
4. Calculate $v_\pi(s) = \sum_{a} \pi(a \mid s) q_\pi(s,a)$

### Algorithm 
**Initialization**

Initialize arbitrarily:
- $V(s)$ for all $s \in \mathcal{S}$
- $\pi(a \mid s)$ as an $\varepsilon$-soft policy

Repeat:

**1. Policy Evaluation**

Repeat until convergence:

$V(s) \leftarrow \sum_a \pi(a \mid s)\sum_{s',r} p(s', r \mid s, a)\left[ r + \gamma V(s') \right]$

---

**2. Policy Improvement (ε-soft)**

For each state $s$:

Compute action values:

$q(s,a) = \sum_{s',r} p(s', r \mid s, a)\left[ r + \gamma V(s') \right]$

Find greedy action:

$a^* = \arg\max_a q(s,a)$

Update policy:

$\pi(a \mid s) =
\begin{cases}
1 - \varepsilon + \frac{\varepsilon}{|\mathcal{A}(s)|}, & \text{if } a = a^* \\
\frac{\varepsilon}{|\mathcal{A}(s)|}, & \text{otherwise}
\end{cases}$

---

**3. Convergence Check**

If the greedy action $a^*$ does not change for any state, then stop.

---

Output:

- $V \approx v_{\pi}$
- $\pi \approx \pi_*$ (optimal within ε-soft policies)