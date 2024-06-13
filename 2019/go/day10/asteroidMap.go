package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strings"
)

func main() {
	fmt.Println("")
	file, err := os.Open("input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	asteroidMap := make([][]string, 0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := arrayFrom(scanner.Text())
		asteroidMap = append(asteroidMap, line)
	}

	maxAsteroids := 0
	curry := 0
	currx := -1
	curry, currx = getNextAsteroid(currx, curry, asteroidMap)
	var targets map[float64]Location
	for currx > -1 && curry > -1 {
		thesetargets, firsthalf := searchForAsteroids(currx, curry, asteroidMap)
		if (firsthalf) > maxAsteroids {
			fmt.Println("MOST SEEN: ", currx, ",", curry)
			maxAsteroids = firsthalf
			targets = thesetargets
		}
		curry, currx = getNextAsteroid(currx, curry, asteroidMap)
	}
	fmt.Println("maxAsteroids: ", maxAsteroids)

	drawMap(asteroidMap)
	asteroidMap, _ = shootAsteroids(0, asteroidMap, targets)
	drawMap(asteroidMap)
}

func shootAsteroids(count int, asteroidMap [][]string, targets map[float64]Location) ([][]string, int) {
	keys := make([]float64, 0)
	for an, _ := range targets {
		keys = append(keys, an)
	}
	sort.Float64s(keys)
	for _, k := range keys {
		t := targets[k]
		asteroidMap[t.y][t.x] = "."
		count++
		fmt.Println(k, ":: nr", count, ": ", t.x, ",", t.y)
	}
	return asteroidMap, count
}

func drawMap(asteroidMap [][]string) {
	for y := 0; y < len(asteroidMap); y++ {
		for x := 0; x < len(asteroidMap[y]); x++ {
			if asteroidMap[y][x] == "#" {
				print("#")
			} else {
				print(".")
			}
		}
		fmt.Println("")
	}
}

func searchForAsteroids(currx int, curry int, asteroidMap [][]string) (map[float64]Location, int) {
	fmt.Println("[", curry, ",", currx, "]")
	rayMap := make(map[float64]Location)
	thisMax := 0

	for y := 0; y < len(asteroidMap); y++ {
		for x := 0; x < len(asteroidMap[y]); x++ {
			if asteroidMap[y][x] == "#" {
				if getDistance(currx, curry, x, y) == 0 {
					continue
				}
				angle := getAngle(x, y, currx, curry)
				if _, ok := rayMap[angle]; !ok {
					rayMap[angle] = Location{x: x, y: y}
					thisMax++
				} else {
					rm := rayMap[angle]
					if getDistance(currx, curry, rm.x, rm.y) > getDistance(currx, curry, x, y) {
						rayMap[angle] = Location{x: x, y: y}
					}
				}
			}
		}
	}
	return rayMap, thisMax
}

func getAngle(x int, y int, x2 int, y2 int) float64 {
	angle := math.Atan2(float64(x-x2), float64(y-y2)) * 180 / math.Pi
	if angle < 0 {
		angle += 360
	}
	return angle
}

func getDistance(x int, y int, x2 int, y2 int) int {
	retX := x - x2
	if retX < 0 {
		retX = retX * -1
	}
	retY := y - y2
	if retY < 0 {
		retY = retY * -1
	}
	return retY + retX
}

func getNextAsteroid(startx int, starty int, asteroidMap [][]string) (currx int, curry int) {
	for y := starty; y < len(asteroidMap); y++ {
		for x := startx + 1; x < len(asteroidMap[y]); x++ {
			if asteroidMap[y][x] == "#" {
				return y, x
			}
		}
		startx = 0
	}
	return -1, -1
}

type Location struct {
	x int
	y int
}

func arrayFrom(data string) []string {
	tmp := strings.Split(data, "")
	memory := make([]string, 0, len(tmp))
	for _, ch := range tmp {
		memory = append(memory, ch)
	}
	return memory
}
