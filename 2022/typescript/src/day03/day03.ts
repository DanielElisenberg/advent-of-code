import fs from "fs";

const characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
const priorityOf = Object.fromEntries(
  characters.split("").map((item, index) => [item, index + 1])
);

const rucksacks = fs
  .readFileSync("src/day03/input")
  .toString("utf-8")
  .split("\n")
  .filter((line) => line != "");

const misplacedItems = rucksacks
  .map((rucksack) => {
    const c1 = rucksack.slice(0, rucksack.length / 2).split("");
    const c2 = rucksack.slice(rucksack.length / 2, rucksack.length).split("");
    return priorityOf[c1.filter((item) => c2.includes(item))[0]];
  })
  .reduce((a, b) => a + b, 0);

console.log("Part 1: " + misplacedItems);

const badges = rucksacks
  .map((rucksack, index) => {
    if (index % 3 != 0) {
      return undefined;
    }
    const r2 = rucksacks[index + 1].split("");
    const r3 = rucksacks[index + 2].split("");
    return priorityOf[
      rucksack
        .split("")
        .filter((item) => r2.includes(item) && r3.includes(item))[0]
    ];
  })
  .filter((item) => item != undefined)
  .reduce((a, b) => a + b, 0);

console.log("Part 2: " + badges);
