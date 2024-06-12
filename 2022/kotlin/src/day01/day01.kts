import java.io.File


val carriedCalories = File("src/day01/input")
    .readText()
    .split("\n\n")
    .map { group -> group.split("\n").filter{it != ""}.map{it.toInt()}.sum() }
    .sorted()
    .reversed()

println("Part 1: ${carriedCalories[0]}")
println("Part 2: ${carriedCalories.slice(0..2).sum()}")
