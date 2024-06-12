import fs from "fs";

const caloriesCarried = fs
  .readFileSync("src/day01/input")
  .toString("utf-8")
  .split("\n\n")
  .map((group) =>
    group
      .split("\n")
      .map((item) => parseInt(item))
      .filter((item) => !Number.isNaN(item))
      .reduce((a, b) => a + b, 0)
  )
  .sort();

const topOne = caloriesCarried[caloriesCarried.length - 1];
const topThree = caloriesCarried
  .slice(caloriesCarried.length - 3, caloriesCarried.length)
  .reduce((a, b) => a + b, 0);

console.log("Part 1: " + topOne);
console.log("Part 2: " + topThree);
