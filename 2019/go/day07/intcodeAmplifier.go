package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

var maxOutglobal int = 0

func main() {

	memory := make([]int, 0)
	fmt.Println(recursiveAmplification(0, 0, 1, memory))
	fmt.Println("::", maxOutglobal)
}

func recursiveAmplification(input int, maxOut int, level int, taken []int) int {
	if level > 5 {
		if input > maxOut {
			maxOutglobal = input
			return input
		} else {
			return maxOut
		}
	}

OUTER:
	for i := 0; i < 5; i++ {
		for _, t := range taken {
			if i == t {
				continue OUTER
			}
		}
		taken = append(taken, i)
		thisOut := intcode(i, input)
		maxOut = recursiveAmplification(thisOut, maxOut, level+1, taken)
		taken = taken[0 : len(taken)-1]
	}
	return maxOut
}

func intcode(phaseInput int, ampInput int) int {
	data := "3,8,1001,8,10,8,105,1,0,0,21,38,55,64,89,114,195,276,357,438,99999,3,9,101,3,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,101,5,9,9,4,9,99,3,9,101,3,9,9,4,9,99,3,9,1002,9,4,9,101,5,9,9,1002,9,5,9,101,5,9,9,102,3,9,9,4,9,99,3,9,101,3,9,9,1002,9,4,9,101,5,9,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99"
	memory := arrayFrom(data)
	setPhase := false
	var i int = 0
processLoop:
	for true {
		opcode, firstMode, secondMode, _ := parseInstruction(memory[i])
		switch opcode {
		case 1:
			memory[getValue(0, i+3, memory)] = memory[getValue(secondMode, i+2, memory)] + memory[getValue(firstMode, i+1, memory)]
			i += 4
		case 2:
			memory[getValue(0, i+3, memory)] = memory[getValue(secondMode, i+2, memory)] * memory[getValue(firstMode, i+1, memory)]
			i += 4
		case 3:
			if setPhase {
				memory[getValue(firstMode, i+1, memory)] = ampInput
			} else {
				memory[getValue(firstMode, i+1, memory)] = phaseInput
				setPhase = true
			}
			i += 2
		case 4:
			return memory[getValue(firstMode, i+1, memory)]
			i += 2
		case 5:
			if memory[getValue(firstMode, i+1, memory)] != 0 {
				i = memory[getValue(secondMode, i+2, memory)]
			} else {
				i += 3
			}
		case 6:
			if memory[getValue(firstMode, i+1, memory)] == 0 {
				i = memory[getValue(secondMode, i+2, memory)]
			} else {
				i += 3
			}
		case 7:
			if memory[getValue(firstMode, i+1, memory)] < memory[getValue(secondMode, i+2, memory)] {
				memory[getValue(0, i+3, memory)] = 1
			} else {
				memory[getValue(0, i+3, memory)] = 0
			}
			i += 4
		case 8:
			if memory[getValue(firstMode, i+1, memory)] == memory[getValue(secondMode, i+2, memory)] {
				memory[getValue(0, i+3, memory)] = 1
			} else {
				memory[getValue(0, i+3, memory)] = 0
			}
			i += 4
		case 99:
			break processLoop
		default:
			fmt.Println("Something went wrong! ", opcode)
			fmt.Println("@index:", i, "  @value:", memory[i])
		}
	}
	return -1
}

func getValue(mode int, parameter int, memory []int) int {
	switch mode {
	case 0:
		return memory[parameter]
	case 1:
		return parameter
	}
	fmt.Println("Yikes")
	return 0
}

func parseInstruction(instruction int) (int, int, int, int) {
	var thirdMode int = instruction / 10000
	instruction -= 10000 * thirdMode
	var secondMode int = instruction / 1000
	instruction -= 1000 * secondMode
	var firstMode int = instruction / 100
	instruction -= 100 * firstMode
	var opcode int = instruction
	return opcode, firstMode, secondMode, thirdMode
}

func arrayFrom(data string) []int {
	tmp := strings.Split(data, ",")
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
