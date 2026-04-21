# Table of Contents
- [Table of Contents](#table-of-contents)
- [Chapter 3](#chapter-3)
  - [Ex. 3.4](#ex-34)
    - [Parameter Definitions](#parameter-definitions)
  - [Ex 3.5](#ex-35)
  - [Ex 3.6](#ex-36)
  - [Ex 3.7](#ex-37)
  - [Ex 3.8](#ex-38)
  - [Ex 3.9](#ex-39)
  - [Ex 3.10](#ex-310)
  - [Ex 3.11](#ex-311)
  - [Exercise 3.12 / 3.13 style derivations](#exercise-312--313-style-derivations)
    - [Law of total expectations (Review)](#law-of-total-expectations-review)
    - [Intuition](#intuition)
    - [Conditional Law of Total Expectation Review](#conditional-law-of-total-expectation-review)
    - [Intuition](#intuition-1)
    - [End Review](#end-review)
    - [3.12](#312)
    - [3.13](#313)
    - [END](#end)
    - [Final equations](#final-equations)
    - [Intuition](#intuition-2)
  - [Ex 3.14](#ex-314)
  - [Ex. 3.17](#ex-317)
  - [Exercise 3.18](#exercise-318)



# Chapter 3

## Ex. 3.4

| s | a | s' | r | p(s'\|s,a) | p(s',r\|s,a) |
|---|---|---|---|---|---|
| high | search | high | 1 | α | α*r<sub>search</sub> |
| high | search | high | 0 | α | α(1-r<sub>search</sub>) |
| high | search | low | 1 | 1-α | (1-α) r<sub>search</sub> |
| high | search | low | 0 | 1-α | (1-α)(1-r<sub>search</sub>) |
| low | search | high | -3 | 1-β | 1-β |
| low | search | low | 1 | β | β*r<sub>search</sub> |
| low | search | low | 0 | β | β(1-r_sear<sub>search</sub>rch) |
| high | wait | high | 1 | 1 | r<sub>wait</sub> |
| high | wait | high | 0 | 1 | 1-r<sub>wait</sub> |
| low | wait | low | 1 | 1 | r<sub>wait</sub> |
| low | wait | low | 0 | 1 | 1-r<sub>wait</sub> |
| low | recharge | high | 0 | 1 | 1 |

__Note:__   
By the chain rule 
$p(X,Y|Z) = p(X|Z)p(Y|X,Z)$:  
-->  
$p(s',r|s,a) = p(s'|s, a) * p(r|s,a,s')$ 


### Parameter Definitions

- **α (alpha):** p(high | high, search)  
  Probability that searching while the battery is **high** leaves the robot in the **high battery state**.

- **β (beta):** p(low | low, search)  
  Probability that searching while the battery is **low** leaves the robot in the **low battery state**.

- **1 − α:** p(low | high, search)  
  Probability that searching while **high** drains the battery to **low**.

- **1 − β:** p(high | low, search)  
  Probability that searching while **low** exhausts the battery and the robot is **rescued**, returning it to **high**.

- **r<sub>search</sub>:** p(r = 1 | s, search)  
  Probability that the **search** action produces reward **1**.

- **1 − r<sub>search</sub>:** p(r = 0 | s, search)  
  Probability that the **search** action produces reward **0**.

- **r<sub>wait</sub>:** p(r = 1 | s, wait)  
  Probability that the **wait** action produces reward **1**.

- **1 − r<sub>wait</sub>:** p(r = 0 | s, wait)  
  Probability that the **wait** action produces reward **0**.

- **Recharge action:** p(high, 0 | low, recharge) = 1  
  Recharging from the **low** state always moves the robot to **high** with reward **0**.

- **Rescue event:** p(high, −3 | low, search) = 1 − β  
  When searching with low battery and energy is exhausted, the robot is **rescued**, returns to **high**, and receives reward **−3**.

## Ex 3.5
Equation (3.3) for the continuing case is:  

$
\sum_{s' \in S} \sum_{r \in R} p(s', r \mid s, a) = 1
$

For the episodic case, the only modification is that the next state may be terminal, so we replace \(S\) with \(S<sup>+</sup>\)  
where S<sup>+</sup> = S ∪ {terminal}.  
So we are just adding the terminal state to make a super set fit for the episodic case.   
$
\sum_{s' \in S^+} \sum_{r \in R} p(s', r \mid s, a) = 1,
\qquad \forall s \in S,\ a \in A(s).
$

The point of this is to generalize.  The text is making generalizations here so we can use the same notation for both episodic and contiuous cases.  

## Ex 3.6 
The issue here is that there is no reward structure during each step.  There is only a reward at the end of the cycle. 
To make this work we give +1 for each step that does not result in failure.  Then the model is directly rewarded for not failing at each step.

The reward at each time: $G_t = \gamma^{T-t-1}$

**Case 1: $\gamma$ = 1**  
Lets first assume that $\gamma = 1$  $G_t = 1^{T-t-1} = -1$  

| episode length | return |
|---|---|
| 10 steps | −1 |
| 100 steps | −1 |

So no matter how many results, we always get -1. 

**Case 1: $\gamma$ < 1** 

Now the return becomes

Example with $\gamma = 0.9$:

| episode length | return |
|---|---|
| 10 steps | $-0.9^9 \approx -0.387$ |
| 100 steps | $-0.9^{99} \approx -0.000026$ |

In this case the reward increases with more steps which gives a week path for learning.  This is not as strong as simply providing a reward as +1 for each step not resulting in failure.  

## Ex 3.7  
In this case we are rewarding only for the solution of the maze.  Every episode will receive the same reward of 1 as of G<sub>t</sub> is always 1 at any point in time.  As a result there is nothing to learn as you get the same reward if you solve the maze in 10 or 1,000 steps.  

Efficient solutions can be encoraged by providing -1 rewards for each action that does not result in the maze being completed.  In this case the model will learn to complete the maze as efficiently as possible to minimize the penalty.

The assumptions of $\gamma$ in $G_t = \gamma^{T-t-1}$ are analagous.   

The same idea when $\gamma$ = 1
| episode length | return |
|---|---|
| 10 steps | −1 |
| 100 steps | −1 |

When $\gamma$ = 1, say .9:
| episode length | return |
|---|---|
| 10 steps | $-0.9^9 \approx +0.387$ |
| 100 steps | $-0.9^{99} \approx +0.000026$ |  

So in this case the weak signal is pushing for fewer steps as the reward at the end is +1.

## Ex 3.8

$T = 5$

$R_1 = -1$, $R_2 = 2$, $R_3 = 6$, $R_4 = 3$, $R_5 = 2$

Return definition:

$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \gamma^3 R_{t+4} + \dots$

with $\gamma = 0.5$

---

$G_5 = 0$

$G_4 = R_5 = 2$

$G_3 = R_4 + \gamma R_5  
= 3 + 0.5(2)  
= 4$

$G_2 = R_3 + \gamma R_4 + \gamma^2 R_5  
= 6 + 0.5(3) + 0.25(2)  
= 8$

$G_1 = R_2 + \gamma R_3 + \gamma^2 R_4 + \gamma^3 R_5  
= 2 + 0.5(6) + 0.25(3) + 0.125(2)  
= 6$

## Ex 3.9

Suppose $\gamma = 0.9$ and the reward sequence is

$R_1 = 2$, and then $R_2 = R_3 = R_4 = \dots = 7$

We use

$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots
$

**Compute $G_1$**

Since all rewards after time 1 are 7,

$
G_1 = 7 + 0.9(7) + 0.9^2(7) + 0.9^3(7) + \dots
$

$
G_1 = 7 \sum_{k=0}^{\infty} (0.9)^k
$

Using the geometric series formula,

$
\sum_{k=0}^{\infty} \gamma^k = \frac{1}{1-\gamma}
$

we get

$
G_1 = \frac{7}{1-0.9} = \frac{7}{0.1} = 70
$

**Compute $G_0$**

$
G_0 = R_1 + \gamma G_1
$

$
G_0 = 2 + 0.9(70)
$

$
G_0 = 2 + 63 = 65
$

**Final Answer**

$
G_1 = 70
$

$
G_0 = 65
$

## Ex 3.10

Suppose the reward at every future step is at most $1$. Then the largest possible return is

$G_t = \sum_{k=0}^{\infty} \gamma^k = 1 + \gamma + \gamma^2 + \gamma^3 + \dots$

with $0 < \gamma < 1$.

To show this is finite, let

$S_n = \sum_{k=0}^{n} \gamma^k = 1 + \gamma + \gamma^2 + \dots + \gamma^n$.

Multiply by $\gamma$:

$\gamma S_n = \gamma + \gamma^2 + \dots + \gamma^{n+1}$.

Subtract:

$S_n - \gamma S_n = 1 - \gamma^{n+1}$

so

$S_n(1-\gamma) = 1 - \gamma^{n+1}$

and therefore

$S_n = \frac{1-\gamma^{n+1}}{1-\gamma}$.

Now take the limit as $n \to \infty$. Since $0 < \gamma < 1$, we have $\gamma^{n+1} \to 0$. Hence

$\sum_{k=0}^{\infty} \gamma^k = \frac{1}{1-\gamma}$.

Therefore,

$G_t \leq \frac{1}{1-\gamma}$.

So the discounted return is finite whenever $0 < \gamma < 1$..

## Ex 3.11

Here is the full solution.

We start with Equation 3.2 from Sutton and Barto, which defines the environment dynamics:

$p(s', r \mid s, a) = \Pr\{S_t = s', R_t = r \mid S_{t-1}=s, A_{t-1}=a\}$

This is the **joint distribution** of the next state and reward, conditioned on the current state and action.

__Step 1:__ Use the law of total expectations to get the expectaion of the joint distribution

If the state $s$ and action $a$ are fixed, then the expected immediate reward is just the weighted average over all possible next states $s'$ and rewards $r$:

$\mathbb{E}[R_t \mid s,a] = \sum_{s'} \sum_r r \, p(s', r \mid s,a)$  

This comes directly from the definition of expectation over the joint distribution in Equation 3.2 and is Equation 3.5.

__Step 2:__ 

$\pi(a \mid s) = \Pr\{A_t = a \mid S_t = s\}$


To compute the expected immediate reward given only the state $s$, we average over all actions the policy might choose:
$P(A) = P(A|B)*P(B)$

$\mathbb{E}[R_t \mid s] = \sum_a \pi(a \mid s)\,\mathbb{E}[R_t \mid s,a]$

$\mathbb{E}[R_t \mid s] = \sum_a \pi(a \mid s)\left(\sum_{s'} \sum_r r \, p(s', r \mid s,a)\right)$

$\mathbb{E}[R_t \mid s] = \sum_a \sum_{s'} \sum_r \pi(a \mid s)\, r \, p(s', r \mid s,a)$

__Intuition:__ 
The policy $(\pi(a|s))$ gives the distribution actions allowed in the current state.  Eqation 3.2 $(p(s', r|s, a))$ gives us the join distribtion of the next state and reward given the current state and actions.

For each state $s$ and given action $a$,  we know the total probablitiy of $s', r$ and from that we calculate the Expectation $\mathbb{E}[R_t \mid s, a]$ (equation 3.5).  This is the weighted average of rewards over all $(s', r)$ outcomes.

The policy $\pi(a \mid s)$ gives the distribution of actions given states.  So we get $\mathbb{E}[R_t \mid s]$ by calculating the weighted average of $\mathbb{E}[R_t \mid s, a]$ over all actions $a$ available from the current state $s$.  

## Exercise 3.12 / 3.13 style derivations

### Law of total expectations (Review) 
Start with the **law of total expectation**

$E[X] = E[E[X|Y]]$

Define a function

$g(Y) = E[X|Y]$

This means the conditional expectation is a **random variable** that depends on the value of $Y$.

Example:

$g(Y) = \{3 \text{ if } Y = 0,\; 9 \text{ if } Y = 1\}$

For a specific value of $Y$:

$g(Y = y) = E[X|Y = y]$

Thus the overall expectation can be written

$E[X] = E[g(Y)]$

If $Y$ is discrete, this becomes

$E[X] = \sum_{y \in Y} P(Y = y)\, g(Y = y)$

or equivalently

$E[X] = \sum_{y \in Y} P(Y = y)\, E[X|Y = y]$

### Intuition

1. Compute the expected value of $X$ for each possible value of $Y$.
2. Weight those expectations by the probability of each $Y$.
3. Sum the weighted values to obtain $E[X]$.

### Conditional Law of Total Expectation Review

The same idea extends when we condition on another random variable $Z$.

$E[X|Z] = E[E[X|Y,Z] \mid Z]$

Define

$g(Y,Z) = E[X|Y,Z]$

Then

$E[X|Z] = E[g(Y,Z) \mid Z]$

This means we are applying the **same law of total expectation**, but **within the world where $Z$ is already known**.

If $Y$ is discrete, then for a particular value $Z=z$:

$E[X|Z=z] = \sum_{y \in Y} P(Y=y \mid Z=z)\, E[X|Y=y, Z=z]$

### Intuition

1. First fix $Z=z$ (we are working in the subset of outcomes where $Z=z$).
2. Partition that subset by the possible values of $Y$.
3. Compute $E[X|Y=y, Z=z]$ for each $y$.
4. Weight those expectations by $P(Y=y|Z=z)$.

So we **do not add another layer of summation**.  
Instead, we apply the same weighted averaging process, but using the **conditional distribution $P(Y|Z)$** rather than $P(Y)$.

Conceptually, this is just the law of total expectation applied **inside the conditional world defined by $Z$**.

### End Review

### 3.12
$v_\pi(s) = \sum_a \pi(a \mid s)\, q_\pi(s,a)$

$q_\pi(s,a) = \sum_{s',r} p(s', r \mid s,a)\,[\,r + \gamma v_\pi(s')\,]$

---

$\mathbb{E}[G_t \mid S_t = s]$

$= \mathbb{E}\!\left[\mathbb{E}[G_t \mid S_t = s, A_t] \mid S_t = s\right]$

$= \sum_a p(A_t = a \mid S_t = s)\, \mathbb{E}[G_t \mid S_t = s, A_t = a]$

$= \sum_a \pi(a \mid s)\, \mathbb{E}[G_t \mid S_t = s, A_t = a]$

$= \sum_a \pi(a \mid s)\, q_\pi(s,a)$

### 3.13

$q_\pi(s,a) = \mathbb{E}[G_t \mid S_t = s, A_t = a]$

$G_t = R_{t+1} + \gamma G_{t+1}$

$v_\pi(s') = \mathbb{E}[G_{t+1} \mid S_{t+1} = s']$

$p(s', r \mid s,a) = \Pr{S_{t+1} = s', R_{t+1} = r \mid S_t = s, A_t = a}$

---

$q_\pi(s,a) = \mathbb{E}[G_t \mid S_t = s, A_t = a]$

$= \mathbb{E}[R_{t+1} + \gamma G_{t+1} \mid S_t = s, A_t = a]$

$= \mathbb{E}\!\left[\mathbb{E}[R_{t+1} + \gamma G_{t+1} \mid S_t = s, A_t = a, S_{t+1}, R_{t+1}] \mid S_t = s, A_t = a\right]$  
By Law of conditional total expectation.  Conditioning on $S_{t+1}, R_{t+1}$.

$= \sum_{s',r} p(s', r \mid s,a)\,\mathbb{E}[R_{t+1} + \gamma G_{t+1} \mid S_t = s, A_t = a, S_{t+1} = s', R_{t+1} = r]$

$= \sum_{s',r} p(s',r \mid s,a) \left[\mathbb{E}[R_{t+1} \mid S_t=s, A_t=a, S_{t+1}=s', R_{t+1}] + \mathbb{E}[\gamma G_{t+1} \mid S_t=s, A_t=a, S_{t+1}=s', R_{t+1}=r]\right]$

$= \sum_{s',r} p(s',r \mid s,a) \left[r + \gamma \mathbb{E}[G_{t+1} \mid S_t=s, A_t=a, S_{t+1}=s', R_{t+1}=r]\right]$

$= \sum_{s',r} p(s', r \mid s,a), \left[r + \gamma \mathbb{E}[G_{t+1} \mid S_{t+1} = s']\right]$

$= \sum_{s',r} p(s', r \mid s,a), \left[r + \gamma v_\pi(s')\right]$

$q_\pi(s,a) = \sum_{s',r} p(s', r \mid s,a), \left[r + \gamma v_\pi(s')\right]$

### END


### Final equations

The two equations are:

$v_\pi(s) = \mathbb{E}_\pi[q_\pi(s,A_t) \mid S_t=s]$

$v_\pi(s) = \sum_a \pi(a \mid s)\, q_\pi(s,a)$

and

$q_\pi(s,a) = \mathbb{E}[R_{t+1} + \gamma v_\pi(S_{t+1}) \mid S_t=s, A_t=a]$

$q_\pi(s,a) = \sum_{s',r} p(s', r \mid s,a)\,\big[r + \gamma v_\pi(s')\big]$

### Intuition

The first equation says:

- the value of a state is the average value of the actions available there,
- weighted by how likely the policy is to choose each action.

The second equation says:

- the value of an action is the expected immediate reward, $r$, plus the discounted value of the next state it leads to ($v_\pi(s')$ discounted by $\gamma$).
- Action values are then averaged (weighted) over the probability of each next state/reward $(p(s', r \mid s,a))$
  
## Ex 3.14

For a fixed policy, the Bellman expectation equation is

$v_\pi(s) = \sum_a \pi(a \mid s)\sum_{s',r} p(s', r \mid s,a)\,[r + \gamma v_\pi(s')]$.

In this gridworld, the dynamics are deterministic except for the random action choice.  
This because in this case, moving results in one new state and on reward.  so this simplifies to:

$v(s) = \sum_a \pi(a \mid s)\,[r(s,a) + \gamma v(s'(s,a))]$.

Because the policy is equiprobable,

$\pi(a \mid s) = \frac{1}{4}$,

so every cell gets an equation of the form

$v(s) = \frac{1}{4}\sum_{a \in \{\text{up, down, left, right}\}} [r(s,a) + 0.9\,v(s'(s,a))]$.

In the case of the center cell:  

$u = 1/4*[(0 + .9*.4) + (0 +.9*-.4) + (0 + .9*.7) + (0 + .9*2.3)]$   
$u = 1/4*.9*(.7 -.4 + .4 + 2.3) \approx .7$  

In the case of the top left cell:
$u = 1/4*[(-1 + .9*3.3) + (-1 +.9*3.3) + (0 + .9*8.8) + (0 + .9*1.5)] \approx 3.3$  

## Ex. 3.17

Start with

$q_\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a]$

Then expand one step:

$q_\pi(s,a) = \mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} \mid S_t=s, A_t=a]$

Conditioning on the next state, reward, and next action gives:

$q_\pi(s,a) = \sum_{s',r} p(s',r \mid s,a)\left[r + \gamma \sum_{a'} \pi(a' \mid s') q_\pi(s',a')\right]$

## Exercise 3.18

The value of a state is the expected value of the actions available in that state under policy $\pi$.

$ v_\pi(s) = \mathbb{E}_\pi[q_\pi(s,A_t)\mid S_t=s] $

Equivalently,

$ v_\pi(s) = \sum_a \pi(a\mid s)\, q_\pi(s,a) $