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
	data := scanner.Text()
	spaceImageFormat := arrayFrom(data)
	for _, vak := range spaceImageFormat {
		fmt.Println("-<", vak)
	}

	layerLen := 150
	var finalImage [150]int

	for t := range finalImage {
		finalImage[t] = 2
	}

	layerCount := len(spaceImageFormat) / layerLen
	for i := 0; i < layerCount; i++ {
		for j := layerLen * i; j < layerLen*(i+1); j++ {
			switch finalImage[j-(layerLen*i)] {
			case 1:
				continue
			case 2:
				finalImage[j-(layerLen*i)] = spaceImageFormat[j]
			case 0:
				continue
			}
		}
	}

	lel := 0
	width := 24
	for count := 0; count < len(finalImage); count++ {
		switch finalImage[count] {
		case 1:
			print(" ")
		case 0:
			print("O")
		}
		lel++
		if lel > width {
			fmt.Println("")
			lel = 0
		}
	}
}

func arrayFrom(data string) []int {
	tmp := strings.Split(data, "")
	memory := make([]int, 0, len(tmp))
	for _, raw := range tmp {
		v, err := strconv.Atoi(raw)
		if err != nil {
			log.Print(err)
			continue
		}
		memory = append(memory, v)
	}
	return memory
}
