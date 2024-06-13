package main

import (
    "fmt"
    "strings"
    "strconv"
    "log"
)
var permutations [][]int

func main() {
    maxOut := 0
    permutation := make([]int, 0)
    recursivePermutations(1,permutation)
    for _, per := range permutations{
        AB := make(chan int)
        BC := make(chan int)
        CD := make(chan int)
        DE := make(chan int)
        EA := make(chan int)
        done := make(chan int)
        go intcode(EA,AB,"a",per[0], done)
        EA <- 0
        go intcode(AB,BC,"b",per[1], done)
        go intcode(BC,CD,"c",per[2], done)
        go intcode(CD,DE,"d",per[3], done)
        go intcode(DE,EA,"e",per[4], done)
        for i:= 0; i<4; i++{
            <-done
        }
        thisOut := <-EA
        if(thisOut > maxOut){
            maxOut=thisOut
        }
    }
    fmt.Println("maxOut: ", maxOut)
}

func recursivePermutations(level int, permutation []int){
    if(level > 5){
        permutations = append(permutations,permutation)
        return
    }
    OUTER:for i := 5; i < 10; i++{
        for _,p := range permutation{
            if(i == p){ continue OUTER }
        }
        permutation = append(permutation,i)
        recursivePermutations(level+1,permutation)
        permutation = permutation[0:len(permutation)-1]
    }
}

 func intcode(input chan int, output chan int, name string, phase int, done chan int) int{
    fmt.Println(name, ": started")
    memory := arrayFrom("3,8,1001,8,10,8,105,1,0,0,21,38,55,64,89,114,195,276,357,438,99999,3,9,101,3,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,101,5,9,9,4,9,99,3,9,101,3,9,9,4,9,99,3,9,1002,9,4,9,101,5,9,9,1002,9,5,9,101,5,9,9,102,3,9,9,4,9,99,3,9,101,3,9,9,1002,9,4,9,101,5,9,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99")
    var i int = 0
    hasPhase := false
    lastOut := 0
    processLoop:for true {
      opcode,firstMode,secondMode,_ := parseInstruction(memory[i])
      fmt.Println(name, ": opcode", opcode)
      switch opcode{
        case 1:
            memory[getValue(0,i+3,memory)] = memory[getValue(secondMode,i+2,memory)] + memory[getValue(firstMode,i+1,memory)]
            i += 4
        case 2:
            memory[getValue(0,i+3,memory)] = memory[getValue(secondMode,i+2,memory)] * memory[getValue(firstMode,i+1,memory)]
            i += 4
        case 3:
            if(hasPhase){
                memory[getValue(firstMode,i+1,memory)] = <-input
                fmt.Println(name,": take in")
            }else{
                memory[getValue(firstMode,i+1,memory)] = phase
                hasPhase = true
            }
            i+=2
        case 4:
            fmt.Println(name,": send out")
            lastOut = memory[getValue(firstMode,i+1,memory)]
            output <- lastOut
            i+=2
        case 5:
            if(memory[getValue(firstMode,i+1,memory)] != 0){
                i = memory[getValue(secondMode,i+2,memory)]
            }else{
                i+=3
            }
        case 6:
            if(memory[getValue(firstMode,i+1,memory)] == 0){
                i = memory[getValue(secondMode,i+2,memory)]
            }else{
                i+=3
            }
        case 7:
            if(memory[getValue(firstMode,i+1,memory)] < memory[getValue(secondMode,i+2,memory)]){
                memory[getValue(0,i+3,memory)] = 1
            }else{
                memory[getValue(0,i+3,memory)] = 0
            }
            i += 4
        case 8:
            if(memory[getValue(firstMode,i+1,memory)] == memory[getValue(secondMode,i+2,memory)]){
                memory[getValue(0,i+3,memory)] = 1
            }else{
                memory[getValue(0,i+3,memory)] = 0
            }
            i += 4
          case 99:
            done <- 0
            fmt.Println(name, " is done with the value ", lastOut)
            break processLoop
        default:
          fmt.Println("Something went wrong! ", opcode)
          fmt.Println("@index:",i,"  @value:", memory[i])
        }
    }
    return -123456789
}

func getValue(mode int, parameter int, memory []int) (int){
    switch mode{
        case 0:
            return memory[parameter]
        case 1:
            return parameter
    }
    fmt.Println("yikeriniz")
    return 0
 }

func parseInstruction(instruction int) (int,int,int,int,){
    var thirdMode int = instruction/10000
    instruction -= 10000*thirdMode
    var secondMode int = instruction/1000
    instruction -= 1000*secondMode
    var firstMode int = instruction/100
    instruction -= 100*firstMode
    var opcode int = instruction
    return opcode,firstMode,secondMode,thirdMode
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
