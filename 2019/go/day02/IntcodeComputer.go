package main

import (
    "fmt"
    "strings"
    "strconv"
    "log"
)

func main() {
    data := "1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,6,23,2,6,23,27,2,27,9,31,1,5,31,35,1,35,10,39,2,39,9,43,1,5,43,47,2,47,10,51,1,51,6,55,1,5,55,59,2,6,59,63,2,63,6,67,1,5,67,71,1,71,9,75,2,75,10,79,1,79,5,83,1,10,83,87,1,5,87,91,2,13,91,95,1,95,10,99,2,99,13,103,1,103,5,107,1,107,13,111,2,111,9,115,1,6,115,119,2,119,6,123,1,123,6,127,1,127,9,131,1,6,131,135,1,135,2,139,1,139,10,0,99,2,0,14,0"

	memory := arrayFrom(data)

    processLoop:for i:=0;i < len(memory); i+=4 {
      switch memory[i]{
        case 1:
       		memory[memory[i+3]] = memory[memory[i+1]] + memory[memory[i+2]]
        case 2:
        	memory[memory[i+3]] = memory[memory[i+1]] * memory[memory[i+2]]
        case 99:
          break processLoop
        default:
          fmt.Println("Something went wrong!")
          fmt.Println("@index:",i,"  @value:", memory[i])
        }
    }

    fmt.Println("answer: ", memory[0])
}

func arrayFrom(data string) []int{
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
