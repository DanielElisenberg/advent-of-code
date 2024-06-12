import fs from "fs";

const pairs = fs
  .readFileSync("src/day04/input")
  .toString("utf-8")
  .split("\n")
  .map((line) => {
    return line.split(",").map((elf) => {
      const min = parseInt(elf.split("-")[0]);
      const max = parseInt(elf.split("-")[1]);
      const size = max - min + 1;
      return [...Array(size).keys()].map((i) => i + min);
    });
  });

const totalOverlapCount = pairs
  .map((pair) => {
    return (
      pair[0].every((n) => pair[1].includes(n)) ||
      pair[1].every((n) => pair[0].includes(n))
    );
  })
  .filter((overlap) => overlap).length;
console.log("Part 1: " + totalOverlapCount);

const overlapCount = pairs
  .map((pair) => {
    return pair[0].some((n) => pair[1].includes(n));
  })
  .filter((overlap) => overlap).length;
console.log("Part 2: " + overlapCount);
