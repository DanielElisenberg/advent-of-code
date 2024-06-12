import java.io.File


val rucksacks = File("src/day03/input").readLines().map {it.toList()}
val characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
val numericValueOf = characters
    .mapIndexed {index, character ->
        character to index +1
    }
    .toMap()

val misplacedItems = rucksacks
    .map { rucksack ->
        val c1 = rucksack.slice(0..rucksack.size/2-1)
        val c2 = rucksack.slice(rucksack.size/2..rucksack.size-1)
        numericValueOf.getOrDefault((c1 intersect c2).first(), 0)
    }
    .sum()
println("Part 1: $misplacedItems")

val badges = rucksacks
    .mapIndexedNotNull { index, rucksack ->
        if (index % 3 != 0) {
            null
        } else {
            val r1 = rucksack
            val r2 = rucksacks[index + 1]
            val r3 = rucksacks[index + 2]
            numericValueOf.getOrDefault(
                (r1 intersect r2 intersect r3).first(), 0
            )
        }
    }
    .sum()
println("Part 2: $badges")
