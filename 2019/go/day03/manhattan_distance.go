package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func main() {
	file, err := os.Open("input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	instructions := scanner.Text()
	fmt.Println(len(instructions))
	path := createPath(instructions)
	scanner.Scan()
	instructions2 := scanner.Text()
	path2 := createPath(instructions2)
	var shortsteps int64 = 100000000
	for i, point := range path {
		for j, point2 := range path2 {
			if point.x == point2.x && point.y == point2.y {
				fmt.Println(i, ":", j, "-match")
				fmt.Println("path:  ", point)
				fmt.Println("path2: ", point2)
				stepamount := point.steps + point2.steps
				if stepamount < shortsteps {
					shortsteps = stepamount
					fmt.Println("new shortest: ", shortsteps)
				}
			}
		}
	}
}

func shortestDistance(path []Location, instructions string) int {
	instructionSet := strings.Split(instructions, ",")
	currentLocation := Location{x: 0, y: 0, steps: 0}
	var shortestSteps int64 = 10000000
	var currsteps int64 = 0

	for _, inst := range instructionSet {
		switch inst[0:1] {
		case "U":
			dist, err := strconv.Atoi(inst[1:len(inst)])
			if err == nil {
				for i := 0; i < dist; i++ {
					currsteps += 1
					currentLocation.x += 1
					iter, found := find(path, currentLocation)
					if found {
						length := path[iter].steps + currsteps
						fmt.Println("length: ", length)
						fmt.Println(path[iter], "==", currentLocation)
						if length < shortestSteps {
							shortestSteps = length
						}
					}
				}
			}
		case "D":
			dist, err := strconv.Atoi(inst[1:len(inst)])
			if err == nil {
				for i := 0; i < dist; i++ {
					currsteps += 1
					currentLocation.x += -1
					iter, found := find(path, currentLocation)
					if found {
						length := path[iter].steps + currsteps
						fmt.Println("length: ", length)
						fmt.Println(path[iter], "==", currentLocation)
						if length < shortestSteps {
							shortestSteps = length
						}
					}
				}
			}
		case "L":
			dist, err := strconv.Atoi(inst[1:len(inst)])
			if err == nil {
				for i := 0; i < dist; i++ {
					currsteps += 1
					currentLocation.y += -1
					iter, found := find(path, currentLocation)
					if found {
						length := path[iter].steps + currsteps
						fmt.Println("length: ", length)
						fmt.Println(path[iter], "==", currentLocation)
						if length < shortestSteps {
							shortestSteps = length
						}
					}
				}
			}
		case "R":
			dist, err := strconv.Atoi(inst[1:len(inst)])
			if err == nil {
				for i := 0; i < dist; i++ {
					currsteps += 1
					currentLocation.y += 1
					iter, found := find(path, currentLocation)
					if found {
						length := path[iter].steps + currsteps
						fmt.Println("length: ", length)
						fmt.Println(path[iter], "==", currentLocation)
						if length < shortestSteps {
							shortestSteps = length
						}
					}
				}
			}
		default:
			fmt.Println("Something went wrong!")
		}
	}
	fmt.Println("fulllength", currsteps)
	fmt.Println("Explored full path", shortestSteps)
	return 0
}

func createPath(instructions string) []Location {
	instructionSet := strings.Split(instructions, ",")
	currentLocation := Location{x: 0, y: 0, steps: 0}
	var path []Location

	for _, inst := range instructionSet {
		switch inst[0:1] {
		case "U":
			dist, err := strconv.Atoi(inst[1:len(inst)])
			if err == nil {
				for i := 0; i < dist; i++ {
					currentLocation.steps += 1
					currentLocation.x += 1
					fmt.Println(currentLocation)
					path = append(path, (Location{x: currentLocation.x, y: currentLocation.y, steps: currentLocation.steps}))
				}
			}
		case "D":
			dist, err := strconv.Atoi(inst[1:len(inst)])
			if err == nil {
				for i := 0; i < dist; i++ {
					currentLocation.steps += 1
					currentLocation.x -= 1
					fmt.Println(currentLocation)
					path = append(path, (Location{x: currentLocation.x, y: currentLocation.y, steps: currentLocation.steps}))
				}
			}
		case "L":
			dist, err := strconv.Atoi(inst[1:len(inst)])
			if err == nil {
				for i := 0; i < dist; i++ {
					currentLocation.steps += 1
					currentLocation.y -= 1
					fmt.Println(currentLocation)
					path = append(path, (Location{x: currentLocation.x, y: currentLocation.y, steps: currentLocation.steps}))
				}
			}
		case "R":
			dist, err := strconv.Atoi(inst[1:len(inst)])
			if err == nil {
				for i := 0; i < dist; i++ {
					currentLocation.steps += 1
					currentLocation.y += 1
					fmt.Println(currentLocation)
					path = append(path, (Location{x: currentLocation.x, y: currentLocation.y, steps: currentLocation.steps}))
				}
			}
		default:
			fmt.Println("Something went wrong!")
		}
	}
	fmt.Println("Created Path: ", len(path))
	return path
}

func find(slice []Location, val Location) (int, bool) {
	for i, item := range slice {
		if item == val {
			return i, true
		}
	}
	return -1, false
}
func Abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

type Location struct {
	x     int64
	y     int64
	steps int64
}
