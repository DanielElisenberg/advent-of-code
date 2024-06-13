package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	file, err := os.Open("input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var totalFuelNeeded int64 = 0

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		moduleMass, err := strconv.ParseInt(scanner.Text(), 10, 64)
		if err == nil {
			var moduleTotal int64 = 0
			var fuelNeeded int64 = moduleMass/3 - 2
			for fuelNeeded > 0 {
				moduleTotal += fuelNeeded
				fuelNeeded = fuelNeeded/3 - 2
			}
			totalFuelNeeded += moduleTotal
		}
	}
	fmt.Println("answer: ", totalFuelNeeded)
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}
