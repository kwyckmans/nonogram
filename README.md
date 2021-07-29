# Commandline nonograms

## Running the program

## References

I initially found the following two papers along with an implementation. Since they seemed to produce nice results I initially started by implementing these. Unfortunately they are pretty sparse on implementation details and the translation to code was, unfortunately, quite hard.

- [Solving nonograms by combining relaxations - K.J. Batenburg](https://homepages.cwi.nl/~kbatenbu/papers/bako_pr_2009.pdf)
- [Constructing simple nonograms of varying difficulty](https://liacs.leidenuniv.nl/~kosterswa/constru.pdf)
- [Open source implementation of the above two papers in C++](https://github.com/attilaszia/nonogram/tree/dca0836629295371b9931d50db48e71771946d13)

Some cursory searching on the internet leads to solving these using DFS, optimise by starting with the most constrained row.

- [Solving nonograms according to stack overflow](https://stackoverflow.com/questions/813366/solving-nonograms-picross)
