# An-asynchronous-computations-in-a-synchronous-control
This project is to investigate how to realize an asynchronous computations in a synchronous control.

The synchronous baseline control is described as follows:
1. There is a stream of transactions queueing and processed into a block.
2. Each transaction is considered to be comprised of equal-sized slots.
3. A bulk of transactions is to be processed in a batch such that a batch of transactions is to be processed as soon as total n number of slots
from a certain number of transactions together is queued into a block, which is, namely, the synchronous control of concern in tis assignment.
4. Note that for simplicity it is assumed that any transaction that is
in excessive size in slots to overflow the capacity of a block, is
to be cut to be accommodated just to fit n.

# Problem #1.
Find the probability, P(i) (e.g., Sum_{i=0}^{n}(P(i)) = 1.0) of the synchronous control to have i number
of slots in the block at equilibrium. Note that the equilibrium state means
the calculated P(i) stays in balance without changing along the maximum
number of slots n but i. The arrival rate of transactions at the block is lambda (e.g., 1/microsecond)
and the service rate mu (e.g., 2/microsecond), and lambda/mu <= 1.0 is assumed.

# Problem #2.
Based on the P(i) from Problem #1, find P(i) when the size of the block (i.e., n) is adaptive.
In other words, find the normalized P(i) to track the adaptive block size.
This P(i) should clearly justify and distinguish itself from the P(i) in #1.
Test and verify your P(i)'s and Sigma(P(i)) = 1.0 for the validity, and plot the appropriate graphs.

# Problem #3.
Ultimately, find P(i) that could realize a pseudo asynchronous block processing.
In other words, each transaction will be posted as nearly soon as executed
than just being posted at the whole block synchronization.
Test and verify your P(i)'s and Sigma(P(i)) = 1.0 for the validity, and plot the appropriate graphs.


