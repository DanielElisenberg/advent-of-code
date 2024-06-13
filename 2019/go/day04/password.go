package main

import (
  "strconv"
  "fmt"
)

func main(){
	validPasswords := 0
	for i := 128392; i < 643282; i++ {
		if(isValid(i)){
			if(strictPair(i)){
				validPasswords++
			}
		}
	}
	fmt.Println("->", validPasswords)
}
func isValid(password int) bool {
	passtring := strconv.Itoa(password)
	hasPair := false
	for i := 0; i < len(passtring)-1; i++{
		num1,_ := strconv.Atoi(passtring[i:i+1])
		num2,_ := strconv.Atoi(passtring[i+1:i+2])
		if(num1 == num2){ hasPair = true }
		if(num1 > num2){ return false }
	}
	return hasPair
}
func strictPair(password int) bool{
	passtring := strconv.Itoa(password)
	strictPair := false
	for i := 0; i < len(passtring)-1; i++{
		num1,_ := strconv.Atoi(passtring[i:i+1])
		num2,_ := strconv.Atoi(passtring[i+1:i+2])
		if(num1 == num2) { 
			if(i > 0){
				numbefore,_ := strconv.Atoi(passtring[i-1:i])
				if(numbefore == num1){
					continue
				}
			}
			if(i<len(passtring)-2){
				numafter,_ := strconv.Atoi(passtring[i+2:i+3])
				if(numafter ==num2){
					continue
				}
			}
			strictPair = true
		}
	}
	return strictPair
} 
