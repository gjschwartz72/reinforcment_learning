# Chapter 3 Equation Cheat Sheet

**Environment dynamics (3.2)**  
$p(s', r \mid s, a) \doteq \Pr\{S_t = s', R_t = r \mid S_{t-1} = s, A_{t-1} = a\}$  
A.K.A, the trantional probability that really defines the MDP.  

**Expected reward function (3.5)**  
$r(s,a) \doteq \mathbb{E}[R_t \mid S_{t-1} = s, A_{t-1} = a] = \sum_{r \in \mathcal{R}} r \sum_{s' \in \mathcal{S}} p(s', r \mid s, a)$

**Expected reward given state, action, next state (3.6)**  
$r(s,a,s') \doteq \mathbb{E}[R_t \mid S_{t-1} = s, A_{t-1} = a, S_t = s'] = \sum_{r \in \mathcal{R}} r \frac{p(s', r \mid s, a)}{p(s' \mid s,a)}$

Note: using $p(A,B) = p(A|B)p(A)$.  In this case $p(A,B)$ is a conditional joint distribution $(p(s', r \mid s, a))$  
$p(s', r \mid s, a) = p(r \mid s, a, s')p(s' \mid s, a)$   
$p(r \mid s, a, s') = \frac{p(s', r \mid s, a)}{p(s' \mid s,a)}$

**Return (3.8)**  
$G_t \doteq R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$  
$G_t = R_{t+1} + \gamma G_{t+1}$

---

**Definition of policy**  
$\pi(a \mid s) \doteq \Pr(A_t = a \mid S_t = s)$  
The probability distribution of all actions given the state.  

**State-value function (expected value given state) (3.12)**  
$v_\pi(s) \doteq \mathbb{E}_\pi[G_t \mid S_t = s], \quad \text{for all } s \in \mathcal{S}$  
$v_\pi(s) = \mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} \mid S_t = s], \quad \text{for all } s \in \mathcal{S}$  

Expected return given you are in state $s$ and follow policy $\pi$  
$v_\pi(s)$ is the expected value from state s.
Calculated by averaging action values, $q_{\pi}(s,a)$, of all actions in policy $\pi$

**Action-value function (3.13)**  
$q_\pi(s,a) \doteq \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a], \quad \text{for all } s \in \mathcal{S}, \ a \in \mathcal{A}(s)$
$q_\pi(s,a)$ is the expected value from a state-action pair. 

**Bellman expectation equation for $q_\pi$ (3.13)**  
$q_\pi(s,a) \doteq \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a]$  
$q_\pi(s,a) = \mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} \mid S_t = s, A_t = a]$  
$q_\pi(s,a) = \sum_{s',r} p(s', r \mid s, a)\left[r + \gamma \sum_{a'} \pi(a' \mid s') q_\pi(s',a')\right]$  
$q_\pi(s,a) = \sum_{s',r} p(s', r \mid s,a)\left[r + \gamma v_\pi(s')\right]$ (as $v_\pi(s) = \sum_{a} \pi(a \mid s) q_\pi(s,a)$ )


**Bellman equation for $v_\pi$ — full 4-line derivation (3.14)**  
$v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$

$\quad = \mathbb{E}*\pi[R*{t+1} + \gamma G_{t+1} \mid S_t = s]$

$\quad = \sum_{a} \pi(a \mid s) \sum_{s',r} p(s', r \mid s,a)\left[r + \gamma \mathbb{E}*\pi[G*{t+1} \mid S_{t+1} = s']\right]$

$\quad = \sum_{a} \pi(a \mid s) \sum_{s',r} p(s', r \mid s,a)\left[r + \gamma v_\pi(s')\right]$

**Relationship between $v_\pi$ and $q_\pi$ ()**  
$v_\pi(s) = \sum_{a} \pi(a \mid s) q_\pi(s,a)$  
Substitue into   $\sum_{s',r} p(s', r \mid s,a)\left[r + \gamma v_\pi(s')\right]$  
to get  $q_\pi(s,a) = \sum_{s',r} p(s', r \mid s, a)\left[r + \gamma \sum_{a'} \pi(a' \mid s') q_\pi(s',a')\right]$  
  
$\therefore \quad \sum_{s',r} p(s', r \mid s, a)\left[r + \gamma \sum_{a'} \pi(a' \mid s') q_\pi(s',a')\right] \equiv \sum_{s',r} p(s', r \mid s,a)\left[r + \gamma v_\pi(s')\right]$ 
  
This makes sense as 3.13 is telling us to use $\sum_{a} \pi(a \mid s) q_\pi(s,a)$   to get the value of the next action.

---

**Optimal Policies and Optimal Value Functions**  
$v_*(s) \doteq max(v_{\pi}(s)  \quad\quad$ Optimal State Value function  
$q_*(s, a) \doteq max(q_\pi(s,a)) \quad$ Optimal Action-Value function 

$v_*(s) = max_a(q_*(s,a))$  
$\qquad = \max_a \sum_{s',r} p(s', r \mid s, a)\big[ r + \gamma v^*(s') \big] \qquad$  (3.19)  
$v_*(s)$ is the maximum value obtainable given the state (and the model).  
The $\max_a$ is taken over all q_*(s,a), or over each of sums in 3.19

$q_\pi(s,a) = \mathbb{E}_\pi[R_{t+1} + \gamma v(S_{t+1}) \mid S_t = s, A_t = a]$   
$q_*(s,a) = \mathbb{E}[R_{t+1} + \gamma v_*(S_{t+1}) \mid S_t = s, A_t = a]$   
$\qquad = \sum_{s',r} p(s', r \mid s, a)\big[ r + \gamma \max_{a'} q^*(s', a') \big] \quad$ (3.20)  
For each action $a$ as state $s$:  
$\quad$ compute its expected value by taking a probability-weighted average over all possible next states and rewards.  
$\quad$ Each outcome contributes its immediate reward plus the discounted optimal future value.  
$\quad$ Then, select the maximum of these values over all actions.

$\quad$ Each action produces a weighted average → then we take the max over those averages.

