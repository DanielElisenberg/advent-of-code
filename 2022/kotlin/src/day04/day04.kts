import java.io.File


val pairs = File("src/day04/input")
    .readLines()
    .map { line ->
        line.split(",").map { elf ->
            (elf.split("-")[0].toInt()..elf.split("-")[1].toInt()).toList()
        }
    }

val totalOverlapCount = pairs
    .filter { pair ->
        pair[0].containsAll(pair[1]) || pair[1].containsAll(pair[0])
    }
    .size
println("Part 1: $totalOverlapCount")

val overlapCount = pairs
    .filter { pair ->
        (pair[0] intersect pair[1]).size > 0
    }
    .size
println("Part 2: $overlapCount")
