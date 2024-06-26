package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

func main() {
	data := "3,225,1,225,6,6,1100,1,238,225,104,0,1002,114,46,224,1001,224,-736,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1,166,195,224,1001,224,-137,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,1001,169,83,224,1001,224,-90,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,101,44,117,224,101,-131,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1101,80,17,225,1101,56,51,225,1101,78,89,225,1102,48,16,225,1101,87,78,225,1102,34,33,224,101,-1122,224,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,66,53,224,101,-119,224,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,51,49,225,1101,7,15,225,2,110,106,224,1001,224,-4539,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,88,78,225,102,78,101,224,101,-6240,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,226,677,224,102,2,223,223,1006,224,329,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,359,1001,223,1,223,1007,226,677,224,1002,223,2,223,1005,224,374,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,389,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,404,1001,223,1,223,1007,226,226,224,1002,223,2,223,1005,224,419,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,434,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,449,1001,223,1,223,1107,677,677,224,102,2,223,223,1005,224,464,1001,223,1,223,108,226,226,224,1002,223,2,223,1006,224,479,1001,223,1,223,1008,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,108,677,226,224,102,2,223,223,1005,224,509,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,524,101,1,223,223,7,226,677,224,1002,223,2,223,1006,224,539,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,554,1001,223,1,223,7,226,226,224,1002,223,2,223,1006,224,569,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,584,101,1,223,223,1108,677,677,224,102,2,223,223,1006,224,599,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,614,1001,223,1,223,8,677,677,224,1002,223,2,223,1006,224,629,1001,223,1,223,107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,659,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226"
	memory := arrayFrom(data)
	var in int
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
			fmt.Println("input value:")
			_, err := fmt.Scanf("%d", &in)
			if err != nil {
				fmt.Println("Couldn't read value")
			}
			memory[getValue(firstMode, i+1, memory)] = in
			i += 2
		case 4:
			fmt.Println("Output number: ", memory[getValue(firstMode, i+1, memory)])
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
