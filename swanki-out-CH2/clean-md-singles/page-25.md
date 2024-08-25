indeed possess useful properties. Consider a random variable $x$ having eight possible states, each of which is equally likely. To communicate the value of $x$ to a receiver, we would need to transmit a message of length 3 bits. Notice that the entropy of this variable is given by

$$
\mathrm{H}[x]=-8 \times \frac{1}{8} \log _{2} \frac{1}{8}=3 \text { bits. }
$$

Now consider an example (Cover and Thomas, 1991) of a variable having eight possible states $\{a, b, c, d, e, f, g, h\}$ for which the respective probabilities are given by $\left(\frac{1}{2}, \frac{1}{4}, \frac{1}{8}, \frac{1}{16}, \frac{1}{64}, \frac{1}{64}, \frac{1}{64}, \frac{1}{64}\right)$. The entropy in this case is given by

$$
\mathrm{H}[x]=-\frac{1}{2} \log _{2} \frac{1}{2}-\frac{1}{4} \log _{2} \frac{1}{4}-\frac{1}{8} \log _{2} \frac{1}{8}-\frac{1}{16} \log _{2} \frac{1}{16}-\frac{4}{64} \log _{2} \frac{1}{64}=2 \text { bits. }
$$

We see that the nonuniform distribution has a smaller entropy than the uniform one, and we will gain some insight into this shortly when we discuss the interpretation of entropy in terms of disorder. For the moment, let us consider how we would transmit the identity of the variable's state to a receiver. We could do this, as before, using a 3-bit number. However, we can take advantage of the nonuniform distribution by using shorter codes for the more probable events, at the expense of longer codes for the less probable events, in the hope of getting a shorter average code length. This can be done by representing the states $\{a, b, c, d, e, f, g, h\}$ using, for instance, the following set of code strings: $0,10,110,1110,111100,111101,111110$, and 111111. The average length of the code that has to be transmitted is then

average code length $=\frac{1}{2} \times 1+\frac{1}{4} \times 2+\frac{1}{8} \times 3+\frac{1}{16} \times 4+4 \times \frac{1}{64} \times 6=2$ bits,

which again is the same as the entropy of the random variable. Note that shorter code strings cannot be used because it must be possible to disambiguate a concatenation of such strings into its component parts. For instance, 11001110 decodes uniquely into the state sequence $c, a, d$. This relation between entropy and shortest coding length is a general one. The noiseless coding theorem (Shannon, 1948) states that the entropy is a lower bound on the number of bits needed to transmit the state of a random variable.

From now on, we will switch to the use of natural logarithms in defining entropy, as this will provide a more convenient link with ideas elsewhere in this book. In this case, the entropy is measured in units of nats (from 'natural logarithm') instead of bits, which differ simply by a factor of $\ln 2$.

\title{
2.5.2 Physics perspective
}

We have introduced the concept of entropy in terms of the average amount of information needed to specify the state of a random variable. In fact, the concept of entropy has much earlier origins in physics where it was introduced in the context of equilibrium thermodynamics and later given a deeper interpretation as a measure of disorder through developments in statistical mechanics. We can understand this alternative view of entropy by considering a set of $N$ identical objects that are to be divided amongst a set of bins, such that there are $n_{i}$ objects in the $i$ th bin. Consider