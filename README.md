# SAT-DependencyAnalysis

## Dependency decision problem

Dependencies between packages can be easily modeled using propositional logic. For instance, package A depends on package B and package C can be expressed by the logical formula A → B ∧ C which in turn can be expressed by the two clauses A → B and A → C (or ¬A ∨ B and ¬A ∨ C). If all the dependencies are requirements of a conjunctive form, even if incompatibilities between packages are expressed, the resulting SAT problem is made of Horn clauses, i.e. clauses containing at most one positive literal, thus is solvable in linear time.

The dependency problem becomes interesting when a given feature can be provided by several artifacts: the same feature is provided by different packages, depending on their origin. For example to install latex in a linux distribution, one can use for instance texlive-latex or tetex-latex. In that case, we would express such dependency by something like latex → texlive latex ∨ tetex latex which is no longer a Horn clause. Thus the dependency problem becomes NP-complete.

## Further exploration

The dependency problem is often underconstrained, which means that there is usually a lot of possible solutions. And not all those solutions are usually equally good. For Linux distributions for instance, one could take into account the number of packages to install, or their size, etc in order to propose an installation with the minimum number of packages or an installation with the smallest footprint on the hard drive. Those criteria can be easily modeled in an optimization framework by an objective function to minimize, (we can use genetic algorithms here).

## Output

[+] To install libgssapi-krb5-2 <br>
[..] Checking dependencies.. <br>
c Building data structures in 0.00s <br>
c Ready to go with 41 variables and 10 clauses <br>
[*] Package can be installed? True <br>
