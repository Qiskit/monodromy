from monodromy.circuits import *
from monodromy.coverage import *
from monodromy.examples import *
import monodromy.render

operations = [
    GatePolytope(
        convex_subpolytopes=thirdCX_polytope.convex_subpolytopes,
        cost=Fraction(1, 3),
        operations=["thirdCX"],
    ),
    GatePolytope(
        convex_subpolytopes=sqrtCX_polytope.convex_subpolytopes,
        cost=Fraction(1, 2),
        operations=["sqrtCX"],
    ),
]

# build the set of covering polytopes
print("==== Working to build a set of covering polytopes ====")
coverage_set = build_coverage_set(operations, chatty=True)

# print it out for user inspection
print("==== Done. Here's what we found: ====")
print_coverage_set(coverage_set)

# flex the rendering code
print("==== Render these in Mathematica: =====")
print(monodromy.render.polytopes_to_mathematica(coverage_set))

# use coverage_set to perform a gate decomposition
alcove_coordinate = [Fraction(3, 8), Fraction(-1, 8), Fraction(-1, 8)]
point_polytope = exactly(*alcove_coordinate)
decomposition = decomposition_hops(coverage_set, operations, point_polytope)
qc = xx_circuit_from_decomposition(
    decomposition, operations
)

# print the circuit for the user to marvel at
print("The following circuit implements the canonical gate at "
      f"{[str(x) for x in alcove_coordinate]}: ", end="")
print((abs(qiskit.quantum_info.Operator(qc).data -
           canonical_matrix(*alcove_to_positive_canonical_coordinate(*alcove_coordinate)))
       < 0.01).all())

print(qc)

