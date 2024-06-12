import fs from "fs";

type Rules = { [name: string]: number };

function calculateScore(strategyGuide: string[], rules: Rules): number {
  return strategyGuide
    .map((line) => rules[line])
    .filter((score) => score !== undefined)
    .reduce((a, b) => a + b, 0);
}

const rules: Rules = {
  "A X": 3 + 1,
  "B Y": 3 + 2,
  "C Z": 3 + 3,
  "A Y": 6 + 2,
  "A Z": 0 + 3,
  "B X": 0 + 1,
  "B Z": 6 + 3,
  "C X": 6 + 1,
  "C Y": 0 + 2,
};

const newRules: Rules = {
  "A X": 0 + 3,
  "B Y": 3 + 2,
  "C Z": 6 + 1,
  "A Y": 3 + 1,
  "A Z": 6 + 2,
  "B X": 0 + 1,
  "B Z": 6 + 3,
  "C X": 0 + 2,
  "C Y": 3 + 3,
};

const strategyGuide = fs
  .readFileSync("src/day02/input")
  .toString("utf-8")
  .split("\n");

console.log("Part 1: " + calculateScore(strategyGuide, rules));
console.log("Part 1: " + calculateScore(strategyGuide, newRules));
