import java.io.File


val rules: Map<String, Int> = mapOf(
    "A X" to 3 + 1,
    "B Y" to 3 + 2,
    "C Z" to 3 + 3,
    "A Y" to 6 + 2,
    "A Z" to 0 + 3,
    "B X" to 0 + 1,
    "B Z" to 6 + 3,
    "C X" to 6 + 1,
    "C Y" to 0 + 2
)

val newRules: Map<String, Int> = mapOf(
    "A X" to 0 + 3,
    "B Y" to 3 + 2,
    "C Z" to 6 + 1,
    "A Y" to 3 + 1,
    "A Z" to 6 + 2,
    "B X" to 0 + 1,
    "B Z" to 6 + 3,
    "C X" to 0 + 2,
    "C Y" to 3 + 3
)

val strategyGuide = File("src/day02/input").readLines()
println("Part 1: ${strategyGuide.map { rules.getOrDefault(it, 0) }.sum()}")
println("Part 2: ${strategyGuide.map { newRules.getOrDefault(it, 0) }.sum()}")