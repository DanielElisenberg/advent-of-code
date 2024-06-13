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

	var totalNum int64 = 0

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		currNum, err := strconv.ParseInt(scanner.Text(), 10, 64)
		if err == nil {
			totalNum += currNum/3 - 2
			fmt.Println("Added fuel: ", totalNum)
		}
	}
	fmt.Println("answer: ", totalNum)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}
