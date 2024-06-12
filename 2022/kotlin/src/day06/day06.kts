import java.io.File


val datastream = File("src/day06/input").readText().toList()

val startOfPacket = datastream
    .windowed(4)
    .mapIndexedNotNull {index, window ->
        if ( window.distinct().size == 4 ) index + 4 else null
    }
    .first()
println("Part 1: $startOfPacket")

val startOfMessage = datastream
    .windowed(14)
    .mapIndexedNotNull {index, window ->
        if ( window.distinct().size == 14 ) index + 14 else null
    }
    .first()
println("Part 2: $startOfMessage")