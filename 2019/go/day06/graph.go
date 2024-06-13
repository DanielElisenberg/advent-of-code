package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {
	file, err := os.Open("input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var nodes map[string]string
	nodes = make(map[string]string)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		tmp := strings.Split(scanner.Text(), ")")
		fmt.Println(tmp[1], ":", tmp[0])
		nodes[tmp[1]] = tmp[0]
	}
	var count int = 0
	var lines int = 0
	for node, _ := range nodes {
		lines++
		point := node
		fmt.Println("from: ", node)
		for true {
			try, ok := nodes[point]
			if !ok {
				break
			}
			print("->", try)
			point = try
			count++
		}
	}
	fmt.Println("done: ", count, "::", lines, "\n\n")

	fromYou := make([]string, 0)
	node := nodes["YOU"]
	for true {
		fromYou = append(fromYou, node)
		try, ok := nodes[node]
		if !ok {
			break
		}
		print("->", try)
		node = try
	}
	fmt.Println("\n\n")
	fromSan := make([]string, 0)
	node2 := nodes["SAN"]
	for true {
		fromSan = append(fromSan, node2)
		try, ok := nodes[node2]
		if !ok {
			break
		}
		print("->", try)
		node2 = try
	}
	var ix int = 0
	for _, val := range fromYou {
		ix2 := 0

		for _, val2 := range fromSan {
			if val == val2 {
				fmt.Println("meetingpoint: ", val, "-", val2, "::", ix, ":", ix2, ":", (ix + ix2))
			}
			ix2++
		}
		ix++
	}
}
