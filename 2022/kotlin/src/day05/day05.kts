import java.io.File

enum class Method(val method: Int) {
    ONE_BY_ONE(1),
    ALL(2);
}

fun doMoves(stacks: List<List<String>>, moves: List<String>, method: Method): String {
    val mutableStacks = stacks.map{it.map{it}}.toMutableList()
    moves
        .forEach {
            val amount = it.split(" ")[1].toInt()
            val fromStack = it.split(" ")[3].toInt() - 1
            val toStack = it.split(" ")[5].toInt() - 1
            val crates = mutableStacks[fromStack].slice(0..amount-1)
            mutableStacks[fromStack] = mutableStacks[fromStack]
                .slice(amount..mutableStacks[fromStack].size - 1)
            if (method == Method.ONE_BY_ONE) {
                mutableStacks[toStack] = (
                    crates.reversed() + mutableStacks[toStack]
                )
            }
            if (method == Method.ALL) {
                mutableStacks[toStack] = crates + mutableStacks[toStack]
            }
        }
    return mutableStacks.map {it[0]}.joinToString("")
}

val lines = File("src/day05/input")
    .readText()
    .split("\n")
    .filter { it != ""}

val moves = lines.slice(9..lines.size - 1)
val stacks = (1..9*4 step 4).toList().reversed()
    .map { stack ->
        (0..7)
            .toList()
            .reversed()
            .map { crate -> lines[crate][stack].toString()}
            .filter { it != " "}
            .reversed()
    }
    .reversed()

println("Part 1: ${doMoves(stacks, moves, Method.ONE_BY_ONE)}")
println("Part 2: ${doMoves(stacks, moves, Method.ALL)}")
